# main.py

import streamlit as st
from section1 import show_section1
from section2 import show_section2

def main():
    # Pequeño control (discreto) para cambiar sección
    st.sidebar.markdown("**Navegación**")
    section = st.sidebar.radio(
        "Ir a sección:",
        ("Movilidad", "Otra sección"),
        label_visibility="collapsed"  # para ocupar menos espacio
    )

    if section == "Movilidad":
        show_section1()
    else:
        show_section2()

if __name__ == "__main__":
    main()
