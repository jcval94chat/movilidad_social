# section2.py

import streamlit as st
import pandas as pd
import plotly.express as px

from data_utils import load_and_process_data

# Diccionario para mapear las categorías del usuario a quintiles.
CLASS_TO_QUINTILES = {
    "Baja Baja": [1],
    "Baja Alta": [2],
    "Media Baja": [3],
    "Media Alta": [4],
    "Alta": [5]
}

def show_section2():
    """
    Movilidad por Cohortes:
    - Aplica filtros de la barra lateral (excepto generación).
    - Cohortes de 3 años.
    - El usuario elige Origen y Destino (clase).
    - Se muestra un lineplot interactivo con Plotly.
    """

    st.title("Movilidad por Cohortes")

    # 1) Cargar datos
    df = load_and_process_data()

    # 2) Crear la columna de cohort_5y si no existe
    #    (La calculamos cada vez para seguridad, o asumimos que no está en el DF)
    df = add_cohort_5y_column(df, step=3)

    # 3) Aplicar filtro de la barra lateral (excepto 'generation')
    df_filtered = apply_filter_except_generation(df)

    # 4) Controles de Origen y Destino
    st.subheader("Selecciona Origen y Destino")
    origin_class = st.selectbox(
        "Origen:",
        list(CLASS_TO_QUINTILES.keys()),
        index=4  # Por ejemplo, "Alta" como default
    )
    dest_class = st.selectbox(
        "Destino:",
        list(CLASS_TO_QUINTILES.keys()),
        index=4  # Por ejemplo, "Alta"
    )

    # 5) Calcular la métrica: porcentaje de quienes estaban en 'origin_class'
    #    que se mueven a 'dest_class', por cohorte y sexo.
    #    - 'origin_mask': df['a_los_14_quintile'].isin(CLASS_TO_QUINTILES[origin_class])
    #    - 'dest_mask': df['actualmente_quintile'].isin(CLASS_TO_QUINTILES[dest_class])

    origin_quintiles = CLASS_TO_QUINTILES[origin_class]
    dest_quintiles   = CLASS_TO_QUINTILES[dest_class]

    df_filtered['in_origin'] = df_filtered['a_los_14_quintile'].isin(origin_quintiles)
    df_filtered['in_dest']   = df_filtered['actualmente_quintile'].isin(dest_quintiles)

    # Solo analizamos quienes estaban en el origen
    df_origin = df_filtered[df_filtered['in_origin'] == True].copy()

    grouped = df_origin.groupby(['cohort_5y','sex'])
    n_origin = grouped.size().rename("n_origin")
    n_dest   = grouped['in_dest'].sum().rename("n_dest")

    df_stats = pd.concat([n_origin, n_dest], axis=1).reset_index()
    df_stats['pct_dest'] = (df_stats['n_dest'] / df_stats['n_origin']) * 100

    # 6) Extraer año de inicio de cohorte (para eje X)
    df_stats['cohort_start'] = df_stats['cohort_5y'].apply(get_lower_year)
    # Ordenar y filtrar NA
    df_stats.sort_values('cohort_start', inplace=True)
    df_stats.dropna(subset=['cohort_start'], inplace=True)

    # 7) Título dinámico
    chart_title = f"Porcentaje de {origin_class} que se mueven a {dest_class}"

    # 8) Graficar con Plotly para interactividad
    fig = px.line(
        df_stats,
        x='cohort_start',
        y='pct_dest',
        color='sex',
        markers=True,
        title=chart_title,
        labels={
            'cohort_start': "Año en que naciste",
            'pct_dest': "% que se mueven",
            'sex': "Sexo"
        }
    )

    # Ajustes de layout
    fig.update_layout(
        xaxis_title="Año en que naciste",
        yaxis_title=f"Porcentaje que se mueven a {dest_class}",
        legend_title_text="Sexo"
    )

    # Mostrar en Streamlit con interactividad
    st.plotly_chart(fig, use_container_width=True)


def add_cohort_5y_column(df, base_year=2017, step=3):
    """
    Crea la columna 'cohort_5y' (tramos de 'step' años) a partir de la edad en p05h.
    """
    def assign_cohort_5y(row_age):
        if pd.isna(row_age):
            return "NA"
        birth_year = base_year - int(row_age)
        lower_bound = (birth_year // step) * step
        upper_bound = lower_bound + (step - 1)
        return f"{lower_bound}-{upper_bound}"

    df['cohort_5y'] = df['p05h'].apply(assign_cohort_5y)
    return df


def get_lower_year(cohort_str):
    """
    Extrae el año inferior de un string tipo '1950-1952'.
    """
    if cohort_str == "NA" or pd.isna(cohort_str):
        return None
    return int(cohort_str.split('-')[0])


def apply_filter_except_generation(df):
    """
    Aplica los filtros de la barra lateral (sex, education, etc.) ignorando 'generation'.
    Esto reutiliza st.session_state['selected_vars'] y st.session_state[f"cats_{var}"].
    """
    dff = df.copy()
    if 'selected_vars' not in st.session_state:
        return dff  # No hay filtros
    for var in st.session_state['selected_vars']:
        # Omitimos 'generation'
        if var == 'generation':
            continue
        chosen_cats = st.session_state.get(f"cats_{var}", [])
        if chosen_cats:
            dff = dff[dff[var].isin(chosen_cats)]
    return dff
