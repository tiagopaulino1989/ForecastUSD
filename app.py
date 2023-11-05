import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt    
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .st-ewNlD {
        background: var(--slider-fill-color);
    }
    .stSlider-9eymE {
        background: var(--slider-handle-color);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Forecast USD time series")

# Sidebar 
start_date = st.sidebar.date_input("Set initial data: ", datetime.today() - timedelta(15) )
forecast_days = st.sidebar.slider("Forecast Days (1-60)", min_value=1, max_value=30, value=7)

st.sidebar.header("Configuração do Modelo ARIMA")
p = st.sidebar.slider("Ordem do Termo Autoregressivo (p):", 0, 5, 3)
d = st.sidebar.slider("Ordem de Diferenciação (d):", 0, 3, 1)
q = st.sidebar.slider("Ordem do Termo de Média Móvel (q):", 0, 8, 7)

def get_dollar_data(start_date, end_date):
    df = yf.download('USDBRL=X', start=start_date, end=end_date)
    return df

# Obter dados do Yahoo Finance 
end_date = datetime.today()
dollar_data = get_dollar_data(start_date, end_date)

# Verificar a estacionariedade da série temporal
result = adfuller(dollar_data['Close'])

# Aplicar a diferenciação para tornar a série estacionária
dollar_data_diff = dollar_data['Close'].diff().dropna()
result_diff = adfuller(dollar_data_diff)

# Treinar o modelo ARIMA
model = ARIMA(dollar_data['Close'], order=(p, d, q))
model_fit = model.fit()

# Fazer a previsão para os próximos 45 dias
forecast_index = pd.date_range(start=dollar_data.index[-1] + pd.Timedelta(days=1), periods=forecast_days, freq='D')
forecast = model_fit.forecast(steps=forecast_days)


# Criar um DataFrame para o gráfico Altair
df = pd.DataFrame({'Data': list(dollar_data['Close'].index) + list(forecast_index),
                    'Valor': list(dollar_data['Close']) + list(forecast),
                    'Tipo': ['Histórico'] * len(dollar_data['Close']) + ['Previsão'] * len(forecast)})

min_value = df['Valor'].min() - 0.02
max_value = df['Valor'].max() + 0.02

# Criar o gráfico Altair
chart = alt.Chart(df).mark_line().encode(
    x='Data:T',
    y=alt.Y('Valor:Q', scale=alt.Scale(domain=[min_value, max_value])),
    color='Tipo:N'
).properties(
    width=1100,
    height=350
)

st.altair_chart(chart)


st.divider()
st.write("Teste ADF após diferenciação:")
st.write(f"Statistic: {result_diff[0]}")
st.write(f"P-value: {result_diff[1]}")
st.write(f"Critical Values: {result_diff[4]}")

st.divider()
st.write("Criado por Tiago Paulino | https://www.linkedin.com/in/tiago-paulino-ds | Dados: Yahoo Finance")
