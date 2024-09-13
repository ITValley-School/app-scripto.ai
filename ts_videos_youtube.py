from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
from pytube import YouTube

# Carrega as variáveis de ambiente
load_dotenv()

# Obtém a chave da API do OpenAI a partir do arquivo .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# Configura as embeddings do OpenAI usando a chave API
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

def get_video_metadata(video_url: str):
    """Extrai metadados do vídeo do YouTube usando pytube."""
    yt = YouTube(video_url)
    video_info = {
        "title": yt.title,
        "channel": yt.author,
        "duration": yt.length // 60,  # Duração em minutos
        "publish_date": yt.publish_date.strftime('%Y-%m-%d'),
        "thumbnail_url": yt.thumbnail_url  # Adiciona a URL da thumbnail
    }
    return video_info

def create_vector_from_yt_url(video_url: str) -> FAISS:
    """Cria uma base de vetores FAISS a partir da URL do vídeo do YouTube."""
    loader = YoutubeLoader.from_youtube_url(video_url, language="pt")
    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    db = FAISS.from_documents(docs, embeddings)
    return db, transcript

def format_transcript(transcript):
    """Formata a transcrição com quebras de linha e estrutura."""
    formatted_text = "\n".join([t.page_content for t in transcript])
    return formatted_text
