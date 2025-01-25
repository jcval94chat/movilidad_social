import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# 1) Función para cargar y procesar los datos
# --------------------------------------------------------------------------
@st.cache_data
def load_and_process_data():
    # Rutas de los archivos (ajusta a la ubicación real en tu repo)
    file_path_person = 'data/ESRU-EMOVI 2017 Entrevistado.dta'
    file_path_hogar = 'data/ESRU-EMOVI 2017 Hogar.dta'

    # Leer los archivos .dta
    df_person = pd.read_stata(file_path_person, convert_categoricals=False)
    df_hogar = pd.read_stata(file_path_hogar, convert_categoricals=False)

    # Merge
    df = pd.merge(
        df_person,
        df_hogar[['folio', 'consecutivo', 'p05h', 'p06h']],  
        on=['folio', 'consecutivo'],
        how='left'
    )

    # Listas de variables
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

    # Función auxiliar de recodificación
    def recodificar_01(valor):
        if pd.isna(valor):
            return 0
        elif valor == 1:
            return 1
        else:
            return 0

    # Recodificar en df
    for var in a_los_14_vars:
        if var in df.columns:
            df[var] = df[var].apply(recodificar_01)

    for var in actualmente_vars:
        if var in df.columns and var != 'p131':
            df[var] = df[var].apply(recodificar_01)

    # p131 es num autos: 0 => 0, >=1 => 1
    if 'p131' in df.columns:
        df['p131'] = df['p131'].fillna(0)
        df['p131'] = np.where(df['p131'] >= 1, 1, 0)

    # Crear índices de riqueza
    df['a_los_14_wealth'] = df[a_los_14_vars].sum(axis=1)
    df['actualmente_wealth'] = df[actualmente_vars].sum(axis=1)

    # Ejemplo de si existiera p133
    if 'p133' in df.columns:
        df['p133_clean'] = df['p133']
        df.loc[df['p133_clean'].isin([8,9]), 'p133_clean'] = np.nan
        # Conviértelo a 0..6 restando 1
        df['p133_score'] = df['p133_clean'] - 1
        df['p133_score'] = df['p133_score'].fillna(0)
        df['actualmente_wealth2'] = df['actualmente_wealth'] + df['p133_score']
    else:
        df['actualmente_wealth2'] = df['actualmente_wealth']

    # Asignar quintiles
    def asignar_quintil(serie):
        return pd.qcut(serie, q=5, labels=False, duplicates='drop') + 1

    df['a_los_14_quintile'] = asignar_quintil(df['a_los_14_wealth'])
    df['actualmente_quintile'] = asignar_quintil(df['actualmente_wealth2'])

    # Generaciones
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

    return df

# --------------------------------------------------------------------------
# 2) Función de graficación
# --------------------------------------------------------------------------
def plot_mobility(df, generation='Todos', sexo='Todos'):
    """
    Graficar la distribución de quintil actual (Q1..Q5) para quienes tuvieron
    a_los_14_quintile==1 y a_los_14_quintile==5, tanto en la muestra total
    como en la muestra filtrada por generation, sexo.
    La 'total' se muestra en el fondo con un color suave.
    """
    # --- Distribución TOTAL (sin filtrar)
    df_total = df.copy()
    # Q1 total
    q1_total = df_total[df_total['a_los_14_quintile'] == 1]
    q1_dist_total = q1_total['actualmente_quintile'].value_counts(normalize=True) * 100
    q1_dist_total = q1_dist_total.sort_index()
    # Q5 total
    q5_total = df_total[df_total['a_los_14_quintile'] == 5]
    q5_dist_total = q5_total['actualmente_quintile'].value_counts(normalize=True) * 100
    q5_dist_total = q5_dist_total.sort_index()

    # --- Distribución FILTRADA
    dff = df.copy()
    if generation != 'Todos':
        dff = dff[dff['generation'] == generation]
    if sexo != 'Todos':
        dff = dff[dff['sex'] == sexo]

    # Q1 filtrado
    q1 = dff[dff['a_los_14_quintile'] == 1]
    q1_dist = q1['actualmente_quintile'].value_counts(normalize=True)*100
    q1_dist = q1_dist.sort_index()

    # Q5 filtrado
    q5 = dff[dff['a_los_14_quintile'] == 5]
    q5_dist = q5['actualmente_quintile'].value_counts(normalize=True)*100
    q5_dist = q5_dist.sort_index()

    # --- Gráfica
    fig, ax = plt.subplots(1, 2, figsize=(10, 5), sharey=True)

    # Gráfica para Q1
    ax[0].bar(q1_dist_total.index.astype(str),
              q1_dist_total.values,
              alpha=0.2, color='gray', label='Total (fondo)')
    ax[0].bar(q1_dist.index.astype(str),
              q1_dist.values,
              alpha=1.0, color='skyblue', label='Filtrado')

    ax[0].set_title(f"Q1 Origen\n(Gen={generation}, Sexo={sexo})")
    ax[0].set_xlabel("Quintil actual")
    ax[0].set_ylabel("% personas")
    ax[0].legend()

    # Gráfica para Q5
    ax[1].bar(q5_dist_total.index.astype(str),
              q5_dist_total.values,
              alpha=0.2, color='gray', label='Total (fondo)')
    ax[1].bar(q5_dist.index.astype(str),
              q5_dist.values,
              alpha=1.0, color='salmon', label='Filtrado')

    ax[1].set_title(f"Q5 Origen\n(Gen={generation}, Sexo={sexo})")
    ax[1].set_xlabel("Quintil actual")
    ax[1].legend()

    plt.suptitle("Movilidad socioeconómica (Q1 vs Q5)")
    plt.tight_layout()
    return fig

# --------------------------------------------------------------------------
# 3) Interfaz principal de Streamlit
# --------------------------------------------------------------------------
def main():
    st.title("Ejemplo de Movilidad Socioeconómica (Q1 vs Q5)")

    # Cargar datos
    df = load_and_process_data()

    # Opciones de dropdown
    gen_options = ['Todos','Gen Z','Millennial','Gen X','Baby Boomer','Traditionalist']
    sex_options = ['Todos','Hombre','Mujer']

    # Controles en la barra lateral (o en la parte principal)
    generation = st.selectbox("Seleccione la generación:", gen_options, index=0)
    sexo = st.selectbox("Seleccione el sexo:", sex_options, index=0)

    # Generar la figura
    fig = plot_mobility(df, generation, sexo)

    # Mostrar la figura en Streamlit
    st.pyplot(fig)

# --------------------------------------------------------------------------
# 4) Punto de entrada
# --------------------------------------------------------------------------
if __name__ == "__main__":
    main()
