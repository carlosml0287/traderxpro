import streamlit as st
# Configuración de la página
st.set_page_config(page_title="Mi Aplicación", layout="wide")
from utils.custom_style import load_css
import pages.home

# Cargamos el archivo css
load_css("styles/style.css")


st.markdown("<div class='title_header'>Trading Project <span>Web</span></div>", unsafe_allow_html=True)
st.markdown("<div class='p_descripcion'>Esta es la descripción de mi proyecto. Elige una opción para continuar.</div>", unsafe_allow_html=True)
    
# Usamos columnas para centrar los botones
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    button_col1, button_col2 = st.columns(2)
    with button_col1:
        if st.button("👤 Iniciar como Visitante"):
            st.session_state.modo = "visitante"
            st.rerun()
    with button_col2:
        if st.button("🔑 Iniciar Sesión"):
            st.session_state.modo = "usuario"
            st.rerun()
            
            
if "modo" in st.session_state:
    if st.session_state.modo =="visitante":
        from pages.visitante import app_visitante
        app_visitante()
        st.stop()
    elif st.session_state.modo=="usuario":
        from pages.autenticacion import login
        login()
        st.stop()

# Detener la ejecución aquí si ya se ha elegido un modo
"""
if "modo" in st.session_state:
    if st.session_state.modo in ["visitante", "usuario"]:
        from router import route
        route(st.session_state.modo)
        st.stop()  # Detener la ejecución del código del archivo inicial
"""