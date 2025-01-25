import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
# 1) FUNCIÓN PARA CARGAR Y PROCESAR DATOS (idéntica a tu versión previa).
#    Aquí, asumo que ya implementaste `load_and_process_data()` con las
#    transformaciones necesarias: merge, recodificaciones, quintiles, etc.
##############################################################################
@st.cache_data
def load_and_process_data():
    """
    Lee los archivos .dta, hace merge, recodificaciones, etc.
    Retorna un DataFrame con las columnas:
      - a_los_14_quintile
      - actualmente_quintile
      - generation
      - sex
      ...
    """
    # -------------------------------------------------------------------------
    # EJEMPLO MUY RESUMIDO:
    # -------------------------------------------------------------------------
    file_path_person = 'data/ESRU-EMOVI 2017 Entrevistado.dta'
    file_path_hogar  = 'data/ESRU-EMOVI 2017 Hogar.dta'
    df_person = pd.read_stata(file_path_person, convert_categoricals=False)
    df_hogar  = pd.read_stata(file_path_hogar, convert_categoricals=False)

    # Supón que aquí haces:
    #   1) Merge
    #   2) Recodificaciones -> a_los_14_vars, actualmente_vars
    #   3) Creas a_los_14_wealth, actualmente_wealth, actualmente_wealth2
    #   4) Asignas a_los_14_quintile, actualmente_quintile
    #   5) Creas "generation", "sex"
    # ...
    # Para el ejemplo final, imagina que ya está todo correcto:

    df = df_person.copy()  # EJEMPLO rápido (reemplazar con tu merge real).
    df['a_los_14_quintile']    = np.random.randint(1,6,size=len(df)) # Q1..Q5
    df['actualmente_quintile'] = np.random.randint(1,6,size=len(df))
    df['generation'] = np.random.choice(['Gen Z','Millennial','Gen X','Baby Boomer','Traditionalist'], size=len(df))
    df['sex']        = np.random.choice(['Hombre','Mujer'], size=len(df))

    return df

##############################################################################
# 2) FUNCIÓN DE GRÁFICA
##############################################################################
def plot_mobility(df_base, df_filter, selected_categories_for_filter, selected_categories_for_base):
    """
    Muestra dos gráficas de barras (Q1 y Q5) comparando:
    - 'base' (barras grises en el fondo)
    - 'filtro' (barras de color encima)

    Además, añade etiquetas con el % (1 decimal) y la diferencia vs base
    en formato 24% (+0.3%) o 24% (-0.5%).
    La diferencia en azul si es positiva, rojo si es negativa.

    df_base:   DataFrame que se usa como base.
    df_filter: DataFrame que se filtra en función de las categorías elegidas.
    """
    # --- Distribución BASE (sin filtrar o filtrada, según el usuario)
    q1_base = df_base[df_base['a_los_14_quintile'] == 1]
    q5_base = df_base[df_base['a_los_14_quintile'] == 5]

    q1_base_dist = q1_base['actualmente_quintile'].value_counts(normalize=True)*100
    q5_base_dist = q5_base['actualmente_quintile'].value_counts(normalize=True)*100

    # Aseguramos index ordenado (1..5)
    q1_base_dist = q1_base_dist.sort_index()
    q5_base_dist = q5_base_dist.sort_index()

    # --- Distribución FILTRADA
    q1_filt = df_filter[df_filter['a_los_14_quintile'] == 1]
    q5_filt = df_filter[df_filter['a_los_14_quintile'] == 5]

    q1_filt_dist = q1_filt['actualmente_quintile'].value_counts(normalize=True)*100
    q5_filt_dist = q5_filt['actualmente_quintile'].value_counts(normalize=True)*100

    q1_filt_dist = q1_filt_dist.sort_index()
    q5_filt_dist = q5_filt_dist.sort_index()

    # --- Crear figura
    fig, ax = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    # ------------------------------------------------------------------------
    # Q1
    # ------------------------------------------------------------------------
    # 1) Barras de base (gris suave)
    base_bars_q1 = ax[0].bar(
        q1_base_dist.index.astype(str),
        q1_base_dist.values,
        alpha=0.2, color='gray', label='Base'
    )
    # 2) Barras filtradas (color principal)
    filt_bars_q1 = ax[0].bar(
        q1_filt_dist.index.astype(str),
        q1_filt_dist.values,
        alpha=1.0, color='skyblue', label='Filtro'
    )
    ax[0].set_title("Origen Q1")
    ax[0].set_xlabel("Quintil Actual")
    ax[0].set_ylabel("% Personas")
    ax[0].legend()

    # Agregar etiquetas a las barras filtradas
    for i, bar in enumerate(filt_bars_q1):
        # Valor "filtrado"
        f_val = bar.get_height()
        # Valor "base" (del mismo índice)
        index_str = bar.get_x() + bar.get_width()/2  # en ejes
        # Para saber el quintil actual real:
        quintil_actual = q1_filt_dist.index[i]  
        # Ojo: i corresponde al "i-ésimo bar" en la vista, 
        #      pero es más robusto hacer un match por index:
        # Tomamos f_val = q1_filt_dist.get(quintil_actual, 0)
        # Tomamos t_val = q1_base_dist.get(quintil_actual, 0)
        t_val = q1_base_dist.get(quintil_actual, 0)

        diff = round(f_val - t_val, 1)

        # Formateo del label
        label_text = f"{f_val:.1f}% ({diff:+.1f}%)"

        # Color de la diferencia
        diff_color = "blue" if diff >= 0 else "red"

        # Coordenadas para colocar el texto
        x_text = bar.get_x() + bar.get_width()/2
        y_text = f_val  # altura de la barra

        ax[0].text(
            x_text, y_text,
            label_text,
            ha='center', va='bottom',
            fontsize=8, color=diff_color, rotation=0
        )

    # ------------------------------------------------------------------------
    # Q5
    # ------------------------------------------------------------------------
    base_bars_q5 = ax[1].bar(
        q5_base_dist.index.astype(str),
        q5_base_dist.values,
        alpha=0.2, color='gray', label='Base'
    )
    filt_bars_q5 = ax[1].bar(
        q5_filt_dist.index.astype(str),
        q5_filt_dist.values,
        alpha=1.0, color='salmon', label='Filtro'
    )
    ax[1].set_title("Origen Q5")
    ax[1].set_xlabel("Quintil Actual")
    ax[1].legend()

    # Etiquetas en las barras Q5 filtradas
    for i, bar in enumerate(filt_bars_q5):
        f_val = bar.get_height()
        quintil_actual = q5_filt_dist.index[i]
        t_val = q5_base_dist.get(quintil_actual, 0)

        diff = round(f_val - t_val, 1)
        label_text = f"{f_val:.1f}% ({diff:+.1f}%)"
        diff_color = "blue" if diff >= 0 else "red"

        x_text = bar.get_x() + bar.get_width()/2
        y_text = f_val

        ax[1].text(
            x_text, y_text,
            label_text,
            ha='center', va='bottom',
            fontsize=8, color=diff_color
        )

    plt.suptitle("Distribución de Quintil Actual (Q1 vs Q5)")
    plt.tight_layout()
    return fig

##############################################################################
# 3) INTERFAZ PRINCIPAL DE STREAMLIT
##############################################################################
def main():
    st.title("Movilidad Socioeconómica Simplificada")

    # Detalles en la barra lateral
    st.sidebar.title("Detalles Explicativos")
    st.sidebar.write("""
    - **Q1**: Primer quintil de riqueza a los 14 años.\n
    - **Q5**: Quinto quintil de riqueza a los 14 años.\n
    - **Quintil Actual**: Con base en el índice de riqueza actual.\n
    - La gráfica compara la distribución actual vs. la base elegida.
    """)

    # Cargar datos
    df = load_and_process_data()

    # ------------------------------------------------------------------------
    # Selección de categorías para FILTRAR (por defecto generation, sex).
    # Podrás permitir hasta 3 categorías (puede ser generation, sex, etc.)
    # ------------------------------------------------------------------------
    posibles_categorias = ["generation", "sex"]  # Agrega más si lo deseas
    st.write("### Filtro (hasta 3 categorías)")
    # Selecciona de las posibles (ponemos `max_selections=3`):
    selected_cats_filter = st.multiselect(
        "Elige categorías para filtrar",
        posibles_categorias,
        default=["generation","sex"],
        max_selections=3
    )

    # Para cada categoría seleccionada, elegimos un valor (o 'Todos'):
    filter_dict = {}
    df_filter = df.copy()

    for cat in selected_cats_filter:
        # Ej. cat="generation" => valores únicos
        valores_unicos = ["Todos"] + sorted(df[cat].dropna().unique().tolist())
        valor_elegido = st.selectbox(
            f"Selecciona {cat} para el filtro:",
            valores_unicos,
            key=f"filtro_{cat}"  # para que no choque en streamlit
        )
        filter_dict[cat] = valor_elegido

    # Aplica el filtro
    for cat, val in filter_dict.items():
        if val != "Todos":
            df_filter = df_filter[df_filter[cat] == val]

    # ------------------------------------------------------------------------
    # Selección de categorías para la BASE
    # Botón "cambiar base" => si se activa, dejamos que escoja la base
    # Si NO, la base es el df original.
    # ------------------------------------------------------------------------
    cambiar_base = st.checkbox("Cambiar Base", value=False)

    if cambiar_base:
        st.write("### Base (hasta 3 categorías)")
        selected_cats_base = st.multiselect(
            "Elige categorías para la base",
            posibles_categorias,
            default=[],
            max_selections=3,
            key="cats_base"
        )

        base_dict = {}
        df_base = df.copy()
        for cat in selected_cats_base:
            valores_unicos = ["Todos"] + sorted(df[cat].dropna().unique().tolist())
            valor_elegido = st.selectbox(
                f"Selecciona {cat} para la base:",
                valores_unicos,
                key=f"base_{cat}"
            )
            base_dict[cat] = valor_elegido

        for cat, val in base_dict.items():
            if val != "Todos":
                df_base = df_base[df_base[cat] == val]

    else:
        # Si NO se cambia la base, la base es el df completo (sin filtrar).
        df_base = df.copy()

    # ------------------------------------------------------------------------
    # Generar la figura
    # ------------------------------------------------------------------------
    fig = plot_mobility(
        df_base   = df_base,
        df_filter = df_filter,
        selected_categories_for_filter = selected_cats_filter,
        selected_categories_for_base   = []
    )

    # Mostrar la figura en Streamlit
    st.pyplot(fig)

##############################################################################
# 4) PUNTO DE ENTRADA
##############################################################################
if __name__ == "__main__":
    main()
