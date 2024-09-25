import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, date, timedelta
from yahoofinancials import YahooFinancials


from bokeh.plotting import figure, column



#import talib

ini = date.today() - timedelta(days=1460) # 4 years ago
ini2 = date.today() - timedelta(days=729) # 2 years ago
today = date.today()
ini_str = str(ini)
ini2_str = str(ini2)
today_str = str(today)

st.set_page_config(layout="wide", page_title="Grafica con indicadores")

tickers = ["AAPL"]
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

df_d = load_dataset()

st.dataframe(df_d)

##descarga de dataframe HORA

def load_dataset2():
    df_h = pd.DataFrame()
    for ticker in tickers:
        company = yf.download(ticker, start = ini2_str, end = today_str, interval='60m')
        
        ## cambio de nombre de las columnas
        company.rename(columns={'Datetime':'datetime','Open':'open','High':'high','Low':'low','Close':'close','Adj Close':'adj close','Volume':'volume'}, inplace = True)
        company['date'] = pd.to_datetime (company.index) #pd.to_datetime (company.index.date)
        company['datetime'] = pd.to_datetime (company.index)    
        company['companyName'] = ticker
        df_h = pd.concat([df_h, company],ignore_index=True)
    return df_h

df_h = load_dataset2()
st.dataframe(df_h)



import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# data
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv').tail(90)
#df = df[df.columns[:6]]
#df['Date'] = pd.date_range("2018-01-01", periods=len(df), freq="H")
# df = df.set_index('Date')

#df.columns = df.columns.str.replace(r'AAPL.', '')
#names = df.columns
#dfd = df.groupby(pd.Grouper(key = 'Date', freq='D')).agg({'Open': 'first',
#                                                          'High': 'max',
#                                                          'Low': 'min',
#                                                          'Close': 'last'}).reset_index()


df_d = df_d.query("date>='2023-10-01' and date<='2023-10-31'")
df_d = df_d.reset_index()

df_h = df_h.query("companyName=='AAPL' and date>='2023-10-01' and date<='2023-10-31'")
df_h = df_h.reset_index()

fig = go.Figure(data=[go.Candlestick(
    x=df_h['datetime'],
    open=df_h['open'], high=df_h['high'],
    low=df_h['low'], close=df_h['close'],
#     increasing_line_color= 'cyan', decreasing_line_color= 'gray'
)])
# fig.show()
fig.update_layout(title = 'Hourly')

# construct menus
updatemenus = [{
#                 'active':1,
                'buttons': [{'method': 'update',
                             'label': 'Toggle Hourly / Daily',
                             'args': [
                                      # 1. updates to the traces
                                      {'open': [list(df_h.open)],
                                       'high': [list(df_h.high)],
                                       'low': [list(df_h.low)],
                                       'low': [list(df_h.close)],
                                       'x':[list(df_h.datetime)],
                                       'visible': True}, 
                                      
                                      # 2. updates to the layout
                                      {'title':'Hourly'},
                                      
                                      # 3. which traces are affected 
#                                       [0, 1],
                                      
                                      ],
                             'args2': [
                                       # 1. updates to the traces  
                                       {'open': [list(df_d.open)],
                                        'high': [list(df_d.high)],
                                        'low': [list(df_d.low)],
                                        'low': [list(df_d.close)],
                                        'x':[list(df_d.date)],
                                       'visible': True},
                                      
                                       # 2. updates to the layout
                                       {'title':'Daily'},
                                       
                                       # 3. which traces are affected
#                                        [0, 1]
                                      ]
                              },
                            ],
                'type':'buttons',
#                 'type':'dropdown',
                'direction': 'down',
                'showactive': True,}]

# update layout with buttons, and show the figure
fig.update_layout(updatemenus=updatemenus)
#fig.show()

st.plotly_chart(fig, use_container_width=True)