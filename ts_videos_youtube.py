from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
from pytube import YouTube

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
    """Extrai metadados do vídeo do YouTube usando pytube."""
    yt = YouTube(video_url)
    
    # Verifica se publish_date está disponível, caso contrário define um valor padrão
    publish_date = yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else "Data indisponível"
    
    video_info = {
        "title": yt.title,
        "channel": yt.author,
        "duration": yt.length // 60,  # Duração em minutos
        "publish_date": publish_date,  # Usa a data formatada ou uma mensagem padrão
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

if __name__ == '__main__':
    # Exemplo de uso (você pode alterar conforme necessário)
    video_url = "https://www.youtube.com/watch?v=exemplo"
    metadata = get_video_metadata(video_url)
    print(f"Metadados do vídeo: {metadata}")
    
    db, transcript = create_vector_from_yt_url(video_url)
    formatted_transcript = format_transcript(transcript)
    print(formatted_transcript)
