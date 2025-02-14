import streamlit as st
def cambiar_pagina(pagina):
    st.session_state.current_page= pagina
    st.text(f"La pagina actual es: {pagina}")
    if pagina=="visitor":
        st.session_state.visitor=True
        st.text(f"La variable state es {st.session_state.logged_in}")
    