# config.py

# Diccionario que mapea cada variable a su lista de categorías posibles.
VAR_CATEGORIES = {
    "generation": [
        "Gen Z",
        "Millennial",
        "Gen X",
        "Baby Boomer",
        "Traditionalist",
        "NA"
    ],
    "sex": [
        "Hombre",
        "Mujer"
    ],
    "education": [
        "Primaria",
        "Secundaria",
        "Preparatoria",
        "Universidad",
        "Posgrado",
        "Otro",
        "NA"
    ]
}

# Lista de variables disponibles para filtrar (usada en la parte principal).
POSSIBLE_VARS = list(VAR_CATEGORIES.keys())
