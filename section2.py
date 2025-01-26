# section2.py

import streamlit as st
import pandas as pd
import plotly.express as px

from data_utils import load_and_process_data

# Diccionario para mapear las clases (Baja Baja, etc.) a quintiles
CLASS_TO_QUINTILES = {
    "Baja Baja": [1],
    "Baja Alta": [2],
    "Media Baja": [3],
    "Media Alta": [4],
    "Alta": [5]
}

def show_section2():
    """
    Evolución Temporal (Sección 2):
    - Botones de reset y aleatoriedad en la parte superior.
    - Origen/Destino como multiselect en una sola fila (2 columnas).
    - Por defecto: Origen=["Media Alta"], Destino=["Alta"].
    - Se genera una gráfica de líneas usando Plotly, con cohortes de 3 años.
    - Se ignora 'generation' en los filtros, pero sí se dividen líneas según
      las variables (sexo, education, etc.) seleccionadas en la barra lateral.
    """

    # 1) Encabezado con botones
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    with col1:
        # No se muestra st.title() ni texto "Selecciona..."
        st.markdown("<h2 style='margin-bottom:0;'> </h2>", unsafe_allow_html=True)
    with col2:
        if st.button("⟳", help="Recargar la app (reset a valores originales)"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with col3:
        if st.button("🎲", help="Aleatoriedad en Origen/Destino"):
            random_origin_dest()
            st.rerun()

    # 2) Crear df con la columna 'cohort_5y'
    df = load_and_process_data()
    df = add_cohort_5y_column(df, step=3)

    # 3) Aplicar filtro excepto generation
    df_filtered = apply_filter_except_generation(df)

    # 4) Controles Origen y Destino en la misma fila
    c1, c2 = st.columns(2)
    with c1:
        origin_multisel = st.multiselect(
            "Origen:",
            options=list(CLASS_TO_QUINTILES.keys()),
            default=st.session_state.get("origin_default", ["Media Alta"])
        )
    with c2:
        dest_multisel = st.multiselect(
            "Destino:",
            options=list(CLASS_TO_QUINTILES.keys()),
            default=st.session_state.get("dest_default", ["Alta"])
        )

    # Guardamos la selección actual por si refrescan
    st.session_state["origin_default"] = origin_multisel
    st.session_state["dest_default"]   = dest_multisel

    # 5) Crear la columna "group_label" combinando las variables del sidebar (except gen)
    #    para la división de líneas. Si no hay variables, será una sola línea.
    color_column = create_label_column(df_filtered)

    # 6) Calcular la métrica: % de origen -> destino
    #    Origen: union de quintiles de las clases en origin_multisel
    #    Destino: union de quintiles de las clases en dest_multisel
    origin_quintiles = set()
    for cls in origin_multisel:
        origin_quintiles.update(CLASS_TO_QUINTILES[cls])
    dest_quintiles = set()
    for cls in dest_multisel:
        dest_quintiles.update(CLASS_TO_QUINTILES[cls])

    df_filtered['in_origin'] = df_filtered['a_los_14_quintile'].isin(origin_quintiles)
    df_filtered['in_dest']   = df_filtered['actualmente_quintile'].isin(dest_quintiles)

    df_origin = df_filtered[df_filtered['in_origin'] == True].copy()

    # Agrupación por cohort_5y + color_column
    grouped = df_origin.groupby(['cohort_5y', color_column], dropna=False)
    n_origin = grouped.size().rename("n_origin")
    n_dest   = grouped['in_dest'].sum().rename("n_dest")

    df_stats = pd.concat([n_origin, n_dest], axis=1).reset_index()
    df_stats['pct_dest'] = (df_stats['n_dest'] / df_stats['n_origin']) * 100

    # Extraer año de inicio de cohorte
    df_stats['cohort_start'] = df_stats['cohort_5y'].apply(get_lower_year)
    df_stats.sort_values('cohort_start', inplace=True)
    df_stats.dropna(subset=['cohort_start'], inplace=True)

    # 7) Armar un título (ej. "Porcentaje de [Media Alta] que se mueven a [Alta]")
    if not origin_multisel:
        origin_multisel = ["(Ninguno)"]
    if not dest_multisel:
        dest_multisel = ["(Ninguno)"]
    chart_title = f"Porcentaje de {origin_multisel} que se mueven a {dest_multisel}"

    # 8) Graficar con Plotly
    fig = px.line(
        df_stats,
        x='cohort_start',
        y='pct_dest',
        color=color_column,  # múltiples líneas
        markers=True,
        title=chart_title,
        labels={
            'cohort_start': "Año en que naciste",
            'pct_dest': f"% que se mueven",
            color_column: "Categoría"
        }
    )
    fig.update_layout(
        xaxis_title="Año en que naciste",
        yaxis_title=f"Porcentaje que se mueven",
        legend_title_text="Categoría"
    )
    st.plotly_chart(fig, use_container_width=True)


def random_origin_dest():
    """Elige aleatoriamente origen y destino (multiselect)."""
    import random
    classes = list(CLASS_TO_QUINTILES.keys())
    # Elegimos 1..2 clases al azar para origen
    n_orig = random.randint(1,2)
    origin = random.sample(classes, n_orig)

    # Elegimos 1..2 clases al azar para destino
    n_dest = random.randint(1,2)
    dest = random.sample(classes, n_dest)

    st.session_state["origin_default"] = origin
    st.session_state["dest_default"]   = dest

def add_cohort_5y_column(df, base_year=2017, step=3):
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
    if cohort_str == "NA" or pd.isna(cohort_str):
        return None
    return int(cohort_str.split('-')[0])

def apply_filter_except_generation(df):
    """
    Aplica los filtros de la barra lateral (st.session_state['selected_vars']),
    pero ignora 'generation'.
    """
    dff = df.copy()
    if 'selected_vars' not in st.session_state:
        return dff
    for var in st.session_state['selected_vars']:
        if var == 'generation':
            continue
        chosen_cats = st.session_state.get(f"cats_{var}", [])
        if chosen_cats:
            dff = dff[dff[var].isin(chosen_cats)]
    return dff

def create_label_column(df):
    """
    Combina las variables (except 'generation') seleccionadas en la barra lateral
    en una sola columna 'group_label' para que px.line pinte líneas separadas.
    Si no se selecciona nada, todos irán en un mismo grupo ("All").
    """
    if 'selected_vars' not in st.session_state:
        df['group_label'] = "All"
        return 'group_label'

    chosen_vars = [v for v in st.session_state['selected_vars'] if v != 'generation']
    if not chosen_vars:
        df['group_label'] = "All"
        return 'group_label'

    # Construimos un label combinando las columnas elegidas
    # Ej. "sex=Mujer | education=Universidad"
    def make_label(row):
        parts = []
        for v in chosen_vars:
            val = row[v]
            parts.append(f"{v}={val}")
        return " | ".join(parts)

    df['group_label'] = df.apply(make_label, axis=1)
    return 'group_label'
