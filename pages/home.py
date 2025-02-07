import streamlit as st
import plotly.express as px
import pandas as pd
from utils.custom_style import load_css


load_css("styles/style.css")


def show():
    st.markdown("""
                <div class="main-container">
                    <div class="info-box">
                        <h3 class="encabezado-h3">Elevate your<br><small> Trading</small><br> Adventure!</h3>
                        <p>orem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica </p>
                    </div>
                    <div class="card-container">
                        <div class="card">
                            <img src="https://raw.githubusercontent.com/LinderCa/assets/refs/heads/main/card1.png">
                        </div>
                        <div class="card">
                        <img src="https://raw.githubusercontent.com/LinderCa/assets/refs/heads/main/card1.png"></div>
                        <div class="card">
                        <img src="https://raw.githubusercontent.com/LinderCa/assets/refs/heads/main/card1.png"></div>
                    </div>
                </div>
        """,unsafe_allow_html=True)