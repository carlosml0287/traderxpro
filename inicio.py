import streamlit as st
import sys, os
from components.header_menu import generar_header
st.set_page_config(page_title="Mi Aplicación", page_icon="📊", layout="wide")

from utils.custom_style import load_css
load_css("styles/style.css")

# Inicializar variables de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "visitor" not in st.session_state:
    st.session_state.visitor = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"  # Se muestra home por defecto

# Función de navegación: solo actualiza el estado
def nav(page):
    st.session_state.current_page = page

# (Opcional) Generar el header, pasándole la función nav
generar_header(nav)

# Enrutador: carga la página según el valor actual
current_page = st.session_state.current_page

if current_page == "login":
    import pages.login as login_page
    login_page.app(nav)
elif current_page == "home":
    import pages.home as home_page
    home_page.app(nav)
elif current_page == "visitor":
    import pages.visitor as visitor_page
    visitor_page.app(nav)
elif current_page == "signup":
    import pages.signup as signup_page
    signup_page.app(nav)
else:
    st.write("Página no encontrada.")
