import streamlit as st

def generar_header(nav):
    # Puedes usar tus variables de sesión o cualquier otra lógica
    logged = st.session_state.get("logged_in", False)
    visitor = st.session_state.get("visitor", False)
    
    # Ejemplo de botones de navegación en el header
    if logged:
        if st.button("Cerrar sesión"):
            st.session_state.logged_in = False
            nav("home")
    elif visitor:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cerrar sesión"):
                st.session_state.visitor = False
                nav("home")
        with col2:
            if st.button("Ingresar como usuario"):
                nav("login")
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Iniciar Sesión"):
                nav("login")
        with col2:
            if st.button("Ingresar como Visitante"):
                st.session_state.visitor = True
                nav("visitor")
