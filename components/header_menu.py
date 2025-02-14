import streamlit as st
from utils.cambia_pagina import cambiar_pagina

def generar_header():
    # Inyecta CSS para el header fijo y para el contenido principal
    st.markdown(
        """
        <style>
        .stVerticalBlock .stHorizontalBlock {
           position: fixed;
           top: 100px;
           padding:10px 20px;
           display:flex;
           z-index:1000;
           justify-content: space-between;
           align-items: center;
           background-color:rgba(29, 29, 29, 1);
           box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
           height: 80px;
        }
        
        .stVerticalBlock > .stHorizontalBlock:first-of-type {
            width:65%;
        }
        
        .stHorizontalBlock > .stColumn:nth-of-type(2) {
        }
        .stHorizontalBlock > .stColumn:nth-of-type(2) .stButton{
            display:flex;   
            justify-content:flex-end;
        }
        .stHorizontalBlock > .stColumn{
            box-shadow: 0 0 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.text("Nuevamente por aqui")
    with st.container():
        col_logo, col_buttons = st.columns([1, 2])
        with col_logo:
            st.button("XPro", key="logo_button", on_click=cambiar_pagina, args=("home",))
        with col_buttons:
            # Se leen los valores de la variable de sesión y si no existen se les asigna un valor por defecto
            logged_in = st.session_state.get("logged_in", False)
            visitor = st.session_state.get("visitor", False)
            current_page = st.session_state.get("current_page", "home")
            
            if logged_in:
                if st.button("Cerrar sesión", key="logout"):
                    st.text("se esta cerrando sesion")
                    st.session_state.logged_in = False
            elif visitor:
                # Solo se muestra el botón de Login en modo visitante
                if st.button("Login", key="to_login", on_click=cambiar_pagina, args=("login",)):
                    st.text("user")
            else:
                col_a, col_b = st.columns(2)
                with col_a:
                    # Solo mostramos el botón de login si no estamos ya en la página de login
                    if current_page != "login":
                        if st.button("Iniciar Sesion", key="login_btn", on_click=cambiar_pagina, args=("login",)):
                            st.session_state.logged_in = True
                            st.text("Regresando del apilamiento a fin de iniciar sesion - button")
                with col_b:
                    st.session_state.visitor = True
                    if st.button("Ingresar como Visitante", key="visitor_btn", on_click=cambiar_pagina, args=("visitor",)):
                        st.session_state.visitor = True
                        st.text("Regresando del apilamiento visitante")

    st.text(f"Logged: {logged_in} | visitor: {visitor} | current_page: {current_page}")
