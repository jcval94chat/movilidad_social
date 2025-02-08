# section4.py

import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

import uuid

from utils.diccionarios import get_nuevo_diccionario, get_data_desc

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
# Función principal que aplica el cuestionario
# ================================

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



def obtener_vecinos_de_mi_respuesta(df_respuestas, df_datos_clusterizados_, 
                                    df_datos_descript_valiosas, n_vecinos=20):
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



def generar_lista_preguntas(data_desc):
    preguntas = []
    for var, info in data_desc.items():
        desc = info.get('Descripción', var)
        vals = info.get('Valores', [])
        etiq = info.get('Etiquetas', [])
        if vals and etiq and len(vals) == len(etiq):
            preguntas.append({'variable': var, 'descripcion': desc, 'tipo': 'opciones', 'opciones': dict(zip(vals, etiq))})
        else:
            preguntas.append({'variable': var, 'descripcion': desc, 'tipo': 'numeric'})
    return preguntas

def preguntar_opciones_streamlit(i, variable, descripcion, opciones):
    import uuid
    key_uid = f"opt_{variable}_{i}_{uuid.uuid4()}"
    st.write(f"**{variable}**: {descripcion}")
    lista = [f"{k} - {v}" for k, v in opciones.items()]
    sel = st.selectbox("", lista, key=key_uid, label_visibility="collapsed")
    cod = int(sel.split(" - ")[0])
    return cod, opciones[cod]

def preguntar_numero_streamlit(i, variable, descripcion):
    import uuid
    key_uid = f"num_{variable}_{i}_{uuid.uuid4()}"
    st.write(f"**{variable}**: {descripcion}")
    val = st.number_input("", value=0.0, step=1.0, key=key_uid, label_visibility="collapsed")
    return val, str(val)

def aplicar_cuestionario(preguntas):
    resp = []
    for i, p in enumerate(preguntas):
        var = p['variable']
        desc = p['descripcion']
        if p['tipo'] == 'opciones':
            rcod, rtxt = preguntar_opciones_streamlit(i, var, desc, p['opciones'])
        else:
            rcod, rtxt = preguntar_numero_streamlit(i, var, desc)
        resp.append({'variable': var, 'descripcion': desc, 'respuesta_codigo': rcod, 'respuesta_texto': rtxt})
    return pd.DataFrame(resp)

def cuestionario_general(data_desc):
    lp = generar_lista_preguntas(data_desc)
    df = aplicar_cuestionario(lp)
    return df

def generar_lista_preguntas(data_desc):
    preguntas = []
    for var, info in data_desc.items():
        desc = info.get('Descripción', var)
        vals = info.get('Valores', [])
        etiq = info.get('Etiquetas', [])
        if vals and etiq and len(vals) == len(etiq):
            preguntas.append({
                'variable': var,
                'descripcion': desc,
                'tipo': 'opciones',
                'opciones': dict(zip(vals, etiq))
            })
        else:
            preguntas.append({
                'variable': var,
                'descripcion': desc,
                'tipo': 'numeric'
            })
    return preguntas

def preguntar_opciones_streamlit(i, variable, descripcion, opciones):
    key_uid = f"opt_{variable}_{i}_{uuid.uuid4()}"
    st.write(f"**{variable}**: {descripcion}")
    lista = [f"{k} - {v}" for k, v in opciones.items()]
    sel = st.selectbox("", lista, key=key_uid, label_visibility="collapsed")
    cod = int(sel.split(" - ")[0])
    return cod, opciones[cod]

def preguntar_numero_streamlit(i, variable, descripcion):
    key_uid = f"num_{variable}_{i}_{uuid.uuid4()}"
    st.write(f"**{variable}**: {descripcion}")
    val = st.number_input("", value=0.0, step=1.0, key=key_uid, label_visibility="collapsed")
    return val, str(val)

def aplicar_cuestionario_en_columnas(preguntas, cols_per_row=3):
    """
    Muestra las preguntas agrupadas en filas con 'cols_per_row' columnas,
    reutilizando las funciones de pregunta.
    """
    resp = []
    # Iteramos en bloques de 'cols_per_row'
    for i in range(0, len(preguntas), cols_per_row):
        # Creamos una fila con las columnas
        cols = st.columns(cols_per_row)
        # Iteramos en cada columna junto a la pregunta correspondiente
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(preguntas):
                p = preguntas[idx]
                var = p['variable']
                desc = p['descripcion']
                # Todo lo que se muestra en esta columna se agrupa con "with col:"
                with col:
                    if p['tipo'] == 'opciones':
                        rcod, rtxt = preguntar_opciones_streamlit(idx, var, desc, p['opciones'])
                    else:
                        rcod, rtxt = preguntar_numero_streamlit(idx, var, desc)
                resp.append({
                    'variable': var,
                    'descripcion': desc,
                    'respuesta_codigo': rcod,
                    'respuesta_texto': rtxt
                })
    return pd.DataFrame(resp)

def cuestionario_general(data_desc, cols_per_row=3):
    lp = generar_lista_preguntas(data_desc)
    df = aplicar_cuestionario_en_columnas(lp, cols_per_row)
    return df


def get_color_for_increment(diff):
    """
    Retorna un color (en formato hexadecimal) que varía de rojo a verde según el valor diff.
    Se asume que diff está en un rango aproximado de -0.5 a 0.5.
    """
    min_diff, max_diff = -0.5, 0.5
    clamped = max(min_diff, min(max_diff, diff))
    # Factor de interpolación: 0 para diff=min_diff (rojo) y 1 para diff=max_diff (verde)
    t = (clamped - min_diff) / (max_diff - min_diff)
    r = int((1-t) * 255)
    g = int(t * 255)
    b = 0
    return f"#{r:02x}{g:02x}{b:02x}"

def map_confidence(value):
    """
    Mapea un valor numérico de confianza a un texto descriptivo.
    Puedes ajustar estos límites según tus necesidades.
    """
    try:
        val = float(value)
    except:
        return value
    if val <= 0:
        return "Baja"
    elif val == 1:
        return "Media"
    elif val == 2:
        return "Alta"
    else:  # para 3 o más
        return "Muy Alta"



def format_cluster_description(raw_desc):
    """
    Recibe la descripción cruda de un cluster (string con saltos de línea)
    y retorna una versión formateada y más concisa según el ejemplo esperado.
    
    Se asume que el string original tiene secciones similares a:
    
      **Cluster 4**
      - Incremento de probabilidad respecto a la media: 0.97
      - Probabilidad: 1.2%
      - Nivel de confianza (Baja:0, Alta 3): 2.0
      - Descripción original: … (se ignora)
      - Variables y rangos:
        - Variable: p128b
          - Descripción: Servicios financieros: cuenta ahorro
          - Rango: 0.0 a 1.5
          - Categorías en rango: 1=Sí
            - ¿Puedo cambiarlo yo?: fácil
            - ¿Puede cambiarlo el gobierno?: no_aplica
            - Involucrados: yo
            - Recursos: Tiempo, Conocimiento, Dinero
        - Variable: p06
          - Descripción: Sexo
          - Rango: 0.0 a 1.5
          - Categorías en rango: 1=Hombre
            - ¿Puedo cambiarlo yo?: imposible
            - ¿Puede cambiarlo el gobierno?: no_aplica
            - Involucrados: yo
            - Recursos: no_aplica
    """
    lines = raw_desc.split("\n")
    summary_lines = []
    variables_lines = []
    in_variables_section = False
    current_var_block = []
    var_blocks = []
    
    for line in lines:
        stripped = line.strip()
        # Detectar el inicio de la sección de variables
        if stripped.startswith("- Variables y rangos:"):
            in_variables_section = True
            continue

        if not in_variables_section:
            # Procesar las líneas del resumen (antes de Variables)
            if stripped.startswith("- Incremento de probabilidad"):
                try:
                    # Extraer el valor numérico (ejemplo: "0.97")
                    incremento = float(stripped.split(":",1)[1].strip())
                    diff = incremento - 1.0  # diferencia respecto a 1
                    diff_percent = diff * 100  # en porcentaje
                    color = get_color_for_increment(diff)
                    # Se usa HTML para aplicar color
                    summary_lines.append(f'<span style="color:{color};font-weight:bold;">Incremento: {diff_percent:+.0f}%</span>')
                except Exception as e:
                    summary_lines.append(stripped)
            elif stripped.startswith("- Probabilidad:"):
                prob = stripped.split(":",1)[1].strip()
                summary_lines.append(f"Probabilidad: {prob}")
            elif stripped.startswith("- Nivel de confianza"):
                try:
                    conf_val = stripped.split(":",1)[1].strip()
                    conf_text = map_confidence(conf_val)
                    summary_lines.append(f"Confianza {conf_text}")
                except:
                    summary_lines.append(stripped)
            # Se ignoran otras líneas como el título del cluster o la descripción original
        else:
            # Acumulamos las líneas correspondientes a cada variable.
            # Cada bloque de variable empieza con "- Variable:" (con algún nivel de indentación)
            if stripped.startswith("- Variable:"):
                if current_var_block:
                    var_blocks.append(current_var_block)
                    current_var_block = []
                current_var_block.append(stripped)
            else:
                if current_var_block:
                    current_var_block.append(stripped)
    if current_var_block:
        var_blocks.append(current_var_block)
    
    # Procesar cada bloque de variable para extraer los datos relevantes
    for block in var_blocks:
        var_info = {}   # contendrá 'descripcion' y 'categorias'
        extra_props = []  # lista de propiedades extra a mostrar
        for line in block:
            if line.startswith("- Variable:"):
                # Si necesitas el código de la variable, lo puedes extraer aquí.
                var_info["codigo"] = line.split(":",1)[1].strip()
            elif line.startswith("- Descripción:"):
                var_info["descripcion"] = line.split(":",1)[1].strip()
            elif line.startswith("- Categorías en rango:"):
                cat_str = line.split(":",1)[1].strip()
                # Se separan las posibles múltiples categorías (por ejemplo "1=Sí, 2=No")
                cats = []
                for part in cat_str.split(","):
                    if "=" in part:
                        cat_val = part.split("=",1)[1].strip()
                        cats.append(cat_val)
                var_info["categorias"] = ", ".join(cats)
            elif line.startswith("- ¿Puedo cambiarlo yo?:"):
                val = line.split(":",1)[1].strip()
                if val.lower() != "no_aplica":
                    extra_props.append(f"¿Puedo cambiarlo yo?: {val}")
            elif line.startswith("- Involucrados:"):
                val = line.split(":",1)[1].strip()
                if val.lower() != "no_aplica":
                    extra_props.append(f"Involucrados: {val}")
            elif line.startswith("- Recursos:"):
                val = line.split(":",1)[1].strip()
                if val.lower() != "no_aplica":
                    extra_props.append(f"Recursos: {val}")
            # Se ignoran líneas como "- ¿Puede cambiarlo el gobierno?: ..."  
        # Solo si tenemos descripción y categoría, armamos la salida
        if "descripcion" in var_info and "categorias" in var_info:
            variables_lines.append(f"- {var_info['descripcion']} -> {var_info['categorias']}")
            for prop in extra_props:
                variables_lines.append(f"    - {prop}")
    
    # Unir las secciones y retornar el string formateado
    formatted = "\n".join(summary_lines) + "\n\n" + "\n\n".join(variables_lines)
    return formatted

def format_all_clusters(resultado):
    """
    Recibe un diccionario (cluster_id -> descripción cruda) y retorna otro diccionario
    con la misma llave pero con la descripción formateada.
    """
    formatted_result = {}
    for cluster_id, desc in resultado.items():
        formatted_result[cluster_id] = format_cluster_description(desc)
    return formatted_result


def show_section4():
    base_path = 'data/'
    if 'df_valiosas_dict' not in st.session_state:
        st.session_state['df_valiosas_dict'] = joblib.load(base_path+'df_valiosas_dict.joblib')
    if 'df_feature_importances_total' not in st.session_state:
        st.session_state['df_feature_importances_total'] = joblib.load(base_path+'df_feature_importances_total.joblib')
    if 'df_clusterizados_total_origi' not in st.session_state:
        st.session_state['df_clusterizados_total_origi'] = pd.read_csv(base_path+'df_clusterizados_total_origi.csv')

    TARGETS = list(st.session_state['df_valiosas_dict'].keys())

    nombres_targets = {
        'OBJ_pobre_a_rico': "De Pobre a Rico",
        'OBJ_rico_a_pobre': "De Rico a Pobre",
        'OBJ_siguie_siendo_rico': "Permanece Rico",
        'OBJ_siguie_siendo_pobre': "Permanece Pobre",
        'OBJ_sigue_siendo_clase_media': "Permanece Clase Media",
        'OBJ_clase_media_a_rico': "De Clase Media a Rico",
        'OBJ_clase_media_a_pobre': "De Clase Media a Pobre",
        'OBJ_subieron': "Ascendieron",
        'OBJ_bajaron': "Descendieron"
    }

    # user_selected_target = st.selectbox("Target", TARGETS, index=0)
    # Crear una lista de tuplas (valor, nombre amigable)
    opciones = [(valor, nombres_targets.get(valor, valor)) for valor in TARGETS]

    # Ordenar o conservar el orden original si es necesario
    # Por ejemplo, en el selectbox se muestra el nombre amigable pero se conserva el valor original:
    retorno_user = st.selectbox("Target", options=[(valor, nombre) for valor, nombre in opciones],
                            format_func=lambda x: x[1])

    user_selected_target = retorno_user[0]

    prefix = f"{user_selected_target}_"
    df_cluster = st.session_state['df_clusterizados_total_origi'].copy()
    rename_map = {}
    for c in df_cluster.columns:
        if c.startswith(prefix):
            rename_map[c] = c.replace(prefix, "")
    df_cluster_target = df_cluster.rename(columns=rename_map)

    df_feature_import = st.session_state['df_feature_importances_total']
    best_val = [x.split('-')[0].strip() for x in 
                df_feature_import[f"{user_selected_target}_importance"].sort_values(ascending=False).index][:7]
    
    best_val = [x for x in best_val if x not in ['p133','CIUO2','p23']]

    base_pregs = ['p05','p86','p33_f',]#'p43','p43m','p13','p98']#,'p151','p64']
    preguntas_lista = sorted(list(set(base_pregs+best_val)))

    # data_desc_global se obtiene de get_data_desc() y contiene la información completa de cada variable
    data_desc_global = get_data_desc()
    data_desc_usable = {k: data_desc_global[k] for k in preguntas_lista if k in data_desc_global}

    with st.form("cuestionario_form"):
        df_respuestas = cuestionario_general(data_desc_usable, cols_per_row=3)
        ejecutar = st.form_submit_button("Ejecutar")

    if ejecutar:
        df_datos_valiosas = st.session_state['df_valiosas_dict'][user_selected_target]
        df_datos_descript_valiosas_respuestas = obtener_vecinos_de_mi_respuesta(df_respuestas, 
                                                                                df_cluster_target, 
                                                                                df_datos_valiosas,
                                                                                n_vecinos=50)
        
        df_datos_descript_valiosas_respuestas['nivel_de_confianza_cluster'] = pd.qcut(
            df_datos_descript_valiosas_respuestas['Soporte'],
            q=4, labels=False
        )
        # if 'N_probabilidad' not in df_datos_descript_valiosas_respuestas.columns:
        #     df_datos_descript_valiosas_respuestas['N_probabilidad'] = np.random.randint(1,5, size=len(df_datos_descript_valiosas_respuestas))

        # Filtrado por defecto: se conservan las filas con alguna medida de cambio y con nivel de confianza > 0.
        df_filtrado = df_datos_descript_valiosas_respuestas[
            ((df_datos_descript_valiosas_respuestas['cambio_yo_moderado']>0)|
             (df_datos_descript_valiosas_respuestas['cambio_yo_difícil']>0)|
             (df_datos_descript_valiosas_respuestas['cambio_yo_fácil']>0))&
            (df_datos_descript_valiosas_respuestas['nivel_de_confianza_cluster']>0)
        ] if all(x in df_datos_descript_valiosas_respuestas.columns for x in ['cambio_yo_moderado',
                                                                              'cambio_yo_difícil',
                                                                              'cambio_yo_fácil',
                                                                              'nivel_de_confianza_cluster']) \
                                                                                else df_datos_descript_valiosas_respuestas

        nuevo_diccionario = get_nuevo_diccionario()

        resultado = construir_descripciones_cluster(
            df_filtrado, 
            data_desc_global, 
            nuevo_diccionario, 
            language='es', 
            show_N_probabilidad=True, 
            show_Probabilidad=True
        )
        
        # Mostrar los resultados:
        # for cluster_id, descripcion in resultado.items():
        #     st.write(descripcion)
        # st.write("\n\n".join(resultado.values()))

        formatted_resultado = format_all_clusters(resultado)

        st.write("### Resultados:")
        # Se usa st.markdown con unsafe_allow_html=True para aplicar el estilo en el incremento
        for cluster_id, desc in formatted_resultado.items():
            st.markdown(desc, unsafe_allow_html=True)

