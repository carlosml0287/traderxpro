import streamlit as st
from firebase_config import db, firebase_admin
from auth import validar_usuario_firestore,generar_google_login
from components.sidebar import generarMenu


def generarLogin():
    """Genera la ventana de login o muestra el menú si el login es valido
    """    
    # Validamos si el usuario ya fue ingresado    
    if 'usuario' in st.session_state:   
        generarMenu()  # Si ya hay usuario cargamos el menú        
    else:   
        with st.form('frmLogin'):
            container_section=f"""
            <style>
                .section_login{{
                    color:red;
                    border: 2px solid rgba(61, 213, 109,0.8);
                    border-radius:5px;
                    background-color: transparent;
                    text-align: center
                }}
            </style>
            <div class="section_login">hOLA<div>
            """
            st.markdown(container_section, unsafe_allow_html=True)
            usuario = st.text_input('Usuario')
            password = st.text_input('Contraseña', type='password')
            btnLogin = st.form_submit_button('Ingresar',use_container_width=True)
            if btnLogin:
                user_data = validar_usuario_firestore(usuario, password)
                if user_data:
                    st.session_state['usuario'] = user_data['user']
                    st.session_state['nombre'] = user_data['name']
                    st.success("Inicio de sesión exitoso")
                    st.rerun()
                else:
                    st.error("Usuario o clave incorrectos")
                    
            #Titulo para metodos alternaitvos de ingreso
            st.markdown("<p style='text-align: left; font-weight: bold;'>Ingresar por:</p>", unsafe_allow_html=True)

            # Botón para iniciar sesión con Google
            google_url = generar_google_login()

            google_button = f"""
            <style>
                .google-btn {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 50px;
                    height: 50px;
                    background-color: white;
                    border-radius: 50%;
                    border: 2px solid rgb(61, 213, 109);
                    box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
                    cursor: pointer;
                    text-decoration: none;
                    transition: transform 0.2s, box-shadow 0.2s;
                }}
                .google-btn:hover {{
                    transform: scale(1.1);
                    box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
                }}
                .google-icon {{
                    width: 24px;
                    height: 24px;
                }}
                
                .btn-container {{
                display: flex;
                justify-content: center;
                margin-top: 20px;
                }}
            </style>

            <div class="btn-container">
                <a href="{google_url}" class="google-btn">
                    <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" class="google-icon" alt="Google Logo">
                </a>
            </div>
            """
            st.markdown(google_button, unsafe_allow_html=True)

if __name__ == "__main__":
    generarLogin()