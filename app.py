import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

    # EJEMPLO de "nivel de estudios"
    # Suponiendo que exista p07 (ajusta a tu variable real).
    # 1=Primaria, 2=Secundaria, 3=Prepa, 4=Universidad, 5=Posgrado
    def assign_education(val):
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
        # Si no existe p07, crea una variable dummy (para demo)
        df['education'] = np.random.choice(
            ['Primaria','Secundaria','Preparatoria','Universidad','Posgrado','NA'],
            size=len(df)
        )

    return df

# --------------------------------------------------------------------------
# 2) Función de filtrado multifactor
# --------------------------------------------------------------------------
def apply_filter(df, generation='Todos', sex='Todos', education='Todos'):
    """Aplica filtros simultáneos (hasta 3) sobre el DataFrame."""
    dff = df.copy()
    if generation != 'Todos':
        dff = dff[dff['generation'] == generation]
    if sex != 'Todos':
        dff = dff[dff['sex'] == sex]
    if education != 'Todos':
        dff = dff[dff['education'] == education]
    return dff

# --------------------------------------------------------------------------
# 3) Función de graficación (Q1 vs. Q5)
#    con base personalizable y etiquetas con % y diferencia.
# --------------------------------------------------------------------------
def plot_mobility(df_filter, df_base):
    """
    - df_filter: DataFrame con el filtro actual del usuario.
    - df_base: DataFrame que se toma como 'base' para comparar.
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
    fig, ax = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

    # ---- Q1: Base (fondo) vs Filtro
    ax[0].bar(q1_dist_base.index.astype(str),
              q1_dist_base.values,
              alpha=0.2, color='gray', label='Base')
    ax[0].bar(q1_dist_filter.index.astype(str),
              q1_dist_filter.values,
              alpha=1.0, color='skyblue', label='Filtro')

    ax[0].set_title("Q1 (Origen)", fontsize=12)
    ax[0].set_xlabel("Quintil actual")
    ax[0].set_ylabel("% personas")
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
            y=val_f + 1,  # Desplaza ligeramente la etiqueta arriba de la barra
            s=label,
            ha='center',
            color=color,
            fontsize=9
        )

    # ---- Q5: Base (fondo) vs Filtro
    ax[1].bar(q5_dist_base.index.astype(str),
              q5_dist_base.values,
              alpha=0.2, color='gray', label='Base')
    ax[1].bar(q5_dist_filter.index.astype(str),
              q5_dist_filter.values,
              alpha=1.0, color='salmon', label='Filtro')

    ax[1].set_title("Q5 (Origen)", fontsize=12)
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

    plt.suptitle("Movilidad socioeconómica (Comparación Q1 vs Q5)", fontsize=14)
    plt.tight_layout()
    return fig

# --------------------------------------------------------------------------
# 4) Aplicación principal
# --------------------------------------------------------------------------
def main():
    # ---------------------------------------------------
    # Barra lateral
    # ---------------------------------------------------
    st.sidebar.title("Configuración")
    st.sidebar.markdown("**Elige una o varias categorías** para filtrar la gráfica.")

    # Información en un expander (oculto por defecto)
    with st.sidebar.expander("¿Qué se muestra en la gráfica?"):
        st.write("""
        En la gráfica vemos cómo, según el **quintil de riqueza a los 14 años (Q1 o Q5)**,
        las personas se encuentran actualmente en alguno de los 5 quintiles de riqueza.
        
        - **Q1 (Origen)**: Personas que estaban en el quintil más bajo a los 14 años.
        - **Q5 (Origen)**: Personas que estaban en el quintil más alto a los 14 años.

        La comparación se hace entre la **base** (barras grises) y el **filtro** (barras de color).
        Las etiquetas encima de cada barra muestran el **porcentaje** y la diferencia 
        frente a la base (en verde si es mayor, rojo si es menor).
        """)

    # Carga de datos
    df = load_and_process_data()

    # Opciones de cada categoría
    gen_options    = ['Todos','Gen Z','Millennial','Gen X','Baby Boomer','Traditionalist']
    sex_options    = ['Todos','Hombre','Mujer']
    edu_options    = ['Todos','Primaria','Secundaria','Preparatoria','Universidad','Posgrado','Otro','NA']

    # ---------------------------------------------------
    # Filtros para la base
    # ---------------------------------------------------
    use_custom_base = st.sidebar.checkbox("Cambiar base")
    if use_custom_base:
        st.sidebar.markdown("**Base personalizada:**")
        generation_base = st.sidebar.selectbox("Generación (base)", gen_options, index=0, key="gen_base")
        sex_base        = st.sidebar.selectbox("Sexo (base)",        sex_options, index=0, key="sex_base")
        edu_base        = st.sidebar.selectbox("Educación (base)",  edu_options, index=0, key="edu_base")
        df_base = apply_filter(df, generation_base, sex_base, edu_base)
    else:
        # Base = total
        df_base = df

    # ---------------------------------------------------
    # Filtros para la vista (filtro principal)
    # ---------------------------------------------------
    st.sidebar.markdown("**Filtro actual (Filtro principal):**")

    # Por defecto, el sexo está seleccionado (y los demás "Todos")
    generation_filter = st.sidebar.selectbox("Generación (filtro)", gen_options, index=0)
    sex_filter        = st.sidebar.selectbox("Sexo (filtro)",        sex_options, index=0)
    edu_filter        = st.sidebar.selectbox("Educación (filtro)",  edu_options, index=0)

    df_filter = apply_filter(df, generation_filter, sex_filter, edu_filter)

    # ---------------------------------------------------
    # Sección principal
    # ---------------------------------------------------
    st.title("Movilidad Socioeconómica Q1 vs Q5")

    st.write("Visualiza el cambio de quintil de riqueza entre la infancia (Q1 o Q5) y la situación actual.")

    # Generar la figura comparando df_filter vs df_base
    fig = plot_mobility(df_filter, df_base)
    st.pyplot(fig)

# --------------------------------------------------------------------------
if __name__ == "__main__":
    main()
