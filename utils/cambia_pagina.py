import streamlit as st
def cambiar_pagina(pagina):
    st.session_state["current_page"]= pagina
    if pagina=="visitor":
        st.session_state["visitor"]=True
