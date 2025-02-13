import streamlit as st

def route(nav):
    # Intentar obtener el parámetro 'page' de la URL
    # Intentar obtener el parámetro 'page' de la URL usando st.query_params (nueva API)
    query_params = st.query_params
    if "page" in query_params:
        st.session_state.current_page = query_params["page"][0]
        st.text(f"RUTA: {query_params['page'][0]}")
    
    st.text(f"RUTA: {query_params}")
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
        login_app(nav)
        
    elif current_page == "home":
        from pages.home import app as home_app
        home_app()
    elif current_page == "visitor":
        from pages.visitor import app as visitor_app
        visitor_app(nav)
    elif current_page == "signup":
        from pages.signup import app as signup_app
        signup_app(nav)
    else:
        st.write("Página no encontrada.")

