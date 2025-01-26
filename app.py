# main.py

import streamlit as st
from section1 import show_section1, random_filter_selection_section1
from section2 import show_section2, random_origin_dest_section2

def main():
    st.set_page_config(layout="wide")

    # -- Definimos Tabs:
    tab1, tab2 = st.tabs(["Movilidad", "Evolución Temporal"])

    # -- Botones en la barra lateral, en una sola fila
    #    Detectamos 'active_section' para saber en qué tab estamos
    with st.sidebar:
        st.write("### ")  # Pequeño espacio
        colA, colB = st.columns([0.5, 0.5])
        with colA:
            if st.button("⟳", help="Refrescar según sección", key="sidebar_refresh"):
                if st.session_state.get('active_section') == 'section2':
                    # Reseteamos la configuración de Section 2
                    for key in list(st.session_state.keys()):
                        if key.startswith("origin_") or key.startswith("dest_") or key == "selected_vars":
                            del st.session_state[key]
                    # En este caso, también podríamos resetear todo si deseas
                    st.rerun()
                else:
                    # Sección 1 por defecto
                    for key in list(st.session_state.keys()):
                        if key.startswith("cats_") or key.startswith("base_cats_") or key == "selected_vars":
                            del st.session_state[key]
                    st.rerun()

        with colB:
            if st.button("🎲", help="Aleatoriedad según sección", key="sidebar_random"):
                if st.session_state.get('active_section') == 'section2':
                    random_origin_dest_section2()
                    st.rerun()
                else:
                    # Sección 1 (Movilidad) por defecto
                    random_filter_selection_section1()
                    st.rerun()

    # -- Renderizamos Sección 1 y Sección 2
    with tab1:
        st.session_state['active_section'] = 'section1'  # Para saber en cuál tab estoy
        show_section1()

    with tab2:
        st.session_state['active_section'] = 'section2'
        show_section2()


if __name__ == "__main__":
    main()
