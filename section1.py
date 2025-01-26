# section1.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_utils import load_and_process_data
from config import VAR_CATEGORIES, POSSIBLE_VARS

def show_section1():
    """
    Sección 1: Movilidad Socioeconómica Q1 vs Q5 (interactiva con Plotly).
    """

    # 1) Manejo de estado
    if 'selected_vars' not in st.session_state:
        st.session_state['selected_vars'] = []
    for var in POSSIBLE_VARS:
        key_name = f"cats_{var}"
        if key_name not in st.session_state:
            st.session_state[key_name] = []

    # 2) Encabezado con botones: Refresh y Dados
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    with col1:
        st.markdown("<h2 style='margin-bottom:0;'>Movilidad Socioeconómica Q1 vs Q5</h2>", unsafe_allow_html=True)
    with col2:
        # Botón Refresh con key único
        if st.button("⟳", help="Recargar la app (reset a valores originales)", key="refresh_section1"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with col3:
        # Botón de Dados (aleatoriedad) con key único
        if st.button("🎲", help="Selecciona 2 variables y 1-3 categorías al azar", key="random_section1"):
            random_filter_selection()
            st.rerun()

    # 3) Barra lateral: Selección de variables y categorías
    st.sidebar.subheader("Filtro actual (filtro principal):")
    st.session_state['selected_vars'] = st.sidebar.multiselect(
        "Selecciona las variables (máximo 3)",
        options=POSSIBLE_VARS,
        default=st.session_state['selected_vars'],
        max_selections=3
    )

    # Para cada variable seleccionada, mostrar multiselect de categorías
    for var in st.session_state['selected_vars']:
        cat_options = VAR_CATEGORIES.get(var, [])
        st.session_state[f"cats_{var}"] = st.sidebar.multiselect(
            f"{var.capitalize()}:",
            cat_options,
            default=st.session_state[f"cats_{var}"]
        )

    # 4) Carga de datos
    df = load_and_process_data()

    # 5) Aplicar el filtro principal
    df_filter = apply_dynamic_filter(df)

    # 6) Cambiar base
    st.sidebar.markdown("---")
    cambiar_base = st.sidebar.checkbox("Cambiar base", value=False)
    if cambiar_base:
        show_base_filters(df)
        df_base = st.session_state.get('df_base', df)
    else:
        df_base = df

    # 7) Construir un título dinámico según el filtro y la base
    filter_desc = describe_filter_selection(st.session_state['selected_vars'], prefix="Filtro: ")
    if cambiar_base and 'base_selected_vars' in st.session_state and st.session_state['base_selected_vars']:
        base_desc = describe_filter_selection(st.session_state['base_selected_vars'], prefix="Base: ", base=True)
        main_title = f"{filter_desc} vs {base_desc}"
    else:
        main_title = filter_desc or "Sin Filtro (Base General)"

    # 8) Mostrar gráfica (ligeramente más pequeña que antes)
    fig = plot_mobility_interactive(df_filter, df_base, main_title)
    st.plotly_chart(fig, use_container_width=True)

    # 9) Logos al final de la página (más pequeños, con "Momentito Cafecito")
    st.markdown("---")
    st.markdown("### ")
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

    # 10) Detalles en un expander
    with st.sidebar.expander("Detalles"):
        st.write("""
        **Origen Clase Baja:** Personas que estaban en el quintil más bajo (Q1).
        **Origen Clase Alta:** Personas que estaban en el quintil más alto (Q5).

        Las etiquetas en el eje X representan la clase socioeconómica actual:
        - Baja Baja
        - Baja Alta
        - Media Baja
        - Media Alta
        - Alta

        El eje Y muestra la "Probabilidad de moverse a otra Clase".
        """)


def random_filter_selection():
    """
    Elige aleatoriamente 2 variables y 1..3 categorías de cada una.
    """
    import random
    for var in POSSIBLE_VARS:
        st.session_state[f"cats_{var}"] = []

    # Elige 2 variables al azar
    num_vars = 2
    chosen_vars = random.sample(POSSIBLE_VARS, num_vars)
    st.session_state['selected_vars'] = chosen_vars

    # Para cada variable, elige categorías
    for var in chosen_vars:
        cat_options = VAR_CATEGORIES.get(var, [])
        if not cat_options:
            continue
        # Escoge 1..3 categorías
        num_cats = random.randint(1, min(3, len(cat_options)))
        chosen_cats = random.sample(cat_options, num_cats)
        st.session_state[f"cats_{var}"] = chosen_cats

    st.rerun()


def apply_dynamic_filter(df):
    """
    Aplica un filtro a df en función de 'selected_vars'
    y las categorías elegidas en st.session_state[f"cats_{var}"].
    """
    dff = df.copy()
    for var in st.session_state['selected_vars']:
        chosen_cats = st.session_state.get(f"cats_{var}", [])
        if chosen_cats:
            dff = dff[dff[var].isin(chosen_cats)]
    return dff


def show_base_filters(df):
    """
    Muestra en la barra lateral los filtros para la 'base'.
    Guarda el resultado en st.session_state['df_base'].
    """
    if 'base_selected_vars' not in st.session_state:
        st.session_state['base_selected_vars'] = []
    for var in POSSIBLE_VARS:
        key_base_cats = f"base_cats_{var}"
        if key_base_cats not in st.session_state:
            st.session_state[key_base_cats] = []

    st.sidebar.markdown("**Base personalizada**:")

    st.session_state['base_selected_vars'] = st.sidebar.multiselect(
        "Variables base:",
        options=POSSIBLE_VARS,
        default=st.session_state['base_selected_vars'],
        max_selections=3
    )

    for var in st.session_state['base_selected_vars']:
        cat_options = VAR_CATEGORIES.get(var, [])
        st.session_state[f"base_cats_{var}"] = st.sidebar.multiselect(
            f"{var.capitalize()} (base):",
            cat_options,
            default=st.session_state[f"base_cats_{var}"]
        )

    dff = df.copy()
    for var in st.session_state['base_selected_vars']:
        chosen_cats = st.session_state.get(f"base_cats_{var}", [])
        if chosen_cats:
            dff = dff[dff[var].isin(chosen_cats)]
    st.session_state['df_base'] = dff


def describe_filter_selection(selected_vars, prefix="", base=False):
    """
    Construye una cadena con las variables y categorías seleccionadas.
    Ej: "Filtro: [generation=Millennial, sex=Mujer]"
    """
    parts = []
    for var in selected_vars:
        chosen_cats = st.session_state.get(f"{'base_cats_' if base else 'cats_'}{var}", [])
        if chosen_cats:
            cats_str = ", ".join(chosen_cats)
            parts.append(f"{var}={cats_str}")

    if parts:
        return prefix + "[" + "; ".join(parts) + "]"
    else:
        return prefix + "(Sin selección)"


def plot_mobility_interactive(df_filter, df_base, title_text):
    """
    Produce 2 subplots (Origen Clase Baja y Origen Clase Alta) con Plotly, en modo de barras:
    - "Base" (gris, opacity=0.2)
    - "Filtro" (skyblue / salmon)
    Muestra las etiquetas en dos renglones:
       line1: "XX.X%"
       line2: "(+YY.Y%)"
    """

    # Cálculo de distribuciones
    # Origen Clase Baja (Q1)
    q1_base = df_base[df_base['a_los_14_quintile'] == 1]
    q1_dist_base = q1_base['actualmente_quintile'].value_counts(normalize=True)*100
    q1_dist_base = q1_dist_base.sort_index()

    q1_filter = df_filter[df_filter['a_los_14_quintile'] == 1]
    q1_dist_filter = q1_filter['actualmente_quintile'].value_counts(normalize=True)*100
    q1_dist_filter = q1_dist_filter.sort_index()

    # Origen Clase Alta (Q5)
    q5_base = df_base[df_base['a_los_14_quintile'] == 5]
    q5_dist_base = q5_base['actualmente_quintile'].value_counts(normalize=True)*100
    q5_dist_base = q5_dist_base.sort_index()

    q5_filter = df_filter[df_filter['a_los_14_quintile'] == 5]
    q5_dist_filter = q5_filter['actualmente_quintile'].value_counts(normalize=True)*100
    q5_dist_filter = q5_dist_filter.sort_index()

    quintil_labels = {
        1: "Baja Baja",
        2: "Baja Alta",
        3: "Media Baja",
        4: "Media Alta",
        5: "Alta"
    }

    # Ejes X
    x_q1 = list(q1_dist_filter.index)
    x_q5 = list(q5_dist_filter.index)

    # Textos para Q1 base/filtro
    text_q1_base = []
    text_q1_filter = []
    for quintil in x_q1:
        val_f = q1_dist_filter.get(quintil, 0)
        val_b = q1_dist_base.get(quintil, 0)
        diff  = val_f - val_b
        # Dividimos en 2 renglones
        txt = f"{val_f:.1f}%<br>({diff:+.1f}%)"
        text_q1_filter.append(txt)

        # Base: solo el porcentaje
        text_q1_base.append(f"{val_b:.1f}%")

    # Textos para Q5 base/filtro
    text_q5_base = []
    text_q5_filter = []
    for quintil in x_q5:
        val_f = q5_dist_filter.get(quintil, 0)
        val_b = q5_dist_base.get(quintil, 0)
        diff  = val_f - val_b
        txt = f"{val_f:.1f}%<br>({diff:+.1f}%)"
        text_q5_filter.append(txt)
        text_q5_base.append(f"{val_b:.1f}%")

    # Crear subplots con Plotly
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Origen Clase Baja", "Origen Clase Alta"),
        shared_yaxes=True
    )

    # Subplot 1 (Q1)
    fig.add_trace(
        go.Bar(
            x=[quintil_labels.get(k, str(k)) for k in x_q1],
            y=[q1_dist_base.get(k, 0) for k in x_q1],
            name="Base",
            marker_color="gray",
            opacity=0.2,
            text=text_q1_base,
            textposition='outside',
            hoverinfo='none'
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(
            x=[quintil_labels.get(k, str(k)) for k in x_q1],
            y=[q1_dist_filter.get(k, 0) for k in x_q1],
            name="Filtro",
            marker_color="skyblue",
            text=text_q1_filter,
            textposition='outside',
            hovertemplate='%{text}<extra></extra>'
        ),
        row=1, col=1
    )

    # Subplot 2 (Q5)
    fig.add_trace(
        go.Bar(
            x=[quintil_labels.get(k, str(k)) for k in x_q5],
            y=[q5_dist_base.get(k, 0) for k in x_q5],
            name="Base",
            marker_color="gray",
            opacity=0.2,
            text=text_q5_base,
            textposition='outside',
            hoverinfo='none'
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(
            x=[quintil_labels.get(k, str(k)) for k in x_q5],
            y=[q5_dist_filter.get(k, 0) for k in x_q5],
            name="Filtro",
            marker_color="salmon",
            text=text_q5_filter,
            textposition='outside',
            hovertemplate='%{text}<extra></extra>'
        ),
        row=1, col=2
    )

    # Actualizar layout
    fig.update_layout(
        title=title_text,
        barmode='group',
        showlegend=True,
        width=900,  # Reducido de 1000 a 900
        height=600  # Reducido de 800 a 600
    )

    # Ocultar marcos superior y derecho en ambos subplots, y el izquierdo en Q5
    for i in range(1, 3):
        fig.update_xaxes(showline=False, showgrid=False, row=1, col=i)
        fig.update_yaxes(showline=False, showgrid=False, row=1, col=i)
        if i == 2:
            fig.update_yaxes(showline=False, showgrid=False, row=1, col=i, showticklabels=True)
            # En Plotly, los marcos no son tan directos, pero podemos ajustar el layout
            # Si necesitas más personalización, podrías usar shapes or other properties
    fig.update_yaxes(title_text="Probabilidad de moverse a otra Clase", row=1, col=1)

    return fig
