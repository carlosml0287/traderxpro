import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import numpy as np

# get some data
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")

# remap to 5 days of hourly data... hence only 8 hrs a day
fivedaydata = (
    df.head(8 * 5)
    .assign(Time=np.array([pd.date_range(d + pd.Timedelta(hours=9), freq="H", periods=8)
                           for d in pd.bdate_range(df.loc[0, "Date"], periods=5, freq="B")
                          ]).flatten()
    )
    .rename(columns={c: c.split(".")[1] for c in df.columns if "AAPL" in c})
)

go.Figure(
    data=[
        go.Candlestick(
            x=fivedaydata.Time,
            open=fivedaydata["Open"],
            high=fivedaydata["High"],
            low=fivedaydata["Low"],
            close=fivedaydata["Close"],
        )
    ]
).show()

go.Figure(
    data=[
        go.Candlestick(
            x=fivedaydata.index,
            open=fivedaydata["Open"],
            high=fivedaydata["High"],
            low=fivedaydata["Low"],
            close=fivedaydata["Close"],
        )
    ]).update_layout(xaxis = {"tickmode":'array',"tickvals" : fivedaydata.index,
                              "ticktext" : fivedaydata["Time"].dt.strftime("%H%p %d %b")})

