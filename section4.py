# section4.py

import streamlit as st
import joblib
import pandas as pd


import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

def generar_lista_preguntas(data_desc):
    """
    Genera una lista de preguntas de manera automática según la estructura de data_desc.
    Si la entrada data_desc tiene la forma:

    data_desc['p86'] = {
        'Descripción': 'Num horas trabaja a la semana',
        'Valores': [],        # vacío => no hay opciones
        'Etiquetas': []       # vacío => no hay opciones
    }

    data_desc['p33_f'] = {
        'Descripción': 'Artículos hogar (14 años): tostador eléctrico',
        'Valores': [1, 2, 8],
        'Etiquetas': ['Sí', 'No', 'NS']
    }

    Entonces, si 'Valores' y 'Etiquetas' NO están vacíos, creará una pregunta de tipo "opciones".
    Si están vacíos, creará una pregunta de tipo "numérico".

    Retorna una lista de dicts con la estructura:
    [
      {
        'variable': 'p86',
        'descripcion': 'Num horas trabaja a la semana',
        'tipo': 'numeric'  # o 'opciones'
        'opciones': { ... } # si aplica
      },
      ...
    ]
    """
    preguntas = []

    for var, info in data_desc.items():
        descripcion = info.get('Descripción', f"Pregunta de {var}")
        valores = info.get('Valores', [])
        etiquetas = info.get('Etiquetas', [])

        # Decidir tipo de pregunta
        if valores and etiquetas and len(valores) == len(etiquetas):
            # Hay opciones
            tipo_pregunta = 'opciones'
            # Crear dict {codigo: texto_opcion} para desplegar
            opciones_dict = {}
            for cod, etiq in zip(valores, etiquetas):
                opciones_dict[cod] = etiq

            preguntas.append({
                'variable': var,
                'descripcion': descripcion,
                'tipo': tipo_pregunta,
                'opciones': opciones_dict
            })

        else:
            # No hay opciones (o están desfasadas), se asume pregunta numérica
            tipo_pregunta = 'numeric'
            preguntas.append({
                'variable': var,
                'descripcion': descripcion,
                'tipo': tipo_pregunta
            })

    return preguntas


# ================================
# Funciones para preguntar en consola
# ================================

def preguntar_opciones_console(variable, descripcion, opciones):
    """
    Muestra una pregunta con opciones en consola y retorna (codigo, texto).
    """
    print(f"\nVariable: {variable}")
    print(f"Pregunta: {descripcion}")
    print("Seleccione una de las siguientes opciones:")

    for codigo, texto_opcion in opciones.items():
        print(f"  {codigo} -> {texto_opcion}")

    while True:
        entrada = input("Ingrese el código de su respuesta: ")
        try:
            codigo_int = int(entrada)
            if codigo_int in opciones:
                return codigo_int, opciones[codigo_int]
            else:
                print("Código inválido, intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")


def preguntar_numero_console(variable, descripcion):
    """
    Muestra una pregunta numérica en consola y retorna (numero, str(numero)).
    """
    print(f"\nVariable: {variable}")
    print(f"Pregunta: {descripcion}")
    print("Ingrese un número (entero o decimal).")

    while True:
        entrada = input("Valor: ")
        try:
            valor = float(entrada)
            return valor, str(valor)
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")


# ================================
# Funciones para preguntar en Streamlit
# ================================

def preguntar_opciones_streamlit(variable, descripcion, opciones, st):
    """
    Muestra una pregunta con opciones en Streamlit y retorna (codigo, texto).
    'st' es el módulo streamlit importado.
    """
    st.write(f"**Variable**: {variable}")
    st.write(descripcion)
    # Creamos la lista de opciones para selectbox
    # ejemplo: "1 - Sí"
    opciones_list = [f"{k} - {v}" for k,v in opciones.items()]
    seleccion = st.selectbox("Seleccione una opción", opciones_list)

    # Extraemos el código (lo que está antes del primer ' - ')
    codigo_str = seleccion.split(" - ")[0]
    codigo_int = int(codigo_str)
    return codigo_int, opciones[codigo_int]


def preguntar_numero_streamlit(variable, descripcion, st):
    """
    Muestra una pregunta numérica en Streamlit y retorna (numero, str(numero)).
    """
    st.write(f"**Variable**: {variable}")
    st.write(descripcion)
    valor = st.number_input("Ingrese un valor", value=0.0, step=1.0)
    return valor, str(valor)


# ================================
# Función principal que aplica el cuestionario
# ================================

def aplicar_cuestionario(preguntas, front='console', st=None):
    """
    Aplica cada pregunta de la lista 'preguntas' usando 'front' (console o streamlit).
    Retorna una lista de respuestas, cada respuesta es un dict:
    {
      'variable': ...,
      'descripcion': ...,
      'respuesta_codigo': ...,
      'respuesta_texto': ...
    }

    Parámetros:
    -----------
    - preguntas: lista de dicts con la estructura generada por generar_lista_preguntas.
    - front: 'console' (por defecto) o 'streamlit'.
    - st: referencia al módulo streamlit (solo si front='streamlit').
    """
    respuestas = []

    for p in preguntas:
        variable = p['variable']
        descripcion = p['descripcion']
        tipo = p['tipo']

        if tipo == 'opciones':
            # Tiene 'opciones'
            opciones = p.get('opciones', {})
            if front == 'console':
                r_codigo, r_texto = preguntar_opciones_console(variable, descripcion, opciones)
            elif front == 'streamlit' and st is not None:
                r_codigo, r_texto = preguntar_opciones_streamlit(variable, descripcion, opciones, st)
            else:
                raise ValueError("Front no válido o no se pasó 'st' para Streamlit.")

        else:
            # pregunta numérica
            if front == 'console':
                r_codigo, r_texto = preguntar_numero_console(variable, descripcion)
            elif front == 'streamlit' and st is not None:
                r_codigo, r_texto = preguntar_numero_streamlit(variable, descripcion, st)
            else:
                raise ValueError("Front no válido o no se pasó 'st' para Streamlit.")

        respuestas.append({
            'variable': variable,
            'descripcion': descripcion,
            'respuesta_codigo': r_codigo,
            'respuesta_texto': r_texto
        })

    return respuestas


def respuestas_a_dataframe(respuestas):
    """
    Convierte la lista de respuestas en un DataFrame de pandas.
    """
    return pd.DataFrame(respuestas)


# ================================
# Función orquestadora
# ================================

def cuestionario_general(data_desc, front='console', st=None):
    """
    Función orquestadora:
    1. Genera la lista de preguntas según 'data_desc'.
    2. Aplica el cuestionario en el front ('console' o 'streamlit').
    3. Retorna un DataFrame con las respuestas.
    """
    # 1. Generar lista de preguntas
    lista_preguntas = generar_lista_preguntas(data_desc)

    # 2. Aplicar el cuestionario
    respuestas = aplicar_cuestionario(lista_preguntas, front=front, st=st)

    # 3. Convertir a DataFrame
    df = respuestas_a_dataframe(respuestas)
    return df



def obtener_vecinos_de_mi_respuesta(df_respuestas, df_datos_clusterizados_, df_datos_descript_valiosas, n_vecinos=20):
    """
    Encuentra los vecinos más cercanos en términos de distancia euclidiana dentro de los datos clusterizados
    y devuelve las características descriptivas de los clusters más representativos.

    Parámetros:
    df_respuestas: DataFrame con las respuestas del usuario (columnas: 'variable', 'respuesta_codigo').
    df_datos_clusterizados_: DataFrame con datos clusterizados (debe contener una columna 'cluster').
    df_datos_descript_valiosas: DataFrame con descripciones de los clusters.
    n_vecinos: Número de vecinos a considerar (default: 20).

    Retorna:
    DataFrame con las características descriptivas de los clusters más representativos.
    """

    # Filtrar datos sin cluster -1
    df_datos_clusterizados = df_datos_clusterizados_[df_datos_clusterizados_['cluster'] != -1]

    # Extraer variables que coinciden entre respuestas del usuario y el dataset
    variables_usuario = df_respuestas['variable'].tolist()
    missing_vars = set(variables_usuario) - set(df_datos_clusterizados.columns)

    if missing_vars:
        print(f"⚠️ Las siguientes variables faltan en 'df_datos_clusterizados': {missing_vars}")
        variables_usuario = [var for var in variables_usuario if var not in missing_vars]

    # Crear vector de respuestas del usuario
    respuesta_usuario = df_respuestas.set_index('variable')['respuesta_codigo'].to_dict()
    user_vector = pd.Series(respuesta_usuario, index=variables_usuario).values.reshape(1, -1)

    # Extraer las variables relevantes de df_datos_clusterizados
    X = df_datos_clusterizados[variables_usuario].values

    # Manejo de valores faltantes en X
    imputer = SimpleImputer(strategy="mean")
    X = imputer.fit_transform(X)

    # Normalización de los datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Normalizar también el vector del usuario con el mismo scaler
    user_vector_scaled = scaler.transform(user_vector)

    # Aplicar K-Nearest Neighbors
    knn = NearestNeighbors(n_neighbors=n_vecinos, metric='euclidean')
    knn.fit(X_scaled)

    # Encontrar los vecinos más cercanos
    distances, indices = knn.kneighbors(user_vector_scaled)

    # Extraer los vecinos utilizando los índices obtenidos
    vecinos = df_datos_clusterizados.iloc[indices[0]].copy()
    vecinos['distancia'] = distances[0]

    # Ordenar por distancia
    vecinos = vecinos.sort_values(by='distancia')
    vecinos = vecinos[variables_usuario + ['cluster', 'distancia']]

    # Obtener los clusters más representativos
    df_clusters = vecinos['cluster'].value_counts().reset_index()
    df_clusters.columns = ['cluster', 'count']

    # Unir con la información descriptiva de los clusters
    df_datos_descript_valiosas_respuestas = df_datos_descript_valiosas.merge(df_clusters, on='cluster', how='inner')

    return df_datos_descript_valiosas_respuestas.sort_values(by='count', ascending=False)


import re

def construir_descripciones_cluster(
    variables_cambio,
    data_desc,
    nuevo_diccionario,
    language='es',          # 'es' para español, 'en' para inglés
    show_N_probabilidad=True,
    show_Probabilidad=True
):
    """
    Construye descripciones concisas de cada 'cluster_descripcion' en variables_cambio.

    Parámetros
    ----------
    variables_cambio : pd.DataFrame
        Debe contener las columnas:
          - 'cluster_descripcion' (ej: "2.5 <= p133 ... AND 0.5 <= p126p ...")
          - 'N_probabilidad' (float, incremento de prob. respecto a la media)
          - 'Probabilidad' (float, probabilidad de pertenecer a ese grupo)
    data_desc : dict
        Diccionario con la descripción de cada variable (por ej. 'p133') y
        una lista de valores y etiquetas.
    nuevo_diccionario : dict
        Diccionario con información extra para cada variable, por ejemplo:
        {
          'p133': (
              {'puedo_cambiarlo_yo': 'difícil'},
              {'puede_cambiarlo_gobierno': 'no_aplica'},
              {'involucrados': ['yo', 'entorno']},
              {'recursos_necesarios': ['Tiempo','Dinero']}
          ),
          ...
        }
    language : str, opcional
        'es' para generar el texto en español, 'en' para inglés. Por defecto 'es'.
    show_N_probabilidad : bool, opcional
        Si True, se muestra el valor de 'N_probabilidad' de cada cluster.
    show_Probabilidad : bool, opcional
        Si True, se muestra la 'Probabilidad' de cada cluster.

    Retorna
    -------
    dict
        Diccionario cuyo índice corresponde al índice de la fila en 'variables_cambio'
        y cuyo valor es un string descriptivo (en el idioma seleccionado).
    """

    # Función auxiliar para intentar convertir valores a int o float
    def try_convert(val):
        try:
            return int(val)
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return val  # Retorna el valor original si no es numérico

    # Mensajes en español/inglés según el parámetro `language`
    if language == 'es':
        txt_cluster = "Cluster"
        txt_original = "Descripción original"
        txt_condiciones = "Variables y rangos:"
        txt_prob = "Probabilidad"
        txt_conf = "Nivel de confianza (Baja:0, Alta 3)"
        txt_N_prob = "Incremento de probabilidad respecto a la media"
        txt_variable = "Variable"
        txt_range = "Rango"
        txt_desc = "Descripción"
        txt_cat = "Categorías en rango"
        txt_no_cat = "No categorías identificadas en este rango"
        txt_puedo = "¿Puedo cambiarlo yo?"
        txt_gob = "¿Puede cambiarlo el gobierno?"
        txt_invol = "Involucrados"
        txt_recursos = "Recursos"
    else:
        txt_cluster = "Group"
        txt_original = "Original description"
        txt_condiciones = "Variables and ranges:"
        txt_prob = "Probability"
        txt_conf = "Confidence Level (Low: 0, High: 3)"
        txt_N_prob = "Probability increment over average"
        txt_variable = "Variable"
        txt_range = "Range"
        txt_desc = "Description"
        txt_cat = "Categories in range"
        txt_no_cat = "No categories identified in this range"
        txt_puedo = "Can I change it?"
        txt_gob = "Can the government change it?"
        txt_invol = "Involved"
        txt_recursos = "Resources"

    # Regex para extraer límites y variable:
    # Ejemplo: "2.5 <= p133 - Ingreso total... <= 10.0"
    patron_intervalo = re.compile(
        r'([0-9.]+)\s*<=\s*(p[\w\d]+)\s*-\s*(.*?)\s*<=\s*([0-9.]+)'
    )

    descripciones_por_cluster = {}

    for idx, row in variables_cambio.iterrows():
        desc_cruda = row['cluster_descripcion']

        # Extraer N_probabilidad y Probabilidad (si existen)
        n_prob_value = row.get('N_probabilidad', None)
        prob_value = row.get('Probabilidad', None)

        conf_val = str(row.get('nivel_de_confianza_cluster', None))

        # Dividir en sub-condiciones por "AND"
        condiciones = [c.strip() for c in desc_cruda.split('AND')]

        # Construir un encabezado conciso
        texto = []
        # Ej: "**Cluster 1**" o "**Group 1**"
        texto.append(f"**{txt_cluster} {idx}**")

        # Mostrar N_probabilidad y Probabilidad si se pide
        if show_N_probabilidad and (n_prob_value is not None):
            texto.append(f"- {txt_N_prob}: {n_prob_value:.2f}")
        if show_Probabilidad and (prob_value is not None):
            # Asumimos que Probabilidad es un decimal de 0 a 1. Mostramos en porcentaje.
            texto.append(f"- {txt_prob}: {prob_value:.1%}")

        texto.append(f"- {txt_conf}: {conf_val}")

        # Agregar descripción original (concisa)
        texto.append(f"- {txt_original}: {desc_cruda}")
        texto.append(f"- {txt_condiciones}")

        # Procesar cada condición
        for cond in condiciones:
            match = patron_intervalo.search(cond)
            if match:
                limite_inferior, variable, texto_var, limite_superior = match.groups()

                # Info de data_desc
                if variable in data_desc:
                    desc_variable = data_desc[variable].get('Descripción', '')
                    # Intentar convertir los valores posibles
                    valores_originales = data_desc[variable].get('Valores', [])
                    valores_posibles = [try_convert(v) for v in valores_originales]
                    etiquetas_valores = data_desc[variable].get('Etiquetas', [])
                else:
                    desc_variable = ""
                    valores_posibles = []
                    etiquetas_valores = []

                # Info de nuevo_diccionario
                info_extra_plano = {}
                if variable in nuevo_diccionario:
                    for d in nuevo_diccionario[variable]:
                        info_extra_plano.update(d)

                # Construir texto corto de la variable
                subtexto = []
                subtexto.append(f"  - {txt_variable}: {variable}")

                # Agregamos su descripción si existe
                if desc_variable:
                    subtexto.append(f"    - {txt_desc}: {desc_variable}")

                # Agregar el rango
                subtexto.append(f"    - {txt_range}: {limite_inferior} a {limite_superior}")

                # Intentar mapear categorías
                cat_in_range = []
                for val, etiq in zip(valores_posibles, etiquetas_valores):
                    # Verificar si 'val' es numérico
                    if isinstance(val, (int, float)):
                        try:
                            li = float(limite_inferior)
                            ls = float(limite_superior)
                            if li <= val <= ls:
                                cat_in_range.append(f"{val}={etiq}")
                        except:
                            continue  # En caso de error en conversión, saltar
                    else:
                        # Si 'val' es una cadena (ej: '25-64'), verificar superposición
                        # Esto puede ser complejo; para simplificar, listamos todas las categorías no numéricas
                        cat_in_range.append(f"{val}={etiq}")

                if cat_in_range:
                    subtexto.append(f"    - {txt_cat}: {', '.join(cat_in_range)}")
                else:
                    subtexto.append(f"    - {txt_no_cat}")

                # Info extra: ¿Puedo cambiarlo? etc.
                if 'puedo_cambiarlo_yo' in info_extra_plano:
                    subtexto.append(f"      - {txt_puedo}: {info_extra_plano['puedo_cambiarlo_yo']}")
                if 'puede_cambiarlo_gobierno' in info_extra_plano:
                    subtexto.append(f"      - {txt_gob}: {info_extra_plano['puede_cambiarlo_gobierno']}")
                if 'involucrados' in info_extra_plano:
                    inv_str = ', '.join(info_extra_plano['involucrados'])
                    subtexto.append(f"      - {txt_invol}: {inv_str}")
                if 'recursos_necesarios' in info_extra_plano:
                    rec_str = ', '.join(info_extra_plano['recursos_necesarios'])
                    subtexto.append(f"      - {txt_recursos}: {rec_str}")

                # Unir y agregar al texto global
                texto.extend(subtexto)
            else:
                # Si no se parseó (formato distinto)
                texto.append(f"  - {cond}")

        # Unir todo el texto en un solo bloque
        descripciones_por_cluster[idx] = "\n".join(texto)

    return descripciones_por_cluster




def show_section4():
    base_path = 'data/'
    if 'df_valiosas_dict' not in st.session_state:
        st.session_state['df_valiosas_dict'] = joblib.load(base_path+'df_valiosas_dict.joblib')
    if 'df_feature_importances_total' not in st.session_state:
        st.session_state['df_feature_importances_total'] = joblib.load(base_path+'df_feature_importances_total.joblib')
    if 'df_clusterizados_total_origi' not in st.session_state:
        st.session_state['df_clusterizados_total_origi'] = pd.read_csv(base_path+'df_clusterizados_total_origi.csv')

    st.write("Sección 4")
    TARGETS = list(st.session_state['df_valiosas_dict'].keys())
    target = st.selectbox("Target", TARGETS, index=0)

    df_datos_descript_valiosas = st.session_state['df_valiosas_dict'][target]
    prefix = f"{target}_"
    df_cluster_target = st.session_state['df_clusterizados_total_origi'].rename(
        columns={
            c: c.replace(prefix,"") 
            for c in st.session_state['df_clusterizados_total_origi'].columns 
            if c.startswith(prefix)
        }
    )

    df_feature_importances_total = st.session_state['df_feature_importances_total']
    best_val = [x.split('-')[0].strip() for x in df_feature_importances_total[f"{target}_importance"].sort_values(ascending=False).index][:10]
    best_val = [x for x in best_val if x not in ['p133','CIUO2']]

    preguntas_lista_ = ['p05','p86','p33_f','p43','p43m','p13','p98','p151','p64']
    preguntas_lista = sorted(list(set(preguntas_lista_+best_val)))

    # Ejemplo de "df_respuestas" en Streamlit (simplificado):
    st.write("Respuestas hipotéticas (demo):")
    df_respuestas = pd.DataFrame([{p: 0 for p in preguntas_lista}])


    # Filtrado
    opciones_filtro = {
        'cambio': lambda df: df[(df['cambio_yo_moderado']>0)|(df['cambio_yo_difícil']>0)|(df['cambio_yo_fácil']>0)].sort_values('N_probabilidad', ascending=False),
        'gobierno': lambda df: df[df['involucrados_gobierno']>0],
        'extenso': lambda df: df[((df['cambio_yo_moderado']>0)|(df['cambio_yo_difícil']>0)|(df['cambio_yo_fácil']>0))&(df['nivel_de_confianza_cluster']==0)&(df['N_probabilidad']>1)],
        'confidence': lambda df: df[((df['cambio_yo_moderado']>0)|(df['cambio_yo_difícil']>0)|(df['cambio_yo_fácil']>0))&(df['nivel_de_confianza_cluster']>0)]
    }

    user_choice = st.selectbox("Filtrar por", list(opciones_filtro.keys()), index=0)

    if st.button("Ejecutar"):
        df_datos_descript_valiosas_respuestas = obtener_vecinos_de_mi_respuesta(
            df_respuestas, 
            df_cluster_target, 
            df_datos_descript_valiosas
        )
        df_datos_descript_valiosas_respuestas['nivel_de_confianza_cluster'] = pd.qcut(
            df_datos_descript_valiosas_respuestas['Soporte'], q=4, labels=False
        )
        df_filtrado = opciones_filtro[user_choice](df_datos_descript_valiosas_respuestas)
        resultado = construir_descripciones_cluster(df_filtrado, None, None, language='es', show_N_probabilidad=True, show_Probabilidad=True)
        st.dataframe(resultado)
