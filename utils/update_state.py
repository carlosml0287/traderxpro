import streamlit as st

def nav(page):
    st.session_state.current_page = page
    # (Opcional) Mensaje de depuración; puedes comentarlo en producción
    st.text(f"MI SESION ACTUAL ES: {page}")
    st.rerun
