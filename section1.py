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

    # 2) Botón Refresh (superior)
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.markdown("<h2 style='margin-bottom:0;'>Movilidad Socioeconómica Q1 vs Q5</h2>", unsafe_allow_html=True)
    with col2:
        if st.button("⟳", help="Recargar la app (reset a valores originales)"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()  # Usar st.rerun() en versiones >= 1.18

    st.markdown("Visualiza cómo cambian los quintiles de riqueza desde la infancia (Q1 o Q5) hasta la actualidad.")

    # 3) Barra lateral: Filtro Actual
    st.sidebar.subheader("Filtro actual (filtro principal):")

    # Botón de “dados” (en lugar de "Aleatoriedad")
    if st.sidebar.button("🎲", help="Selecciona 2 variables y 1-3 categorías al azar"):
        random_filter_selection()

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

    # Cargar datos
    df = load_and_process_data()

    # Aplicar el filtro principal
    df_filter = apply_dynamic_filter(df)

    # 4) Cambiar base
    st.sidebar.markdown("---")
    cambiar_base = st.sidebar.checkbox("Cambiar base", value=False)

    if cambiar_base:
        show_base_filters(df)
    else:
        df_base = df

    # 5) Mostrar gráfica
    if cambiar_base and 'df_base' in st.session_state:
        fig = plot_mobility(df_filter, st.session_state['df_base'])
    else:
        fig = plot_mobility(df_filter, df)

    st.pyplot(fig)

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
        # Escoge un número random de categorías entre 1 y 3
        num_cats = random.randint(1, min(3, len(cat_options)))
        chosen_cats = random.sample(cat_options, num_cats)
        st.session_state[f"cats_{var}"] = chosen_cats

    st.rerun()

def apply_dynamic_filter(df):
    """ 
    Aplica un filtro a df en función de las 'selected_vars'
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
    Se guarda el resultado en st.session_state['df_base'].
    """
    # Variables de base
    if 'base_selected_vars' not in st.session_state:
        st.session_state['base_selected_vars'] = []
    # Aseguramos listas de categorías
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

    # Guardarlo
    st.session_state['df_base'] = dff

def plot_mobility(df_filter, df_base):
    """
    Gráfica Q1 vs. Q5 comparando df_filter (filtro principal) contra df_base (la base).
    Muestra etiquetas con porcentajes y diferencias.
    """
    # Distribución "base"
    q1_base = df_base[df_base['a_los_14_quintile'] == 1]
    q5_base = df_base[df_base['a_los_14_quintile'] == 5]

    q1_dist_base = q1_base['actualmente_quintile'].value_counts(normalize=True)*100
    q5_dist_base = q5_base['actualmente_quintile'].value_counts(normalize=True)*100

    q1_dist_base = q1_dist_base.sort_index()
    q5_dist_base = q5_dist_base.sort_index()

    # Distribución "filtro"
    q1_filter = df_filter[df_filter['a_los_14_quintile'] == 1]
    q5_filter = df_filter[df_filter['a_los_14_quintile'] == 5]

    q1_dist_filter = q1_filter['actualmente_quintile'].value_counts(normalize=True)*100
    q5_dist_filter = q5_filter['actualmente_quintile'].value_counts(normalize=True)*100

    q1_dist_filter = q1_dist_filter.sort_index()
    q5_dist_filter = q5_dist_filter.sort_index()

    # Crear la figura (más grande, título más pequeño)
    fig, ax = plt.subplots(1, 2, figsize=(14, 8), sharey=True)

    # ---- Q1
    ax[0].bar(q1_dist_base.index.astype(str),
              q1_dist_base.values,
              alpha=0.2, color='gray', label='Base')
    ax[0].bar(q1_dist_filter.index.astype(str),
              q1_dist_filter.values,
              alpha=1.0, color='skyblue', label='Filtro')

    ax[0].set_title("Q1 (Origen)", fontsize=11)
    ax[0].set_xlabel("Quintil actual")
    ax[0].set_ylabel("% de personas")
    ax[0].legend()

    # Etiquetas Q1
    for i, quintil in enumerate(q1_dist_filter.index):
        val_f = q1_dist_filter[quintil]
        val_b = q1_dist_base[quintil] if quintil in q1_dist_base else 0
        diff  = val_f - val_b
        color = 'green' if diff >= 0 else 'red'
        label = f"{val_f:.1f}% ({diff:+.1f}%)"
        ax[0].text(
            x=i,
            y=val_f + 1,
            s=label,
            ha='center',
            color=color,
            fontsize=9
        )

    # ---- Q5
    ax[1].bar(q5_dist_base.index.astype(str),
              q5_dist_base.values,
              alpha=0.2, color='gray', label='Base')
    ax[1].bar(q5_dist_filter.index.astype(str),
              q5_dist_filter.values,
              alpha=1.0, color='salmon', label='Filtro')

    ax[1].set_title("Q5 (Origen)", fontsize=11)
    ax[1].set_xlabel("Quintil actual")
    ax[1].legend()

    # Etiquetas Q5
    for i, quintil in enumerate(q5_dist_filter.index):
        val_f = q5_dist_filter[quintil]
        val_b = q5_dist_base[quintil] if quintil in q5_dist_base else 0
        diff  = val_f - val_b
        color = 'green' if diff >= 0 else 'red'
        label = f"{val_f:.1f}% ({diff:+.1f}%)"
        ax[1].text(
            x=i,
            y=val_f + 1,
            s=label,
            ha='center',
            color=color,
            fontsize=9
        )

    plt.suptitle("Movilidad socioeconómica: Q1 vs Q5", fontsize=13)
    plt.tight_layout()
    return fig
