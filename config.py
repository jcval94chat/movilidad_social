# config.py

VAR_CATEGORIES = {
    "generation": [
        "Millennial",
        "Gen X",
        "Baby Boomer",
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

# Lista de variables disponibles para filtrar
POSSIBLE_VARS = list(VAR_CATEGORIES.keys())
