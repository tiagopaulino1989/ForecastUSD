import streamlit as st
st.set_page_config(layout="wide")
st.title("Documentação dos Parâmetros e Teste ADF")

st.divider()
st.header("Parâmetros do Modelo ARIMA")
st.markdown("O Modelo ARIMA (AutoRegressive Integrated Moving Average) é amplamente utilizado para previsão de séries temporais. "
            "Aqui estão os principais parâmetros que você pode configurar:")

st.subheader("Ordem do Termo Autoregressivo (p):")
st.markdown("Isso representa a quantidade de períodos anteriores que serão usados para prever o valor futuro da série temporal. "
            "Um valor maior de 'p' indica que o modelo levará em consideração mais períodos passados para fazer a previsão.")

st.subheader("Ordem de Diferenciação (d):")
st.markdown("Isso está relacionado à quantidade de vezes que a série temporal é diferenciada para torná-la estacionária. "
            "Diferenciação é uma técnica para remover tendências e fazer com que a série seja mais previsível. "
            "Um valor maior de 'd' significa que a série será mais diferenciada.")

st.subheader("Ordem do Termo de Média Móvel (q):")
st.markdown("Isso indica quantos erros passados afetarão as previsões futuras. A média móvel modela a relação entre "
            "um erro anterior e um valor atual da série temporal. Um valor maior de 'q' considera mais erros passados.")

st.divider()
st.header("Teste ADF (Augmented Dickey-Fuller)")
st.markdown("O Teste ADF é usado para determinar se a série temporal é estacionária após a diferenciação. "
            "Aqui estão os principais resultados do teste:")

st.subheader("Teste ADF após diferenciação:")
st.markdown("Este é um teste estatístico chamado Teste ADF (Augmented Dickey-Fuller). É usado para determinar se a série "
            "temporal é estacionária após a diferenciação. Se o valor de 'p-valor' for menor ou igual a 0,05, "
            "a série é considerada estacionária, o que é uma condição desejável para a modelagem.")

st.subheader("Statistic:")
st.markdown("É o valor estatístico calculado pelo Teste ADF. Quanto mais negativo esse valor for, mais forte é a evidência "
            "de que a série é estacionária.")

st.subheader("P-value:")
st.markdown("Este valor é usado para determinar a significância estatística do teste. Um valor baixo (geralmente menor ou igual a 0,05) "
            "indica que a série é estacionária.")

st.subheader("Critical Values:")
st.markdown("São os valores críticos que servem como referência para a decisão do teste ADF. Se o valor estatístico for menor "
            "do que esses valores críticos, a série é considerada estacionária.")
