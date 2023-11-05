import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
 
st.set_page_config(layout="wide")

st.title("Forecast USD time series")

# Sidebar 
start_date = st.sidebar.date_input("Set initial data: ", datetime(2023, 1, 1))
forecast_days = st.sidebar.slider("Forecast Days (1-60)", min_value=1, max_value=60, value=30)

st.sidebar.header("Configuração do Modelo ARIMA")
p = st.sidebar.slider("Ordem do Termo Autoregressivo (p):", 0, 10, 5)
d = st.sidebar.slider("Ordem de Diferenciação (d):", 0, 2, 1)
q = st.sidebar.slider("Ordem do Termo de Média Móvel (q):", 0, 10, 0)

def get_dollar_data(start_date, end_date):
    df = yf.download('USDBRL=X', start=start_date, end=end_date)
    return df

# Obter dados do Yahoo Finance para os últimos 120 dias
end_date = start_date + pd.DateOffset(days=forecast_days + 120)
dollar_data = get_dollar_data(start_date, datetime.today())

# Verificar a estacionariedade da série temporal
result = adfuller(dollar_data['Close'])  # Use a coluna 'Close' em vez de 'Adj Close'
st.write("Teste ADF (Dickey-Fuller):")
st.write(f"Statistic: {result[0]}")
st.write(f"P-value: {result[1]}")
st.write(f"Critical Values: {result[4]}")

if result[1] <= 0.05:
    st.write("A série é estacionária.")
else:
    st.write("A série não é estacionária. Aplicando diferenciação.")

    # Aplicar a diferenciação para tornar a série estacionária
    dollar_data_diff = dollar_data['Close'].diff().dropna()  # Use a coluna 'Close' em vez de 'Adj Close'
    result_diff = adfuller(dollar_data_diff)
    st.write("Teste ADF após diferenciação:")
    st.write(f"Statistic: {result_diff[0]}")
    st.write(f"P-value: {result_diff[1]}")
    st.write(f"Critical Values: {result_diff[4]}")

    if result_diff[1] <= 0.05:
        st.write("A série após a diferenciação é estacionária.")
    else:
        st.write("A série não é estacionária após a diferenciação. Considere outras transformações.")

    # Treinar o modelo ARIMA
    model = ARIMA(dollar_data['Close'], order=(p, d, q))
    model_fit = model.fit()

    # Fazer a previsão para os próximos 45 dias
    forecast, stderr, conf_int = model_fit.forecast(steps=forecast_days)

    fig, ax = plt.subplots()
    ax.plot(dollar_data['Close'].index, dollar_data['Close'], label='Dados Históricos', color='blue')
    ax.plot(pd.date_range(start=start_date, periods=forecast_days, freq='D'), forecast, label='Previsão', color='red')
    ax.fill_between(pd.date_range(start=start_date, periods=forecast_days, freq='D'), conf_int[:, 0], conf_int[:, 1], color='pink', alpha=0.3, label='Intervalo de Confiança')
    ax.set_xlabel('Data')
    ax.set_ylabel('USD/BRL')
    ax.set_title('Previsão da Cotação do Dólar')
    ax.legend()

    # Ajuste dos rótulos no eixo X
    num_ticks = 6  
    x_ticks = dollar_data['Close'].index[::len(dollar_data) // num_ticks]
    ax.set_xticks(x_ticks)
    ax.xaxis.set_tick_params(rotation=25) 

    # Ajuste do tamanho da fonte
    ax.set_xlabel('Date', fontsize=8)  
    ax.set_ylabel('USD/BRL', fontsize=10)  
    ax.set_title('USD History', fontsize=12) 

    fig.set_figheight(2.025)
    st.pyplot(fig, use_container_width=False)

st.write("Fonte dos dados: Yahoo Finance")
