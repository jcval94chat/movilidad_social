# section2.py

import streamlit as st
import pandas as pd
import plotly.express as px

from data_utils import load_and_process_data

# Paleta de colores para mantener consistencia (igual que Section 1)
BASE_COLOR = "gray"
PRIMARY_COLOR = "skyblue"
SECONDARY_COLOR = "salmon"

CLASS_TO_QUINTILES = {
    "Baja Baja": [1],
    "Baja Alta": [2],
    "Media Baja": [3],
    "Media Alta": [4],
    "Alta": [5]
}

def show_section2():
    """
    Sección 2: Evolución Temporal.
    - Botones de Refresh y Aleatoriedad en la barra lateral.
    - Origen/Destino con multiselect, por defecto Media Alta->Alta.
    - Filtra por las variables del sidebar (except generation).
    - Gráfica px.line con Plotly, usando la misma paleta de colores.
    """

    # Botones en barra lateral (a la derecha de "Filtro actual (filtro principal)")
    st.sidebar.subheader("Filtro actual (filtro principal):")
    col_side1, col_side2 = st.sidebar.columns([0.7, 0.3])
    with col_side2:
        if st.button("⟳", help="Reset Sección 2", key="refresh_s2"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        if st.button("🎲", help="Aleatoriedad Sección 2", key="random_s2"):
            random_origin_dest()
            st.rerun()

    # Creación del DF y columna de cohorte
    df = load_and_process_data()
    df = add_cohort_5y_column(df, step=3)

    # Filtro except generation
    df_filtered = apply_filter_except_generation(df)

    # Controles Origen/Destino
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

    # Guardamos la selección por si refrescan
    st.session_state["origin_default"] = origin_multisel
    st.session_state["dest_default"]   = dest_multisel

    # Etiquetas para la línea
    color_col = create_label_column(df_filtered)

    # Construimos las máscaras de origen/destino
    origin_q = set()
    for cls_ in origin_multisel:
        origin_q.update(CLASS_TO_QUINTILES[cls_])
    dest_q = set()
    for cls_ in dest_multisel:
        dest_q.update(CLASS_TO_QUINTILES[cls_])

    df_filtered['in_origin'] = df_filtered['a_los_14_quintile'].isin(origin_q)
    df_filtered['in_dest']   = df_filtered['actualmente_quintile'].isin(dest_q)

    df_origin = df_filtered[df_filtered['in_origin']].copy()

    grouped = df_origin.groupby(['cohort_5y', color_col], dropna=False)
    n_origin = grouped.size().rename("n_origin")
    n_dest   = grouped['in_dest'].sum().rename("n_dest")
    df_stats = pd.concat([n_origin, n_dest], axis=1).reset_index()
    df_stats['pct_dest'] = (df_stats['n_dest'] / df_stats['n_origin']) * 100

    # Extraer año de inicio
    df_stats['cohort_start'] = df_stats['cohort_5y'].apply(get_lower_year)
    df_stats.sort_values('cohort_start', inplace=True)
    df_stats.dropna(subset=['cohort_start'], inplace=True)

    # Título
    if not origin_multisel:
        origin_multisel = ["(Ninguno)"]
    if not dest_multisel:
        dest_multisel = ["(Ninguno)"]
    origin_str = ", ".join(origin_multisel)
    dest_str   = ", ".join(dest_multisel)
    chart_title = f"Porcentaje de {origin_str} que se mueven a {dest_str}"

    # Plot
    fig = px.line(
        df_stats,
        x='cohort_start',
        y='pct_dest',
        color=color_col,
        markers=True,
        title=chart_title,
        labels={
            'cohort_start': "Año en que naciste",
            'pct_dest': "% que se mueven",
            color_col: "Categoría"
        },
        color_discrete_sequence=[PRIMARY_COLOR, SECONDARY_COLOR, BASE_COLOR]
    )
    fig.update_layout(
        xaxis_title="Año en que naciste",
        yaxis_title="Porcentaje que se mueven",
        legend_title_text="Categoría",
        width=850,
        height=550
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    st.plotly_chart(fig, use_container_width=True)

    # Logos
    st.markdown("---")
    st.markdown("### ")
    c1_, c2_ = st.columns([0.5, 0.5])
    with c1_:
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
    with c2_:
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

# -----------------------------------------------------
# Auxiliares de Section 2
# -----------------------------------------------------
def random_origin_dest():
    import random
    classes = list(CLASS_TO_QUINTILES.keys())
    n_orig = random.randint(1,2)
    origin = random.sample(classes, n_orig)
    n_dest = random.randint(1,2)
    dest = random.sample(classes, n_dest)
    st.session_state["origin_default"] = origin
    st.session_state["dest_default"]   = dest

def add_cohort_5y_column(df, base_year=2017, step=3):
    def assign_cohort(row_age):
        if pd.isna(row_age):
            return "NA"
        birth_year = base_year - int(row_age)
        lower_bound = (birth_year // step) * step
        upper_bound = lower_bound + (step - 1)
        return f"{lower_bound}-{upper_bound}"
    df['cohort_5y'] = df['p05h'].apply(assign_cohort)
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
    """
    Si no hay vars (except generation), todos en un mismo 'All'.
    Caso contrario, combinamos sus valores en "var=cat | var2=cat2".
    """
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
            parts.append(f"{v}={row[v]}")
        return " | ".join(parts)

    df['group_label'] = df.apply(make_label, axis=1)
    return 'group_label'
