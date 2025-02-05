import streamlit as st
from components.sidebar import generarMenu
from utils.custom_style import load_css
from pages import home, login

# Configuración de la página (debe ir antes de todo)
st.set_page_config(page_title="Mi Aplicación", page_icon="📊", layout="wide")

# Cargar estilos CSS personalizados
load_css("styles/style.css")

# Verificar si el usuario está autenticado
if not st.session_state.get("logged_in", False):
    login.generarLogin()
else:
    # Mostrar la barra lateral con el menú
    generarMenu()

    # Diccionario de páginas disponibles para usuarios autenticados
    PAGES = {
        "🏠 Inicio": home.show,
    }

    # Selector en la barra lateral para navegar entre páginas
    st.sidebar.title("Navegación")
    page_selection = st.sidebar.radio("Ir a:", list(PAGES.keys()))

    # Mostrar la página seleccionada
    PAGES[page_selection]()
