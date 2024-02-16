# Use a imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Crie e ative o ambiente virtual
RUN python3 -m venv /venv
RUN /venv/bin/pip install --upgrade pip

# Instale as dependências
RUN /venv/bin/pip install -r requirements.txt

# Copie o restante do projeto para o diretório de trabalho
COPY . .

# Exponha a porta em que o servidor Streamlit está escutando
EXPOSE 80

# Execute o comando para iniciar o servidor Stremalit
CMD ["/venv/bin/streamlit", "run", "--server.port", "80", "app.py"]
