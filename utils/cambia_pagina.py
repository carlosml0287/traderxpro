import streamlit as st
def cambiar_pagina(pagina):
    st.session_state.current_page= pagina
    st.text(f"La pagina actual es: {pagina}")