# grafica basado en: https://docs.bokeh.org/en/latest/docs/user_guide/topics/timeseries.html#candlestick-chart
import pandas as pd
import streamlit as st
import yfinance as yf

from bokeh.plotting import figure, show, column
from bokeh.sampledata.stocks import MSFT
from yahoofinancials import YahooFinancials
from datetime import datetime, date, timedelta
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter, CategoricalAxis,FactorRange

file_path = r'./pages/pga_h.txt'


tickers = [
'AAPL',
'AMZN',
'GOOG',
'GOOGL',
'META',
'MSFT',
'QQQ',
'TSLA',
'SPY',
'NFLX',
'MRNA',
'TNA',
'GLD',
'SLV',
'USO',
'BAC',
'CVX',
'XOM'
]

ini = date.today() - timedelta(days=1460) # 4 years ago
ini2 = date.today() - timedelta(days=729) # 2 years ago 
today = date.today()
ini_str = str(ini)
ini2_str = str(ini2)
today_str = str(today)

st.set_page_config(layout="wide", page_title="Estrategias")

@st.cache_data

def load_dataset():
    yahoo_financials = YahooFinancials (tickers)
    historical_stock_prices = yahoo_financials.get_historical_price_data(ini_str, today_str, 'daily')
    index = 1
    df_d = pd.DataFrame()
    for ticker in tickers:
        index+=1
        tupla = pd.DataFrame(historical_stock_prices[ticker]['prices'])
        if index==1:        
            df_d = tupla
        else:
            df_d = pd.concat([df_d, tupla], ignore_index=True)
    df_d = df_d.drop('date',axis=1)
    df_d.rename(columns={"formatted_date": "date"}, inplace = True)
    df_d['date']=pd.to_datetime(df_d['date'])
    df_d["BarColor"] = df_d[["open","close"]].apply(lambda o: "red" if o.open>o.close else "green", axis=1)
    df_d["Date_str"] = df_d["date"].astype(str)
    
    return df_d

def load_dataset2():
    df_h = pd.DataFrame()
    for ticker in tickers:
        company = yf.download(ticker, start = ini2_str, end = today_str, interval='60m')
        ## cambio de nombre de las columnas
        company.rename(columns={'Datetime':'datetime','Open':'open','High':'high','Low':'low','Close':'close','Adj Close':'adj close','Volume':'volume'}, inplace = True)
        company['date'] = pd.to_datetime (company.index.date)
        company['datetime'] = pd.to_datetime (company.index)    
        company['companyName'] = ticker
        company["Datetime_str"] = company["datetime"].astype(str)
        df_h = pd.concat([df_h, company],ignore_index=True)
    return df_h

def load_dataset3():
    df = pd.read_csv(file_path, sep='\t')
    df['date'] = pd.to_datetime (df.date)
    df['datetime'] = pd.to_datetime (df.datetime) 
    df["Datetime_str"] = df["datetime"].astype(str)
    df["BarColor"] = df[["open","close"]].apply(lambda o: "red" if o.open>o.close else "green", axis=1)
    return df

#df = load_dataset2()
#df = df.query("date>='2023-10-01' and date<='2023-10-05'")

#container = st.beta_container()

df = load_dataset3()

#allcompanys = st.sidebar.checkbox("Seleccionar todas las compañias", value=False)

companys = df['companyName'].drop_duplicates()

sel_companys = st.sidebar.selectbox("Seleccionar caso:",
        companys,0)


# if allcompanys:
#     sel_companys = st.sidebar.multiselect("Seleccionar caso:",
#         companys,companys)
# else:
#     sel_companys =  st.sidebar.multiselect("Seleccionar caso:",
#         companys)
    
#allcasos = st.sidebar.checkbox("Seleccionar todos los casos", value=False)


df_filtrado = df.query("companyName in @sel_companys")
casos=df_filtrado['id_posiblegpa'].drop_duplicates()


# if allcasos:
#     sel_casos = st.sidebar.multiselect("Seleccionar caso:",
#         casos,casos)
# else:
#     sel_casos =  st.sidebar.multiselect("Seleccionar caso:",
#         casos)


sel_casos = st.sidebar.selectbox("Seleccionar caso:",
        casos,0)

df = df.query("companyName in @sel_companys and id_posiblegpa == @sel_casos")

print (sel_companys)
print (sel_casos)

st.dataframe(df)


inc = df.query("close>open")
dec = df.query("open>close")

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

p = figure(width=1000, height=500,
           title="Estrategia Primer GAP al alza - HORA",
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
p.segment("index", "high", "index", "low", color="black", line_width=1, source=df)


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

#p.segment("datetime", "low", "datetime", "high", color="black", line_width=1, source=df)
#p.segment("datetime", "open", "datetime", "close", color="BarColor", line_width=2 if len(df)>100 else 6, source=df)
p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
p.xaxis.axis_label = "Fecha"
p.yaxis.axis_label = "Precio"
p.legend.location="top_left"


## Volume Bars Logic
volume = figure(x_axis_type="datetime", height=120, width=1000, tooltips = [("Volumen", "@volume")])
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