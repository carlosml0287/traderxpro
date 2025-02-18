import streamlit as st
from utils.cambia_pagina import cambiar_pagina

def route():
    # Inicializar variables de sesión (si aún no existen)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "visitor" not in st.session_state:
        st.session_state.visitor = False
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"  # Página por defecto

    current_page = st.session_state.current_page

    if current_page == "login":
        from pages.login import app as login_app
        login_app()
    elif current_page == "home":
        from pages.home import app as home_app
        home_app()
    elif current_page == "visitor":
        from pages.visitor import app as visitor_app
        visitor_app()
    elif current_page == "signup":
        from pages.signup import app as signup_app
        st.text("INGRESO A SIGNUP")
    else:
        st.write("Página no encontrada.")