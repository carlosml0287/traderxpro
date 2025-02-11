import streamlit as st

def app(nav):
    st.title("Página para Visitantes")
    st.write("Bienvenido a la vista de visitante.")
    
    if st.button("Ir a Home"):
        nav("home")
