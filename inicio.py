import streamlit as st
st.set_page_config(page_title="Mi Aplicación", page_icon="📊", layout="wide")

from components.sidebar import generarMenu
from components.header_menu import generar_header
from utils.custom_style import load_css
from layout import aplicar_layout
from pages.home import show
import pages.login as login_page

# Cargar estilos CSS personalizados
load_css("styles/style.css")

# Leer el query parameter
query_params = st.query_params
page = query_params.get("page", ["home"])[0]

# Si se solicita logout, limpiamos la sesión y actualizamos el query parameter
if page == "logout":
    st.session_state.clear()
    st.experimental_set_query_params(page="home")
    page = "home"  # Redirigimos a home


if page == "login":
    # Si se ha solicitado el login, mostrarlo en esta misma página
    login_page.generarLogin()
elif page=="visitor":
    # Si es modo visitante, activamos una bandera y mostramos la home con sidebar
    st.session_state["visitor"] = True
    # En caso contrario, usar el layout para mostrar la home
    @aplicar_layout
    def render_home():
        show()
    render_home()
else:
    # Página de inicio normal
    @aplicar_layout
    def render_home():
        show()
    render_home()

