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
from utils.custom_style import load_css
from bokeh.models import HoverTool


# Carga de configuración
load_css("styles/style.css")

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    
file_url = config["file_url"]
tickers = config["tickers"]


def mostrar_pm40():
    st.title("HOLA SOY PM40")
    """
    #agregar_tarjetas()
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

    # Definir la figura p (como ya lo tienes)
    p = figure(
        width=1000, 
        height=500,
        title="PM40",
        background_fill_color="rgba(29, 29, 29, 0.5)",
        border_fill_color="#1D1D1D",
        outline_line_color=None,
        tooltips=[("datetime", "@Datetime_str"), ("open", "@open"), ("high", "@high"), ("low", "@low"), ("close", "@close")]
    )
    # Ajustar colores de los ejes y texto
    p.xaxis.major_label_text_color = "#56E990"
    p.yaxis.major_label_text_color = "#56E990"
    p.xaxis.axis_label_text_color = "#348c56"
    p.yaxis.axis_label_text_color = "#348c56"
    p.title.text_color = "#45ba73"
    
    #----
    # (Opcional) Configurar la cuadrícula secundaria
    p.xgrid.minor_grid_line_color = "#555555"
    p.xgrid.minor_grid_line_dash = [2, 2]
    p.xgrid.minor_grid_line_alpha = 0.5
    p.ygrid.minor_grid_line_color = "#555555"
    p.ygrid.minor_grid_line_dash = [2, 2]
    p.ygrid.minor_grid_line_alpha = 0.5

    p.xaxis.major_label_orientation = 0.8
    p.x_range.range_padding = 0.05

    # (Opcional) Configuración de la cuadrícula secundaria para el eje x
    p.xgrid.minor_grid_line_color = "#555555"   # Color de las líneas secundarias
    p.xgrid.minor_grid_line_dash = [2, 2]         # Patrón de guiones para las líneas menores
    p.xgrid.minor_grid_line_alpha = 0.5           # Opacidad de las líneas secundarias

    # (Opcional) Configuración de la cuadrícula secundaria para el eje y
    p.ygrid.minor_grid_line_color = "#555555"
    p.ygrid.minor_grid_line_dash = [2, 2]
    p.ygrid.minor_grid_line_alpha = 0.5

    
    
    

    p.xaxis.major_label_orientation = 0.8
    p.x_range.range_padding = 0.05

    # Segmentos de barras y tendencias
    p.segment("index", "high", "index", "low", color="white", line_width=1, source=df)
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
    p.legend.label_text_color = "#1D1D1D"
    p.xaxis.axis_label = "Fecha"
    p.yaxis.axis_label = "Precio"
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    

    # Configuración del gráfico de volumen
    volume = figure(x_axis_type="datetime", height=120, width=1000, tooltips=[("Volumen", "@volume")], background_fill_color="#1D1D1D", border_fill_color="#1D1D1D",      # Borde negro
    outline_line_color=None)
    volume.vbar(x="index", width=0.6, top="volume", fill_color="BarColor", line_color="BarColor", source=df)
    volume.yaxis.axis_label = "Volumen"
    volume.yaxis.axis_label_text_color = "white"
    volume.yaxis.major_label_text_color = "#56E990"
    
    
    
    #asas
    volume.grid.grid_line_color = "#444444"      # Color de la cuadrícula (un gris oscuro)
    volume.grid.grid_line_dash = [6, 4]            # Patrón de guiones: 6 píxeles dibujados, 4 píxeles en pausa
    volume.grid.grid_line_width = 1              # Ancho de las líneas
    volume.grid.grid_line_alpha = 0.6            # Transparencia (0 a 1)

    
    
    

    fig = column(children=[p, volume], sizing_mode="scale_width")

    # Mostrar el gráfico en Streamlit
    st.bokeh_chart(fig, use_container_width=True)

    # Mostrar el DataFrame en una tabla
    st.dataframe(df)
    """

mostrar_pm40()