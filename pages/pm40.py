import streamlit as st
import pandas as pd
import requests
from io import StringIO
from bokeh.plotting import figure, column
from bokeh.models import NumeralTickFormatter
from scipy import stats
import numpy as np
import json
from datetime import datetime
from layout import aplicar_layout  # Importa el decorador
from utils.custom_style import load_css

# Carga de configuración
st.set_page_config(layout="wide", page_title="PM40")
load_css("styles/style.css")

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    
file_url = config["file_url"]
tickers = config["tickers"]

# Función para agregar tarjetas personalizadas
def agregar_tarjetas():
    # Crear una estructura de columnas para mostrar las tarjetas como un tablero
    col1, col2 = st.columns(2)  # Tres columnas

    with col1:
        st.markdown(
            """
            <div style="background-color:#1D1D1D; padding:20px; border:2px solid red; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h3>Tarjeta 1: Información Básica</h3>
                <p>Aquí puedes agregar contenido sobre la compañía o cualquier otro dato.</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div style="background-color:#1D1D1D; border:4px solid red padding:20px; border-radius:8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h3 style="color:red; padding:10px;">Tarjeta 3: Detalles Adicionales</h3>
                <p>Puedes agregar cualquier detalle adicional relevante.</p>
            </div>
            """, unsafe_allow_html=True)

@aplicar_layout  # Aplica el decorador para agregar el layout
def mostrar_pm40():
    agregar_tarjetas()
    @st.cache_data
    def load_dataset3():
        response = requests.get(file_url)
        data = StringIO(response.text)
        df = pd.read_csv(data, sep='\t')
        df['date'] = pd.to_datetime(df.date)
        df['datetime'] = pd.to_datetime(df.datetime)
        df["Datetime_str"] = df["datetime"].astype(str)
        df["BarColor"] = df[["open", "close"]].apply(lambda o: "red" if o.open > o.close else "green", axis=1)
        return df

    df = load_dataset3()

    # Filtramos las compañías
    companys = df['companyName'].drop_duplicates()

    # Selector para elegir una compañía
    st.sidebar.markdown("<h4 style='font-size: 16px;'>Seleccionar caso:</h4>", unsafe_allow_html=True)  # Reducir tamaño del texto
    sel_companys = st.sidebar.selectbox("", companys, 0)  # El texto ya está modificado por el HTML

    # Filtrar el dataframe por la compañía seleccionada
    df_filtrado = df.query("companyName in @sel_companys")
    
    # Filtrar donde ind_posicion sea 0 y obtener solo las fechas de esos casos
    df_casos_filtrados = df_filtrado[(df_filtrado.ind_posicion == 0) & (df_filtrado.id_posiblepm40 != '') & (df_filtrado.id_posiblepm40.isnull() == False)][['id_posiblepm40', 'date']]
    
    # Convertir la fecha a string para mostrarla en selectbox
    df_casos_filtrados['date_str'] = df_casos_filtrados['date'].astype(str)
    
    # Crear un diccionario que mapea fecha → id_posiblepm40
    casos_dict = dict(zip(df_casos_filtrados['date_str'], df_casos_filtrados['id_posiblepm40']))
    
    st.sidebar.markdown("<h4 style='font-size: 16px;'>Seleccionar fecha del caso:</h4>", unsafe_allow_html=True)  # Reducir tamaño del texto
    # Mostrar selectbox con las fechas en lugar de los IDs
    sel_fecha = st.sidebar.selectbox("", list(casos_dict.keys()), 0)

    # Obtener el id_posiblepm40 correspondiente a la fecha seleccionada
    sel_caso_id = casos_dict[sel_fecha]

    # Filtrar el DataFrame con la compañía y el caso seleccionado
    df = df.query("companyName in @sel_companys and id_posiblepm40 == @sel_caso_id")

    # Reiniciar los índices del DataFrame
    df.reset_index(drop=True, inplace=True)

    # Creación de las gráficas y lógica de tendencias
    inc = df.query("close > open")
    dec = df.query("open > close")

    p = figure(width=1000, height=500,
               title="PM40",
               background_fill_color="#efefef",
               tooltips=[("datetime", "@Datetime_str"), ("open", "@open"), ("high", "@high"), ("low", "@low"), ("close", "@close")]
               )
    p.xaxis.major_label_orientation = 0.8
    p.x_range.range_padding = 0.05

    # Segmentos de barras y tendencias
    p.segment("index", "high", "index", "low", color="black", line_width=1, source=df)
    p.vbar(x="index", width=0.6, bottom="open", top="close", fill_color="red", line_color="red", source=dec)
    p.vbar(x="index", width=0.6, bottom="open", top="close", fill_color="green", line_color="green", source=inc)

    # Líneas SMA y tendencia
    p.line(x="index", y="SMA20", color="#ffb81c", legend_label="SMA20", source=df)
    p.line(x="index", y="SMA40", color="red", legend_label="SMA40", source=df)
    p.line(x="index", y="SMA100", color="green", legend_label="SMA100", source=df)
    p.line(x="index", y="SMA200", color="purple", legend_label="SMA200", source=df)

    # Gráfico de tendencia
    p.line(x="index", y="trend", color="purple", legend_label="TENDENCIA", source=df)

    # Configuración del formato del eje Y y X
    p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
    p.xaxis.axis_label = "Fecha"
    p.yaxis.axis_label = "Precio"
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    # Configuración del gráfico de volumen
    volume = figure(x_axis_type="datetime", height=120, width=1000, tooltips=[("Volumen", "@volume")], background_fill_color="#efefef")
    volume.vbar(x="index", width=0.6, top="volume", fill_color="BarColor", line_color="BarColor", source=df)
    volume.yaxis.axis_label = "Volumen"

    fig = column(children=[p, volume], sizing_mode="scale_width")

    # Mostrar el gráfico en Streamlit
    st.bokeh_chart(fig, use_container_width=True)

    # Mostrar el DataFrame en una tabla
    st.dataframe(df)

# Llamar la función decorada
mostrar_pm40()
