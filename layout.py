import streamlit as st 
from components.sidebar import generarMenu

# Esta función se encargará de generar la estructura base para cada página
def aplicar_layout(func):
    def wrapper(*args, **kwargs):
        # Generar el sidebar solo una vez
        generarMenu()
        
        # Llamar a la función de la página específica
        return func(*args, **kwargs)
    
    return wrapper