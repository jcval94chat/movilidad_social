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
    # Quitar título de la sección
    # st.title("")

    # Cargar el modelo si no está en session_state
    modelo_path = 'models/modelo_entrenado.joblib'
    if not os.path.exists(modelo_path):
        st.error(f"No se encontró el archivo de modelo '{modelo_path}'.")
        return

    if 'modelo_regr' not in st.session_state:
        regr = joblib.load(modelo_path)
        st.session_state['modelo_regr'] = regr
    else:
        regr = st.session_state['modelo_regr']

    # Variables que el usuario marcará (0/1)
    # variables = {
    #     'p126d': 'Horno de microondas',
    #     'p131':  'Automóvil propio',
    #     'p125d': 'Calentador de agua',
    #     'p126o': 'Computadora',
    #     'p126f': 'Tostador de pan',
    #     'p126g': 'Aspiradora',
    #     'p125e': 'Servicio doméstico',
    #     'p129a': 'Otra casa/depto',
    #     'p126h': 'DVD/Blu-Ray',
    #     'p126b': 'Lavadora'
    # }

    variables = {'p126d': 'Microondas',
        'p131': 'Automóvil propio',
        'p125d': 'Calentador de agua',
        'p126f': 'Tostador eléctrico de pan',
        'p126g': 'Aspiradora',
        'p125e': 'Servicio doméstico',
        'p129a': 'Otra casa/depto',
        'p125a': 'Agua entubada',
        'p126b': 'Lavadora'
        }

    # Mensaje breve
    st.write("Selecciona y presiona **Procesar**:")

    # Crear un formulario para que no haya recarga en cada click de checkbox
    with st.form("form_variables"):
        # Dibujamos los checkboxes en filas de 5 columnas
        keys_list = list(variables.keys())
        num_vars = len(keys_list)
        cols_per_row = 5

        # Recorrido en bloques de 5
        for start_idx in range(0, num_vars, cols_per_row):
            row_vars = keys_list[start_idx:start_idx+cols_per_row]
            cols = st.columns(len(row_vars))

            for i, var in enumerate(row_vars):
                desc = variables[var]
                # Checkbox => True/False
                # No usamos help= para evitar el icono de "?"
                cols[i].checkbox(
                    label=desc,
                    key=f"chk_{var}",
                    value=False
                )

        st.write("")  # Espacio en blanco
        # Colocar el botón "Procesar" justo aquí, al final del form
        procesar = st.form_submit_button("Procesar")

    # Solo si el usuario pulsa "Procesar"
    if procesar:
        # Construimos DataFrame con valores 0/1
        # (checkbox True => 1, False => 0)
        datos_usuario = {}
        for var in variables:
            # El checkbox se guardó en session_state[f"chk_{var}"]
            is_checked = st.session_state.get(f"chk_{var}", False)
            datos_usuario[var] = 1 if is_checked else 0

        df_usuario = pd.DataFrame([datos_usuario])

        # Orden de features
        if hasattr(regr, 'feature_names_in_'):
            modelo_feats = list(regr.feature_names_in_)
        else:
            modelo_feats = list(variables.keys())

        # Asegurar todas las columnas
        for feat in modelo_feats:
            if feat not in df_usuario.columns:
                df_usuario[feat] = 0
        df_usuario = df_usuario[modelo_feats]

        if hasattr(regr, "predict_proba"):
            probabilidades = regr.predict_proba(df_usuario)
            clases = regr.classes_
            probs = probabilidades[0]

            # Mapeo 1..5 => texto
            class_mapping = {
                1: "Baja Baja",
                2: "Baja Alta",
                3: "Media Baja",
                4: "Media Alta",
                5: "Alta"
            }
            # Convertir clases => texto
            clases_texto = []
            for c in clases:
                if c in class_mapping:
                    clases_texto.append(class_mapping[c])
                else:
                    # Si tu modelo maneja otras clases (ej. 0, 6, etc.)
                    # las dejamos tal cual
                    clases_texto.append(str(c))

            df_plot = pd.DataFrame({
                'Clase': clases_texto,
                'Probabilidad': probs
            })

            fig = px.bar(
                df_plot,
                x='Clase',
                y='Probabilidad',
                range_y=[0, 1],
                text='Probabilidad',
                color='Clase',
                title=""
            )
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig.update_layout(
                yaxis=dict(title='Probabilidad'),
                xaxis=dict(title='Clase'),
                uniformtext_minsize=8,
                uniformtext_mode='hide'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Clase con mayor probabilidad
            idx_pred = np.argmax(probs)
            clase_pred = clases_texto[idx_pred]
            prob_pred = probs[idx_pred]
            st.write(f"Predicción: **{clase_pred}** con {prob_pred:.2%} de probabilidad.")
        else:
            st.warning("El modelo no soporta 'predict_proba'.")

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
