# main.py

import streamlit as st
from section1 import show_section1
from section2 import show_section2

def main():
    st.set_page_config(layout="wide")

    # Navegación con Tabs
    tab1, tab2 = st.tabs(["Movilidad", "Otra sección"])

    with tab1:
        show_section1()

    with tab2:
        show_section2()

if __name__ == "__main__":
    main()
