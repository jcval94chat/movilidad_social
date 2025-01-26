# section1.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_utils import load_and_process_data
from config import VAR_CATEGORIES, POSSIBLE_VARS

# Paleta de colores (compartida con la Sección 2)
BASE_COLOR = "gray"
PRIMARY_COLOR = "skyblue"
SECONDARY_COLOR = "salmon"

def show_section1():
    """
    Sección 1: Movilidad Socioeconómica Q1 vs Q5.
    Con Plotly interactivo, ejes ajustados, y botones en la barra lateral.
    """

    # 1) Inicializar estado
    if 'selected_vars' not in st.session_state:
        st.session_state['selected_vars'] = []
    for var in POSSIBLE_VARS:
        key_name = f"cats_{var}"
        if key_name not in st.session_state:
            st.session_state[key_name] = []

    # ---------------------------
    # 2) Botones en la barra lateral (a la derecha de "Filtro actual")
    # ---------------------------
    st.sidebar.subheader("Filtro actual (filtro principal):")
    col_side1, col_side2 = st.sidebar.columns([0.7, 0.3])
    with col_side2:
        # Botón Refresh
        if st.button("⟳", help="Reset Sección 1", key="refresh_s1"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        # Botón Aleatorio
        if st.button("🎲", help="Aleatoriedad Sección 1", key="random_s1"):
            random_filter_selection()
            st.rerun()

    # ---------------------------
    # 3) Multiselect variables
    # ---------------------------
    st.session_state['selected_vars'] = st.sidebar.multiselect(
        "Selecciona las variables (máximo 3)",
        options=POSSIBLE_VARS,
        default=st.session_state['selected_vars'],
        max_selections=3
    )

    # Para cada variable seleccionada
    for var in st.session_state['selected_vars']:
        cat_options = VAR_CATEGORIES.get(var, [])
        st.session_state[f"cats_{var}"] = st.sidebar.multiselect(
            f"{var.capitalize()}:",
            cat_options,
            default=st.session_state[f"cats_{var}"]
        )

    # 4) Carga de datos
    df = load_and_process_data()

    # 5) Filtro principal
    df_filter = apply_dynamic_filter(df)

    # 6) Cambiar base
    st.sidebar.markdown("---")
    cambiar_base = st.sidebar.checkbox("Cambiar base", value=False)
    if cambiar_base:
        show_base_filters(df)
        df_base = st.session_state.get('df_base', df)
    else:
        df_base = df

    # 7) Construir título dinámico
    filter_desc = describe_filter_selection(st.session_state['selected_vars'], prefix="Filtro: ")
    if cambiar_base and 'base_selected_vars' in st.session_state and st.session_state['base_selected_vars']:
        base_desc = describe_filter_selection(st.session_state['base_selected_vars'], prefix="Base: ", base=True)
        main_title = f"{filter_desc} vs {base_desc}"
    else:
        main_title = filter_desc or "Sin Filtro (Base General)"

    # 8) Gráfica Plotly
    fig = plot_mobility_q1_q5(df_filter, df_base, title_text="Movilidad Socioeconómica Q1 vs Q5", subtitle=main_title)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------
# Funciones auxiliares
# ----------------------------------------------------------------------

def random_filter_selection():
    """Elige aleatoriamente 2 variables y 1..3 categorías."""
    import random
    for var in POSSIBLE_VARS:
        st.session_state[f"cats_{var}"] = []

    num_vars = 2
    chosen_vars = random.sample(POSSIBLE_VARS, num_vars)
    st.session_state['selected_vars'] = chosen_vars

    for var in chosen_vars:
        cat_options = VAR_CATEGORIES.get(var, [])
        if not cat_options:
            continue
        n_cats = random.randint(1, min(3, len(cat_options)))
        chosen = random.sample(cat_options, n_cats)
        st.session_state[f"cats_{var}"] = chosen

def apply_dynamic_filter(df):
    """Aplica el filtro según st.session_state['selected_vars'] y cats_{var}."""
    dff = df.copy()
    for var in st.session_state['selected_vars']:
        chosen_cats = st.session_state.get(f"cats_{var}", [])
        if chosen_cats:
            dff = dff[dff[var].isin(chosen_cats)]
    return dff

def show_base_filters(df):
    """Checkboxes para definir la base de comparación en la barra lateral."""
    if 'base_selected_vars' not in st.session_state:
        st.session_state['base_selected_vars'] = []
    for var in POSSIBLE_VARS:
        base_cat_key = f"base_cats_{var}"
        if base_cat_key not in st.session_state:
            st.session_state[base_cat_key] = []

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
    """Construye una cadena con las variables/categorías seleccionadas."""
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

def plot_mobility_q1_q5(df_filter, df_base, title_text, subtitle=""):
    """
    Gráfica Q1 vs Q5 con Plotly.
    - Eje Y: un 10% más alto para no recortar etiquetas.
    - Etiquetas más grandes, color verde si diff>=0, rojo si diff<0.
    - Se quita el eje Y en la parte de Q5 (origen clase alta).
    - Usa la misma paleta de colores definidas al inicio.
    """
    # Distribuciones
    q1b = df_base[df_base['a_los_14_quintile'] == 1]
    q1_base_dist = q1b['actualmente_quintile'].value_counts(normalize=True)*100

    q1f = df_filter[df_filter['a_los_14_quintile'] == 1]
    q1_filt_dist = q1f['actualmente_quintile'].value_counts(normalize=True)*100

    q5b = df_base[df_base['a_los_14_quintile'] == 5]
    q5_base_dist = q5b['actualmente_quintile'].value_counts(normalize=True)*100

    q5f = df_filter[df_filter['a_los_14_quintile'] == 5]
    q5_filt_dist = q5f['actualmente_quintile'].value_counts(normalize=True)*100

    quintil_labels = {
        1: "Baja Baja",
        2: "Baja Alta",
        3: "Media Baja",
        4: "Media Alta",
        5: "Alta"
    }

    x_q1 = sorted(q1_filt_dist.index)
    x_q5 = sorted(q5_filt_dist.index)

    # Preparamos datos Q1
    base_y_q1 = [q1_base_dist.get(k, 0) for k in x_q1]
    filt_y_q1 = [q1_filt_dist.get(k, 0) for k in x_q1]

    # Text (2 líneas) + color distinto según diff
    text_q1_base = []
    text_q1_filter = []
    color_q1_filter = []
    for i, k in enumerate(x_q1):
        val_b = base_y_q1[i]
        val_f = filt_y_q1[i]
        diff  = val_f - val_b
        # label en 2 líneas
        # -> line1 = "{val_f:.1f}%"
        # -> line2 = "(+/- X.X%)"
        lab = f"{val_f:.1f}%<br>({diff:+.1f}%)"
        text_q1_filter.append(lab)

        # Base no necesita 2 líneas
        text_q1_base.append(f"{val_b:.1f}%")

        color = "green" if diff >= 0 else "red"
        color_q1_filter.append(color)

    # Preparamos datos Q5
    base_y_q5 = [q5_base_dist.get(k, 0) for k in x_q5]
    filt_y_q5 = [q5_filt_dist.get(k, 0) for k in x_q5]

    text_q5_base = []
    text_q5_filter = []
    color_q5_filter = []
    for i, k in enumerate(x_q5):
        val_b = base_y_q5[i]
        val_f = filt_y_q5[i]
        diff  = val_f - val_b
        lab = f"{val_f:.1f}%<br>({diff:+.1f}%)"
        text_q5_filter.append(lab)

        text_q5_base.append(f"{val_b:.1f}%")

        color = "green" if diff >= 0 else "red"
        color_q5_filter.append(color)

    # Construimos subplots
    fig = make_subplots(
        rows=1, cols=2, shared_yaxes=True,
        subplot_titles=("Origen Clase Baja", "Origen Clase Alta")
    )

    # Q1 - Base
    fig.add_trace(
        go.Bar(
            x=[quintil_labels[k] for k in x_q1],
            y=base_y_q1,
            name="Base",
            marker_color=BASE_COLOR,
            opacity=0.2,
            text=text_q1_base,
            textposition='outside',
            hoverinfo='none'  # Para que no muestre tooltip
        ),
        row=1, col=1
    )
    # Q1 - Filtro
    fig.add_trace(
        go.Bar(
            x=[quintil_labels[k] for k in x_q1],
            y=filt_y_q1,
            name="Filtro",
            marker_color=PRIMARY_COLOR,
            text=text_q1_filter,
            textposition='outside',
            hovertemplate='%{text}<extra></extra>',
            # Colorear texto
            textfont=dict(color=color_q1_filter, size=13)
        ),
        row=1, col=1
    )

    # Q5 - Base
    fig.add_trace(
        go.Bar(
            x=[quintil_labels[k] for k in x_q5],
            y=base_y_q5,
            name="Base",
            marker_color=BASE_COLOR,
            opacity=0.2,
            text=text_q5_base,
            textposition='outside',
            hoverinfo='none'
        ),
        row=1, col=2
    )
    # Q5 - Filtro
    fig.add_trace(
        go.Bar(
            x=[quintil_labels[k] for k in x_q5],
            y=filt_y_q5,
            name="Filtro",
            marker_color=SECONDARY_COLOR,
            text=text_q5_filter,
            textposition='outside',
            hovertemplate='%{text}<extra></extra>',
            textfont=dict(color=color_q5_filter, size=13)
        ),
        row=1, col=2
    )

    # Aumentar el eje Y un 10%:
    # hallamos el valor más alto
    max_val_q1 = max(base_y_q1 + filt_y_q1) if (base_y_q1 + filt_y_q1) else 0
    max_val_q5 = max(base_y_q5 + filt_y_q5) if (base_y_q5 + filt_y_q5) else 0
    max_val = max(max_val_q1, max_val_q5) * 1.1  # 10% extra

    fig.update_yaxes(range=[0, max_val], row=1, col=1)
    fig.update_yaxes(range=[0, max_val], row=1, col=2)

    # Ocultar eje Y en Q5
    fig.update_yaxes(showticklabels=False, row=1, col=2)

    # Layout
    fig.update_layout(
        title={
            "text": f"{title_text}<br><span style='font-size:14px;'>{subtitle}</span>",
            "y":0.95,
            "x":0.5,
            "xanchor": "center",
            "yanchor": "top"
        },
        barmode='group',
        showlegend=True
    )

    # Ocultar marco top/right
    fig.update_xaxes(showline=False, showgrid=False)
    fig.update_yaxes(showline=False, showgrid=False)

    fig.update_yaxes(title_text="Probabilidad de moverse a otra Clase", row=1, col=1)

    return fig
