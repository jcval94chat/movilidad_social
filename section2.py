# section2.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_utils import load_and_process_data

def show_section2():
    """
    Sección 2:
    Ejemplo de cálculo de cohorts (cada 3 años), 
    y porcentajes de movilidad para 'ricos de origen', 'pobres de origen', etc.
    """

    st.title("Sección 2 - Análisis por Cohorte")

    # 1) Carga de datos
    df = load_and_process_data()

    # 2) Función auxiliar
    def assign_cohort_5y(row_age, base_year=2017, step=3):
        """
        row_age: edad en 2017
        base_year: año en que se realizó la encuesta (2017)
        step: tamaño del intervalo (por defecto, 3 años en este caso)

        Devuelve un string del estilo '1950-1952', '1953-1955', etc.
        """
        if pd.isna(row_age):
            return "NA"
        birth_year = base_year - int(row_age)
        lower_bound = (birth_year // step) * step
        upper_bound = lower_bound + (step - 1)
        return f"{lower_bound}-{upper_bound}"

    # 3) Crear columna 'cohort_5y'
    df['cohort_5y'] = df['p05h'].apply(assign_cohort_5y)

    # 4) Definir pobres, ricos, medios en origen/destino
    df['poor_origin'] = df['a_los_14_quintile'].isin([1,2])
    df['rich_origin'] = df['a_los_14_quintile'].isin([4,5])
    df['middle_origin'] = (df['a_los_14_quintile'] == 3)

    df['poor_dest'] = df['actualmente_quintile'].isin([1,2])
    df['rich_dest'] = df['actualmente_quintile'].isin([4,5])
    df['middle_dest'] = (df['actualmente_quintile'] == 3)

    # 5) Análisis Ricos de origen
    df_rich = df[df['rich_origin'] == True]
    grouped_rich = df_rich.groupby(['cohort_5y','sex'], dropna=True)

    n_rich = grouped_rich.size().rename("n_rich")
    n_rich_stay = grouped_rich['rich_dest'].sum().rename("n_rich_stay")

    df_rich_stats = pd.concat([n_rich, n_rich_stay], axis=1)
    df_rich_stats['pct_stay_rich'] = (df_rich_stats['n_rich_stay'] / df_rich_stats['n_rich']) * 100
    df_rich_stats.reset_index(inplace=True)

    # Cohort start (año inferior)
    def get_lower_year(cohort_str):
        if cohort_str == "NA" or pd.isna(cohort_str):
            return None
        return int(cohort_str.split('-')[0])

    df_rich_stats['cohort_start'] = df_rich_stats['cohort_5y'].apply(get_lower_year)
    df_rich_stats.sort_values('cohort_start', inplace=True)
    df_rich_stats = df_rich_stats.dropna(subset=['cohort_start'])

    # 6) Gráfica: % de ricos que se mantienen en Q4/Q5
    fig, ax = plt.subplots(figsize=(8,5))
    sns.lineplot(
        data=df_rich_stats,
        x='cohort_start',
        y='pct_stay_rich',
        hue='sex',
        marker='o',
        ax=ax
    )
    ax.set_title("Porcentaje de los 'ricos de origen' que se mantienen en Q4/Q5")
    ax.set_xlabel("Año de inicio de cohorte (nacimiento cada 3 años)")
    ax.set_ylabel("% que permanecen en Q4/Q5")

    # 7) Mostramos la figura con Streamlit
    st.pyplot(fig)

    # NOTA: Si deseas mostrar pobres o clase media, 
    # podrías usar df_poor_stats, df_mid_stats de manera similar.
    # (Se omitió para no alargar en exceso.)
