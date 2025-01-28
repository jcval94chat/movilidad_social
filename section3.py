# section3.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import os

# Diccionario para mapear clases a quintiles
CLASS_TO_QUINTILES = {
    "Baja Baja": [1],
    "Baja Alta": [2],
    "Media Baja": [3],
    "Media Alta": [4],
    "Alta": [5]
}

def show_section3():
    """
    Sección 3: Predicción de modelo con un sistema de toggles (0/1) a través de
    botones con emojis (🔴/🟢). El usuario primero configura todas las variables
    y luego presiona "Procesar" para generar la predicción.
    """

    st.title("Modelo de Clasificación con Probabilidades")

    # Ruta del modelo entrenado (ajusta a tu carpeta, p.e. 'models/')
    modelo_path = 'models/modelo_entrenado.joblib'
    if not os.path.exists(modelo_path):
        st.error(f"No se encontró el archivo de modelo '{modelo_path}'. Asegúrate de que exista.")
        return

    # Cargar el modelo en session_state (para no recargarlo tras cada interacción)
    if 'modelo_regr' not in st.session_state:
        regr = joblib.load(modelo_path)
        st.session_state['modelo_regr'] = regr
        st.success("Modelo cargado exitosamente.")
    else:
        regr = st.session_state['modelo_regr']

    # Diccionario de variables: {variable: descripción}
    variables = {
        'p126d': 'Horno de microondas',
        'p131':  'Automóvil(es) propio(s)',
        'p125d': 'Calentador de agua',
        'p126o': 'Computadora',
        'p126f': 'Tostador de pan',
        'p126g': 'Aspiradora',
        'p125e': 'Servicio doméstico',
        'p129a': 'Otra casa/depto',
        'p126h': 'DVD/Blu-Ray',
        'p126b': 'Lavadora de ropa'
    }

    st.caption("Pulsa en cada botón para alternar entre **🔴 (0)** y **🟢 (1)**. Luego presiona **Procesar**.")

    # ----------------------------------------------------------------------------------
    # 1) Mostrar los toggles (emoji-rojo/verde) en una rejilla de 5 columnas
    # ----------------------------------------------------------------------------------
    keys_list = list(variables.keys())
    num_vars = len(keys_list)
    cols_per_row = 5

    # Asegurar valores en session_state para cada variable (por defecto 0)
    for var in variables:
        if var not in st.session_state:
            st.session_state[var] = 0  # 0 = 🔴, 1 = 🟢

    # Dibujar filas de 5 columnas con botones
    for start_idx in range(0, num_vars, cols_per_row):
        row_vars = keys_list[start_idx:start_idx+cols_per_row]
        col_objs = st.columns(len(row_vars))

        for i, var in enumerate(row_vars):
            current_val = st.session_state[var]
            label_emoji = "🔴" if current_val == 0 else "🟢"
            desc = variables[var]

            # El botón alterna de 0 a 1 y viceversa
            if col_objs[i].button(
                label_emoji,
                key=f"toggle_{var}",
                help=f"{var}: {desc}\n\nPulsa para cambiar a {'1' if current_val == 0 else '0'}",
            ):
                st.session_state[var] = 1 - st.session_state[var]

    st.write("---")

    # ----------------------------------------------------------------------------------
    # 2) Botón "Procesar" para generar la predicción y la gráfica
    # ----------------------------------------------------------------------------------
    if st.button("Procesar", key="procesar_modelo"):
        # Construir DataFrame con los valores de session_state
        df_usuario = pd.DataFrame([{var: st.session_state[var] for var in variables}])

        # Asegurar orden de features
        if hasattr(regr, 'feature_names_in_'):
            modelo_feats = list(regr.feature_names_in_)
        else:
            modelo_feats = list(variables.keys())

        # Asegurar que todas las columnas existan
        for feat in modelo_feats:
            if feat not in df_usuario.columns:
                df_usuario[feat] = 0

        df_usuario = df_usuario[modelo_feats]

        # Verificar predict_proba
        if hasattr(regr, "predict_proba"):
            probabilidades = regr.predict_proba(df_usuario)  # (1, n_classes)
            clases = regr.classes_
            probs = probabilidades[0]

            df_plot = pd.DataFrame({'Clase': clases, 'Probabilidad': probs})
            fig = px.bar(
                df_plot,
                x='Clase',
                y='Probabilidad',
                range_y=[0,1],
                text='Probabilidad',
                color='Clase',
                title="Probabilidades de Predicción para Cada Clase"
            )
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig.update_layout(
                yaxis=dict(title='Probabilidad'),
                xaxis=dict(title='Clases'),
                uniformtext_minsize=8,
                uniformtext_mode='hide'
            )

            st.plotly_chart(fig, use_container_width=True)

            idx_pred = np.argmax(probs)
            clase_pred = clases[idx_pred]
            prob_pred = probs[idx_pred]
            st.markdown(f"**Clase predicha:** `{clase_pred}` con **{prob_pred:.2%}** de probabilidad.")

        else:
            st.warning("El modelo no soporta 'predict_proba'. Usa un modelo de clasificación con esta funcionalidad.")

    else:
        st.info("Cuando hayas terminado de ajustar los toggles, presiona **Procesar** para ver la predicción.")



def random_origin_dest():
    """
    Elige aleatoriamente 1..2 clases para ORIGEN y 1..2 para DESTINO.
    Se invoca al dar clic en el botón "Random" en main.py.
    """
    import random
    classes = list(CLASS_TO_QUINTILES.keys())
    # Origen
    n_orig = random.randint(1, 2)
    origin = random.sample(classes, n_orig)
    # Destino
    n_dest = random.randint(1, 2)
    dest   = random.sample(classes, n_dest)

    st.session_state["origin_default"] = origin
    st.session_state["dest_default"]   = dest