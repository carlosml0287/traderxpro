import streamlit as st
import pandas as pd
import time
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import plotly.express as px
from bokeh.plotting import figure, show, column
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter, CategoricalAxis,FactorRange, Span
#from components.diagramar import tipo_vela

def app_visitante():
    # Pantalla de carga
    loading_placeholder = st.empty()
    spinner_css = """
    <style>
    .loading-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(87, 204, 153, 0);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }
    .loader {
        border: 8px solid #c7f9cc;
        border-top: 8px solid #57cc99;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    <div class="loading-screen">
      <div class="loader"></div>
    </div>
    """
    loading_placeholder.markdown(spinner_css, unsafe_allow_html=True)
    time.sleep(2)
    loading_placeholder.empty()

    # URLs
    url_casos = "https://raw.githubusercontent.com/LinderCa/Notebooks_Trading/main/notebooks/data/cb_h.txt"
    url_stats="https://raw.githubusercontent.com/LinderCa/Notebooks_Trading/main/notebooks/data/backtesting/result.csv"
    trade_urls = {
        "META": "https://raw.githubusercontent.com/LinderCa/Notebooks_Trading/refs/heads/main/notebooks/data/backtesting/trades_META.csv",
        "AAPL": "https://raw.githubusercontent.com/LinderCa/Notebooks_Trading/refs/heads/main/notebooks/data/backtesting/trades_AAPL.csv",
        "SPY": "https://raw.githubusercontent.com/LinderCa/Notebooks_Trading/refs/heads/main/notebooks/data/backtesting/trades_SPY.csv"
    }

    st.markdown("""
        <div style='text-align: left;'>
            <h1 style='
                font-size: 38px;
                font-weight: bold;
                background: linear-gradient(to right,#57cc99, #c7f9cc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                display: inline-block;
            '>
                Estrategia Ruptura de Resistencia
            </h1>
            <hr style='
                border: none;
                height: 2px;
                width: 460px;
                background-color: #212529;
                margin-top: 0;
                margin-bottom: 10px;
            '/>
        </div>
    """, unsafe_allow_html=True)
    try:
        df_casos=pd.read_csv(url_casos,sep='\t')
        df_stats = pd.read_csv(url_stats)
        df_stats["Start"]=pd.to_datetime(df_stats["Start"])
        df_stats["End"]=pd.to_datetime(df_stats["End"])
        dict_fecha={'Start':df_stats["Start"].loc[0],'End':df_stats["End"].loc[0]}

        # Mostrar métricas por ticker con selectbox
        tickers = sorted(df_stats["Ticker"].unique())
        tickers.insert(0,"Todos")
        
        if "ticker_seleccionado" not in st.session_state:
            st.session_state["ticker_seleccionado"]="Todos"
            
        st.write(f"El valor de ticker_seleccionado es: {st.session_state['ticker_seleccionado']}")
        ticker_input = st.selectbox("Selecciona un ticker:", tickers, key="ticker_selector")
        st.session_state["ticker_seleccionado"] = ticker_input
        
        st.write(f"El valor de ticker_seleccionado es: {st.session_state['ticker_seleccionado']}")
        ticker_select= st.session_state["ticker_seleccionado"]
        st.write(f"->{ticker_select}")
    
        if ticker_select=="Todos":
            dfs_trades=[]
            for ticker, url in trade_urls.items():
                df = pd.read_csv(url)
                df["Ticker"] = ticker
                dfs_trades.append(df)
            df_trades = pd.concat(dfs_trades, ignore_index=True)
            mostrar_kpis_por_ticker(df_stats.groupby("Ticker").mean(numeric_only=True).reset_index(), promedio=True,fecha=dict_fecha)
        else:
            # Solo el archivo del ticker seleccionado
            df_trades = pd.read_csv(trade_urls[ticker_select])
            df_trades["Ticker"] = ticker_select
            mostrar_kpis_por_ticker(df_stats[df_stats["Ticker"] == ticker_select],promedio=False,fecha=dict_fecha)

        # Preprocesar columnas para grilla
        columnas = ["Ticker", "EntryTime", "ExitTime", "EntryPrice","ExitPrice", "Duration","Size","EntryBar","ExitBar"]
        data = df_trades[columnas].copy()

        data.sort_values("EntryTime", ascending=False, inplace=True)

        # Mostrar grilla interactiva
        #st.markdown("## 📋 Trades del Ticker Seleccionado")
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_selection("single", use_checkbox=True)
        grid_options = gb.build()

        grid_response = AgGrid(
            data,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            height=400,
            width='100%',
            fit_columns_on_grid_load=True
        )

        selected = grid_response["selected_rows"]

        #FUNCION PROBADA
        def tipo_vela():
            df_casos['datetime'] = pd.to_datetime (df_casos.datetime) 
            df_casos["Datetime_str"] = df_casos["datetime"].astype(str)
            df_casos["BarColor"] = df_casos[["Open","Close"]].apply(lambda o: "red" if o.Open>o.Close else "green", axis=1)
            return df_casos

        if selected is not None and not selected.empty:
            titulo = "Gráfico"
            st.markdown(f'<h3 style="color: #57cc99; text-align: right;"> {titulo}</h3>', unsafe_allow_html=True)
            df=tipo_vela()
            fila = selected.iloc[0] 
            ticker_seleccionado = fila["Ticker"]
            fecha_open_select=fila["EntryTime"]
            df_row = df.query("companyName == @ticker_seleccionado and datetime==@fecha_open_select")
            #Hallamos el numero de caso
            caso=df_row.iloc[0]['caso']
            st.success(f"Fila seleccionada: {ticker_seleccionado} | Fecha de entrada: {fecha_open_select}")
            st.write(f"\n\t->Ticker de grilla: {ticker_seleccionado}")
            st.session_state["ticker_seleccionado"]=ticker_seleccionado
            st.write(f"\t->Ticker de grilla actual: {st.session_state['ticker_seleccionado']}")
            dfpl = df.query("companyName == @ticker_seleccionado and caso == @caso")
            st.write(f"ticker seleccioandod {ticker_seleccionado}")
            #DIbujar
            dfpl.reset_index(drop=True, inplace=True)
            inc = dfpl.query("Close>Open")
            dec = dfpl.query("Open>Close")
            TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

            p = figure(width=1000, height=500,
                    title="RCB",
                    background_fill_color="#efefef",
                    tooltips=[("Index", "@index"),("datetime", "@Datetime_str"), ("Open", "@Open"), ("High","@High"), ("Low","@Low"), ("Close","@Close"), 
                            ("cdlengulfing","@cdlengulfing"), 
                            ("cdlhammer","@cdlhammer"), 
                            ("cdlmorningstar","@cdlmorningstar"), 
                            ("cdlpiercing","@cdlpiercing"), 
                            ("cdlclosingmarubozu","@cdlclosingmarubozu"), 
                            ("cdlmarubozu","@cdlmarubozu"), 
                            ("cdl3whitesoldiers","@cdl3whitesoldiers"), 
                            ("cdlharami","@cdlharami"), 
                            ("cdlharamicross","@cdlharamicross"), 
                            ("cdlinvertdhammer","@cdlinvertdhammer"), 
                            ("cdlladderbottom","@cdlladderbottom")]
                    )
            p.xaxis.major_label_orientation = 0.8 # radians
            p.x_range.range_padding = 0.05
            p.xaxis.axis_line_width = 4
            p.xaxis.major_label_overrides = {
                i: date.strftime('%b %d %T') for i, date in zip(dfpl.index, dfpl["datetime"])
            }

            p.segment("index", "High", "index","Low",  color="black", line_width=1, source=dfpl)
            p.vbar(    
                x="index",
                width=0.6,
                bottom="Open",
                top="Close",
                fill_color="red",
                line_color="red",    
                source=dec   
            )
            p.vbar(    
                x="index",
                width=0.6,
                bottom="Open",
                top="Close",
                fill_color="green",
                line_color="green", 
                source=inc   
            )
            p.line(
                x="index", 
                y="SMA20", 
                color="#ffb81c",
                legend_label="SMA20",
                source=dfpl)
            p.line(
                x="index", 
                y="SMA40", 
                color="red",
                legend_label="SMA40",
                source=dfpl)
            
            slopeH=dfpl["sl_highs"].iloc[0]

            r_sq_h=dfpl["r_sq_h"].iloc[0]

            val = str(slopeH) + "," + str(r_sq_h)
            
            p.scatter(x="index", y="pivotLow", marker="circle", size=5,
                    line_color="navy", fill_color="red", alpha=0.5, legend_label="Cambio Tendencia Alcista", source=dfpl)
            p.scatter(x="index", y="pivotHigh", marker="circle", size=5,
                    line_color="navy", fill_color="green", alpha=0.5, legend_label="Cambio Tendencia Bajista", source=dfpl)
            p.scatter(x="index", y="High", marker="square_pin", size=8,
                    line_color="navy", fill_color="black", alpha=0.5, legend_label=val , source=dfpl[(dfpl.trendH==1)])
            p.scatter(x="index", y="breakpointpos", marker="triangle", size=12,
                    line_color="navy", fill_color="black", alpha=0.5, legend_label="Ruptura del Canal", source=dfpl)
            inicio = (dfpl[(dfpl.ind_posicion==0)].index).tolist()[0]
            vline=Span(location=inicio,dimension='height', line_color='grey',line_width=0.8, line_dash_offset= 0, line_dash='dashed', name="hola esto es una prueba", level='annotation', tags= ['square'])


            p.line(
            x="index",
            y="trendcurrhigh",
            color="purple",
            legend_label="Slope High",
            source=dfpl)
            
            p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
            p.xaxis.axis_label = "Fecha"
            p.yaxis.axis_label = "Precio"
            p.legend.location="top_left"
            p.legend.click_policy="hide"
            p.renderers.extend([vline])
            volume = figure(x_axis_type="datetime", height=120, width=1000, tooltips = [("Volume", "@Volume"),("datetime", "@Datetime_str")],background_fill_color="#efefef")
            volume.x_range.range_padding = 0.05
            volume.vbar(    
                x="index",
                width=0.6,
                top="Volume",
                fill_color="BarColor",
                line_color="BarColor", 
                source=dfpl   
            )


            volume.yaxis.axis_label="Volume"
            volume.xaxis.major_label_overrides = {
                i: date.strftime('%b %d %T') for i, date in zip(dfpl.index, dfpl["datetime"])
            }
            volume.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
            fig = column(children=[p, volume], sizing_mode="scale_width")
            st.bokeh_chart(fig, use_container_width=True)

        else:
            st.warning("⚠️ No hay ninguna fila seleccionada.")


    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")

def mostrar_kpis_por_ticker(df_stats, promedio=False, fecha={}):
    start = fecha['Start'].strftime("%d/%m/%Y %H:%M")
    end = fecha['End'].strftime("%d/%m/%Y %H:%M")
    st.markdown(f"""
        <div style="text-align: right; font-size: 14px; color: #c7f9cc; font-weight: 600;">
            🕒 Periodo analizado: <strong>{start}</strong> → <strong>{end}</strong>
        </div>
    """, unsafe_allow_html=True)
    if promedio:
        row = {}
        row["# Trades"] = df_stats["# Trades"].sum()
        columnas_promedio = [
            "Win Rate [%]", "Max. Drawdown [%]", "Return [%]",
            "Sharpe Ratio", "Profit Factor", "CAGR [%]", "Expectancy [%]"
        ]
        for col in columnas_promedio:
            row[col] = df_stats[col].mean()
            
    else:
        row = df_stats.iloc[0]

    titulo = f"Todos los Ticker" if promedio else row["Ticker"]

    

    st.markdown(f"""
        <style>
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(5, 1fr); 
            gap: 20px;
            margin-top: 20px;
            justify-items: center;
            margin-bottom: 30px;

        }}
        .kpi-card {{
            position: relative;
            width: 95%;
            height: 140px;
            background: linear-gradient(145deg, #121416, #1a1d1f);
            box-shadow: 0 4px 10px #212529, 0 0 10px rgb(33, 37, 41); 
            border-radius: 5px;
            padding: 20px;
            overflow: hidden;
            transition: transform 0.3s ease-in-out, background 0.3s, color 0.3s;
            color: #c7f9cc;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}
         .kpi-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 15px #212529, 0 0 12px #212529;
        }}
         .kpi-card:hover .kpi-title {{
            color: #57cc99; /* Color nuevo para título en hover */
        }}
        .kpi-card:hover .kpi-value {{
            color: #80ed99; /* Color nuevo para valor en hover */
        }}
        
        .kpi-title {{
            position: absolute;
            bottom: 10px;
            left: 15px;
            font-size: 14px;
            font-weight: 600;
            color: #80ed99;
        }}
        .kpi-value {{
            font-size: 40px;
            font-weight: bold;
            color: #c7f9cc;
            z-index: 1;
        }}
        </style>

        <h3 style="color: #57cc99; text-align: right;">🎯 {titulo}</h3>
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-title">∑ # Trades</div>
                <div class="kpi-value">{int(row["# Trades"])}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">∆ Win Rate</div>
                <div class="kpi-value">{round(row["Win Rate [%]"], 2)}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">↓ Max Drawdown</div>
                <div class="kpi-value">{round(row["Max. Drawdown [%]"], 2)}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">↑ Retorno</div>
                <div class="kpi-value">{round(row["Return [%]"], 2)}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">ƒ Sharpe Ratio</div>
                <div class="kpi-value">{round(row["Sharpe Ratio"], 2)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">⚐ Profit Factor</div>
                <div class="kpi-value">{round(row["Profit Factor"], 2)}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">✓ CAGR</div>
                <div class="kpi-value">{round(row["CAGR [%]"], 2)}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">≈ Expectancy</div>
                <div class="kpi-value">{round(row["Expectancy [%]"], 2)}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Para probar la función de inmediato
if __name__ == "__main__":
    app_visitante()
