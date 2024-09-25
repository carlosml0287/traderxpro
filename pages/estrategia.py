import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from bokeh.plotting import figure, show, column
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter
import matplotlib.pyplot as plt


st.set_page_config(layout="wide", page_title="Grafica con indicadores")

#file_path = 'C:/Users/carlo/OneDrive/Documentos/TRADER/traderapp/data/pga_h.txt'
file_path = r'C:\\Users\\carlo\\OneDrive\\Documentos\\TRADER\\traderapp\\pages\\pga_h.txt'


def load_dataset():
    df = pd.read_csv(file_path, sep='\t')
    df["BarColor"] = df[["open","close"]].apply(lambda o: "red" if o.open>o.close else "green", axis=1)
    df["Datetime_str"] = df["datetime"].astype(str)
    df["Date_str"] = df["date"].astype(str)
    df = df.astype({"date": "datetime64[ns]"})
    df = df.astype({"datetime": "datetime64[ns]"})
    return df



df = load_dataset()
st.dataframe(df)
df.info()
indicator_colors = {"SMA20":"yellow", "SMA40":"red", "SMA100":"purple", "SMA200":"green"}


#include_vol=False,
def create_chart(df):
    ##Candlestick Pattern Logic
    #candle = figure(x_axis_type="datetime", height=500, x_range = (df.date.values[0], df.date.values[-1]),
    #            tooltips=[("datetime", "@Date_str"), ("open", "@open"), ("high","@high"), ("low","@low"), ("close","@close")],)

    candle = figure( width=1000, height=500,
           title="Candlestick without missing dates",
           background_fill_color="#efefef",
            tooltips=[("datetime", "@Datetime_str"), ("open", "@open"), ("high","@high"), ("low","@low"), ("close","@close")]
           )

    candle.segment("index", "low", "index", "high", color="black", line_width=1, source=df)
    candle.segment("index", "open", "index", "close", color="BarColor", line_width=2 if len(df)>100 else 6, source=df)


    candle.xaxis.major_label_orientation = 0.8 # radians
    candle.x_range.range_padding = 0.05
    # one tick per week (5 weekdays)
    #candle.xaxis.ticker = list(range(df.index[0], df.index[-1], 5))

    candle.xaxis.axis_label="Date"
    candle.yaxis.axis_label="Price"

    candle.xaxis.major_label_overrides = {
    #i: date.strftime('%b %d') for i, date in zip(df.index, df["datetime"])
    i: date.strftime('%b %d %T') for i, date in zip(df.index, df["datetime"])
    }   

    candle.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
    candle.xaxis[0].formatter = DatetimeTickFormatter(hours="%b %d %T")

    ##Close Price Line
    #if close_line:
     #   candle.line("datetime", "close", color="black", source=df)
    #for indicator in indicators:
     #  candle.line("datetime", indicator, color=indicator_colors[indicator], line_width=1, source=df, legend_label=indicator)
    
    return candle

talib_indicators = ["SMA20","SMA40","SMA100","SMA200"]

##Dashboard
st.title(":green[Candle]:red[stick] Pattern Technical Analysis")
st.sidebar.markdown('#### Date Range Selection')

col1, col2 = st.sidebar.columns(2)


#with col1:
#    start_date = st.date_input(label="Start date:", value=datetime(2023,10,1))
#with col2:
#    end_date = st.date_input(label="End date:", value=datetime(2023,12,31))'''

sub_df = df.query("companyName=='AAPL' and id_posiblegpa==1")
sub_df = sub_df.reset_index()

#close_line=st.sidebar.checkbox(label="Close Price Line")
#indicators = st.sidebar.multiselect(label="Technical Indicators:", options=talib_indicators)

fig = create_chart(sub_df)
st.bokeh_chart(fig, use_container_width=True)