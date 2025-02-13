import streamlit as st
from utils.router import route

def generar_header(nav):
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
            background-color:rgba(29, 29, 29, 1) ;
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
            width:200px !import;
        }
        .stHorizontalBlock > .stColumn{
            box-shadow: 0 0 0;
            
        }

        </style>
       
        """,
        unsafe_allow_html=True
    )

    with st.container():
        col_logo, col_buttons = st.columns([1, 2])
        with col_logo:
            st.button("XPro", key="logo_button", on_click=lambda: nav("inicio"))
        with col_buttons:
            logged = st.session_state.get("logged_in", False)
            visitor = st.session_state.get("visitor", False)
            current_page = st.session_state.get("current_page", "inicio")
            
            if logged:
                if st.button("Cerrar sesión", key="logout"):
                    st.session_state.logged_in = False
                    nav("home")
            elif visitor:
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("Cerrar sesión", key="logout_visitor"):
                        st.session_state.visitor = False
                        nav("home")
                with col_b:
                    if st.button("Ingresar como usuario", key="to_login"):
                        nav("login")
            else:
                col_a, col_b = st.columns(2)
                with col_a:
                    # Solo mostramos el botón de login si no estamos ya en la página de login
                    if current_page != "login":
                        if st.button("Iniciar Sesión", key="login"):
                            nav("login")
                with col_b:
                    if st.button("Ingresar como Visitante", key="visitor_btn"):
                        st.session_state.visitor = True
                        nav("visitor")

