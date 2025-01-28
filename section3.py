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
    Sección 3: Un formulario con checkboxes (0/1) dispuestos en 5 columnas x N filas.
    El formulario solo se procesa al pulsar "Procesar", evitando recargas continuas.
    """

    st.title("Modelo de Clasificación con Probabilidades")

    # Ruta del modelo (ajusta si lo guardaste en otra parte)
    modelo_path = 'models/modelo_entrenado.joblib'
    if not os.path.exists(modelo_path):
        st.error(f"No se encontró el archivo de modelo '{modelo_path}'.")
        return

    # Cargar el modelo en session_state para no recargarlo en cada submit
    if 'modelo_regr' not in st.session_state:
        regr = joblib.load(modelo_path)
        st.session_state['modelo_regr'] = regr
        st.success("Modelo cargado exitosamente.")
    else:
        regr = st.session_state['modelo_regr']

    # Diccionario de variables (hasta 10, 15, etc.) {variable: descripción}
    variables = {
        'p126d': 'Horno de microondas',
        'p131':  'Automóvil propio',
        'p125d': 'Calentador de agua',
        'p126o': 'Computadora',
        'p126f': 'Tostador de pan',
        'p126g': 'Aspiradora',
        'p125e': 'Servicio doméstico',
        'p129a': 'Otra casa/depto',
        'p126h': 'DVD/Blu-Ray',
        'p126b': 'Lavadora de ropa'
    }

    st.caption("Marca un checkbox si la variable vale 1 (verde), desmarca para 0 (rojo). " 
               "Luego pulsa **Procesar** para generar la predicción.")

    # --------------------------------------------------------------------------------
    # 1) Creamos el FORMULARIO, para que no haya recargas en cada clic de checkbox
    # --------------------------------------------------------------------------------
    with st.form("form_variables"):
        # --- Dibujamos en filas de 5 columnas ---
        keys_list = list(variables.keys())
        num_vars = len(keys_list)
        cols_per_row = 5

        # Diccionario que guardará temporalmente los valores
        user_values = {}

        # Recorremos las variables en bloques de 5
        for start_idx in range(0, num_vars, cols_per_row):
            row_vars = keys_list[start_idx:start_idx+cols_per_row]
            col_objs = st.columns(len(row_vars))

            for i, var in enumerate(row_vars):
                desc = variables[var]
                # Con checkbox, True -> 1, False -> 0
                # st.checkbox dev. True/False
                val_checkbox = col_objs[i].checkbox(
                    label=desc,  # Texto pequeño
                    value=False,  # Por defecto
                    help=f"Variable: {var}\n(Desmarcado=0, Marcado=1)"
                )
                user_values[var] = 1 if val_checkbox else 0

        # Botón que envía el formulario
        procesar = st.form_submit_button("Procesar")

    # --------------------------------------------------------------------------------
    # 2) Tras pulsar "Procesar", generamos la predicción
    # --------------------------------------------------------------------------------
    if procesar:
        # Convertimos user_values en DataFrame
        df_usuario = pd.DataFrame([user_values])

        # Orden de las features según el modelo
        if hasattr(regr, 'feature_names_in_'):
            modelo_feats = list(regr.feature_names_in_)
        else:
            modelo_feats = list(variables.keys())

        # Validación: si hay mismatch
        for feat in modelo_feats:
            if feat not in df_usuario.columns:
                df_usuario[feat] = 0

        df_usuario = df_usuario[modelo_feats]

        # Verificamos si soporta predict_proba
        if hasattr(regr, "predict_proba"):
            probabilidades = regr.predict_proba(df_usuario)
            clases = regr.classes_
            probs = probabilidades[0]

            df_plot = pd.DataFrame({
                'Clase': clases,
                'Probabilidad': probs
            })

            fig = px.bar(
                df_plot,
                x='Clase',
                y='Probabilidad',
                range_y=[0,1],
                text='Probabilidad',
                color='Clase',
                title="Probabilidades de Predicción para Cada Clase"
            )
            fig.update_traces(
                texttemplate='%{text:.2f}',
                textposition='outside'
            )
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
            st.markdown(f"**Clase predicha:** `{clase_pred}` con **{prob_pred:.2%}** de prob.")
        else:
            st.warning("El modelo no soporta 'predict_proba'. Usa un modelo de clasificación con esta funcionalidad.")
    else:
        st.info("Ajusta las variables (check=1, sin check=0) y pulsa **Procesar** para ver el resultado.")


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