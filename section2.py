# section2.py

import streamlit as st
import pandas as pd
import plotly.express as px

from data_utils import load_and_process_data

CLASS_TO_QUINTILES = {
    "Baja Baja": [1],
    "Baja Alta": [2],
    "Media Baja": [3],
    "Media Alta": [4],
    "Alta": [5]
}

def show_section2():
    """
    Sección 2: Evolución Temporal
    (Los botones de refresh / aleatoriedad están ahora en main.py).
    """

    # 1) Carga datos y crea cohort_5y
    df = load_and_process_data()
    df = add_cohort_5y_column(df, step=3)

    # 2) Filtro excepto generation
    df_filtered = apply_filter_except_generation(df)

    # 3) Controles de Origen / Destino (multiselect) en la misma fila
    c1, c2 = st.columns(2)
    with c1:
        origin_multisel = st.multiselect(
            "",
            options=list(CLASS_TO_QUINTILES.keys()),
            default=st.session_state.get("origin_default", ["Media Alta"]),
            key="origin_multisel"
        )
    with c2:
        dest_multisel = st.multiselect(
            "",
            options=list(CLASS_TO_QUINTILES.keys()),
            default=st.session_state.get("dest_default", ["Alta"]),
            key="dest_multisel"
        )

    # Guardamos la selección
    st.session_state["origin_default"] = origin_multisel
    st.session_state["dest_default"]   = dest_multisel

    # 4) Construimos la columna color (group_label) con las vars del sidebar (except gen)
    color_column = create_label_column(df_filtered)

    # 5) Cálculo de % Origen->Destino
    origin_quintiles = set()
    for cls in origin_multisel:
        origin_quintiles.update(CLASS_TO_QUINTILES[cls])

    dest_quintiles = set()
    for cls in dest_multisel:
        dest_quintiles.update(CLASS_TO_QUINTILES[cls])

    df_filtered['in_origin'] = df_filtered['a_los_14_quintile'].isin(origin_quintiles)
    df_filtered['in_dest']   = df_filtered['actualmente_quintile'].isin(dest_quintiles)

    df_origin = df_filtered[df_filtered['in_origin'] == True].copy()

    grouped = df_origin.groupby(['cohort_5y', color_column], dropna=False)
    n_origin = grouped.size().rename("n_origin")
    n_dest   = grouped['in_dest'].sum().rename("n_dest")
    df_stats = pd.concat([n_origin, n_dest], axis=1).reset_index()
    df_stats['pct_dest'] = (df_stats['n_dest'] / df_stats['n_origin']) * 100

    df_stats['cohort_start'] = df_stats['cohort_5y'].apply(get_lower_year)
    df_stats.sort_values('cohort_start', inplace=True)
    df_stats.dropna(subset=['cohort_start'], inplace=True)

    # 6) Armar título
    if not origin_multisel:
        origin_multisel = ["(Ninguno)"]
    if not dest_multisel:
        dest_multisel = ["(Ninguno)"]
    origin_str = ", ".join(origin_multisel)
    dest_str = ", ".join(dest_multisel)
    chart_title = f"Porcentaje de {origin_str} que se mueven a {dest_str}"

    # 7) Graficar con Plotly
    #    Usar la misma paleta que Sección 1, p.ej.
    color_sequence = ["skyblue","salmon","gray","green","red"]  
    fig = px.line(
        df_stats,
        x='cohort_start',
        y='pct_dest',
        color=color_column,
        markers=True,
        title=chart_title,
        labels={
            'cohort_start': "Año en que naciste",
            'pct_dest': "% que se mueven",
            color_column: "Categoría"
        },
        color_discrete_sequence=color_sequence
    )
    fig.update_layout(
        xaxis_title="Año en que naciste",
        yaxis_title="Porcentaje que se mueven",
        legend_title_text="Categoría",
        width=800,
        height=600
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    st.plotly_chart(fig, use_container_width=True)

    # 8) Logos
    st.markdown("---")
    c1, c2 = st.columns([0.5, 0.5])
    with c1:
        st.markdown(
            """
            <a href='https://www.youtube.com/@momentitocafecito' target='_blank'
               style='text-decoration:none;'>
                <img src='https://cdn-icons-png.flaticon.com/512/1384/1384060.png'
                     height='25' style='vertical-align:middle;' />
                <span style='font-size:14px; margin-left:6px;'>Momentito Cafecito</span>
            </a>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            """
            <a href='https://instagram.com/momentitocafecito' target='_blank'
               style='text-decoration:none;'>
                <img src='https://cdn-icons-png.flaticon.com/512/1384/1384063.png'
                     height='25' style='vertical-align:middle;' />
                <span style='font-size:14px; margin-left:6px;'>Momentito Cafecito</span>
            </a>
            """,
            unsafe_allow_html=True
        )

def random_origin_dest_section2():
    """
    Aleatoriza la selección de Origen y Destino para Sección 2
    (1..2 clases en origen, 1..2 en destino).
    """
    import random
    classes = list(CLASS_TO_QUINTILES.keys())
    n_orig = random.randint(1,2)
    origin = random.sample(classes, n_orig)
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
    if 'selected_vars' not in st.session_state:
        df['group_label'] = "All"
        return 'group_label'
    chosen_vars = [v for v in st.session_state['selected_vars'] if v != 'generation']
    if not chosen_vars:
        df['group_label'] = "All"
        return 'group_label'

    def make_label(row):
        parts = []
        for v in chosen_vars:
            val = row[v]
            parts.append(f"{v}={val}")
        return " | ".join(parts)

    df['group_label'] = df.apply(make_label, axis=1)
    return 'group_label'
