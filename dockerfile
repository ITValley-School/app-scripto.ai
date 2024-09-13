# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Instala o compilador Rust
RUN apt-get update && apt-get install -y curl \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . "$HOME/.cargo/env"

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o contêiner
COPY . .

# Define a variável de ambiente para desabilitar buffering de logs
ENV PYTHONUNBUFFERED=1

# Expõe a porta 8080 (porta padrão do Google Cloud Run)
EXPOSE 8080

# Define o comando para iniciar o Streamlit na porta 8080 e com o endereço 0.0.0.0
CMD ["streamlit", "run", "front_youtube_scripto.py", "--server.port", "8080", "--server.address", "0.0.0.0"]

# Copia o logo para o contêiner
COPY it_valley.png /app/

# Definir variáveis de ambiente para o Streamlit
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

