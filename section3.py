# section3.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import os

def show_section3():
    """
    Sección 3: Predicción de modelo con probabilidades y visualización de barras.
    """

    st.title("Modelo de Clasificación con Probabilidades")

    # Ruta del modelo entrenado (ajusta según tu estructura)
    modelo_path = 'models/modelo_entrenado.joblib'

    if not os.path.exists(modelo_path):
        st.error(f"No se encontró el archivo de modelo '{modelo_path}'. Carga el modelo en tu repo o ajusta la ruta.")
        return

    # Cargar el modelo si aún no está en session_state
    if 'modelo_regr' not in st.session_state:
        regr = joblib.load(modelo_path)
        st.session_state['modelo_regr'] = regr
        st.success("Modelo cargado exitosamente.")
    else:
        regr = st.session_state['modelo_regr']

    # Diccionario de variables a preguntar (ejemplo)
    # Ajusta este diccionario a tus variables reales y sus descripciones.
    variables = {
        "var_a": "Descripción de var_a",
        "var_b": "Descripción de var_b",
        "var_c": "Descripción de var_c"
        # Agrega las que necesites...
    }

    st.write("Completa los siguientes campos (0 o 1) para realizar la predicción:")

    # Recolectamos la entrada del usuario (0/1) por cada variable
    datos_usuario = {}
    for var, desc in variables.items():
        datos_usuario[var] = st.selectbox(
            f"{desc} ({var}):",
            options=[0,1],
            index=0,  # default
            format_func=lambda x: f"{x} (valor entero)"
        )

    # Convertir las entradas en DataFrame respetando el orden de las features
    df_usuario = pd.DataFrame([datos_usuario])

    # Asegurarnos de que las características coincidan con las del modelo
    if hasattr(regr, 'feature_names_in_'):
        caracteristicas_modelo = list(regr.feature_names_in_)
    else:
        # Si tu modelo no tiene 'feature_names_in_', define manualmente el orden
        # Ejemplo:
        caracteristicas_modelo = list(variables.keys())

    # Validación: si hay mismatch entre df_usuario y caracteristicas_modelo
    for col in caracteristicas_modelo:
        if col not in df_usuario.columns:
            df_usuario[col] = 0  # o un valor por defecto

    df_usuario = df_usuario[caracteristicas_modelo]

    # Verificar si el modelo soporta predict_proba
    if hasattr(regr, "predict_proba"):
        probabilidades = regr.predict_proba(df_usuario)  # shape: (1, n_classes)
        clases = regr.classes_

        # Extraemos las probabilidades
        probs_row = probabilidades[0]  # Probabilidades de la fila única

        # Crear DataFrame para plotly
        df_plot = pd.DataFrame({
            'Clase': clases,
            'Probabilidad': probs_row
        })

        # Graficar con plotly
        fig = px.bar(
            df_plot,
            x='Clase',
            y='Probabilidad',
            range_y=[0,1],
            text='Probabilidad',
            color='Clase',  # si quieres colores distintos por clase
            title="Probabilidades de Predicción para Cada Clase"
        )
        # Personalizar layout
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

        # Clase con mayor probabilidad
        indice_prediccion = np.argmax(probs_row)
        clase_predicha = clases[indice_prediccion]
        probabilidad_predicha = probs_row[indice_prediccion]

        st.markdown(f"**La clase predicha por el modelo es:** `{clase_predicha}` con una probabilidad de **{probabilidad_predicha:.2%}**")
    else:
        st.warning("El modelo no soporta 'predict_proba'. Usa un modelo de clasificación con esta funcionalidad.")
