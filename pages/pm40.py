# grafica basado en: https://docs.bokeh.org/en/latest/docs/user_guide/topics/timeseries.html#candlestick-chart
import pandas as pd
import streamlit as st
import yfinance as yf
import numpy as np
import requests
from io import StringIO

from bokeh.plotting import figure, show, column
#from bokeh.sampledata.stocks import MSFT 25092024
from yahoofinancials import YahooFinancials
from datetime import datetime, date, timedelta
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter, CategoricalAxis,FactorRange
from scipy import stats
import login
import os

#Importacion del archivo de configuracion 
import json

st.set_page_config(layout="wide", page_title="PM40")


login.generarLogin()

with open("config.json","r") as config_file:
    config=json.load(config_file)

if 'usuario' in st.session_state:    
    file_url = config["file_url"]
    tickers = config["tickers"]


    @st.cache_data
    def load_dataset3():
        #Descargar el archivo desde la URL
        response=requests.get(file_url)
        print("hito 1")
        #convertir el contenido a un archivo de memoria 
        data=StringIO(response.text)
        df = pd.read_csv(data, sep='\t')
        df['date'] = pd.to_datetime (df.date)
        df['datetime'] = pd.to_datetime (df.datetime) 
        df["Datetime_str"] = df["datetime"].astype(str)
        df["BarColor"] = df[["open","close"]].apply(lambda o: "red" if o.open>o.close else "green", axis=1)
        return df

    

    df = load_dataset3()

    #Filtramos las compañias
    companys = df['companyName'].drop_duplicates()

    #Selector para elegir una compañia
    sel_companys = st.sidebar.selectbox("Seleccionar caso:", companys,0)

    #Filtrar el dataframe por la compañia seleccionada
    df_filtrado = df.query("companyName in @sel_companys")
    
    #Filtrar donde ind_posicion sea 0 y obtener solo las fechas de esos casos
    df_casos_filtrados = df_filtrado[(df_filtrado.ind_posicion == 0) & (df_filtrado.id_posiblepm40!='') & (df_filtrado.id_posiblepm40.isnull()==False)][['id_posiblepm40', 'date']]
    
    #Convertir la fecha a string para mostrarla en selectbox
    df_casos_filtrados['date_str'] = df_casos_filtrados['date'].astype(str)
    
    # Crear un diccionario que mapea fecha → id_posiblepm40
    casos_dict = dict(zip(df_casos_filtrados['date_str'], df_casos_filtrados['id_posiblepm40']))
    
    # Mostrar selectbox con las fechas en lugar de los IDs
    sel_fecha = st.sidebar.selectbox("Seleccionar fecha del caso:", list(casos_dict.keys()), 0)

    # Obtener el id_posiblepm40 correspondiente a la fecha seleccionada
    sel_caso_id = casos_dict[sel_fecha]

    # Filtrar el DataFrame con la compañía y el caso seleccionado
    df = df.query("companyName in @sel_companys and id_posiblepm40 == @sel_caso_id")

    # Reiniciar los índices del DataFrame
    df.reset_index(drop=True, inplace=True)
    
 
       
    
    #casos=df_filtrado['id_posiblepm40'].drop_duplicates()

    #sel_casos = st.sidebar.selectbox("Seleccionar caso:",casos,0)

    #df = df.query("companyName in @sel_companys and id_posiblepm40 == @sel_casos")
    #reiniciar index dataframe
    #df.reset_index(drop=True, inplace=True) 

    #crea la linea trend solo con los 2 valores HIGH mas altos a partir del ultimo trendlower
    def collect_channel(candle, backcandles, window):
        #localdf = df_h4[candle-backcandles-window:candle-window]
        
        highs = df[(df['ind_high']>0)].high.values
        idxhighs = df[(df['ind_high']>0)].high.index

        if len(highs)>=2:
            sl_highs, interc_highs, r_value_h, _, _ = stats.linregress(idxhighs,highs)

            return(sl_highs, interc_highs, r_value_h**2)
        else:
            return(0,0,0)
    
    #crea la linea trend con todos los datos HIGH a partir del ultimo trendlower
    def collect_channel2(candle, backcandles, window):
        #localdf = df_h4[candle-backcandles-window:candle-window]
        tupla = df[['datetime', 'id_posiblepm40', 'iniTrendLow']].query("iniTrendLow==True")
        fec = tupla['datetime'].iloc[0]
        print("fecha:", fec)
        
        highs = df[(df['datetime']>=fec) & (df.index<=candle)].high.values
        idxhighs = df[(df['datetime']>=fec) & (df.index<=candle)].high.index

        if len(highs)>=2:
            sl_highs, interc_highs, r_value_h, _, _ = stats.linregress(idxhighs,highs)

            return(sl_highs, interc_highs, r_value_h**2)
        else:
            return(0,0,0)

    #linea TREND
    tupla = df.query("ind_posicion==0")
    candle = tupla.index[0]
    backcandles = 20
    window = 0
    sl_highs, interc_highs,  r_sq_h = collect_channel2(candle, backcandles, window)
    x = np.array(range(candle-backcandles-window, candle+5))

    dfTrend = pd.DataFrame(x, columns=["x"])
    dfTrend['trend'] = sl_highs*dfTrend['x'] + interc_highs
    resultprev=df.join(dfTrend)
    df=resultprev.drop('x',axis=1)
    del resultprev    

    #st.dataframe(df)


    inc = df.query("close>open")
    dec = df.query("open>close")

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(width=1000, height=500,
            title="PM40",
            background_fill_color="#efefef",
            tooltips=[("datetime", "@Datetime_str"), ("open", "@open"), ("high","@high"), ("low","@low"), ("close","@close")]
            )
    p.xaxis.major_label_orientation = 0.8 # radians
    p.x_range.range_padding = 0.05
    #p.xaxis.axis_line_join = "bevel" # radians
    p.xaxis.axis_line_width = 2

    # map dataframe indices to date strings and use as label overrides
    p.xaxis.major_label_overrides = {
        #i: date.strftime('%b %d') for i, date in zip(df.index, df["datetime"])
        i: date.strftime('%b %d %T') for i, date in zip(df.index, df["datetime"])
    }

    # one tick per week (5 weekdays)
    #p.xaxis.ticker = list(range(df.index[0], df.index[-1], 5))

    #p.segment(df.index, df.high, df.index, df.low, color="black")
    p.segment("index", "high", "index","low",  color="black", line_width=1, source=df)
    #p.segment("low", color="red", line_width=1, source=df)


    #p.vbar(df.index[dec], 0.6, df.open[dec], df.close[dec], color="#eb3c40")
    p.vbar(    
        x="index",
        width=0.6,
        bottom="open",
        top="close",
        fill_color="red",
        line_color="red",    
        source=dec   
    )

    #p.vbar(df.index[inc], 0.6, df.open[inc], df.close[inc], fill_color="white",line_color="#49a3a3", line_width=2)
    p.vbar(    
        x="index",
        width=0.6,
        bottom="open",
        top="close",
        fill_color="green",
        line_color="green", 
        source=inc   
    )

    p.line(
        x="index", 
        y="SMA20", 
        color="#ffb81c",
        legend_label="SMA20",
        source=df)

    p.line(
        x="index", 
        y="SMA40", 
        color="red",
        legend_label="SMA40",
        source=df)

    p.line(
        x="index", 
        y="SMA100", 
        color="green",
        legend_label="SMA100",
        source=df)

    p.line(
        x="index",
        y="SMA200",
        color="purple",
        legend_label="SMA200",
        source=df)
    
    p.scatter(x="index", y="trendhigher", marker="inverted_triangle", size=14,
              line_color="navy", fill_color="blue", alpha=0.5, legend_label="Cambio Tend. Bajista", source=df)
    
    p.scatter(x="index", y="trendlower", marker="triangle", size=14,
              line_color="navy", fill_color="red", alpha=0.5, legend_label="Cambio Tend. Alcista", source=df)
    

    #fig.add_trace(go.Scatter(x=x, y=sl_highs*x + interc_highs, mode='lines', name='TENDENCIA'))

    p.line(
    x="index",
    y="trend",
    color="purple",
    legend_label="TENDENCIA",
    source=df)

    #p.segment("datetime", "low", "datetime", "high", color="black", line_width=1, source=df)
    #p.segment("datetime", "open", "datetime", "close", color="BarColor", line_width=2 if len(df)>100 else 6, source=df)
    p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
    p.xaxis.axis_label = "Fecha"
    p.yaxis.axis_label = "Precio"
    p.legend.location="top_left"
    p.legend.click_policy="hide"

    ## Volume Bars Logic
    volume = figure(x_axis_type="datetime", height=120, width=1000, tooltips = [("Volumen", "@volume")],background_fill_color="#efefef")
    #volume.segment("index", 0, "index", "volume", line_width=2 if len(df)>100 else 6, line_color="BarColor", alpha=0.8, source=df)
    volume.x_range.range_padding = 0.05

    volume.vbar(    
        x="index",
        width=0.6,
        top="volume",
        fill_color="BarColor",
        line_color="BarColor", 
        source=df   
    )


    volume.yaxis.axis_label="volumen"
    volume.xaxis.major_label_overrides = {
        #i: date.strftime('%b %d') for i, date in zip(df.index, df["datetime"])
        i: date.strftime('%b %d %T') for i, date in zip(df.index, df["datetime"])
    }
    volume.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

    fig = column(children=[p, volume], sizing_mode="scale_width")

    #show(p)
    st.bokeh_chart(fig, use_container_width=True)
    
    st.dataframe(df)