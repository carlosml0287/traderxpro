import streamlit as st

st.set_page_config(page_title="Mi Aplicación", page_icon="📊", layout="wide")
from utils.update_state import nav
from utils.custom_style import load_css
from utils.routerv2 import route
load_css("styles/style.css")

st.text("DEPURACIOPN")

route()


st.text("DEPURACIOON 02")
