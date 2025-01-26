# main.py

import streamlit as st
from section1 import show_section1, random_filter_selection as random_section1
from section2 import show_section2, random_origin_dest as random_section2

def main():
    st.set_page_config(layout="wide")

    # -----------------------------------------------------------------
    # BARRA LATERAL (parte superior): Botones Refresh y Random
    # -----------------------------------------------------------------
    col_btn1, col_btn2 = st.sidebar.columns([0.5, 0.5])
    with col_btn1:
        if st.button("Refresh", key="refresh_main", help="Recargar la app"):
            # Limpia todo el session_state y recarga
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    with col_btn2:
        if st.button("Random", key="random_main", help="Selección aleatoria"):
            # Aplica la lógica de random a Sección 1 (Movilidad)
            random_section1()
            # Aplica la lógica de random a Sección 2 (Evolución Temporal)
            random_section2()
            st.rerun()

    # -----------------------------------------------------------------
    # Título del Filtro principal (bajo los botones)
    # -----------------------------------------------------------------
    st.sidebar.subheader("Filtro actual (filtro principal):")

    # -----------------------------------------------------------------
    # TABS
    # -----------------------------------------------------------------
    tab1, tab2 = st.tabs(["Movilidad", "Evolución Temporal"])

    with tab1:
        show_section1()

    with tab2:
        show_section2()

if __name__ == "__main__":
    main()
