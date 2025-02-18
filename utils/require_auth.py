import streamlit as st
import functools

def require_auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Verifica que el usuario esté autenticado o haya ingresado como visitante
        if not (st.session_state.get("logged_in", False) or st.session_state.get("visitor", False)):
            st.error("Acceso restringido. Debes iniciar sesión o ingresar como visitante para acceder a esta página.")
            st.stop()  # Detiene la ejecución de la página
        return func(*args, **kwargs)
    return wrapper
