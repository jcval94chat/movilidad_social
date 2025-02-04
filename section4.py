# section4.py

import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


# section4.py
import uuid
import streamlit as st

def get_nuevo_diccionario():
    nuevo_diccionario = {

    # p09_2 - (puedo cambiarlo yo / relacionado a mi)
    "p09_2": (
        {"puedo_cambiarlo_yo": "fácil"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["yo", "entorno"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento"]}
    ),

    # p134e - (puede cambiarlo el gobierno / a mi entorno)
    "p134e": (
        {"puedo_cambiarlo_yo": "difícil"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["gobierno", "entorno"]},
        {"recursos_necesarios": ["Infraestructura", "Dinero"]}
    ),

    # p70 - (puedo cambiarlo yo / relacionado a mi)
    "p70": (
        {"puedo_cambiarlo_yo": "fácil"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento"]}
    ),

    # p35 - (no puedo cambiarlo / a mis padres)
    "p35": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p54 - (no puedo cambiarlo / a mis padres)
    "p54": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p09_3 - (puedo cambiarlo yo / relacionado a mi)
    "p09_3": (
        {"puedo_cambiarlo_yo": "moderado"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["yo", "entorno"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento"]}
    ),

    # p140 - (no puedo cambiarlo / relacionado a mi)
    "p140": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p58 - (no puedo cambiarlo / a mis padres)
    "p58": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p62g - (puede cambiarlo el gobierno / a mi entorno)
    "p62g": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["gobierno", "entorno"]},
        {"recursos_necesarios": ["Infraestructura", "Dinero"]}
    ),

    # p126p - (no puedo cambiarlo / a mi entorno)
    "p126p": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["entorno"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p151 - (no puedo cambiarlo / relacionado a mi)
    "p151": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p15 - (puedo cambiarlo yo / relacionado a mi)
    "p15": (
        {"puedo_cambiarlo_yo": "fácil"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["Tiempo"]}
    ),

    # p06 - (no puedo cambiarlo / relacionado a mi)
    "p06": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p40m - (no puedo cambiarlo / a mis padres)
    "p40m": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p40 - (no puedo cambiarlo / a mis padres)
    "p40": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p134c - (puede cambiarlo el gobierno / a mi entorno)
    "p134c": (
        {"puedo_cambiarlo_yo": "difícil"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["gobierno", "entorno"]},
        {"recursos_necesarios": ["Infraestructura", "Dinero"]}
    ),

    # p128b - (puedo cambiarlo yo / relacionado a mi)
    "p128b": (
        {"puedo_cambiarlo_yo": "fácil"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento", "Dinero"]}
    ),

    # p138 - (no puedo cambiarlo / relacionado a mi)
    "p138": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p66 - (puedo cambiarlo yo / relacionado a mi)
    "p66": (
        {"puedo_cambiarlo_yo": "fácil"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento"]}
    ),

    # p115 - (no puedo cambiarlo / relacionado a mi)
    "p115": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p34_f - (no puedo cambiarlo / a mi entorno)
    "p34_f": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["entorno"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p134i - (puede cambiarlo el gobierno / a mi entorno)
    "p134i": (
        {"puedo_cambiarlo_yo": "difícil"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["gobierno", "entorno"]},
        {"recursos_necesarios": ["Infraestructura", "Dinero"]}
    ),

    # p128a - (puedo cambiarlo yo / relacionado a mi)
    "p128a": (
        {"puedo_cambiarlo_yo": "moderado"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento", "Dinero"]}
    ),

    # p23 - (no puedo cambiarlo / relacionado a mi)
    "p23": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p130c_11 - (puede cambiarlo el gobierno / a mi entorno)
    "p130c_11": (
        {"puedo_cambiarlo_yo": "difícil"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["gobierno", "entorno"]},
        {"recursos_necesarios": ["Infraestructura", "Dinero"]}
    ),

    # p116 - (no puedo cambiarlo / relacionado a mi)
    "p116": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p33_f - (no puedo cambiarlo / a mi entorno)
    "p33_f": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["entorno"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p62h - (puede cambiarlo el gobierno / a mi entorno)
    "p62h": (
        {"puedo_cambiarlo_yo": "difícil"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["gobierno", "entorno"]},
        {"recursos_necesarios": ["Infraestructura", "Dinero"]}
    ),

    # p136 - (no puedo cambiarlo / relacionado a mi)
    "p136": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p117 - (no puedo cambiarlo / relacionado a mi)
    "p117": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p113 - (no puedo cambiarlo / relacionado a mi)
    "p113": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p134f - (puede cambiarlo el gobierno / a mi entorno)
    "p134f": (
        {"puedo_cambiarlo_yo": "difícil"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["gobierno", "entorno"]},
        {"recursos_necesarios": ["Infraestructura", "Dinero"]}
    ),

    # p134h - (puede cambiarlo el gobierno / a mi entorno)
    "p134h": (
        {"puedo_cambiarlo_yo": "difícil"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["gobierno", "entorno"]},
        {"recursos_necesarios": ["Infraestructura", "Dinero"]}
    ),

    # p93 - (no puedo cambiarlo / relacionado a mi)
    "p93": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p139 - (no puedo cambiarlo / relacionado a mi)
    "p139": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p113_11 - (no puedo cambiarlo / relacionado a mi)
    "p113_11": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # CIUO2 - (no puedo cambiarlo / a mis padres)
    "CIUO2": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p130b - (puede cambiarlo el gobierno / relacionado a mi)
    "p130b": (
        {"puedo_cambiarlo_yo": "difícil"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["yo", "gobierno", "entorno"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento", "Infraestructura", "Dinero"]}
    ),

    # p130d - (no puedo cambiarlo / a mi entorno)
    "p130d": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["entorno"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p98 - (no puedo cambiarlo / relacionado a mi)
    "p98": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p86 - (puedo cambiarlo yo / relacionado a mi)
    "p86": (
        {"puedo_cambiarlo_yo": "moderado"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo", "entorno"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento"]}
    ),

    # p68 - (puedo cambiarlo yo / relacionado a mi)
    "p68": (
        {"puedo_cambiarlo_yo": "fácil"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo", "entorno"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento"]}
    ),

    # p13 - (puedo cambiarlo yo / relacionado a mi)
    "p13": (
        {"puedo_cambiarlo_yo": "moderado"},
        {"puede_cambiarlo_gobierno": "moderado"},
        {"involucrados": ["yo", "entorno"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento"]}
    ),

    # p05 - (no puedo cambiarlo / relacionado a mi)
    "p05": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p53 - (no puedo cambiarlo / a mis padres)
    "p53": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p43m - (no puedo cambiarlo / a mis padres)
    "p43m": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p43 - (no puedo cambiarlo / a mis padres)
    "p43": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p46 - (no puedo cambiarlo / a mis padres)
    "p46": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p133 - (puedo cambiarlo yo / a mi entorno)
    "p133": (
        {"puedo_cambiarlo_yo": "difícil"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo", "entorno"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento", "Infraestructura", "Dinero"]}
    ),

    # p76 - (puedo cambiarlo yo / relacionado a mi)
    "p76": (
        {"puedo_cambiarlo_yo": "moderado"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["yo", "entorno"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento"]}
    ),

    # p64 - (puedo cambiarlo yo / a mi entorno)
    "p64": (
        {"puedo_cambiarlo_yo": "moderado"},
        {"puede_cambiarlo_gobierno": "difícil"},
        {"involucrados": ["yo", "gobierno", "entorno"]},
        {"recursos_necesarios": ["Tiempo", "Conocimiento", "Infraestructura", "Dinero"]}
    ),

    # p38_11 - (no puedo cambiarlo / a mis padres)
    "p38_11": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),

    # p38m_11 - (no puedo cambiarlo / a mis padres)
    "p38m_11": (
        {"puedo_cambiarlo_yo": "imposible"},
        {"puede_cambiarlo_gobierno": "no_aplica"},
        {"involucrados": ["padres"]},
        {"recursos_necesarios": ["no_aplica"]}
    ),
    }
    return nuevo_diccionario


def get_data_desc():
    data_desc = {
        "folio": {
            "Descripción": "Folio identificador del entrevistado",
            "Valores": [],
            "Etiquetas": []
        },
        "Estado": {
            "Descripción": "Entidad federativa (1-32, ver pestaña Estado)",
            "Valores": ["1-32"],
            "Etiquetas": []
        },
        "folio_ageb": {
            "Descripción": "Listado de AGEB elegidas para la muestra",
            "Valores": [],
            "Etiquetas": []
        },
        "consecutivo": {
            "Descripción": "Folio identificador para base de hogares",
            "Valores": [],
            "Etiquetas": []
        },
        "Origen": {
            "Descripción": "Origen de las coordenadas geográficas",
            "Valores": [],
            "Etiquetas": []
        },
        "Latitud": {
            "Descripción": "Coordenadas de latitud",
            "Valores": [],
            "Etiquetas": []
        },
        "Longitud": {
            "Descripción": "Coordenadas de longitud",
            "Valores": [],
            "Etiquetas": []
        },
        "LatitudGP": {
            "Descripción": "Coordenadas de latitud GP",
            "Valores": [],
            "Etiquetas": []
        },
        "LongitudGP": {
            "Descripción": "Coordenadas de longitud GP",
            "Valores": [],
            "Etiquetas": []
        },
        "recontacto": {
            "Descripción": "Asintió recontacto",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "Factor": {
            "Descripción": "Factor de expansión",
            "Valores": [],
            "Etiquetas": []
        },
        "clavelocalidad": {
            "Descripción": "Clave de la localidad",
            "Valores": [],
            "Etiquetas": []
        },
        "est_dis": {
            "Descripción": "Estrato de diseño",
            "Valores": [],
            "Etiquetas": []
        },
        "upm": {
            "Descripción": "Unidades Primarias de Muestreo",
            "Valores": [],
            "Etiquetas": []
        },
        "ezona": {
            "Descripción": "Entrevistador: evalúa la zona de la entrevista",
            "Valores": [1, 2, 3, 4, 5, 6],
            "Etiquetas": [
                "Tranquilo, con personas en la calle",
                "Tranquilo pero solitario",
                "Inseguro en algunas zonas",
                "Inseguro",
                "Inseguro (confirmado por habitantes)",
                "Inseguro y difícil trabajar"
            ]
        },
        "p01": {
            "Descripción": "Número de personas que viven normalmente en esta vivienda",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            "Etiquetas": []
        },
        "p02": {
            "Descripción": "Personas comparten el mismo gasto para comer",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p03": {
            "Descripción": "Número de hogares con gastos separados para comer",
            "Valores": [1, 2, 3, 4, 5],
            "Etiquetas": []
        },
        "p05": {
            "Descripción": "Edad actual del entrevistado (años cumplidos)",
            "Valores": ["25-64"],
            "Etiquetas": []
        },
        "p06": {
            "Descripción": "Sexo",
            "Valores": [1, 2],
            "Etiquetas": ["Hombre", "Mujer"]
        },
        "p08": {
            "Descripción": "Parentesco con el jefe del hogar",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "Etiquetas": [
                "Jefe(a) del hogar",
                "Cónyuge o pareja",
                "Hijo(a)",
                "Padre o madre",
                "Suegro(a)",
                "Yerno o nuera",
                "Hermano(a)",
                "Otro",
                "Sin parentesco"
            ]
        },
        "p09_1": {
            "Descripción": "Dónde se atiende de salud (1ª mención)",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 98],
            "Etiquetas": [
                "IMSS (IMSS-Oportunidades)",
                "ISSSTE/ISSSTE Estatal",
                "Pemex, Defensa o Marina",
                "Centro SSA",
                "Seguro Popular",
                "Otro servicio público (DIF, etc.)",
                "Clínica/hospital privado",
                "Consultorio farmacia",
                "Se automedica",
                "Otro lugar",
                "No se atiende",
                "NS"
            ]
        },
        "p09_2": {
            "Descripción": "Dónde se atiende de salud (2ª mención)",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 98],
            "Etiquetas": [
                "IMSS (IMSS-Oportunidades)",
                "ISSSTE/ISSSTE Estatal",
                "Pemex, Defensa o Marina",
                "Centro SSA",
                "Seguro Popular",
                "Otro servicio público",
                "Clínica/hospital privado",
                "Consultorio farmacia",
                "Se automedica",
                "Otro lugar",
                "No se atiende",
                "NS"
            ]
        },
        "p09_3": {
            "Descripción": "Dónde se atiende de salud (3ª mención)",
            "Valores": [2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Etiquetas": [
                "ISSSTE/ISSSTE Estatal",
                "Pemex, Defensa o Marina",
                "Centro SSA",
                "Seguro Popular",
                "Otro servicio público",
                "Clínica/hospital privado",
                "Consultorio farmacia",
                "Se automedica",
                "Otro lugar"
            ]
        },
        "p10_1": {
            "Descripción": "Derecho a servicios médicos (1ª respuesta)",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 98],
            "Etiquetas": [
                "IMSS",
                "ISSSTE o ISSSTE estatal",
                "Pemex, Defensa o Marina",
                "Seguro Popular/Nva Generación",
                "IMSS Oportunidades",
                "Seguro privado",
                "Otra institución",
                "No tiene derecho",
                "NS"
            ]
        },
        "p10_2": {
            "Descripción": "Derecho a servicios médicos (2ª respuesta)",
            "Valores": [2, 3, 4, 5, 6, 7],
            "Etiquetas": [
                "ISSSTE o ISSSTE estatal",
                "Pemex, Defensa o Marina",
                "Seguro Popular/Nva Generación",
                "IMSS Oportunidades",
                "Seguro privado",
                "Otra institución"
            ]
        },
        "p10_3": {
            "Descripción": "Derecho a servicios médicos (3ª respuesta)",
            "Valores": [3, 5, 6, 7],
            "Etiquetas": [
                "Pemex, Defensa o Marina",
                "IMSS Oportunidades",
                "Seguro privado",
                "Otra institución"
            ]
        },
        "p11_1": {
            "Descripción": "Cómo obtiene el servicio de salud (1ª mención)",
            "Valores": [1, 2, 3, 4, 5, 6, 7],
            "Etiquetas": [
                "Trabajo",
                "Jubilación/invalidez",
                "Algún familiar en el hogar",
                "Ser estudiante",
                "Contratación personal",
                "Familiar de otro hogar",
                "Programa social"
            ]
        },
        "p11_2": {
            "Descripción": "Cómo obtiene el servicio de salud (2ª mención)",
            "Valores": [1, 2, 3, 5, 6, 7],
            "Etiquetas": [
                "Trabajo",
                "Jubilación/invalidez",
                "Familiar en el hogar",
                "Contratación personal",
                "Familiar de otro hogar",
                "Programa social"
            ]
        },
        "p11_3": {
            "Descripción": "Cómo obtiene el servicio de salud (3ª mención)",
            "Valores": [1, 2, 5, 7],
            "Etiquetas": [
                "Trabajo",
                "Jubilación/invalidez",
                "Contratación personal",
                "Programa social"
            ]
        },
        "p12": {
            "Descripción": "Asiste actualmente a la escuela",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p13": {
            "Descripción": "Último nivel que alcanzó en la escuela",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 97],
            "Etiquetas": [
                "Preescolar",
                "Primaria",
                "Secundaria técnica",
                "Secundaria general",
                "Preparatoria técnica",
                "Preparatoria general",
                "Técnica/comercial c/ secundaria",
                "Técnica/comercial c/ preparatoria",
                "Normal básica",
                "Normal licenciatura",
                "Profesional",
                "Posgrado",
                "Ninguno/no fue"
            ]
        },
        "p13_1": {
            "Descripción": "Obtuvo certificado que acredite ese nivel",
            "Valores": [1, 2, 98],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p14": {
            "Descripción": "Último grado o año que alcanzó",
            "Valores": [0, 1, 2, 3, 4, 5, 6],
            "Etiquetas": []
        },
        "p15": {
            "Descripción": "Situación laboral la semana pasada",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8],
            "Etiquetas": [
                "Trabajó (>=1 hora pagada)",
                "Trabajó sin pago",
                "No trabajó, pero tenía trabajo",
                "Buscó trabajo",
                "Estudiante",
                "Quehaceres del hogar",
                "Jubilado/pensionado",
                "Incapacitado"
            ]
        },
        "p18": {
            "Descripción": "Estado civil",
            "Valores": [1, 2, 3, 4, 5, 6],
            "Etiquetas": [
                "Separado(a)",
                "Divorciado(a)",
                "Viudo(a)",
                "Soltero(a)",
                "Unión libre",
                "Casado(a)"
            ]
        },
        "p19": {
            "Descripción": "Cómo diría que es su salud",
            "Valores": [1, 2, 3, 4, 5],
            "Etiquetas": ["Excelente", "Muy buena", "Buena", "Regular", "Mala"]
        },
        "p20_1": {
            "Descripción": "Estatura (metros)",
            "Valores": [1, 2],  # en la tabla sale 1=17,662 obs y 2=3 obs (raro), lo simplificamos
            "Etiquetas": []
        },
        "p20_2": {
            "Descripción": "Estatura (centímetros)",
            "Valores": ["0-99"],
            "Etiquetas": []
        },
        "p21": {
            "Descripción": "Peso aproximado",
            "Valores": ["36-158"],
            "Etiquetas": []
        },
        "p22": {
            "Descripción": "Figura que se parece a usted (contextura corporal)",
            "Valores": [
                "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R"
            ],
            "Etiquetas": []
        },
        "p23": {
            "Descripción": "Estado en que vivía a los 14 años",
            "Valores": [],
            "Etiquetas": []
        },
        "p23_1": {
            "Descripción": "Municipio/Delegación en que vivía a los 14 años",
            "Valores": [],
            "Etiquetas": []
        },
        "p23_2": {
            "Descripción": "Localidad en que vivía a los 14 años",
            "Valores": [],
            "Etiquetas": []
        },
        "p24": {
            "Descripción": "Percepción del tamaño de la localidad",
            "Valores": [1, 2, 3, 4, 5],
            "Etiquetas": [
                "Metrópoli (>500 mil hab.)",
                "Ciudad grande (100-500 mil)",
                "Ciudad mediana (15-100 mil)",
                "Ciudad chica (2,500-15 mil)",
                "Pueblo (<2,500)"
            ]
        },
        "p25": {
            "Descripción": "Con quién vivía a los 14 años",
            "Valores": [1, 2, 3, 4, 5],
            "Etiquetas": [
                "Con el padre sin la madre",
                "Con la madre sin el padre",
                "Con ambos padres",
                "Con otros parientes (sin padres)",
                "Con personas no parientes (sin padres)"
            ]
        },
        "p26": {
            "Descripción": "Principal sostén económico a los 14 años",
            "Valores": [1, 2, 3, 4, 5],
            "Etiquetas": [
                "Su padre",
                "Su madre",
                "Usted mismo",
                "Otro pariente",
                "Otro no pariente"
            ]
        },
        "p27": {
            "Descripción": "Número de personas en el hogar a los 14 años",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                        11, 12, 13, 14, 15, 16, 17, 18,
                        19, 20],
            "Etiquetas": []
        },
        "p28": {
            "Descripción": "Número de cuartos (contando cocina) a los 14 años",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                        11, 12, 13, 14, 15, 16, 18, 20],
            "Etiquetas": []
        },
        "p28_1": {
            "Descripción": "Número de cuartos usados para dormir a los 14 años",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9,
                        10, 11, 12, 13, 14, 15, 20],
            "Etiquetas": []
        },
        "p29": {
            "Descripción": "Material del piso de la vivienda (14 años)",
            "Valores": [1, 2, 3],
            "Etiquetas": ["Tierra", "Cemento/firme", "Madera/mosaico/otro"]
        },
        "p30_a": {
            "Descripción": "Agua entubada (14 años)",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p30_b": {
            "Descripción": "Electricidad (14 años)",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p30_c": {
            "Descripción": "Baño dentro de la vivienda (14 años)",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p30_d": {
            "Descripción": "Calentador de agua (14 años)",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p30_e": {
            "Descripción": "Servicio doméstico (14 años)",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p31": {
            "Descripción": "Tenencia de la vivienda (14 años)",
            "Valores": [1, 2, 3, 4, 5, 8],
            "Etiquetas": [
                "Rentada",
                "Prestada",
                "Propia",
                "Intestada/en litigio",
                "Otra situación",
                "NS"
            ]
        },
        "p32_a": {
            "Descripción": "Servicios financieros (14 años): cuenta de ahorros",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p32_b": {
            "Descripción": "Servicios financieros (14 años): cuenta bancaria",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p32_c": {
            "Descripción": "Servicios financieros (14 años): tarjeta de crédito",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p32_d": {
            "Descripción": "Servicios financieros (14 años): tarjeta tienda depto.",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_a": {
            "Descripción": "Artículos hogar (14 años): estufa gas/eléctrica",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_b": {
            "Descripción": "Artículos hogar (14 años): lavadora de ropa",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_c": {
            "Descripción": "Artículos hogar (14 años): refrigerador",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_d": {
            "Descripción": "Artículos hogar (14 años): teléfono fijo",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_e": {
            "Descripción": "Artículos hogar (14 años): televisor",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_f": {
            "Descripción": "Artículos hogar (14 años): tostador eléctrico",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_g": {
            "Descripción": "Artículos hogar (14 años): aspiradora",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_h": {
            "Descripción": "Artículos hogar (14 años): televisión por cable",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_i": {
            "Descripción": "Artículos hogar (14 años): horno microondas",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_j": {
            "Descripción": "Artículos hogar (14 años): teléfono celular",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_k": {
            "Descripción": "Artículos hogar (14 años): computadora",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_l": {
            "Descripción": "Artículos hogar (14 años): conexión a internet",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_m": {
            "Descripción": "Artículos hogar (14 años): consola videojuegos",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p33_n": {
            "Descripción": "Artículos hogar (14 años): videocasetera o DVD",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p34_a": {
            "Descripción": "Bienes hogar (14 años): otra casa/departamento",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p34_b": {
            "Descripción": "Bienes hogar (14 años): local comercial",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p34_c": {
            "Descripción": "Bienes hogar (14 años): tierras de labor",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p34_d": {
            "Descripción": "Bienes hogar (14 años): terrenos/predios (no campo)",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p34_e": {
            "Descripción": "Bienes hogar (14 años): automóvil/camioneta",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p34_f": {
            "Descripción": "Bienes hogar (14 años): tractor",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p34_g": {
            "Descripción": "Bienes hogar (14 años): animales de trabajo",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p34_h": {
            "Descripción": "Bienes hogar (14 años): ganado",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p35": {
            "Descripción": "Padre vive actualmente",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p36_11": {
            "Descripción": "Edad del padre cuando murió",
            "Valores": ["14-99"],
            "Etiquetas": []
        },
        "p37_11": {
            "Descripción": "Edad del entrevistado al morir su padre",
            "Valores": ["1-64"],
            "Etiquetas": []
        },
        "p38_11": {
            "Descripción": "Edad actual del padre",
            "Valores": ["35-97"],
            "Etiquetas": []
        },
        "p39": {
            "Descripción": "Padre habla lengua indígena",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p40": {
            "Descripción": "Padre recibe pensión o jubilación",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p41": {
            "Descripción": "Procedencia de la pensión del padre",
            "Valores": [1, 2, 3, 4, 6],
            "Etiquetas": ["IMSS", "ISSSTE", "Otra pública", "Privado", "NS"]
        },
        "p42": {
            "Descripción": "Padre asistió a la escuela",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p43": {
            "Descripción": "Último nivel educativo que alcanzó su padre",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 98],
            "Etiquetas": [
                "Preescolar/kínder",
                "Primaria",
                "Secundaria técnica",
                "Secundaria general",
                "Preparatoria técnica",
                "Preparatoria general",
                "Técnica c/secundaria",
                "Técnica c/preparatoria",
                "Normal básica",
                "Normal licenciatura",
                "Profesional",
                "Posgrado",
                "NS"
            ]
        },
        "p44": {
            "Descripción": "Último grado que alcanzó su padre",
            "Valores": [1, 2, 3, 4, 5, 6],
            "Etiquetas": []
        },
        "p45": {
            "Descripción": "Padre sabe/sabía leer y escribir",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p35m": {
            "Descripción": "Madre vive actualmente",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p36m_11": {
            "Descripción": "Edad de la madre cuando murió",
            "Valores": ["13-99"],
            "Etiquetas": []
        },
        "p37m_11": {
            "Descripción": "Edad del entrevistado al morir su madre",
            "Valores": ["1-64"],
            "Etiquetas": []
        },
        "p38m_11": {
            "Descripción": "Edad actual de la madre",
            "Valores": ["30-97"],
            "Etiquetas": []
        },
        "p39m": {
            "Descripción": "Madre habla lengua indígena",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p40m": {
            "Descripción": "Madre recibe pensión o jubilación",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p41m": {
            "Descripción": "Procedencia de la pensión de la madre",
            "Valores": [1, 2, 3, 4, 5, 6],
            "Etiquetas": [
                "IMSS",
                "ISSSTE",
                "Otra pública",
                "Privado",
                "Por divorcio",
                "NS"
            ]
        },
        "p42m": {
            "Descripción": "Madre asistió a la escuela",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p43m": {
            "Descripción": "Último nivel educativo que alcanzó su madre",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 98],
            "Etiquetas": [
                "Preescolar/kínder",
                "Primaria",
                "Secundaria técnica",
                "Secundaria general",
                "Preparatoria técnica",
                "Preparatoria general",
                "Técnica c/secundaria",
                "Técnica c/preparatoria",
                "Normal básica",
                "Normal licenciatura",
                "Profesional",
                "Posgrado",
                "NS"
            ]
        },
        "p44m": {
            "Descripción": "Último grado que alcanzó su madre",
            "Valores": [1, 2, 3, 4, 5, 6],
            "Etiquetas": []
        },
        "p45m": {
            "Descripción": "Madre sabe/sabía leer y escribir",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p46": {
            "Descripción": "Padre trabajaba (principal ocupación)",
            "Valores": [1, 2, 3, 8],
            "Etiquetas": [
                "Sí",
                "No, pero sí trabajó",
                "No, nunca trabajó",
                "NS"
            ]
        },
        "p47": {
            "Descripción": "Tareas que desempeñaba su padre (texto)",
            "Valores": [],
            "Etiquetas": []
        },
        "p48": {
            "Descripción": "Nombre del oficio de su padre (texto)",
            "Valores": [],
            "Etiquetas": []
        },
        "SINCO1": {
            "Descripción": "Ocupación del padre (cod. SINCO)",
            "Valores": [],
            "Etiquetas": []
        },
        "CIUO1": {
            "Descripción": "Ocupación del padre (cod. CIUO)",
            "Valores": [],
            "Etiquetas": []
        },
        "p49": {
            "Descripción": "Posición del padre en ese trabajo",
            "Valores": [1, 2, 3, 4, 5, 6, 7],
            "Etiquetas": [
                "Empleado privado",
                "Empleado gobierno",
                "Jornalero/peón",
                "Patrón/empleador",
                "Cuenta propia",
                "Trabajador sin pago",
                "NS"
            ]
        },
        "p50": {
            "Descripción": "Padre tenía personal a su cargo",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p51": {
            "Descripción": "Num personas laboraban con su padre",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8],
            "Etiquetas": [
                "0 (era único)",
                "1 persona",
                "2-5",
                "6-9",
                "10-14",
                "15-49",
                "50+",
                "NS"
            ]
        },
        "p52": {
            "Descripción": "Padre estaba asegurado/afiliado a...",
            "Valores": [1, 2, 3, 4, 5, 8],
            "Etiquetas": [
                "IMSS",
                "ISSSTE",
                "Otra institución pública",
                "Institución privada",
                "No afiliado",
                "NS"
            ]
        },
        "p53": {
            "Descripción": "Madre trabajaba (principal actividad)",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "Etiquetas": [
                "Trabajaba",
                "Ayudaba negocio familiar/no familiar",
                "Vendía algún producto",
                "Ayudaba en el campo",
                "Trabajo a cambio de pago en especie",
                "No trabajaba, pero sí trabajó",
                "Nunca trabajó",
                "NS",
                "Ya había fallecido"
            ]
        },
        "p54": {
            "Descripción": "Tareas que desempeñaba su madre (texto)",
            "Valores": [],
            "Etiquetas": []
        },
        "p55": {
            "Descripción": "Oficio, puesto o cargo de su madre (texto)",
            "Valores": [],
            "Etiquetas": []
        },
        "SINCO2": {
            "Descripción": "Ocupación de la madre (cod. SINCO)",
            "Valores": [],
            "Etiquetas": []
        },
        "CIUO2": {
            "Descripción": "Ocupación de la madre (cod. CIUO)",
            "Valores": [],
            "Etiquetas": []
        },
        "p56": {
            "Descripción": "Posición de la madre en su trabajo",
            "Valores": [1, 2, 3, 4, 5, 6, 8],
            "Etiquetas": [
                "Empleado privado",
                "Empleado gobierno",
                "Jornalero/peón",
                "Patrón/empleador",
                "Cuenta propia",
                "Trabajador sin pago",
                "NS"
            ]
        },
        "p57": {
            "Descripción": "Madre tenía personal a su cargo",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p58": {
            "Descripción": "Num personas laboraban con su madre",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8],
            "Etiquetas": [
                "0 (único)",
                "1 persona",
                "2-5",
                "6-9",
                "10-14",
                "15-49",
                "50+",
                "NS"
            ]
        },
        "p59": {
            "Descripción": "Madre estaba asegurada/afiliada",
            "Valores": [1, 2, 3, 4, 5, 8],
            "Etiquetas": [
                "IMSS",
                "ISSSTE",
                "Otra pública",
                "Privada",
                "No afiliada",
                "NS"
            ]
        },
        "p60": {
            "Descripción": "Número de hijos(as) vivos(as) que tuvo su madre",
            "Valores": [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                11, 12, 13, 14, 15, 16, 17, 18,
                19, 20, 21, 22, 24
            ],
            "Etiquetas": []
        },
        "p61": {
            "Descripción": "Orden de nacimiento del entrevistado",
            "Valores": [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                11, 12, 13, 14, 15, 16, 17, 18,
                19, 20, 21, 22, 23
            ],
            "Etiquetas": []
        },
        "p62a": {
            "Descripción": "Alumbrado público a los 14 años",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p62b": {
            "Descripción": "Escuelas/bibliotecas públicas cercanas (14 años)",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p62c": {
            "Descripción": "Centros de salud cercanos (14 años)",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p62d": {
            "Descripción": "Lugares de esparcimiento cercanos (14 años)",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },


        "p62e": {
            "Descripción": "Servicios 14 años: seguridad en la colonia",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p62f": {
            "Descripción": "Servicios 14 años: facilidad para transportarse",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p62g": {
            "Descripción": "Servicios 14 años: limpieza en las calles",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p62h": {
            "Descripción": "Servicios 14 años: venta de alcohol clandestinos",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p62i": {
            "Descripción": "Servicios 14 años: terrenos/casas abandonadas",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p63a": {
            "Descripción": "Escuelas privadas/publicas: primaria",
            "Valores": [1, 2, 3, 4, 8],
            "Etiquetas": [
                "Siempre privadas",
                "Mayoritariamente privadas",
                "Mayoritariamente públicas",
                "Siempre públicas",
                "No aplica"
            ]
        },
        "p63b": {
            "Descripción": "Sondeo si fue secundaria general o secundaria técnica",
            "Valores": [1, 2],
            "Etiquetas": ["General", "Técnica"]
        },
        "p63b_1": {
            "Descripción": "Escuelas privadas/publicas: secundaria general",
            "Valores": [1, 2, 3, 4, 8],
            "Etiquetas": [
                "Siempre privadas",
                "Mayoritariamente privadas",
                "Mayoritariamente públicas",
                "Siempre públicas",
                "No aplica"
            ]
        },
        "p63b_2": {
            "Descripción": "Escuelas privadas/publicas: secundaria técnica",
            "Valores": [1, 2, 3, 4, 8],
            "Etiquetas": [
                "Siempre privadas",
                "Mayoritariamente privadas",
                "Mayoritariamente públicas",
                "Siempre públicas",
                "No aplica"
            ]
        },
        "p63c": {
            "Descripción": "Sondeo si fue preparatoria general o preparatoria técnica",
            "Valores": [1, 2],
            "Etiquetas": ["Técnica", "General"]
        },
        "p63c_1": {
            "Descripción": "Escuelas privadas/publicas: preparatoria técnica",
            "Valores": [1, 2, 3, 4, 8],
            "Etiquetas": [
                "Siempre privadas",
                "Mayoritariamente privadas",
                "Mayoritariamente públicas",
                "Siempre públicas",
                "No aplica"
            ]
        },
        "p63c_2": {
            "Descripción": "Escuelas privadas/publicas: preparatoria general",
            "Valores": [1, 2, 3, 4, 8],
            "Etiquetas": [
                "Siempre privadas",
                "Mayoritariamente privadas",
                "Mayoritariamente públicas",
                "Siempre públicas",
                "No aplica"
            ]
        },
        "p63d": {
            "Descripción": "Escuelas privadas/publicas: universidad",
            "Valores": [1, 2, 3, 4, 8],
            "Etiquetas": [
                "Siempre privadas",
                "Mayoritariamente privadas",
                "Mayoritariamente públicas",
                "Siempre públicas",
                "No aplica"
            ]
        },
        "p64": {
            "Descripción": "Edad que dejó de asistir a la escuela",
            "Valores": list(range(4, 65)),
            "Etiquetas": []
        },
        "p65": {
            "Descripción": "Cuando dejó de estudiar, ¿quién tomó la decisión?",
            "Valores": [1, 2, 3, 4],
            "Etiquetas": [
                "Su padre o madre",
                "Su pareja o novio",
                "Usted mismo",
                "Otra persona"
            ]
        },
        "p65_41": {
            "Descripción": "Cuando dejó de estudiar, ¿quién tomó la decisión? Otro",
            "Valores": [1, 2, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 96, 99],
            "Etiquetas": [
                "Su padre o madre",
                "Su pareja o novio",
                "Hermano (a)",
                "Tío (a)",
                "Abuelo (a)",
                "Padrastro o madrastra",
                "Padrino o madrina",
                "Amigos o conocidos",
                "Director / Maestros",
                "No asistían los maestros",
                "Fue expulsado(a)",
                "No había escuela / Estaba lejos",
                "Se enfermó",
                "Falta de recursos",
                "No tenía documentos",
                "VERIFICAR FILTROS DESDE P12",
                "No contestó"
            ]
        },
        "p66": {
            "Descripción": "¿Estuvo de acuerdo con esa decisión?",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p67": {
            "Descripción": "Motivo principal por el que no continuó estudiando",
            "Valores": list(range(1, 14)),
            "Etiquetas": [
                "Mi familia no me apoyó para continuar",
                "Formé una pareja, me casé o tuve un hijo",
                "Me dediqué a las tareas del hogar",
                "Ya había cumplido mi meta educativa",
                "Emigré y no continué estudiando",
                "El trabajo no me permitió continuar",
                "No me gustaba estudiar",
                "Me faltaban recursos económicos",
                "La escuela me quedaba lejos",
                "Tenía un rendimiento muy bajo en la escuela",
                "Tuve un mal resultado en un examen de admisión",
                "Tenía promedio insuficiente para continuar",
                "Otra razón"
            ]
        },
        "p68": {
            "Descripción": "¿La semana pasada trabajó por lo menos una hora?",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p69": {
            "Descripción": "¿Tiene algún empleo del que estuvo ausente?",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p70": {
            "Descripción": "¿Usted ha tratado de…?",
            "Valores": [1, 2, 3],
            "Etiquetas": [
                "Buscar trabajo durante los últimos tres meses",
                "Poner un negocio o realizar una actividad por cuenta propia",
                "¿No ha tratado de buscar trabajo?"
            ]
        },
        "p71": {
            "Descripción": "¿Usted es…?",
            "Valores": [1, 2, 3, 4, 6],
            "Etiquetas": [
                "Pensionado o jubilado de su empleo",
                "Estudiante",
                "Una persona que se dedica a los quehaceres del hogar",
                "Una persona con alguna limitación física",
                "Otra condición"
            ]
        },
        "p71_61": {
            "Descripción": "¿Usted es…? Otra codificado",
            "Valores": list(range(1, 19)) + [96, 97],
            "Etiquetas": [
                "Pensionado o jubilado de su empleo",
                "Estudiante",
                "Persona que se dedica a los quehaceres del hogar",
                "Persona con limitación física o mental",
                "Por su edad",
                "Tiene problemas de salud",
                "Cuida a sus hijos, padres, hermanos por",
                "Embarazada",
                "Desempleado",
                "No necesita trabajar",
                "Quiere descansar",
                "Recibe ayuda de hijos o familiares",
                "Recibe pensión por viudez",
                "Es extranjero, recibe dinero de EUA",
                "Recibe apoyo de Programa Social",
                "Razones personales",
                "Realiza otras actividades",
                "Corregir P69, 70 u otra / no respetó el",
                "Insuficientemente especificado",
                "No contestó"
            ]
        },
        "p72": {
            "Descripción": "Usted tiene necesidad de trabajar",
            "Valores": [1, 2, 3],
            "Etiquetas": [
                "Sí tiene necesidad de trabajar",
                "Solo tiene deseos de trabajar",
                "No tiene necesidad ni deseos de trabajar"
            ]
        },
        "p73_1": {
            "Descripción": "Alguna otra razón, por la que usted no esté buscando trabajo",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 99],
            "Etiquetas": [
                "Esperando respuesta a una solicitud",
                "No hay trabajo en su especialidad, oficio",
                "No cuenta con escolaridad, papeles o experiencia",
                "Piensa que por su edad o por su aspecto",
                "En su localidad no hay trabajo o solo sea",
                "La inseguridad pública o el exceso de tiempo",
                "Espera recuperarse de una enfermedad o",
                "Está embarazada",
                "No tiene quién cuide a sus hijos pequeños",
                "No lo(a) deja un familiar",
                "Otras razones de mercado",
                "Otras razones personales",
                "No"
            ]
        },
        "p74": {
            "Descripción": "¿Ha trabajado por pago alguna vez en su vida?",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p75": {
            "Descripción": "Tareas que desempeña en su trabajo",
            "Valores": [],
            "Etiquetas": []
        },
        "p76": {
            "Descripción": "Nombre del oficio que tiene su pareja en su trabajo",
            "Valores": [],
            "Etiquetas": []
        },
        "SINCO5": {
            "Descripción": "Codificación ocupación pareja entrevistado, SINCO",
            "Valores": list(range(1, 7)) + [99],
            "Etiquetas": [
                "Véase catálogo INEGI"
            ]
        },
        "CIUO5": {
            "Descripción": "Codificación ocupación pareja entrevistado, CIUO",
            "Valores": list(range(1, 7)) + [99],
            "Etiquetas": [
                "Véase catálogo INEGI"
            ]
        },
        "p138": {
            "Descripción": "En su trabajo principal, ¿su pareja es …?",
            "Valores": [1, 2, 3, 4, 5, 6],
            "Etiquetas": [
                "Empleado u obrero del sector privado",
                "Empleado en el gobierno",
                "Jornalero o peón",
                "Patrón o empleador",
                "Trabajador por cuenta propia",
                "Trabajador sin pago"
            ]
        },
        "p139": {
            "Descripción": "Su pareja tiene personal a su cargo en ese trabajo",
            "Valores": [1, 2, 8],
            "Etiquetas": ["Sí", "No", "NS"]
        },
        "p140": {
            "Descripción": "Número de personas que laboran donde su pareja trabaja",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8],
            "Etiquetas": [
                "Ninguna, era trabajador único",
                "Una persona",
                "De 2 a 5 personas",
                "De 6 a 9 personas",
                "De 10 a 14 personas",
                "De 15 a 49 personas",
                "50 personas o más",
                "NS"
            ]
        },
        "p141": {
            "Descripción": "¿Tuvo usted otra unión o matrimonio?",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p142": {
            "Descripción": "Edad en que comenzó a vivir en pareja por primera vez",
            "Valores": list(range(12, 61)),
            "Etiquetas": []
        },
        "p143": {
            "Descripción": "Número de hijas e hijos nacidos(as) vivos(as)",
            "Valores": list(range(1, 10)),
            "Etiquetas": []
        },
        "p144": {
            "Descripción": "Qué edad tenía Usted cuando nació su primer hijo",
            "Valores": list(range(12, 62)),
            "Etiquetas": []
        },
        "p145": {
            "Descripción": "Falleció alguno de sus hijos antes de los 5 años",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p146": {
            "Descripción": "Edad falleció hijos menores 5 años",
            "Valores": [1, 2, 3, 4, 66, 77],
            "Etiquetas": []
        },
        "p147": {
            "Descripción": "Dónde pondría usted su hogar",
            "Valores": list(range(1, 11)),
            "Etiquetas": []
        },
        "p148": {
            "Descripción": "14 años, dónde pondría usted su hogar de ese entonces",
            "Valores": list(range(1, 11)),
            "Etiquetas": []
        },
        "p149": {
            "Descripción": "A quién debería privilegiarse, al hijo o a la hija",
            "Valores": [1, 2, 3],
            "Etiquetas": ["Hijo", "Hija", "Ambos"]
        },
        "p150a": {
            "Descripción": "Discriminación: por no tener dinero",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p150a_1": {
            "Descripción": "Discriminación, donde: Trabajo",
            "Valores": [1],
            "Etiquetas": []
        },
        "p150a_2": {
            "Descripción": "Discriminación, donde: Escuela",
            "Valores": [2],
            "Etiquetas": []
        },
        "p150a_3": {
            "Descripción": "Discriminación, donde: Oficina pública",
            "Valores": [3],
            "Etiquetas": []
        },
        "p150a_4": {
            "Descripción": "Discriminación, donde: Hogar",
            "Valores": [4],
            "Etiquetas": []
        },
        "p150a_5": {
            "Descripción": "Discriminación, donde: Barrio, colonia",
            "Valores": [5],
            "Etiquetas": []
        },
        "p150a_6": {
            "Descripción": "Discriminación, donde: Otro",
            "Valores": [6],
            "Etiquetas": []
        },
        "p150b": {
            "Descripción": "Discriminación: por su apariencia física",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p150b_1": {
            "Descripción": "Discriminación, donde: Trabajo",
            "Valores": [1],
            "Etiquetas": []
        },
        "p150b_2": {
            "Descripción": "Discriminación, donde: Escuela",
            "Valores": [2],
            "Etiquetas": []
        },
        "p150b_3": {
            "Descripción": "Discriminación, donde: Oficina pública",
            "Valores": [3],
            "Etiquetas": []
        },
        "p150b_4": {
            "Descripción": "Discriminación, donde: Hogar",
            "Valores": [4],
            "Etiquetas": []
        },
        "p150b_5": {
            "Descripción": "Discriminación, donde: Barrio, colonia",
            "Valores": [5],
            "Etiquetas": []
        },
        "p150b_6": {
            "Descripción": "Discriminación, donde: Otro",
            "Valores": [6],
            "Etiquetas": []
        },
        "p150c": {
            "Descripción": "Discriminación: por su edad",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p150c_1": {
            "Descripción": "Discriminación, donde: Trabajo",
            "Valores": [1],
            "Etiquetas": []
        },
        "p150c_2": {
            "Descripción": "Discriminación, donde: Escuela",
            "Valores": [2],
            "Etiquetas": []
        },
        "p150c_3": {
            "Descripción": "Discriminación, donde: Oficina pública",
            "Valores": [3],
            "Etiquetas": []
        },
        "p150c_4": {
            "Descripción": "Discriminación, donde: Hogar",
            "Valores": [4],
            "Etiquetas": []
        },
        "p150c_5": {
            "Descripción": "Discriminación, donde: Barrio, colonia",
            "Valores": [5],
            "Etiquetas": []
        },
        "p150c_6": {
            "Descripción": "Discriminación, donde: Otro",
            "Valores": [6],
            "Etiquetas": []
        },
        "p150d": {
            "Descripción": "Discriminación: por ser hombre/ser mujer",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p150d_1": {
            "Descripción": "Discriminación, donde: Trabajo",
            "Valores": [1],
            "Etiquetas": []
        },
        "p150d_2": {
            "Descripción": "Discriminación, donde: Escuela",
            "Valores": [2],
            "Etiquetas": []
        },
        "p150d_3": {
            "Descripción": "Discriminación, donde: Oficina pública",
            "Valores": [3],
            "Etiquetas": []
        },
        "p150d_4": {
            "Descripción": "Discriminación, donde: Hogar",
            "Valores": [4],
            "Etiquetas": []
        },
        "p150d_5": {
            "Descripción": "Discriminación, donde: Barrio, colonia",
            "Valores": [5],
            "Etiquetas": []
        },
        "p150d_6": {
            "Descripción": "Discriminación, donde: Otro",
            "Valores": [6],
            "Etiquetas": []
        },
        "p150e": {
            "Descripción": "Discriminación: por su color de piel",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p150e_1": {
            "Descripción": "Discriminación, donde: Trabajo",
            "Valores": [1],
            "Etiquetas": []
        },
        "p150e_2": {
            "Descripción": "Discriminación, donde: Escuela",
            "Valores": [2],
            "Etiquetas": []
        },
        "p150e_3": {
            "Descripción": "Discriminación, donde: Oficina pública",
            "Valores": [3],
            "Etiquetas": []
        },
        "p150e_4": {
            "Descripción": "Discriminación, donde: Hogar",
            "Valores": [4],
            "Etiquetas": []
        },
        "p150e_5": {
            "Descripción": "Discriminación, donde: Barrio, colonia",
            "Valores": [5],
            "Etiquetas": []
        },
        "p150e_6": {
            "Descripción": "Discriminación, donde: Otro",
            "Valores": [6],
            "Etiquetas": []
        },
        "p150f": {
            "Descripción": "Discriminación: otro",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p150f_11": {
            "Descripción": "Discriminación: otro",
            "Valores": [1, 2, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 97, 99],
            "Etiquetas": [
                "No tener dinero",
                "Su apariencia física",
                "Su edad",
                "Ser hombre/ser mujer",
                "Su color de piel",
                "Discapacidad / enfermedad / problemas de salud",
                "Embarazo",
                "Orientación sexual",
                "Ser indígena",
                "Adicciones (alcoholismo, drogadicción)",
                "Lugar de origen (no indígena)",
                "Religión / culto",
                "Analfabetismo / nivel de estudios",
                "Opinión / ideología / forma de pensar",
                "Carácter",
                "Lengua / idioma / forma de hablar",
                "Bulling",
                "Haber estado preso(a)",
                "Burocracia / ineficiencia de servidores",
                "Otros",
                "Insuficientemente especificado",
                "No contestó"
            ]
        },
        "p150f_1": {
            "Descripción": "Discriminación, donde: Trabajo",
            "Valores": [1],
            "Etiquetas": []
        },
        "p150f_2": {
            "Descripción": "Discriminación, donde: Escuela",
            "Valores": [2],
            "Etiquetas": []
        },
        "p150f_3": {
            "Descripción": "Discriminación, donde: Oficina pública",
            "Valores": [3],
            "Etiquetas": []
        },
        "p150f_4": {
            "Descripción": "Discriminación, donde: Hogar",
            "Valores": [4],
            "Etiquetas": []
        },
        "p150f_5": {
            "Descripción": "Discriminación, donde: Barrio, colonia",
            "Valores": [5],
            "Etiquetas": []
        },
        "p150f_6": {
            "Descripción": "Discriminación, donde: Otro",
            "Valores": [6],
            "Etiquetas": []
        },
        "p151": {
            "Descripción": "¿Cuál considera que es el color de piel de su cara?",
            "Valores": list(range(1, 12)),
            "Etiquetas": ["⬛A", "B", "👍🏿C", "D", "👍🏾E", "👍🏽F", "G", "👍🏼H", "I", "👍🏻J", "⬜K"]
        },
        "region": {
            "Descripción": "Región del país",
            "Valores": [1, 2, 3, 4, 5],
            "Etiquetas": ["Norte", "Norte-occidente", "Centro-norte", "Centro", "Sur"]
        },
        "cdmx": {
            "Descripción": "Ciudad de México",
            "Valores": [1],
            "Etiquetas": []
        },
        "rururb": {
            "Descripción": "Localidades rurales y urbanas - ITER 2010",
            "Valores": [0, 1],
            "Etiquetas": ["Urbano", "Rural"]
        },
        "cmo1_2": {
            "Descripción": "CMO1 dos posiciones del padre",
            "Valores": [11, 12, 13, 14, 21, 41, 51, 52, 53, 54, 55, 61, 62, 71, 72, 81, 82, 83, 99],
            "Etiquetas": [
                # Asumiendo que cada código tiene una etiqueta específica
                "Etiqueta correspondiente a cada código"
            ]
        },
        "cmo2_2": {
            "Descripción": "CMO1 dos posiciones de la madre",
            "Valores": [11, 12, 13, 14, 21, 41, 51, 52, 53, 54, 55, 61, 62, 71, 72, 81, 82, 83, 99],
            "Etiquetas": [
                "Etiqueta correspondiente a cada código"
            ]
        },
        "cmo3_2": {
            "Descripción": "CMO1 dos posiciones entrevistado",
            "Valores": [11, 12, 13, 14, 21, 41, 51, 52, 53, 54, 55, 61, 62, 71, 72, 81, 82, 83, 99],
            "Etiquetas": [
                "Etiqueta correspondiente a cada código"
            ]
        },
        "cmo4_2": {
            "Descripción": "CMO1 dos posiciones primera ocupación del entrevistado",
            "Valores": [11, 12, 13, 14, 21, 41, 51, 52, 53, 54, 55, 61, 62, 71, 72, 81, 82, 83, 99],
            "Etiquetas": [
                "Etiqueta correspondiente a cada código"
            ]
        },
        "cmo5_2": {
            "Descripción": "CMO1 dos posiciones pareja del entrevistado",
            "Valores": [11, 12, 13, 14, 21, 41, 51, 52, 53, 54, 55, 61, 62, 71, 72, 81, 82, 83, 99],
            "Etiquetas": [
                "Etiqueta correspondiente a cada código"
            ]
        },

        "p26_41": {
            "Descripción": "Principal sostenedor económico a 14 años, pariente, cod",
            "Valores": [3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 21, 22, 96, 97],
            "Etiquetas": [
                "Usted mismo",
                "Hermano (a)",
                "Ambos (padre y madre)",
                "Tío (a)",
                "Abuelo (a)",
                "Cónyuge o pareja",
                "Suegro(a)",
                "Cuñado(a)",
                "Primo(a)",
                "Padrastro o madrastra",
                "Sobrino(a)",
                "Padre adoptivo",
                "Amigos o conocidos",
                "Padrino o madrina",
                "Vecino",
                "96",
                "Insuficientemente especificado"
            ]
        },
        "p26_51": {
            "Descripción": "Principal sostenedor económico a 14 años, no pariente, cod",
            "Valores": [6, 7, 8, 9, 10, 12, 13, 14, 16, 20, 21, 22, 24, 25, 26, 27, 97],
            "Etiquetas": [
                "Hermano (a)",
                "Ambos (padre y madre)",
                "Tío (a)",
                "Abuelo (a)",
                "Cónyuge o pareja",
                "Cuñado(a)",
                "Primo(a)",
                "Padrastro o madrastra",
                "Padre adoptivo",
                "Amigos o conocidos",
                "Padrino o madrina",
                "Vecino",
                "Patrones / Jefes",
                "Tutor",
                "Internado / Casa Hogar / Iglesia",
                "Desconocido",
                "Insuficientemente especificado"
            ]
        },
        "p31_51": {
            "Descripción": "Tenencia de la vivienda, otra codificada",
            "Valores": [3, 6, 7, 8, 9, 10, 11],
            "Etiquetas": [
                "Propia",
                "De familiares",
                "Propia, la estaban pagando",
                "Internado / Casa Hogar",
                "Invadida / posesión",
                "Propiedad del lugar donde trabaja",
                "Vivía en la calle / en cualquier lugar"
            ]
        },
        "SINCO3": {
            "Descripción": "Codificación ocupación pareja entrevistado, SINCO",
            "Valores": [],
            "Etiquetas": []
        },
        "CIUO3": {
            "Descripción": "Codificación ocupación pareja entrevistado, CIUO",
            "Valores": [],
            "Etiquetas": []
        },
        "p77": {
            "Descripción": "Posición en el trabajo",
            "Valores": [1, 2, 3, 4, 5, 6],
            "Etiquetas": [
                "Empleado u obrero del sector privado",
                "Empleado en el gobierno",
                "Jornalero o peón",
                "Patrón o empleador",
                "Trabajador por cuenta propia",
                "Trabajador sin pago"
            ]
        },
        "p78": {
            "Descripción": "Tiene personal a su cargo en su trabajo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p79": {
            "Descripción": "Num personas que están a su cargo",
            "Valores": [],
            "Etiquetas": []
        },
        "p80": {
            "Descripción": "A que se dedica la empresa donde usted trabaja",
            "Valores": [],
            "Etiquetas": []
        },
        "SCIAN3": {
            "Descripción": "A que se dedica la empresa donde usted trabaja, codificación SCIAN",
            "Valores": [],
            "Etiquetas": []
        },
        "p81": {
            "Descripción": "Num personas donde usted trabaja",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 98],
            "Etiquetas": [
                "1 persona",
                "De 2 a 5 personas",
                "De 6 a 10 personas",
                "De 11 a 15 personas",
                "De 16 a 20 personas",
                "De 21 a 30 personas",
                "De 31 a 50 personas",
                "De 51 a 100 personas",
                "De 101 a 250 personas",
                "De 251 a 500 personas",
                "501 y más personas",
                "NS"
            ]
        },
        "p82": {
            "Descripción": "Esta asegurado o afiliado al",
            "Valores": [1, 2, 3, 4, 5, 8],
            "Etiquetas": [
                "IMSS",
                "ISSSTE",
                "Otra institución de seguridad social",
                "Una institución privada",
                "No está afiliado o asegurado",
                "NS"
            ]
        },
        "p83": {
            "Descripción": "Cuenta con un contrato por escrito",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p84": {
            "Descripción": "Tipo de contrato",
            "Valores": [1, 2, 3, 4, 5],
            "Etiquetas": [
                "Es temporal o por obra determinada",
                "Es de base, planta o por tiempo indeterminado",
                "Por capacitación inicial",
                "Por periodo de prueba",
                "Hasta el término de la obra"
            ]
        },
        "p85_1": {
            "Descripción": "Prestaciones primer empleo: Aguinaldo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p85_2": {
            "Descripción": "Prestaciones primer empleo: Vacaciones con goce de sueldo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p85_3": {
            "Descripción": "Prestaciones primer empleo: Reparto de utilidades",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p85_4": {
            "Descripción": "Prestaciones primer empleo: Crédito de vivienda",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p85_5": {
            "Descripción": "Prestaciones primer empleo: Préstamos personales",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p85_6": {
            "Descripción": "Prestaciones primer empleo: Guarderías y/o estancias infantiles",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p85_7": {
            "Descripción": "Prestaciones primer empleo: Ahorro para el retiro",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p85_8": {
            "Descripción": "Prestaciones primer empleo: Seguro privado para gastos médicos",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p85_9": {
            "Descripción": "Prestaciones primer empleo: Otras prestaciones",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p85_9_1": {
            "Descripción": "Prestaciones primer empleo: Otras prestaciones, especificar",
            "Valores": [5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 97, 98, 99],
            "Etiquetas": [
                "Préstamos personales y/o caja de ahorro",
                "Ahorro para el retiro",
                "Seguro privado para gastos médicos",
                "Ninguna",
                "Comisiones",
                "Bono de productividad / Puntualidad",
                "Seguro de vida",
                "Vales de despensa",
                "Ayuda cuando se enferma",
                "Seguridad social (IMSS)",
                "Liquidación",
                "Ayuda por defunción",
                "Dinero",
                "Transporte",
                "Insuficientemente especificado",
                "No sabe",
                "No contestó"
            ]
        },
        "p85_10": {
            "Descripción": "Ninguna",
            "Valores": [10],
            "Etiquetas": ["Ninguna"]
        },
        "p86": {
            "Descripción": "Num horas trabaja a la semana",
            "Valores": [],
            "Etiquetas": []
        },
        "p87": {
            "Descripción": "Año en que empezó a trabajar en esta actividad",
            "Valores": [],
            "Etiquetas": []
        },
        "p88": {
            "Descripción": "Ha tratado de buscar un nuevo trabajo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p89": {
            "Descripción": "Motivo principal por el que está buscando otro trabajo",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8],
            "Etiquetas": [
                "Mejorar sus ingresos/salario trabajando",
                "Contar con seguridad social (IMSS, ISSS)",
                "Mejorar sus condiciones de trabajo",
                "Tener un trabajo acorde a su escolaridad",
                "Tener un trabajo independiente",
                "Tener tiempo para atender o convivir con...",
                "Teme quedarse sin su actual trabajo",
                "Otro"
            ]
        },
        "p89_11": {
            "Descripción": "Motivo principal por el que está buscando otro trabajo, Otro cod",
            "Valores": [1, 2, 3, 7, 9, 10, 11, 12, 97],
            "Etiquetas": [
                "Mejorar sus ingresos/salario trabajando",
                "Contar con seguridad social (IMSS, ISSS)",
                "Mejorar sus condiciones de trabajo",
                "Teme quedarse sin su actual trabajo",
                "Estabilidad laboral",
                "Ser productivo / Tener algo qué hacer",
                "Mejorar ambiente de trabajo",
                "Por la edad",
                "Insuficientemente especificado"
            ]
        },
        "p90": {
            "Descripción": "Num trabajos que ha tenido, incluyendo el actual",
            "Valores": [],
            "Etiquetas": []
        },
        "p91": {
            "Descripción": "Usted se quedó sin trabajo y tuvo que buscar otro",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p92": {
            "Descripción": "Num veces ha estado sin trabajar por más de 6 meses",
            "Valores": [],
            "Etiquetas": []
        },
        "p93": {
            "Descripción": "Última vez que se quedó sin trabajo, situación",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8],
            "Etiquetas": [
                "Perdió o terminó su empleo",
                "Renunció a su empleo",
                "Cerró o dejó un negocio propio",
                "Se pensionó, jubiló o se retiró de su empleo",
                "Lo detuvieron o se enfermó por una larga enfermedad",
                "Regresó o lo deportaron de Estados Unidos",
                "Un fenómeno natural o siniestro afectó",
                "Ninguna de las anteriores"
            ]
        },
        "p94": {
            "Descripción": "Situación por la que se quedó sin trabajo",
            "Valores": [1, 2, 3, 4, 5, 6, 7],
            "Etiquetas": [
                "La fuente de empleo cerró o quebró",
                "Hubo recorte de personal",
                "La empresa se cambió de ciudad o de país",
                "No le renovaron su contrato",
                "No lo volvieron a llamar",
                "Lo despidieron",
                "Ninguna de las anteriores"
            ]
        },
        "p95": {
            "Descripción": "Cuál fue el motivo principal",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Etiquetas": [
                "Conflicto laboral y/o sindical",
                "Conflicto con su jefe o superior",
                "Falta de calificación o capacitación",
                "Ya no hubo más trabajo",
                "Incumplimiento con la empresa",
                "Discriminación por su aspecto físico",
                "La edad (joven o viejo)",
                "Enfermedad o discapacidad",
                "Embarazo y/o responsabilidades maternas",
                "Ninguno de los anteriores"
            ]
        },
        "p96": {
            "Descripción": "Cuál fue el motivo principal",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "Etiquetas": [
                "Quería ganar más",
                "Quería independizarse",
                "Cambio o deterioro en las condiciones de trabajo",
                "El trabajo era riesgoso y/o insalubre",
                "Lo forzaron a renunciar o a pensionarse",
                "Falta de oportunidades para superarse",
                "Acoso o falta de respeto a su persona",
                "Conflicto con su jefe o superior",
                "Matrimonio, embarazo y/o responsabilidad",
                "Un familiar le impidió seguir trabajando",
                "Quería seguir estudiando",
                "Ninguno de los anteriores"
            ]
        },
        "p97": {
            "Descripción": "Ha recibido capacitación laboral",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p97_11": {
            "Descripción": "Ha recibido capacitación laboral: Num veces",
            "Valores": [],
            "Etiquetas": []
        },
        "p98": {
            "Descripción": "Edad a la que tuvo usted su primer trabajo",
            "Valores": [],
            "Etiquetas": []
        },
        "p99": {
            "Descripción": "Último nivel y grado en la escuela al primer trabajo",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "Etiquetas": [
                "Preescolar o kínder",
                "Primaria",
                "Secundaria técnica",
                "Secundaria general",
                "Preparatoria técnica",
                "Preparatoria general",
                "Técnica o comercial con secundaria",
                "Técnica o comercial con preparatoria",
                "Normal básica (con primaria o secundaria)",
                "Normal de licenciatura",
                "Profesional (licenciatura o ingeniería)",
                "Postgrado (maestría o doctorado)"
            ]
        },
        "p99a": {
            "Descripción": "Año o grado",
            "Valores": [1, 2, 3, 4, 5, 6],
            "Etiquetas": []
        },
        "p100": {
            "Descripción": "Tareas que usted desempeñaba en su primer trabajo",
            "Valores": [],
            "Etiquetas": []
        },
        "p101": {
            "Descripción": "Nombre del oficio, puesto o cargo en ese trabajo",
            "Valores": [],
            "Etiquetas": []
        },
        "SINCO4": {
            "Descripción": "Codificación ocupación del primer trabajo entrevistado, SINCO4",
            "Valores": [],
            "Etiquetas": []
        },
        "CIUO4": {
            "Descripción": "Codificación ocupación del primer trabajo entrevistado, CIUO4",
            "Valores": [],
            "Etiquetas": []
        },
        "p102": {
            "Descripción": "Posición en su primer trabajo",
            "Valores": [1, 2, 3, 4, 5, 6],
            "Etiquetas": [
                "Empleado u obrero del sector privado",
                "Empleado en el gobierno",
                "Jornalero o peón",
                "Patrón o empleador",
                "Trabajador por cuenta propia",
                "Trabajador sin pago"
            ]
        },
        "p103": {
            "Descripción": "Tenía personal a su cargo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p104": {
            "Descripción": "Num personas que estaban a su cargo",
            "Valores": [],
            "Etiquetas": []
        },
        "p105": {
            "Descripción": "A que se dedicaba la empresa, el servicio o negocio",
            "Valores": [],
            "Etiquetas": []
        },
        "SCIAN4": {
            "Descripción": "A que se dedicaba la empresa, el servicio o negocio, codificación SCIAN4",
            "Valores": [],
            "Etiquetas": []
        },
        "p106": {
            "Descripción": "Num personas que laboraban en su primer trabajo",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "Etiquetas": [
                "1 persona",
                "De 2 a 5 personas",
                "De 6 a 10 personas",
                "De 11 a 15 personas",
                "De 16 a 20 personas",
                "De 21 a 30 personas",
                "De 31 a 50 personas",
                "De 51 a 100 personas",
                "De 101 a 250 personas",
                "De 251 a 500 personas",
                "501 y más personas",
                "NS"
            ]
        },
        "p107": {
            "Descripción": "Estaba asegurado o afiliado al",
            "Valores": [1, 2, 3, 4, 5, 8],
            "Etiquetas": [
                "IMSS",
                "ISSSTE",
                "Otra institución de seguridad social",
                "Una institución privada",
                "No estuvo afiliado o asegurado",
                "NS"
            ]
        },
        "p108": {
            "Descripción": "Contaba con un contrato por escrito",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p109": {
            "Descripción": "Tipo de contrato de su primer trabajo",
            "Valores": [1, 2],
            "Etiquetas": [
                "Fue temporal o por obra determinada",
                "Fue de base, planta o por tiempo indeterminado"
            ]
        },
        "p110_1": {
            "Descripción": "Prestaciones primer empleo: Aguinaldo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p110_2": {
            "Descripción": "Prestaciones primer empleo: Vacaciones con sueldo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p110_3": {
            "Descripción": "Prestaciones primer empleo: Reparto utilidades",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p110_4": {
            "Descripción": "Prestaciones primer empleo: Crédito de vivienda",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p110_5": {
            "Descripción": "Prestaciones primer empleo: Préstamos personales",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p110_6": {
            "Descripción": "Prestaciones primer empleo: Guarderías",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p110_7": {
            "Descripción": "Prestaciones primer empleo: Ahorro para el retiro",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p110_8": {
            "Descripción": "Prestaciones primer empleo: Seguro gastos médicos",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p110_9": {
            "Descripción": "Prestaciones primer empleo: Otras prestaciones",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p110_9_1": {
            "Descripción": "Prestaciones primer empleo: Otras prestaciones, especificar",
            "Valores": [5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 97, 98, 99],
            "Etiquetas": [
                "Préstamos personales y/o caja de ahorro",
                "Ahorro para el retiro",
                "Seguro privado para gastos médicos",
                "Ninguna",
                "Comisiones",
                "Bono de productividad / Puntualidad",
                "Seguro de vida",
                "Vales de despensa",
                "Ayuda de alimentos",
                "Seguridad social (IMSS)",
                "Liquidación",
                "Ayuda por defunción",
                "Dinero",
                "Transporte",
                "Insuficientemente especificado",
                "No sabe",
                "No contestó"
            ]
        },
        "p110_10": {
            "Descripción": "Ninguna",
            "Valores": [10],
            "Etiquetas": ["Ninguna"]
        },


        "p111": {
            "Descripción": "Número de horas trabajaba a la semana",
            "Valores": ["1-168"]
        },
        "p112": {
            "Descripción": "Primer trabajo, recibió capacitación laboral",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p113": {
            "Descripción": "Familiar trabajaba en la misma empresa donde tuvo su primer trabajo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p113_11": {
            "Descripción": "Familiar cercano que trabajaba en la misma empresa donde tuvo su primer trabajo",
            "Valores": ["11", "12", "13", "14", "15", "16", "17", "18"],
            "Etiquetas": ["Madre", "Padre", "Hermano(a)", "Abuelo(a)", "Tío(a)", "Cónyuge o pareja", "Suegro(a)", "Otro"]
        },
        "p114": {
            "Descripción": "Cuánto sirvieron las habilidades de escuela en el primer trabajo",
            "Valores": [1, 2, 3, 4],
            "Etiquetas": ["Mucho", "Regular", "Poco", "No le sirvieron"]
        },
        "p115": {
            "Descripción": "Primer trabajo fue acorde con sus estudios",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p116": {
            "Descripción": "Recibió apoyo para conseguir su primer empleo",
            "Valores": [1, 2, 3, 4, 5, 6, 7],
            "Etiquetas": [
                "Algún familiar",
                "Algún amigo o conocido de usted o de sus padres",
                "Algún vecino",
                "Portal en internet de empleo, municipio",
                "Agencia de empleo (no gubernamental)",
                "Nadie lo ayudó",
                "Otro"
            ]
        },
        "p116_71": {
            "Descripción": "Recibió apoyo para conseguir su primer empleo, otro",
            "Valores": ["2", "3", "4", "5", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "97", "99"],
            "Etiquetas": [
                "Utilizaría sus ahorros",
                "Utilizaría el dinero de una tanda",
                "Solicitaría préstamo a una entidad financiera",
                "Solicitaría préstamo a familiares o amigos",
                "No podría pagarla",
                "Vendería algo",
                "Buscaría trabajo / Trabajar más",
                "Solicitaría un préstamo en su trabajo",
                "Solicitaría ayuda del gobierno",
                "Pediría limosna",
                "Tarjeta de crédito",
                "Familiares le darían dinero",
                "Cancelar servicios",
                "Nada / Esperar / Aguantarme",
                "Insuficientemente especificado",
                "No contestó"
            ]
        },
        "p117": {
            "Descripción": "En su primer empleo, recibió un ascenso",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p118": {
            "Descripción": "Edad a la que cambió de puesto o posición",
            "Valores": ["8 - 58"]
        },
        "p119": {
            "Descripción": "Edad que tenía cuando terminó este trabajo",
            "Valores": ["6 - 72"]
        },
        "p120": {
            "Descripción": "Material del piso de la vivienda",
            "Valores": [1, 2, 3],
            "Etiquetas": ["Tierra", "Cemento o firme", "Madera, mosaico u otro recubrimiento"]
        },
        "p121": {
            "Descripción": "Número de cuartos que usan para dormir",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        },
        "p122": {
            "Descripción": "Número de cuartos en total en la vivienda, contando cocina",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        },
        "p123": {
            "Descripción": "Es usted (o su cónyuge) propietario de esta vivienda",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p124": {
            "Descripción": "Situación de la vivienda",
            "Valores": [1, 2, 3, 4, 5, 6],
            "Etiquetas": [
                "Es rentada",
                "Es prestada",
                "Es propiedad de otra persona que está en el hogar",
                "Está intestada, en litigio u otra situación",
                "Es propia, pero la sigue pagando",
                "Otra situación"
            ]
        },
        "p124_61": {
            "Descripción": "Situación de la vivienda, otra codificada",
            "Valores": ["3", "4", "7", "8", "9", "10", "11"],
            "Etiquetas": [
                "Es propiedad de otra persona que está en el hogar",
                "Está intestada, en litigio u otra situación",
                "Es propiedad de familiares",
                "Propia",
                "Es propiedad de otra persona que NO está en el hogar",
                "Propiedad del lugar donde trabaja",
                "Invadida"
            ]
        },
        "p125a": {
            "Descripción": "Servicios financieros: ahorros en tanda/caja ahorro",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p125b": {
            "Descripción": "Servicios financieros: cuenta ahorro",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p125c": {
            "Descripción": "Servicios financieros: cuenta bancaria",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p125d": {
            "Descripción": "Servicios financieros: tarjeta de crédito bancaria",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p125e": {
            "Descripción": "Servicios financieros: tarjeta de tienda departamental",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126a": {
            "Descripción": "Artículos vivienda: estufa de gas o eléctrica",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126b": {
            "Descripción": "Artículos vivienda: lavadora de ropa",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126c": {
            "Descripción": "Artículos vivienda: refrigerador",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126d": {
            "Descripción": "Artículos vivienda: horno de microondas",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126e": {
            "Descripción": "Artículos vivienda: televisor digital",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126f": {
            "Descripción": "Artículos vivienda: tostador eléctrico de pan",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126g": {
            "Descripción": "Artículos vivienda: aspiradora",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126h": {
            "Descripción": "Artículos vivienda: DVD, Blu-Ray",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126i": {
            "Descripción": "Artículos vivienda: consola de videojuegos",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126j": {
            "Descripción": "Artículos vivienda: televisión de paga",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126k": {
            "Descripción": "Artículos vivienda: línea telefónica fija",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126l": {
            "Descripción": "Artículos vivienda: teléfono celular",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126m": {
            "Descripción": "Artículos vivienda: conexión a internet",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126n": {
            "Descripción": "Artículos vivienda: tableta electrónica",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126o": {
            "Descripción": "Artículos vivienda: computadora",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126p": {
            "Descripción": "Artículos vivienda: animales de trabajo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126q": {
            "Descripción": "Artículos vivienda: ganado",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p126r": {
            "Descripción": "Artículos vivienda: maquinaria o equipo agrícola",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p127": {
            "Descripción": "Si tuviera urgencia económica, cómo haría para pagar",
            "Valores": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "Etiquetas": [
                "Empeñaría algo que le pertenece",
                "Utilizaría sus ahorros",
                "Utilizaría el dinero de una tanda",
                "Solicitaría préstamo a una entidad financiera",
                "Solicitaría préstamo a familiares o amigos",
                "Solicitaría un préstamo a un prestamista",
                "Podría cubrirlo con sus ingresos normal",
                "Otro",
                "No podría pagarla"
            ]
        },
        "p127_81": {
            "Descripción": "Si tuviera urgencia económica, cómo haría para pagar, otro",
            "Valores": ["2", "3", "4", "5", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "97", "99"],
            "Etiquetas": [
                "Utilizaría sus ahorros",
                "Utilizaría el dinero de una tanda",
                "Solicitaría préstamo a una entidad financiera",
                "Solicitaría préstamo a familiares o amigos",
                "No podría pagarla",
                "Vendería algo",
                "Buscaría trabajo / Trabajar más",
                "Solicitaría un préstamo en su trabajo",
                "Solicitaría ayuda del gobierno",
                "Pediría limosna",
                "Tarjeta de crédito",
                "Familiares le darían dinero",
                "Cancelar servicios",
                "Nada / Esperar / Aguantarme",
                "Insuficientemente especificado",
                "No contestó"
            ]
        },
        "p128a": {
            "Descripción": "Servicios financieros: ahorros en tanda/caja ahorro",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p128b": {
            "Descripción": "Servicios financieros: cuenta ahorro",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p128c": {
            "Descripción": "Servicios financieros: cuenta bancaria",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p128d": {
            "Descripción": "Servicios financieros: tarjeta de crédito bancaria",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p128e": {
            "Descripción": "Servicios financieros: tarjeta de tienda departamental",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p128f": {
            "Descripción": "Servicios financieros: préstamo o crédito",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p129a": {
            "Descripción": "Bienes del hogar: otra casa o departamento",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p129b": {
            "Descripción": "Bienes del hogar: local para uso comercial",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p129c": {
            "Descripción": "Bienes del hogar: negocio o parte de un negocio",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p129d": {
            "Descripción": "Bienes del hogar: tierras para labores del campo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p129e": {
            "Descripción": "Bienes del hogar: algún otro terreno",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p130a": {
            "Descripción": "Subsidios: apoyo del programa Prospera (Oportunidades)",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p130b": {
            "Descripción": "Subsidios: apoyo del Programa Adultos Mayores",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p130c": {
            "Descripción": "Subsidios: dinero o apoyo de otro programa de gobierno",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p130c_11": {
            "Descripción": "Subsidios: dinero o apoyo de otro programa de gobierno, otro",
            "Valores": ["10", "11", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "97", "99"],
            "Etiquetas": [
                "Del programa Prospera (Oportunidades)",
                "Del programa Adultos Mayores",
                "Beca educativa / Fomento a la educación",
                "Sedesol",
                "PROCAMPO / SAGARPA / PROAGRO / Apoyos p",
                "PROPESCA",
                "Madres solteras / Mujeres vulnerables",
                "Secretaría de Economía",
                "Programas sociales Estatal / Municipal",
                "Despensa",
                "FONDEN",
                "DIF",
                "LICONSA",
                "Seguro Popular",
                "Personas con discapacidad",
                "Útiles escolares",
                "Otros",
                "DICONSA",
                "Pensión",
                "Insuficientemente especificado",
                "No sabe / No contestó"
            ]
        },
        "p130d": {
            "Descripción": "Subsidios: apoyo de familiares que vivan en extranjero",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p130e": {
            "Descripción": "Subsidios: apoyo de familiares que vivan en México",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },
        "p130f": {
            "Descripción": "Subsidios: apoyo de otro tipo",
            "Valores": [1, 2],
            "Etiquetas": ["Sí", "No"]
        },

        'p130f_11': {
            'Descripción': 'Subsidios: dinero o apoyo de otro tipo, ¿cuál?',
            'Valores': [10, 11, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 97, 99],
            'Etiquetas': [
                'Del programa Prospera (Oportunidades)',
                'Del programa Adultos Mayores',
                'Beca educativa / Fomento a la educación',
                'Sedesol',
                'PROCAMPO / SAGARPA / PROAGRO / Apoyos p',
                'PROPESCA',
                'Madres solteras / Mujeres vulnerables',
                'Secretaría de Economía',
                'Programas sociales Estatal / Municipal',
                'Despensa',
                'FONDEN',
                'DIF',
                'LICONSA',
                'Seguro Popular',
                'Personas con discapacidad',
                'Útiles escolares',
                'Otros',
                'DICONSA',
                'Pensión',
                'Insuficientemente especificado',
                'No sabe / No contestó'
            ]
        },
        'p131': {
            'Descripción': 'Número de automóviles propios',
            'Valores': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 19]
        },
        'p132': {
            'Descripción': 'Número de miembros que aportan ingresos al hogar',
            'Valores': [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]
        },
        'p133': {
            'Descripción': 'Ingreso total que recibe este hogar en un mes normal',
            'Valores': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'Etiquetas': [
                'Menor a 1 salario mínimo ($0 – $2,399)',
                'Igual a un salario mínimo ($2,400)',
                'Más de 1 salario mínimo hasta 2 ($2,401 - $4,800)',
                'Más de 2 salarios mínimos hasta 3 ($4,801 - $7,200)',
                'Más de 3 salarios mínimos hasta 5 ($7,201 - $12,000)',
                'Más de 5 salarios mínimos hasta 10 ($12,001 - $24,000)',
                'Más de 10 salarios mínimos ($24,001 o más)',
                'No quiso dar información',
                'NS'
            ]
        },
        'p134a': {
            'Descripción': 'Servicios públicos: alumbrado público',
            'Valores': [1, 2, 8],
            'Etiquetas': ['Sí', 'No', 'NS']
        },
        'p134b': {
            'Descripción': 'Servicios públicos: escuelas/bibliotecas públicas',
            'Valores': [1, 2, 8],
            'Etiquetas': ['Sí', 'No', 'NS']
        },
        'p134c': {
            'Descripción': 'Servicios públicos: centros de salud cercanos',
            'Valores': [1, 2, 8],
            'Etiquetas': ['Sí', 'No', 'NS']
        },
        'p134d': {
            'Descripción': 'Servicios públicos: lugares de esparcimiento cercanos',
            'Valores': [1, 2, 8],
            'Etiquetas': ['Sí', 'No', 'NS']
        },
        'p134e': {
            'Descripción': 'Servicios públicos: seguridad en su colonia',
            'Valores': [1, 2, 8],
            'Etiquetas': ['Sí', 'No', 'NS']
        },
        'p134f': {
            'Descripción': 'Servicios públicos: facilidad para transportarse',
            'Valores': [1, 2, 8],
            'Etiquetas': ['Sí', 'No', 'NS']
        },
        'p134g': {
            'Descripción': 'Servicios públicos: limpieza en las calles',
            'Valores': [1, 2, 8],
            'Etiquetas': ['Sí', 'No', 'NS']
        },
        'p134h': {
            'Descripción': 'Servicios públicos: centros venta de alcohol clandestinos',
            'Valores': [1, 2, 8],
            'Etiquetas': ['Sí', 'No', 'NS']
        },
        'p134i': {
            'Descripción': 'Servicios públicos: terrenos/casas abandonadas',
            'Valores': [1, 2, 8],
            'Etiquetas': ['Sí', 'No', 'NS']
        },
        'p135': {
            'Descripción': 'Pareja trabajo al menos una hora',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p136': {
            'Descripción': 'Tareas que desempeña su pareja en su trabajo',
            'Valores': [],
            'Etiquetas': ['Véase la variable codificada SINCO5/CIUO5']
        },
        'p137': {
            'Descripción': 'Nombre del oficio que tiene su pareja en su trabajo',
            'Valores': [],
            'Etiquetas': ['Véase la variable codificada SINCO5/CIUO5']
        },
        'O150f_11': {
            'Descripción': 'Discriminación: otro',
            'Valores': [10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 97, 99],
            'Etiquetas': [
                'No tener dinero',
                'Su apariencia física',
                'Su edad',
                'Ser hombre/ser mujer',
                'Su color de piel',
                'Discapacidad / enfermedad / problemas d',
                'Embarazo',
                'Orientación sexual',
                'Ser indígena',
                'Adicciones (alcoholismo, drogadicción)',
                'Lugar de origen (no indígena)',
                'Religión / culto',
                'Analfabetismo / nivel de estudios',
                'Opinión / ideología / forma de pensar',
                'Carácter',
                'Lengua / idioma / forma de hablar',
                'Bulling',
                'Haber estado preso(a)',
                'Burocracia / ineficiencia de servidores',
                'Otros',
                'Insuficientemente especificado',
                'No contestó'
            ]
        },
        'p128a': {
            'Descripción': 'Servicios financieros: ahorros en tanda/caja ahorro',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p128b': {
            'Descripción': 'Servicios financieros: cuenta ahorro',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p128c': {
            'Descripción': 'Servicios financieros: cuenta bancaria',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p128d': {
            'Descripción': 'Servicios financieros: tarjeta de crédito bancaria',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p128e': {
            'Descripción': 'Servicios financieros: tarjeta de tienda departamental',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p128f': {
            'Descripción': 'Servicios financieros: préstamo o crédito',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p129a': {
            'Descripción': 'Bienes del hogar: otra casa o departamento',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p129b': {
            'Descripción': 'Bienes del hogar: local para uso comercial',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p129c': {
            'Descripción': 'Bienes del hogar: negocio o parte de un negocio',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p129d': {
            'Descripción': 'Bienes del hogar: tierras para labores del campo',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p129e': {
            'Descripción': 'Bienes del hogar: algún otro terreno',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p130a': {
            'Descripción': 'Subsidios: apoyo del programa Prospera (Oportunidades)',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p130b': {
            'Descripción': 'Subsidios: apoyo del Programa Adultos Mayores',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p130c': {
            'Descripción': 'Subsidios: dinero o apoyo de otro programa de gobierno',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p130c_11': {
            'Descripción': 'Subsidios: dinero o apoyo de otro programa de gobierno, ¿cuál?',
            'Valores': [10, 11, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 97, 99],
            'Etiquetas': [
                'Del programa Prospera (Oportunidades)',
                'Del programa Adultos Mayores',
                'Beca educativa / Fomento a la educación',
                'Sedesol',
                'PROCAMPO / SAGARPA / PROAGRO / Apoyos p',
                'PROPESCA',
                'Madres solteras / Mujeres vulnerables',
                'Secretaría de Economía',
                'Programas sociales Estatal / Municipal',
                'Despensa',
                'FONDEN',
                'DIF',
                'LICONSA',
                'Seguro Popular',
                'Personas con discapacidad',
                'Útiles escolares',
                'Otros',
                'DICONSA',
                'Pensión',
                'Insuficientemente especificado',
                'No sabe / No contestó'
            ]
        },
        'p130d': {
            'Descripción': 'Subsidios: apoyo de familiares que vivan en el extranjero',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p130e': {
            'Descripción': 'Subsidios: apoyo de familiares que vivan en México',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        },
        'p130f': {
            'Descripción': 'Subsidios: apoyo de otro tipo',
            'Valores': [1, 2],
            'Etiquetas': ['Sí', 'No']
        }


    }
    return data_desc


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

# def show_section4():
#     base_path = 'data/'
#     if 'df_valiosas_dict' not in st.session_state:
#         st.session_state['df_valiosas_dict'] = joblib.load(base_path+'df_valiosas_dict.joblib')
#     if 'df_feature_importances_total' not in st.session_state:
#         st.session_state['df_feature_importances_total'] = joblib.load(base_path+'df_feature_importances_total.joblib')
#     if 'df_clusterizados_total_origi' not in st.session_state:
#         st.session_state['df_clusterizados_total_origi'] = pd.read_csv(base_path+'df_clusterizados_total_origi.csv')

#     st.write("Sección 4")

#     TARGETS = list(st.session_state['df_valiosas_dict'].keys())
#     user_selected_target = st.selectbox("Target", TARGETS, index=0)

#     prefix = f"{user_selected_target}_"
#     df_cluster = st.session_state['df_clusterizados_total_origi'].copy()
#     rename_map = {}
#     for c in df_cluster.columns:
#         if c.startswith(prefix):
#             rename_map[c] = c.replace(prefix,"")
#     df_cluster_target = df_cluster.rename(columns=rename_map)

#     df_feature_import = st.session_state['df_feature_importances_total']
#     best_val = [x.split('-')[0].strip() for x in df_feature_import[f"{user_selected_target}_importance"].sort_values(ascending=False).index][:10]
#     best_val = [x for x in best_val if x not in ['p133','CIUO2']]

#     base_pregs = ['p05','p86','p33_f','p43','p43m','p13','p98','p151','p64']
#     preguntas_lista = sorted(list(set(base_pregs+best_val)))

#     # data_desc real vendría de get_data_desc() y tendría info completa
#     data_desc_global = get_data_desc()
#     data_desc_usable = {k: data_desc_global[k] for k in preguntas_lista if k in data_desc_global}

#     st.write("Contesta el cuestionario:")
#     cols_per_row = 3

#     with st.form("cuestionario_form"):

#         df_respuestas = cuestionario_general(data_desc_usable)
#         ejecutar = st.form_submit_button("Ejecutar")

#     if ejecutar:
#         df_datos_valiosas = st.session_state['df_valiosas_dict'][user_selected_target]
#         df_datos_descript_valiosas_respuestas = obtener_vecinos_de_mi_respuesta(df_respuestas, df_cluster_target, df_datos_valiosas)
#         df_datos_descript_valiosas_respuestas['nivel_de_confianza_cluster'] = pd.qcut(
#             df_datos_descript_valiosas_respuestas['Soporte'], q=4, labels=False
#         )
#         if 'N_probabilidad' not in df_datos_descript_valiosas_respuestas.columns:
#             df_datos_descript_valiosas_respuestas['N_probabilidad'] = np.random.randint(1,5, size=len(df_datos_descript_valiosas_respuestas))

#         # Filtrado por defecto: confidence
#         df_filtrado = df_datos_descript_valiosas_respuestas[
#             ((df_datos_descript_valiosas_respuestas['cambio_yo_moderado']>0)|
#              (df_datos_descript_valiosas_respuestas['cambio_yo_difícil']>0)|
#              (df_datos_descript_valiosas_respuestas['cambio_yo_fácil']>0))&
#             (df_datos_descript_valiosas_respuestas['nivel_de_confianza_cluster']>0)
#         ] if all(x in df_datos_descript_valiosas_respuestas.columns for x in ['cambio_yo_moderado','cambio_yo_difícil','cambio_yo_fácil','nivel_de_confianza_cluster']) else df_datos_descript_valiosas_respuestas
        
        
#         nuevo_diccionario = get_nuevo_diccionario()

#         resultado = construir_descripciones_cluster(df_filtrado, 
#                                                     data_desc_global, 
#                                                     nuevo_diccionario, 
#                                                     language='es', 
#                                                     show_N_probabilidad=True, 
#                                                     show_Probabilidad=True)


#         # Opción 1: Iterar e imprimir cada descripción
#         for cluster_id, descripcion in resultado.items():
#             st.write(descripcion)
            
#         # Opción 2: Imprimir todas las descripciones en un solo bloque (separadas por dos saltos de línea)
#         st.write("\n\n".join(resultado.values()))


def show_section4():
    base_path = 'data/'
    if 'df_valiosas_dict' not in st.session_state:
        st.session_state['df_valiosas_dict'] = joblib.load(base_path + 'df_valiosas_dict.joblib')
    if 'df_feature_importances_total' not in st.session_state:
        st.session_state['df_feature_importances_total'] = joblib.load(base_path + 'df_feature_importances_total.joblib')
    if 'df_clusterizados_total_origi' not in st.session_state:
        st.session_state['df_clusterizados_total_origi'] = pd.read_csv(base_path + 'df_clusterizados_total_origi.csv')

    st.write("Sección 4")

    TARGETS = list(st.session_state['df_valiosas_dict'].keys())
    user_selected_target = st.selectbox("Target", TARGETS, index=0)

    prefix = f"{user_selected_target}_"
    df_cluster = st.session_state['df_clusterizados_total_origi'].copy()
    rename_map = {}
    for c in df_cluster.columns:
        if c.startswith(prefix):
            rename_map[c] = c.replace(prefix, "")
    df_cluster_target = df_cluster.rename(columns=rename_map)

    df_feature_import = st.session_state['df_feature_importances_total']
    best_val = [x.split('-')[0].strip() for x in df_feature_import[f"{user_selected_target}_importance"].sort_values(ascending=False).index][:10]
    best_val = [x for x in best_val if x not in ['p133', 'CIUO2']]

    base_pregs = ['p05', 'p86', 'p33_f', 'p43', 'p43m', 'p13', 'p98', 'p151', 'p64']
    preguntas_lista = sorted(list(set(base_pregs + best_val)))

    # data_desc_global vendría de get_data_desc() y tiene la info completa
    data_desc_global = get_data_desc()
    data_desc_usable = {k: data_desc_global[k] for k in preguntas_lista if k in data_desc_global}

    st.write("Contesta el cuestionario:")

    import re
    with st.form("cuestionario_form"):
        respuestas = {}
        # Mostrar 2 preguntas por fila
        for i in range(0, len(preguntas_lista), 2):
            cols = st.columns(2)
            # Primera pregunta de la fila
            var = preguntas_lista[i]
            q_text = data_desc_usable.get(var, "")
            # Se remueve el nombre de la variable (ej. "p05") del comienzo del texto
            q_text_clean = re.sub(r"^" + re.escape(var) + r"[\s\-\:]*", "", q_text)
            respuestas[var] = cols[0].text_input("", placeholder=q_text_clean, key=f"{var}_cuest")
            # Segunda pregunta, si existe
            if i + 1 < len(preguntas_lista):
                var2 = preguntas_lista[i + 1]
                q_text2 = data_desc_usable.get(var2, "")
                q_text2_clean = re.sub(r"^" + re.escape(var2) + r"[\s\-\:]*", "", q_text2)
                respuestas[var2] = cols[1].text_input("", placeholder=q_text2_clean, key=f"{var2}_cuest")
        ejecutar = st.form_submit_button("Ejecutar")
        df_respuestas = respuestas

    if ejecutar:
        df_datos_valiosas = st.session_state['df_valiosas_dict'][user_selected_target]
        df_datos_descript_valiosas_respuestas = obtener_vecinos_de_mi_respuesta(df_respuestas, df_cluster_target, df_datos_valiosas)
        df_datos_descript_valiosas_respuestas['nivel_de_confianza_cluster'] = pd.qcut(
            df_datos_descript_valiosas_respuestas['Soporte'], q=4, labels=False
        )
        if 'N_probabilidad' not in df_datos_descript_valiosas_respuestas.columns:
            df_datos_descript_valiosas_respuestas['N_probabilidad'] = np.random.randint(1, 5, size=len(df_datos_descript_valiosas_respuestas))

        # Filtrado por defecto: confidence
        df_filtrado = df_datos_descript_valiosas_respuestas[
            ((df_datos_descript_valiosas_respuestas['cambio_yo_moderado'] > 0) |
             (df_datos_descript_valiosas_respuestas['cambio_yo_difícil'] > 0) |
             (df_datos_descript_valiosas_respuestas['cambio_yo_fácil'] > 0)) &
            (df_datos_descript_valiosas_respuestas['nivel_de_confianza_cluster'] > 0)
        ] if all(x in df_datos_descript_valiosas_respuestas.columns for x in [
            'cambio_yo_moderado', 'cambio_yo_difícil', 'cambio_yo_fácil', 'nivel_de_confianza_cluster'
        ]) else df_datos_descript_valiosas_respuestas

        nuevo_diccionario = get_nuevo_diccionario()

        resultado = construir_descripciones_cluster(
            df_filtrado,
            data_desc_global,
            nuevo_diccionario,
            language='es',
            show_N_probabilidad=True,
            show_Probabilidad=True
        )

        # Mostrar el resultado: se pueden elegir entre iterar o mostrar en bloque
        for cluster_id, descripcion in resultado.items():
            st.write(descripcion)
        st.write("\n\n".join(resultado.values()))

