import streamlit as st
from components.sidebar import generarMenu
from components.header_menu import generar_header

def aplicar_layout(func):
    def wrapper(*args, **kwargs):
        generar_header()  # Se muestra el header en la parte superior
        # Mostrar el sidebar solo si el usuario está autenticado o en modo visitante
        if st.session_state.get("logged_in", False) or st.session_state.get("visitor", False):
            generarMenu()
        return func(*args, **kwargs)
    return wrapper
