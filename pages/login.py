import streamlit as st
from firebase_config import db, firebase_admin
from auth import validar_usuario_firestore, generar_google_login
from components.sidebar import generarMenu

def generarLogin():
    """Genera la ventana de login o muestra el menú si el login es válido."""    
    if 'logged_in' in st.session_state and st.session_state['logged_in']:   
        generarMenu()  # Si el usuario ya está autenticado, carga el menú        
    else:   
        with st.form('frmLogin'):
            st.markdown("<h2 style='text-align: center;'>Iniciar Sesión</h2>", unsafe_allow_html=True)
            usuario = st.text_input('Usuario')
            password = st.text_input('Contraseña', type='password')
            btnLogin = st.form_submit_button('Ingresar', use_container_width=True)

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
                    
        # Opciones de autenticación alternativa
        st.markdown("<p style='font-weight: bold;'>Ingresar con:</p>", unsafe_allow_html=True)

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
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            .google-btn:hover {{
                transform: scale(1.1);
                box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
            }}
            .btn-container {{
                display: flex;
                justify-content: center;
                margin-top: 20px;
            }}
        </style>
        <div class="btn-container">
            <a href="{google_url}" class="google-btn">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="24" height="24">
            </a>
        </div>
        """
        st.markdown(google_button, unsafe_allow_html=True)

if __name__ == "__main__":
    generarLogin()
