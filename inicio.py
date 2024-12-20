import streamlit as st
import login as login

st.header('Trader :green[XPRO]')
login.generarLogin()
if 'usuario' in st.session_state:
    st.subheader('Información página principal')