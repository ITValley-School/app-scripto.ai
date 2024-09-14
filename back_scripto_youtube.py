from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
from pytube import YouTube
from datetime import datetime

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API do OpenAI a partir do arquivo .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# Verifica se a chave API foi carregada corretamente
if not openai_api_key:
    raise ValueError("A chave da API do OpenAI não foi encontrada. Verifique se o arquivo .env está configurado corretamente.")
else:
    print(f"Chave API OpenAI: {openai_api_key}")  # Verifique a saída no console (remover em produção)

# Configura as embeddings do OpenAI usando a chave API
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

def get_video_metadata(video_url: str):
    """Extrai metadados do vídeo do YouTube usando pytube, com tratamento de exceções e formatação segura."""
    try:
        yt = YouTube(video_url)
    except Exception as e:
        raise ValueError(f"Erro ao carregar o vídeo do YouTube: {e}")

    # Tenta extrair e formatar a data de publicação, com tratamento de exceções
    try:
        publish_date = yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else "Data indisponível"
    except Exception as e:
        print(f"Erro ao processar a data de publicação: {e}")
        publish_date = "Data indisponível"

    # Monta o dicionário com as informações do vídeo
    video_info = {
        "title": yt.title if yt.title else "Título indisponível",
        "channel": yt.author if yt.author else "Canal indisponível",
        "duration": yt.length // 60 if yt.length else 0,  # Duração em minutos, 0 se indisponível
        "publish_date": publish_date,
        "thumbnail_url": yt.thumbnail_url if yt.thumbnail_url else None
    }

    return video_info


def create_vector_from_yt_url(video_url: str) -> FAISS:
    """Cria uma base de vetores FAISS a partir da URL do vídeo do YouTube com tratamento de exceções."""
    try:
        loader = YoutubeLoader.from_youtube_url(video_url, language="pt")
        transcript = loader.load()
        print(f"Transcrição: {transcript}")  # Verifique o conteúdo da transcrição
    except Exception as e:
        raise ValueError(f"Erro ao carregar a transcrição do YouTube: {e}")

    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(transcript)
        print(f"Documentos divididos: {docs}")  # Verifique o conteúdo dos documentos divididos
    except Exception as e:
        raise ValueError(f"Erro ao dividir o texto da transcrição: {e}")

    try:
        # Debug para verificar docs e embeddings antes de criar FAISS
        print(f"Documentos: {docs}")
        print(f"Quantidade de documentos: {len(docs)}")

        db = FAISS.from_documents(docs, embeddings)
        print(f"Base de vetores FAISS criada com sucesso.")
    except Exception as e:
        print(f"Erro: {e}")
        raise ValueError(f"Erro ao criar a base de vetores FAISS: {e}")

    return db, transcript



def format_transcript(transcript):
    """Formata a transcrição com quebras de linha e estrutura, com tratamento de exceções."""
    try:
        formatted_text = "\n".join([t.page_content for t in transcript])
    except Exception as e:
        raise ValueError(f"Erro ao formatar a transcrição: {e}")
    
    return formatted_text


if __name__ == '__main__':
    # Exemplo de uso (você pode alterar conforme necessário)
    video_url = "https://www.youtube.com/watch?v=exemplo"
    
    try:
        metadata = get_video_metadata(video_url)
        print(f"Metadados do vídeo: {metadata}")

        db, transcript = create_vector_from_yt_url(video_url)
        formatted_transcript = format_transcript(transcript)
        print(formatted_transcript)
    except Exception as e:
        print(f"Erro: {e}")
