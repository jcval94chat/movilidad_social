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
    Sección 3: Predicción de modelo con probabilidades y visualización de barras
    con un sistema de botones que alternan entre 0 (rojo) y 1 (verde).
    """

    st.title("Modelo de Clasificación con Probabilidades")

    # Ruta del modelo entrenado (ajusta a tu carpeta 'models/')
    modelo_path = 'models/modelo_entrenado.joblib'
    if not os.path.exists(modelo_path):
        st.error(f"No se encontró el archivo de modelo '{modelo_path}'. Por favor, cárgalo o ajusta la ruta.")
        return

    # Cargar el modelo en session_state para no recargarlo en cada interacción
    if 'modelo_regr' not in st.session_state:
        regr = joblib.load(modelo_path)
        st.session_state['modelo_regr'] = regr
        st.success("Modelo cargado exitosamente.")
    else:
        regr = st.session_state['modelo_regr']

    # Diccionario de variables a preguntar: { variable : descripción }
    variables = {
        'p126d': 'Artículos vivienda: horno de microondas',
        'p131':  'Tiene automóvil(es) propio(s)',
        'p125d': 'Servicios vivienda: calentador de agua',
        'p126o': 'Artículos vivienda: computadora',
        'p126f': 'Artículos vivienda: tostador eléctrico de pan',
        'p126g': 'Artículos vivienda: aspiradora',
        'p125e': 'Servicios vivienda: servicio doméstico',
        'p129a': 'Bienes del hogar: otra casa o departamento',
        'p126h': 'Artículos vivienda: DVD/Blu-Ray',
        'p126b': 'Artículos vivienda: lavadora de ropa'
    }

    st.write("Pulsa en cada botón para alternar entre 0 (rojo) y 1 (verde).")

    # -----------------------------
    # 1) Inicializar y mostrar los botones en rejilla de 5 columnas
    # -----------------------------
    keys_list = list(variables.keys())
    num_vars = len(keys_list)
    cols_per_row = 5

    # Asegurarnos de que cada variable tenga un valor en session_state
    for var in variables:
        if var not in st.session_state:
            st.session_state[var] = 0  # Por defecto 0

    # Dibujar filas y columnas
    for start_index in range(0, num_vars, cols_per_row):
        row_vars = keys_list[start_index:start_index+cols_per_row]
        cols = st.columns(len(row_vars))  # crear N columnas para la fila

        for i, var in enumerate(row_vars):
            var_value = st.session_state[var]
            # Decidir color y label
            if var_value == 1:
                bg_color = "#aaffaa"  # verde claro
                label_text = "1"
            else:
                bg_color = "#ffaaaa"  # rojo claro
                label_text = "0"

            # Etiqueta a mostrar
            # Usamos HTML y CSS inline para lograr el fondo de color
            desc = variables[var]
            button_label = f"{desc} ({var}): {label_text}"

            # Al presionar el botón, alterna el valor 0/1
            if cols[i].button(
                button_label,
                key=f"btn_{var}",
                help=f"{desc} → pulso para alternar entre 0 y 1"
            ):
                st.session_state[var] = 1 - st.session_state[var]

            # Ajustes de estilo con markdown (opcional)
            # Si deseas que TODO el botón sea del color,
            # se requiere un workaround con st.markdown y HTML.
            # A nivel de st.button es más difícil inyectar CSS,
            # pero con un pequeño truco de st.markdown + button
            # se puede simular. Aquí, optamos por un label textual.

            # Podemos mostrar un texto al lado del botón simulando color:
            # (Descomentar si quieres un recuadro de color)
            html_color_box = f"""
            <div style='width: 100%; background-color: {bg_color}; height: 5px; margin-top: -10px; margin-bottom: 8px'></div>
            """
            cols[i].markdown(html_color_box, unsafe_allow_html=True)

    # -----------------------------
    # 2) Construir el DataFrame de usuario según los valores en session_state
    # -----------------------------
    datos_usuario = {}
    for var in variables:
        datos_usuario[var] = st.session_state[var]

    df_usuario = pd.DataFrame([datos_usuario])

    # Asegurarnos de que las características coincidan con las del modelo
    if hasattr(regr, 'feature_names_in_'):
        caracteristicas_modelo = list(regr.feature_names_in_)
    else:
        # Si tu modelo no tiene 'feature_names_in_', define manualmente el orden
        caracteristicas_modelo = list(variables.keys())

    # Validación: si hay mismatch entre df_usuario y caracteristicas_modelo
    for col in caracteristicas_modelo:
        if col not in df_usuario.columns:
            df_usuario[col] = 0  # Valor por defecto

    df_usuario = df_usuario[caracteristicas_modelo]

    # -----------------------------
    # 3) Realizar la predicción de probabilidades y graficar
    # -----------------------------
    if hasattr(regr, "predict_proba"):
        probabilidades = regr.predict_proba(df_usuario)  # (1, n_classes)
        clases = regr.classes_
        probs_row = probabilidades[0]

        # DataFrame para plotly
        df_plot = pd.DataFrame({
            'Clase': clases,
            'Probabilidad': probs_row
        })

        # Gráfica
        fig = px.bar(
            df_plot,
            x='Clase',
            y='Probabilidad',
            range_y=[0,1],
            text='Probabilidad',
            color='Clase',  # si quieres distinto color por clase
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

        # Determinar clase más probable
        idx_pred = np.argmax(probs_row)
        clase_predicha = clases[idx_pred]
        prob_predicha = probs_row[idx_pred]

        st.markdown(f"**La clase predicha por el modelo es:** `{clase_predicha}` con una probabilidad de **{prob_predicha:.2%}**")
    else:
        st.warning("El modelo no soporta 'predict_proba'. Usa un modelo de clasificación con esta funcionalidad.")

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