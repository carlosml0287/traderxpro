import streamlit as st
from layout import aplicar_layout_con_sidebar

@aplicar_layout_con_sidebar()
def app():
    st.title("Página para Visitantes")
    st.write("Bienvenido a la vista de visitante.")
    
