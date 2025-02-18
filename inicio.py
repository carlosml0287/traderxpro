import streamlit as st

st.set_page_config(page_title="Mi Aplicación", page_icon="📊", layout="wide")
from utils.custom_style import load_css
from utils.router import route
load_css("styles/style.css")

route()


