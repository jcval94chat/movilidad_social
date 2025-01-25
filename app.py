import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# --------------------------------------------------------------------------
# 1) Cargar datos y procesar
# --------------------------------------------------------------------------
@st.cache_data
def load_and_process_data():
    # Lee tus archivos .dta desde la carpeta 'data'
    # Ajusta las rutas según tu repositorio
    file_path_person = 'data/ESRU-EMOVI 2017 Entrevistado.dta'
    file_path_hogar  = 'data/ESRU-EMOVI 2017 Hogar.dta'

    df_person = pd.read_stata(file_path_person, convert_categoricals=False)
    df_hogar  = pd.read_stata(file_path_hogar,  convert_categoricals=False)

    # Merge
    df = pd.merge(
        df_person,
        df_hogar[['folio','consecutivo','p05h','p06h']],  
        on=['folio','consecutivo'],
        how='left'
    )

    # Variables y recodificación
    a_los_14_vars = [
        'p30_a','p30_b','p30_c','p30_d','p30_e',
        'p32_a','p32_b','p32_c','p32_d',
        'p33_a','p33_b','p33_c','p33_d','p33_e','p33_f','p33_g','p33_h','p33_i',
        'p33_j','p33_k','p33_l','p33_m','p33_n',
        'p34_a','p34_b','p34_c','p34_d','p34_e','p34_f','p34_g','p34_h'
    ]

    actualmente_vars = [
        'p125a','p125b','p125c','p125d','p125e',
        'p126a','p126b','p126c','p126d','p126e','p126f','p126g','p126h','p126i',
        'p126j','p126k','p126l','p126m','p126n','p126o','p126p','p126q','p126r',
        'p129a','p129b','p129c','p129d','p129e',
        'p131'
    ]

    def recodificar_01(valor):
        if pd.isna(valor):
            return 0
        elif valor == 1:
            return 1
        else:
            return 0

    # Recodificar a_los_14
    for var in a_los_14_vars:
        if var in df.columns:
            df[var] = df[var].apply(recodificar_01)

    # Recodificar actualmente
    for var in actualmente_vars:
        if var in df.columns and var != 'p131':
            df[var] = df[var].apply(recodificar_01)

    # p131 -> número de autos (0 => 0, >=1 =>1)
    if 'p131' in df.columns:
        df['p131'] = df['p131'].fillna(0)
        df['p131'] = np.where(df['p131'] >= 1, 1, 0)

    # Índices de riqueza
    df['a_los_14_wealth']       = df[a_los_14_vars].sum(axis=1)
    df['actualmente_wealth']    = df[actualmente_vars].sum(axis=1)
    df['actualmente_wealth2']   = df['actualmente_wealth']  # Ajuste si tuvieras p133

    # Asignar quintiles
    def asignar_quintil(serie):
        return pd.qcut(serie, q=5, labels=False, duplicates='drop') + 1

    df['a_los_14_quintile']    = asignar_quintil(df['a_los_14_wealth'])
    df['actualmente_quintile'] = asignar_quintil(df['actualmente_wealth2'])

    # Generación
    def assign_generation(age):
        if pd.isna(age):
            return "NA"
        age = int(age)
        if age <= 20:
            return "Gen Z"
        elif 21 <= age <= 36:
            return "Millennial"
        elif 37 <= age <= 52:
            return "Gen X"
        elif 53 <= age <= 71:
            return "Baby Boomer"
        else:
            return "Traditionalist"

    df['generation'] = df['p05h'].apply(assign_generation)

    # Sexo
    df['sex'] = df['p06h'].map({1: 'Hombre', 2: 'Mujer'})

    # EJEMPLO de "nivel de estudios" (ajusta a tu variable real)
    def assign_education(val):
        # E.g.: 1=Primaria, 2=Secundaria, 3=Prepa, 4=Uni, 5=Posg
        if pd.isna(val):
            return "NA"
        elif val == 1:
            return "Primaria"
        elif val == 2:
            return "Secundaria"
        elif val == 3:
            return "Preparatoria"
        elif val == 4:
            return "Universidad"
        elif val == 5:
            return "Posgrado"
        else:
            return "Otro"

    if 'p07' in df.columns:
        df['education'] = df['p07'].apply(assign_education)
    else:
        # Si no existe p07, crea un dummy random para demo
        df['education'] = np.random.choice(
            ['Primaria','Secundaria','Preparatoria','Universidad','Posgrado','Otro','NA'],
            size=len(df)
        )

    return df

# --------------------------------------------------------------------------
# 2) Filtrado dinámico: hasta 3 variables con selección múltiple de categorías
# --------------------------------------------------------------------------
def apply_dynamic_filter(df):
    """
    Aplica un filtro a df en función de st.session_state['selected_vars']
    y de las categorías elegidas en st.session_state[<var>].
    Si no se eligen categorías para una variable, NO se filtra por esa variable.
    """
    dff = df.copy()

    # Para cada variable en selected_vars, aplicamos un filtrado por las categorías elegidas
    for var in st.session_state['selected_vars']:
        chosen_cats = st.session_state.get(f"cats_{var}", [])
        # Si chosen_cats está vacío, interpretamos que NO se filtra esa variable
        if chosen_cats:
            dff = dff[dff[var].isin(chosen_cats)]

    return dff

# --------------------------------------------------------------------------
# 3) Función de graficación (Q1 vs. Q5)
#    con base personalizable y etiquetas con % y diferencia.
# --------------------------------------------------------------------------
def plot_mobility(df_filter, df_base):
    """
    - df_filter: DataFrame con el filtro actual del usuario.
    - df_base:   DataFrame que se toma como 'base' para comparar.
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

    # Gráfica
    fig, ax = plt.subplots(1, 2, figsize=(14, 8), sharey=True)

    # ---- Q1: Base vs Filtro
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

    # ---- Q5: Base vs Filtro
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

# --------------------------------------------------------------------------
# 4) Lógica de "aleatoriedad" (botón)
# --------------------------------------------------------------------------
def random_filter_selection():
    """
    Elige aleatoriamente 2 variables de entre las posibles
    y hasta 3 categorías de cada variable.
    """
    possible_vars = ['generation', 'sex', 'education']
    # Elige 2 variables al azar (puedes cambiar a 1..3 si deseas)
    num_vars = 2  
    chosen_vars = random.sample(possible_vars, num_vars)

    # Actualiza st.session_state['selected_vars']
    st.session_state['selected_vars'] = chosen_vars

    # Para cada variable, elige categorías
    for var in chosen_vars:
        if var == 'generation':
            all_cats = ['Gen Z','Millennial','Gen X','Baby Boomer','Traditionalist','NA']
        elif var == 'sex':
            all_cats = ['Hombre','Mujer']
        elif var == 'education':
            all_cats = ['Primaria','Secundaria','Preparatoria','Universidad','Posgrado','Otro','NA']
        else:
            all_cats = []

        # Escoge aleatoriamente entre 1 y 3 categorías
        num_cats = random.randint(1, min(3,len(all_cats)))
        chosen_cats = random.sample(all_cats, num_cats)
        st.session_state[f"cats_{var}"] = chosen_cats

    # Forzamos un rerun para actualizar la interfaz
    st.experimental_rerun()

# --------------------------------------------------------------------------
# 5) Aplicación principal
# --------------------------------------------------------------------------
def main():
    # ---------------------------------------------------
    # Manejo de estado inicial
    # ---------------------------------------------------
    if 'selected_vars' not in st.session_state:
        st.session_state['selected_vars'] = []
    # Aseguramos también que las listas de categorías estén definidas
    for var in ['generation','sex','education']:
        if f"cats_{var}" not in st.session_state:
            st.session_state[f"cats_{var}"] = []

    # ---------------------------------------------------
    # Botón refresh en la parte principal
    # ---------------------------------------------------
    # Mostramos en la parte superior de la página
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.markdown("<h2 style='margin-bottom:0;'>Movilidad Socioeconómica Q1 vs Q5</h2>", unsafe_allow_html=True)
    with col2:
        if st.button("⟳", help="Recargar la app (reset a valores originales)"):
            # Resetea session_state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

    st.markdown("Visualiza cómo cambian los quintiles de riqueza desde la infancia (Q1 o Q5) hasta la actualidad.")

    # ---------------------------------------------------
    # Barra lateral
    # ---------------------------------------------------
    st.sidebar.title("Parámetros")

    # 1) Sección: Filtro Actual (filtro principal)
    colA, colB = st.sidebar.columns([0.6, 0.4])
    with colA:
        st.subheader("Filtro actual (Filtro principal):")

    with colB:
        if st.button("Aleatoriedad", help="Selecciona 2 variables y 1-3 categorías al azar"):
            random_filter_selection()

    # Multiselect de variables a filtrar
    st.session_state['selected_vars'] = st.sidebar.multiselect(
        "Selecciona las variables (máximo 3)",
        options=['generation','sex','education'],
        default=st.session_state['selected_vars'],
        max_selections=3
    )

    # Para cada variable seleccionada, pedimos sus categorías
    if 'generation' in st.session_state['selected_vars']:
        st.session_state['cats_generation'] = st.sidebar.multiselect(
            "Generación:",
            ['Gen Z','Millennial','Gen X','Baby Boomer','Traditionalist','NA'],
            default=st.session_state['cats_generation']
        )
    if 'sex' in st.session_state['selected_vars']:
        st.session_state['cats_sex'] = st.sidebar.multiselect(
            "Sexo:",
            ['Hombre','Mujer'],
            default=st.session_state['cats_sex']
        )
    if 'education' in st.session_state['selected_vars']:
        st.session_state['cats_education'] = st.sidebar.multiselect(
            "Nivel de estudios:",
            ['Primaria','Secundaria','Preparatoria','Universidad','Posgrado','Otro','NA'],
            default=st.session_state['cats_education']
        )

    # Carga de datos
    df = load_and_process_data()

    # Aplicar el filtro principal
    df_filter = apply_dynamic_filter(df)

    # 2) Sección: Cambiar base
    st.sidebar.markdown("---")
    cambiar_base = st.sidebar.checkbox("Cambiar base", value=False)

    if cambiar_base:
        # Mismos controles (o parecidos) para la base
        st.sidebar.markdown("**Base personalizada** (elige variables/categorías):")
        # Para simplificar, usaremos un set aparte. Ej: base_vars, base_cats
        if 'base_selected_vars' not in st.session_state:
            st.session_state['base_selected_vars'] = []
        if 'base_cats_generation' not in st.session_state:
            st.session_state['base_cats_generation'] = []
        if 'base_cats_sex' not in st.session_state:
            st.session_state['base_cats_sex'] = []
        if 'base_cats_education' not in st.session_state:
            st.session_state['base_cats_education'] = []

        st.session_state['base_selected_vars'] = st.sidebar.multiselect(
            "Variables base:",
            options=['generation','sex','education'],
            default=st.session_state['base_selected_vars'],
            max_selections=3
        )

        # Para cada variable de base
        if 'generation' in st.session_state['base_selected_vars']:
            st.session_state['base_cats_generation'] = st.sidebar.multiselect(
                "Gen (base):",
                ['Gen Z','Millennial','Gen X','Baby Boomer','Traditionalist','NA'],
                default=st.session_state['base_cats_generation']
            )
        if 'sex' in st.session_state['base_selected_vars']:
            st.session_state['base_cats_sex'] = st.sidebar.multiselect(
                "Sexo (base):",
                ['Hombre','Mujer'],
                default=st.session_state['base_cats_sex']
            )
        if 'education' in st.session_state['base_selected_vars']:
            st.session_state['base_cats_education'] = st.sidebar.multiselect(
                "Educación (base):",
                ['Primaria','Secundaria','Preparatoria','Universidad','Posgrado','Otro','NA'],
                default=st.session_state['base_cats_education']
            )

        # Aplicar ese filtro
        def apply_base_filter(df):
            dff = df.copy()
            for var in st.session_state['base_selected_vars']:
                chosen_cats = st.session_state.get(f"base_cats_{var}", [])
                if chosen_cats:
                    dff = dff[dff[var].isin(chosen_cats)]
            return dff

        df_base = apply_base_filter(df)
    else:
        df_base = df

    # ---------------------------------------------------
    # Mostrar la gráfica en la página principal
    # ---------------------------------------------------
    fig = plot_mobility(df_filter, df_base)
    st.pyplot(fig)


# --------------------------------------------------------------------------
if __name__ == "__main__":
    main()
