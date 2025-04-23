import streamlit as st
import pandas as pd
import time
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import plotly.express as px

from utils.set_get_json import set_status,get_status
from utils.graficar import graficar
from utils.load_data import load_data

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
        
        #PRUEBA
        #if "ticker_anterior" not in st.session_state:
        #    st.session_state["ticker_anterior"] = None
            
        #ticker_actual = st.selectbox("Selecciona un ticker", tickers,key="ticker_selector")
        #st.write(f"->El valor de ticker actual es: {ticker_actual}")
        
        #hubo_interaccion = ticker_actual != st.session_state["ticker_anterior"]
        #st.write(f"El valor de hubo_interaccion es: {hubo_interaccion}")
        #st.write(f"->el valor de status_row es: {get_status('status_row')}")

        #if hubo_interaccion:
        #    st.success(f"✅ Se hizo clic y seleccionaste: {ticker_actual}")
        #    ticker_current=ticker_actual
        #    set_status("status_row", "None")
        #else:
        #    st.info("ℹ️ No se ha cambiado la selección aún")
        #    st.write(f"->El valor de status_row es: {get_status('status_row')}")
        #    ticker_current=get_status("status_row")

        # Actualizar valor anterior
        #st.session_state["ticker_anterior"] = ticker_current
        
        ticker_current=st.selectbox("Selecciona un ticker", tickers,key="ticker_selector")
        #RESERVA DE ESPACIO
        kpi_holder=st.empty()
        #Mostramos lo inicial
        df_inicial=df_stats.groupby("Ticker").mean(numeric_only=True).reset_index()
        
        with kpi_holder:
            mostrar_kpis_por_ticker(df_inicial, promedio=True,fecha=dict_fecha)
        
        if ticker_current=="Todos":
            dfs_trades=[]
            for ticker, url in trade_urls.items():
                df = pd.read_csv(url)
                df["Ticker"] = ticker
                dfs_trades.append(df)
            df_trades = pd.concat(dfs_trades, ignore_index=True)
            #mostrar_kpis_por_ticker(df_stats.groupby("Ticker").mean(numeric_only=True).reset_index(), promedio=True,fecha=dict_fecha)
        else:
            df_trades = pd.read_csv(trade_urls[ticker_current])
            df_trades["Ticker"] = ticker_current
            #mostrar_kpis_por_ticker(df_stats[df_stats["Ticker"] == ticker_current],promedio=False,fecha=dict_fecha)

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
        st.write("--- SELECTED DEBUG ---")
        st.write(f"selected: {selected}")
        st.write(f"type(selected): {type(selected)}")

        #FUNCION PROBADA
        def tipo_vela():
            df_casos['datetime'] = pd.to_datetime (df_casos.datetime) 
            df_casos["Datetime_str"] = df_casos["datetime"].astype(str)
            df_casos["BarColor"] = df_casos[["Open","Close"]].apply(lambda o: "red" if o.Open>o.Close else "green", axis=1)
            return df_casos

        # 6) Cuando el usuario cambie el selectbox, **vuelve a pintar solo el placeholder**
        if ticker_current != "Todos":
            df_sub = df_stats[df_stats["Ticker"] == ticker_current]
            with kpi_holder:
                mostrar_kpis_por_ticker(df_sub, promedio=False, fecha=dict_fecha)

        if selected is not None:
            st.write(f"len(selected): {len(selected)}")
            if len(selected) > 0:
                titulo = "Gráfico"
                st.markdown(f'<h3 style="color: #57cc99; text-align: right;"> {titulo}</h3>', unsafe_allow_html=True)
                df=tipo_vela()
                ticker=selected.iloc[0]['Ticker']
                fecha_open_select=selected.iloc[0]['EntryTime']
                df_row = df.query("companyName == @ticker and datetime==@fecha_open_select")
                caso=df_row.iloc[0]['caso']
                st.success(f"Fila seleccionada: {ticker} | Fecha de entrada: {fecha_open_select}")
                dfpl = df.query("companyName == @ticker and caso == @caso")
                df_sub = df_stats[df_stats["Ticker"] == ticker]
                #CAMBIAR EL ESTADO DE JSON
                #set_status("status_row",ticker)
                #set_status("is_input","false")
                
                with kpi_holder:
                    mostrar_kpis_por_ticker(df_sub, promedio=False, fecha=dict_fecha)
                
                graficar(dfpl)
            else:
                st.warning("⚠️ No hay ninguna fila seleccionada.")
        else:
            st.warning("⚠️ 'selected' es None.")
            set_status("status_row","None")
            set_status("is_input","true")



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
