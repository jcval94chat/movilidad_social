# section1.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

from data_utils import load_and_process_data
from config import VAR_CATEGORIES, POSSIBLE_VARS

def show_section1():
    """
    Muestra la sección principal de "Movilidad Socioeconómica Q1 vs Q5".
    """
    # 1) Manejo de estado
    if 'selected_vars' not in st.session_state:
        st.session_state['selected_vars'] = []
    # Aseguramos que cada variable tenga su lista de categorías
    for var in POSSIBLE_VARS:
        key_name = f"cats_{var}"
        if key_name not in st.session_state:
            st.session_state[key_name] = []

    # 2) Encabezado con botones: Refresh y Dados
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    with col1:
        st.markdown("<h2 style='margin-bottom:0;'>Movilidad Socioeconómica Q1 vs Q5</h2>", unsafe_allow_html=True)
    with col2:
        # Botón Refresh
        if st.button("⟳", help="Recargar la app (reset a valores originales)"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()  # En Streamlit >= 1.18
    with col3:
        # Botón de Dados (aleatoriedad)
        if st.button("🎲", help="Selecciona 2 variables y 1-3 categorías al azar"):
            random_filter_selection()

    st.markdown("Visualiza cómo cambian los quintiles de riqueza desde la infancia (Q1 o Q5) hasta la actualidad.")

    # 3) Barra lateral: Selección de variables y categorías
    st.sidebar.subheader("Filtro actual (filtro principal):")

    # Multiselect de variables
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

    # Carga de datos
    df = load_and_process_data()

    # Aplicar el filtro principal
    df_filter = apply_dynamic_filter(df)

    # 4) Cambiar base
    st.sidebar.markdown("---")
    cambiar_base = st.sidebar.checkbox("Cambiar base", value=False)
    if cambiar_base:
        show_base_filters(df)
        df_base = st.session_state.get('df_base', df)
    else:
        df_base = df

    # 5) Construir un título dinámico según el filtro y la base
    filter_desc = describe_filter_selection(st.session_state['selected_vars'], prefix="Filtro: ")
    if cambiar_base and 'base_selected_vars' in st.session_state and st.session_state['base_selected_vars']:
        base_desc = describe_filter_selection(st.session_state['base_selected_vars'], prefix="Base: ", base=True)
        main_title = f"{filter_desc} vs {base_desc}"
    else:
        main_title = filter_desc or "Sin Filtro (Base General)"

    # 6) Mostrar gráfica
    fig = plot_mobility(df_filter, df_base, main_title)
    st.pyplot(fig)

    # 7) Logos al final de la página
    st.markdown("---")
    st.markdown("### ")
    c1, c2 = st.columns([0.1, 0.1])
    with c1:
        # Logo YouTube
        st.markdown(
            "[![YouTube](https://cdn-icons-png.flaticon.com/512/1384/1384060.png)]"
            "(https://www.youtube.com/@momentitocafecito)", 
            unsafe_allow_html=True
        )
    with c2:
        # Logo Instagram (ajusta tu enlace)
        st.markdown(
            "[![Instagram](https://cdn-icons-png.flaticon.com/512/1384/1384063.png)]"
            "(https://instagram.com/momentitocafecito)", 
            unsafe_allow_html=True
        )

    # 8) Detalles al final de la barra lateral
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
    # Limpiamos variables actuales
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
    # Variables de base
    if 'base_selected_vars' not in st.session_state:
        st.session_state['base_selected_vars'] = []
    # Aseguramos listas de categorías para la base
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

    # Aplicar ese filtro
    dff = df.copy()
    for var in st.session_state['base_selected_vars']:
        chosen_cats = st.session_state.get(f"base_cats_{var}", [])
        if chosen_cats:
            dff = dff[dff[var].isin(chosen_cats)]

    # Guardarlo en session_state
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
        # Si no hay nada seleccionado
        return prefix + "(Sin selección)"

def plot_mobility(df_filter, df_base, title_text):
    """
    Gráfica Q1 vs. Q5 comparando df_filter (filtro principal) vs df_base (la base).
    - Q1 -> "Origen Clase Baja"
    - Q5 -> "Origen Clase Alta"
    - Eje X -> ["Baja Baja","Baja Alta","Media Baja","Media Alta","Alta"]
    - Eje Y -> "Probabilidad de moverse a otra Clase"
    - Etiquetas de barra un poco más grandes (fontsize=11)
    """
    # Distribución base
    q1_base = df_base[df_base['a_los_14_quintile'] == 1]
    q5_base = df_base[df_base['a_los_14_quintile'] == 5]

    q1_dist_base = q1_base['actualmente_quintile'].value_counts(normalize=True)*100
    q5_dist_base = q5_base['actualmente_quintile'].value_counts(normalize=True)*100

    q1_dist_base = q1_dist_base.sort_index()
    q5_dist_base = q5_dist_base.sort_index()

    # Distribución filtro
    q1_filter = df_filter[df_filter['a_los_14_quintile'] == 1]
    q5_filter = df_filter[df_filter['a_los_14_quintile'] == 5]

    q1_dist_filter = q1_filter['actualmente_quintile'].value_counts(normalize=True)*100
    q5_dist_filter = q5_filter['actualmente_quintile'].value_counts(normalize=True)*100

    q1_dist_filter = q1_dist_filter.sort_index()
    q5_dist_filter = q5_dist_filter.sort_index()

    # Crear figura
    fig, ax = plt.subplots(1, 2, figsize=(14, 8), sharey=True)

    # Etiquetas de quintil
    quintil_labels = {
        1: "Baja Baja",
        2: "Baja Alta",
        3: "Media Baja",
        4: "Media Alta",
        5: "Alta"
    }

    # Para Q1
    x_q1 = q1_dist_filter.index
    ax[0].bar(x_q1, q1_dist_base.reindex(x_q1, fill_value=0).values,
              alpha=0.2, color='gray', label='Base')
    ax[0].bar(x_q1, q1_dist_filter.values,
              alpha=1.0, color='skyblue', label='Filtro')
    ax[0].set_title("Origen Clase Baja", fontsize=11)
    ax[0].set_xlabel("")
    ax[0].set_ylabel("Probabilidad de moverse a otra Clase")
    ax[0].legend()

    # Eliminar marco superior y derecho
    ax[0].spines["top"].set_visible(False)
    ax[0].spines["right"].set_visible(False)

    # Etiquetas Q1
    for i, quintil in enumerate(x_q1):
        val_f = q1_dist_filter[quintil]
        val_b = q1_dist_base[quintil] if quintil in q1_dist_base else 0
        diff  = val_f - val_b
        color = 'green' if diff >= 0 else 'red'
        label = f"{val_f:.1f}% ({diff:+.1f}%)"
        ax[0].text(
            x=quintil,
            y=val_f + 1,
            s=label,
            ha='center',
            color=color,
            fontsize=11
        )

    # Eje X con etiquetas
    ax[0].set_xticks(x_q1)
    ax[0].set_xticklabels([quintil_labels.get(i, str(i)) for i in x_q1])

    # Para Q5
    x_q5 = q5_dist_filter.index
    ax[1].bar(x_q5, q5_dist_base.reindex(x_q5, fill_value=0).values,
              alpha=0.2, color='gray', label='Base')
    ax[1].bar(x_q5, q5_dist_filter.values,
              alpha=1.0, color='salmon', label='Filtro')
    ax[1].set_title("Origen Clase Alta", fontsize=11)
    ax[1].set_xlabel("")

    # Eliminar marco superior, derecho e izquierdo
    ax[1].spines["top"].set_visible(False)
    ax[1].spines["right"].set_visible(False)
    ax[1].spines["left"].set_visible(False)

    # Etiquetas Q5
    for i, quintil in enumerate(x_q5):
        val_f = q5_dist_filter[quintil]
        val_b = q5_dist_base[quintil] if quintil in q5_dist_base else 0
        diff  = val_f - val_b
        color = 'green' if diff >= 0 else 'red'
        label = f"{val_f:.1f}% ({diff:+.1f}%)"
        ax[1].text(
            x=quintil,
            y=val_f + 1,
            s=label,
            ha='center',
            color=color,
            fontsize=11
        )

    ax[1].set_xticks(x_q5)
    ax[1].set_xticklabels([quintil_labels.get(i, str(i)) for i in x_q5])

    # Título principal dinámico
    plt.suptitle(title_text, fontsize=13)
    plt.tight_layout()
    return fig
