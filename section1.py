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
    Sección 1 (Movilidad).
    Genera la gráfica "Movilidad Socioeconómica Q1 vs Q5" usando Plotly.
    Los botones de refresh/aleatoriedad están en main.py, no aquí.
    """

    # 1) Manejo de estado: selected_vars
    if 'selected_vars' not in st.session_state:
        st.session_state['selected_vars'] = []
    for var in POSSIBLE_VARS:
        key_name = f"cats_{var}"
        if key_name not in st.session_state:
            st.session_state[key_name] = []

    # 2) Barra lateral (filtros) - sin refresh/aleatoriedad
    st.sidebar.subheader("Filtro actual (filtro principal):")
    st.session_state['selected_vars'] = st.sidebar.multiselect(
        "Selecciona las variables (máximo 3)",
        options=POSSIBLE_VARS,
        default=st.session_state['selected_vars'],
        max_selections=3
    )
    for var in st.session_state['selected_vars']:
        cat_options = VAR_CATEGORIES.get(var, [])
        st.session_state[f"cats_{var}"] = st.sidebar.multiselect(
            f"{var.capitalize()}:",
            cat_options,
            default=st.session_state[f"cats_{var}"]
        )

    st.sidebar.markdown("---")
    cambiar_base = st.sidebar.checkbox("Cambiar base", value=False)
    if cambiar_base:
        show_base_filters(load_and_process_data())

    # 3) Carga y filtra
    df = load_and_process_data()
    df_filter = apply_dynamic_filter(df)
    if cambiar_base and 'df_base' in st.session_state:
        df_base = st.session_state['df_base']
    else:
        df_base = df

    # 4) Título dinámico de la gráfica
    filter_desc = describe_filter_selection(st.session_state['selected_vars'], prefix="Filtro: ")
    if cambiar_base and 'base_selected_vars' in st.session_state and st.session_state['base_selected_vars']:
        base_desc = describe_filter_selection(st.session_state['base_selected_vars'], prefix="Base: ", base=True)
        main_title = f"Movilidad Socioeconómica Q1 vs Q5 | {filter_desc} vs {base_desc}"
    else:
        main_title = "Movilidad Socioeconómica Q1 vs Q5"
        if filter_desc and filter_desc != "(Sin selección)":
            main_title += f" | {filter_desc}"

    # 5) Generar la gráfica interactiva
    fig = plot_mobility_interactive(df_filter, df_base, main_title)
    st.plotly_chart(fig, use_container_width=True)

    # 6) Pie de logos
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

    with st.sidebar.expander("Detalles"):
        st.write("""
        Origen Clase Baja = Q1.
        Origen Clase Alta = Q5.

        Eje X: [Baja Baja, Baja Alta, Media Baja, Media Alta, Alta].
        Eje Y: "Probabilidad de moverse a otra Clase".
        """)


def random_filter_selection_section1():
    """Elige aleatoriamente 2 variables y 1..3 categorías de cada una (para Sección 1)."""
    import random
    for var in POSSIBLE_VARS:
        st.session_state[f"cats_{var}"] = []

    num_vars = 2
    chosen_vars = random.sample(POSSIBLE_VARS, num_vars)
    st.session_state['selected_vars'] = chosen_vars

    for var in chosen_vars:
        cat_options = VAR_CATEGORIES.get(var, [])
        if cat_options:
            num_cats = random.randint(1, min(3, len(cat_options)))
            chosen_cats = random.sample(cat_options, num_cats)
            st.session_state[f"cats_{var}"] = chosen_cats


def show_base_filters(df):
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


def apply_dynamic_filter(df):
    dff = df.copy()
    for var in st.session_state['selected_vars']:
        chosen_cats = st.session_state.get(f"cats_{var}", [])
        if chosen_cats:
            dff = dff[dff[var].isin(chosen_cats)]
    return dff


def describe_filter_selection(selected_vars, prefix="", base=False):
    parts = []
    for var in selected_vars:
        chosen_cats = st.session_state.get(f"{'base_cats_' if base else 'cats_'}{var}", [])
        if chosen_cats:
            cats_str = ", ".join(chosen_cats)
            parts.append(f"{var}={cats_str}")

    if parts:
        return prefix + "[" + "; ".join(parts) + "]"
    else:
        return "(Sin selección)"


def plot_mobility_interactive(df_filter, df_base, main_title):
    """
    Produce 2 subplots en la misma fila (Origen Clase Baja Q1 vs Origen Clase Alta Q5),
    con:

    - Base (gris con opacidad)
    - Filtro Q1 = skyblue
    - Filtro Q5 = salmon

    Se ajusta el Y-range en la subgráfica 1 para ~10% extra.
    Se quita el Eje Y en la subgráfica 2.
    Etiquetas grandes y en 2 líneas, con color verde/rojo según la diferencia.
    """

    # --- Datos Q1
    q1_base = df_base[df_base['a_los_14_quintile'] == 1]
    q1_b = q1_base['actualmente_quintile'].value_counts(normalize=True)*100
    q1_b = q1_b.sort_index()

    q1_filter = df_filter[df_filter['a_los_14_quintile'] == 1]
    q1_f = q1_filter['actualmente_quintile'].value_counts(normalize=True)*100
    q1_f = q1_f.sort_index()

    # --- Datos Q5
    q5_base = df_base[df_base['a_los_14_quintile'] == 5]
    q5_b = q5_base['actualmente_quintile'].value_counts(normalize=True)*100
    q5_b = q5_b.sort_index()

    q5_filter = df_filter[df_filter['a_los_14_quintile'] == 5]
    q5_f = q5_filter['actualmente_quintile'].value_counts(normalize=True)*100
    q5_f = q5_f.sort_index()

    quintil_labels = {
        1: "Baja Baja",
        2: "Baja Alta",
        3: "Media Baja",
        4: "Media Alta",
        5: "Alta"
    }

    x_q1 = list(q1_f.index)
    x_q5 = list(q5_f.index)

    # Preparamos texto y colores
    text_q1_f, color_q1_f, yvals_q1_f = [], [], []
    for quintil in x_q1:
        val_f = q1_f.get(quintil, 0)
        val_b = q1_b.get(quintil, 0)
        diff = val_f - val_b
        sign_color = "green" if diff >= 0 else "red"
        txt = f"{val_f:.1f}%<br>({diff:+.1f}%)"
        text_q1_f.append(txt)
        color_q1_f.append(sign_color)
        yvals_q1_f.append(val_f)

    text_q5_f, color_q5_f, yvals_q5_f = [], [], []
    for quintil in x_q5:
        val_f = q5_f.get(quintil, 0)
        val_b = q5_b.get(quintil, 0)
        diff = val_f - val_b
        sign_color = "green" if diff >= 0 else "red"
        txt = f"{val_f:.1f}%<br>({diff:+.1f}%)"
        text_q5_f.append(txt)
        color_q5_f.append(sign_color)
        yvals_q5_f.append(val_f)

    # Subplots
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=["Origen Clase Baja", "Origen Clase Alta"],
                        shared_yaxes=False)

    # Gráfica Q1 - Base
    fig.add_trace(
        go.Bar(
            x=[quintil_labels.get(k, str(k)) for k in x_q1],
            y=[q1_b.get(k, 0) for k in x_q1],
            marker_color="gray",
            opacity=0.2,
            name="Base",
            text=[f"{q1_b.get(k,0):.1f}%" for k in x_q1],
            textposition="outside",
            hoverinfo='none'
        ),
        row=1, col=1
    )
    # Gráfica Q1 - Filtro
    fig.add_trace(
        go.Bar(
            x=[quintil_labels.get(k, str(k)) for k in x_q1],
            y=yvals_q1_f,
            marker_color="skyblue",
            name="Filtro",
            text=text_q1_f,
            textposition="outside",
            textfont_size=13,
            textfont_color=color_q1_f,  # color verde o rojo
            hovertemplate='%{text}<extra></extra>'
        ),
        row=1, col=1
    )

    # Ajuste del rango Y en la subgráfica 1 (+10%)
    max_q1 = 0
    if q1_b.size > 0:
        max_q1 = max(max_q1, q1_b.max())
    if q1_f.size > 0:
        max_q1 = max(max_q1, q1_f.max())
    fig.update_yaxes(range=[0, max_q1 * 1.1], row=1, col=1)

    # Gráfica Q5 - Base
    fig.add_trace(
        go.Bar(
            x=[quintil_labels.get(k, str(k)) for k in x_q5],
            y=[q5_b.get(k, 0) for k in x_q5],
            marker_color="gray",
            opacity=0.2,
            name="Base",
            text=[f"{q5_b.get(k,0):.1f}%" for k in x_q5],
            textposition="outside",
            hoverinfo='none'
        ),
        row=1, col=2
    )
    # Gráfica Q5 - Filtro
    fig.add_trace(
        go.Bar(
            x=[quintil_labels.get(k, str(k)) for k in x_q5],
            y=yvals_q5_f,
            marker_color="salmon",
            name="Filtro",
            text=text_q5_f,
            textposition="outside",
            textfont_size=13,
            textfont_color=color_q5_f,
            hovertemplate='%{text}<extra></extra>'
        ),
        row=1, col=2
    )

    # Ocultar eje Y en subgráfica 2
    fig.update_yaxes(visible=False, row=1, col=2)

    # Configurar layout
    fig.update_layout(
        title=main_title,
        barmode='group',
        showlegend=True,
        width=900,
        height=600
    )
    # Eje Y => "Probabilidad de moverse a otra Clase" en col=1
    fig.update_yaxes(title_text="Probabilidad de moverse a otra Clase", row=1, col=1)

    # Ocultar marcos superiores/derechos
    fig.update_xaxes(showline=False, showgrid=False)
    fig.update_yaxes(showline=False, showgrid=False)

    return fig
