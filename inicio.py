import streamlit as st
st.set_page_config(page_title="Mi Aplicación", page_icon="📊", layout="wide")

from components.sidebar import generarMenu
from utils.custom_style import load_css
from layout import aplicar_layout
from pages.home import show


# Cargar estilos CSS personalizados
load_css("styles/style.css")

@aplicar_layout
def mostrar_inicio():
    # Aquí van los elementos específicos de la página de inicio
    show()
    
    
mostrar_inicio()



# Verificar si el usuario está autenticado
#if not st.session_state.get("logged_in", False):
#    login.generarLogin()
#else:
#    # Mostrar la barra lateral con el menú
