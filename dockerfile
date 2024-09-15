# Use a imagem base oficial do Python 3.11
FROM python:3.11-slim

# Instale o Git e apt-utils, e limpe o cache do apt após a instalação
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    apt-utils \
  && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt para o container
COPY requirements.txt .

# Atualiza o pip para a versão mais recente
RUN pip install --upgrade pip

# Instala as dependências do Python sem cache para reduzir o tamanho da imagem
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o container
COPY . .

# Define a variável de ambiente para desabilitar buffering de logs
ENV PYTHONUNBUFFERED=1

# Expor a porta que será usada (Cloud Run define via variável de ambiente)
EXPOSE 8080

# Comando para rodar o Streamlit, definindo a porta a partir da variável de ambiente PORT (fallback para 8080)
CMD ["sh", "-c", "streamlit run front_youtube_scripto.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]
