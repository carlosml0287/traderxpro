import streamlit as st
import pandas as pd
import time
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import plotly.express as px


def app_visitante():
    # Creamos un contenedor vacío para la pantalla de carga
    loading_placeholder = st.empty()

    # Definimos el CSS del spinner, sin fondo (o con fondo totalmente transparente)
    spinner_css = """
    <style>
    .loading-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0); /* Fondo transparente */
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }
    .loader {
        border: 8px solid #f3f3f3; /* Gris claro */
        border-top: 8px solid #3498db; /* Azul */
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

    # Mostrar la pantalla de carga con el spinner CSS
    loading_placeholder.markdown(spinner_css, unsafe_allow_html=True)
    time.sleep(3)  # Ajusta este tiempo según tus necesidades
    loading_placeholder.empty() #  eliminamos la pantalla de carga

    url = "https://raw.githubusercontent.com/LinderCa/Notebooks_Trading/main/notebooks/data/cb_h.txt"
    url_backtesting="https://raw.githubusercontent.com/LinderCa/Notebooks_Trading/main/notebooks/data/backtesting/result.csv"
    url_backtest_meta="https://raw.githubusercontent.com/LinderCa/Notebooks_Trading/refs/heads/main/notebooks/data/backtesting/trades_META.csv"
    url_backtest_appl="https://raw.githubusercontent.com/LinderCa/Notebooks_Trading/refs/heads/main/notebooks/data/backtesting/trades_AAPL.csv"
    url_backtest_spy="https://raw.githubusercontent.com/LinderCa/Notebooks_Trading/refs/heads/main/notebooks/data/backtesting/trades_SPY.csv"
    
    st.title("📈 ESTRATEGIA RCB2 ")
    try:
        #Cargar data
        df = pd.read_csv(url, delimiter="\t") 
        df_stats = pd.read_csv(url_backtesting,delimiter=',')
        df_spy=pd.read_csv(url_backtest_spy,delimiter=',')
        
        #st.markdown("### 📄 Datos Originales")
        #st.dataframe(df, use_container_width=True)
        st.dataframe(df_spy,use_container_width=True)
        
        # Procesar data para AgGrid
        data = df[df["ind_posicion"] == 0].copy()
        data = data[["companyName", "Open", "Close", "High", "Low", "datetime"]]
        data.rename(columns={"companyName": "Ticket", "datetime": "Fecha Hora"}, inplace=True)

        mostrar_kpis_por_ticker(df_stats)

        # AgGrid interactiva
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
        
        # Mostrar la grilla de resultados de backtesting
        #st.markdown("### 📊 Resultados del Backtest por Ticker")
        if selected:
            fila = selected[0]
            st.success(f"Fila seleccionada: {fila['Ticket']} - {fila['Fecha Hora']}")

            fig = px.bar(
                x=["Open", "Close", "High", "Low"],
                y=[fila["Open"], fila["Close"], fila["High"], fila["Low"]],
                labels={"x": "Precio", "y": "Valor"},
                title=f"📊 Gráfico de {fila['Ticket']} ({fila['Fecha Hora']})"
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"No se pudo cargar la data: {e}")

def mostrar_kpis_por_ticker(df_stats):
    st.markdown("### 📌 Indicadores por Ticker")

    tickers = sorted(df_stats["Ticker"].unique())
    ticker_seleccionado = st.selectbox("Selecciona un ticker:", tickers)

    row = df_stats[df_stats["Ticker"] == ticker_seleccionado].iloc[0]

    st.subheader(f"🎯 {ticker_seleccionado}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💼 # Trades", int(row["# Trades"]))
    col2.metric("📈 Win Rate", f"{round(row['Win Rate [%]'], 2)}%")
    col3.metric("📉 Max Drawdown", f"{round(row['Max. Drawdown [%]'], 2)}%")
    col4.metric("🔁 Retorno", f"{round(row['Return [%]'], 2)}%")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("📊 Sharpe Ratio", round(row["Sharpe Ratio"], 2))
    col6.metric("💰 Profit Factor", round(row["Profit Factor"], 2))
    col7.metric("📐 CAGR", f"{round(row['CAGR [%]'], 2)}%")
    col8.metric("💡 Expectancy", f"{round(row['Expectancy [%]'], 2)}%")




# Para probar la función de inmediato
if __name__ == "__main__":
    app_visitante()
