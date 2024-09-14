# Use a imagem base oficial do Python 3.11
FROM python:3.11-slim

# Instale o Git
RUN apt-get update && apt-get install -y git

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

# Expor a porta que será usada (Cloud Run define via variável de ambiente)
EXPOSE 8080

# Executar o Streamlit na porta definida pela variável PORT ou usar 8080 como fallback
CMD ["sh", "-c", "streamlit run front_youtube_scripto.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]
