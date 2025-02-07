import streamlit as st
import os

def load_css(css_relative_path: str):
    """
    Carga y aplica estilos CSS desde un archivo.
    
    :param css_relative_path: Ruta relativa al archivo CSS desde la raíz del proyecto.
    """
    # Construir la ruta absoluta del archivo CSS
    base_path = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(base_path, "..", css_relative_path)
    
    try:
        with open("styles/style.css", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo CSS: {css_path}")
