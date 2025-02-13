import streamlit as st
import plotly.express as px
import pandas as pd
from utils.custom_style import load_css
from layout import aplicar_layout
from utils.update_state import nav

@aplicar_layout(nav)
def app():
    load_css("styles/style.css")
    st.markdown("""
                <div class="main-container">
                    <div class="info-box">
                        <h3 class="encabezado-h3">Elevate your<br><small> Trading</small><br> Adventure!</h3>
                        <p>orem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica </p>
                    </div>
                    <div class="card-container">
                        <div class="card">
                            <h3>Vela Alcista</h3>
                            <img src="https://raw.githubusercontent.com/LinderCa/assets/refs/heads/main/card1.png">
                        </div>
                        <div class="card">
                            <h3>Vela Bajista</h3>
                            <img src="https://raw.githubusercontent.com/LinderCa/assets/refs/heads/main/card1.png"></div>
                        <div class="card">
                            <h3>Vela Alcista</h3>
                            <img src="https://raw.githubusercontent.com/LinderCa/assets/refs/heads/main/card1.png"></div>
                    </div>
                </div>
        """,unsafe_allow_html=True)


    st.markdown("""
    <div class="container-outer">
        <div class="card_">
            <div class="col1">
                <img src="https://raw.githubusercontent.com/LinderCa/assets/refs/heads/main/card1.png" alt="Tendencia Alcista">
            </div>
            <div class="col2">
                <h3 > Tendencia Alcista</h3>
                <p>
                    La tendencia alcista es una condición de mercado en la que los precios suelen subir. Las tendencias alcistas pueden identificarse utilizando medias móviles, líneas de tendencia y niveles de soporte y resistencia. Estas son algunas características clave de una tendencia alcista:
                    Los máximos de cada vela son superiores a los máximos de las velas anteriores.
                    Los mínimos de cada vela son superiores a los mínimos de las velas anteriores.
                    Es probable que la tendencia continúe hasta que los precios rompan por debajo del nivel de soporte importante.
                </p>
            </div>
        </div>
        <div class="card_">
            <div class="col1">
                <img src="https://raw.githubusercontent.com/LinderCa/assets/refs/heads/main/card1.png" alt="Tendencia Alcista">
            </div>
            <div class="col2">
                <h3 > Tendencia Alcista</h3>
                <p>
                    La tendencia alcista es una condición de mercado en la que los precios suelen subir. Las tendencias alcistas pueden identificarse utilizando medias móviles, líneas de tendencia y niveles de soporte y resistencia. Estas son algunas características clave de una tendencia alcista:
                    Los máximos de cada vela son superiores a los máximos de las velas anteriores.
                    Los mínimos de cada vela son superiores a los mínimos de las velas anteriores.
                    Es probable que la tendencia continúe hasta que los precios rompan por debajo del nivel de soporte importante.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
