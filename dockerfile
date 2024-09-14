# Use uma imagem base oficial do Python 3.11
FROM python:3.11-slim

# Instala o compilador Rust (caso necessário para pacotes Python)
RUN apt-get update && apt-get install -y curl \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . "$HOME/.cargo/env"

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Define a variável de ambiente para desabilitar buffering de logs
ENV PYTHONUNBUFFERED=1

# Expor a porta que o Google Cloud Run usa (8080)
EXPOSE 8080

# Executar o Streamlit na porta 8080 e com o endereço 0.0.0.0
CMD ["streamlit", "run", "front_youtube_scripto.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
