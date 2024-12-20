import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from yahoofinancials import YahooFinancials

from bokeh.plotting import figure, column
import login


#import talib

ini = date.today() - timedelta(days=1460) # 4 years ago
ini2 = date.today() - timedelta(days=729) # 2 years ago
today = date.today()
ini_str = str(ini)
ini2_str = str(ini2)
today_str = str(today)


st.set_page_config(layout="wide", page_title="Grafica con indicadores")

login.generarLogin()
if 'usuario' in st.session_state:  

    @st.cache_data

    def load_dataset():
        tickers = ['SPY']
        yahoo_financials = YahooFinancials (tickers)
        historical_stock_prices = yahoo_financials.get_historical_price_data(ini_str, today_str, "daily")
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
        ##Calculo de promedios moviles
        df_d['SMA20'] = df_d['close'].rolling(20).mean()
        df_d['SMA40'] = df_d['close'].rolling(40).mean()
        df_d['SMA100'] = df_d['close'].rolling(100).mean()
        df_d['SMA200'] = df_d['close'].rolling(200).mean()
        return df_d

    df_d = load_dataset()
    indicator_colors = {"SMA20":"yellow", "SMA40":"red", "SMA100":"purple", "SMA200":"green"}


    def create_chart(df, close_line=False, include_vol=False, indicators=[]):
        ##Candlestick Pattern Logic
        candle = figure(x_axis_type="datetime", height=500, x_range=(df.date.values[0], df.date.values[-1]),
                    tooltips=[("date", "@Date_str"), ("open", "@open"), ("high","@high"), ("low","@low"), ("close","@close")],)

        candle.segment("date", "low", "date", "high", color="black", line_width=0.5, source=df)
        candle.segment("date", "open", "date", "close", color="BarColor", line_width=2 if len(df)>100 else 6, source=df)

        candle.xaxis.axis_label="Date"
        candle.yaxis.axis_label="Price ($)"

        ##Close Price Line
        if close_line:
            candle.line("date", "close", color="black", source=df)

        for indicator in indicators:
            candle.line("date", indicator, color=indicator_colors[indicator], line_width=1, source=df, legend_label=indicator)


        ## Volume Bars Logic
        volume = None
        if include_vol:
            volume = figure(x_axis_type="datetime", height=150, x_range=(df.date.values[0], df.date.values[-1]),)
            volume.segment("date", 0, "date", "volume", line_width=2 if len(df)>100 else 6, line_color="BarColor", alpha=0.8, source=df)
            volume.yaxis.axis_label="Volume"

        return column(children=[candle, volume], sizing_mode="scale_width") if volume else candle


    talib_indicators = ["SMA20","SMA40","SMA100","SMA200"]

    ##Dashboard
    st.title(":green[Candle]:red[stick] Pattern Technical Analysis :tea: :coffee:")
    st.sidebar.markdown('#### Date Range Selection')

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(label="Start date:", value=datetime(2022,1,1))
    with col2:
        end_date = st.date_input(label="End date:", value=datetime(2022,12,31))

    close_line=st.sidebar.checkbox(label="Close Price Line")
    volume = st.sidebar.checkbox(label="Include Trading Volume")

    indicators = st.sidebar.multiselect(label="Technical Indicators:", options=talib_indicators)

    sub_df = df_d.set_index("date").loc[str(start_date):str(end_date)]
    sub_df = sub_df.reset_index()

    fig = create_chart(sub_df, close_line, volume, indicators)

    st.bokeh_chart(fig, use_container_width=True)