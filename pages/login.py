import streamlit as st
from firebase_config import db, firebase_admin
from auth import validar_usuario_firestore, generar_google_login
from components.sidebar import generarMenu
from utils.custom_style import load_css


# Cargar estilos CSS personalizados
load_css("styles/style.css")


def generarLogin():
    """Genera la ventana de login o muestra el menú si el login es válido."""    
    if 'logged_in' in st.session_state and st.session_state['logged_in']:   
        generarMenu()  # Si el usuario ya está autenticado, carga el menú      
    else:   
        with st.form('frmLogin'):
            st.markdown("""
                <div>
                    <h3 class="h-3">Welcome Trader <span style="color: #a1a1b4; font-size: 40px; font-weight: bold;">XPro</span></h3>
                    <p>Hey there! Ready to log in? Just enter your username and password below and you'll be back in action in no time. Let's go!</p>
                </div>
                """,
                unsafe_allow_html=True)
            usuario = st.text_input('User')
            password = st.text_input('Password', type='password')
            btnLogin = st.form_submit_button('Sign In', use_container_width=True)

            st.markdown("""
                <div style="display: flex; align-items: center; text-align: center; width: 100%; margin: 20px 0;">
                    <hr style="flex-grow: 1; border: none; height: 1.4px; background-color: gray;">
                    <span style="padding: 0 13px; font-weight: bold; color: gray;">Sign in via</span>
                    <hr style="flex-grow: 1; border: none; height: 2px; background-color: gray;">
                </div>
            """, unsafe_allow_html=True)
            st.page_link("pages/signup.py", label="Registro", icon=":material/person_add:")

            google_url = generar_google_login()
            google_button = f"""
            <div class="btn-container">
                <a href="{google_url}" class="google-btn">
                    <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="24" height="24">
                </a>
            </div>
            <p style="color:#f0f0f0; text-align: center;">No tienes una cuenta <a href="?page=signup" style="color:#fff; font-weight:bold" target="__self">Sign up</a></p>
            """
          

            st.markdown(google_button, unsafe_allow_html=True)

            if btnLogin:
                user_data = validar_usuario_firestore(usuario, password)
                if user_data:
                    st.session_state['logged_in'] = True
                    st.session_state['usuario'] = user_data['user']
                    st.session_state['nombre'] = user_data['name']
                    st.success("Inicio de sesión exitoso")
                    st.rerun()
                else:
                    st.error("Usuario o clave incorrectos")

if __name__ == "__main__":
    generarLogin()
