import streamlit as st
from token_azure import obter_token_azure  # Certifique-se de que o arquivo token_azure.py está no mesmo diretório
from obter_token_video_indexer import obter_token_video_indexer, buscar_transcricao_video  # Mesmo diretório
from dotenv import load_dotenv
import os
import time

# Configuração da página
st.set_page_config(
    page_title="scripto.ai",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Carrega as variáveis do arquivo .env
load_dotenv()

# Aplicar estilos personalizados com base nas cores da imagem de referência
st.markdown(
    """
    <style>
    /* Fundo em gradiente inspirado na imagem de referência */
    body, .stApp {
        background: linear-gradient(135deg, #2C2C54, #6A0572, #1B1464) !important;
        color: #FFFFFF !important;
        font-family: 'Arial', sans-serif;
    }

    /* Título principal */
    .main-title {
        font-size: 3em;
        color: #E0E0FF !important;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px #000000;
    }

    /* Subtítulo */
    .subtitle {
        font-size: 1.5em;
        color: #D4D4FF !important;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #1B1464 !important;  /* Azul escuro */
        color: #FFFFFF !important;
    }

    .stTextArea textarea {
        background-color: #2C2C54 !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: 1px solid #9159A9;
    }

    /* Ajuste da cor do placeholder e do texto da URL na barra lateral */
    .stTextArea textarea::placeholder,
    .stTextArea textarea {
        color: #D4D4FF !important;
    }

    /* Cor do rótulo (label) */
    label {
        color: #FFFFFF !important;
    }

    /* Botões */
    .stButton button {
        background: linear-gradient(90deg, #8A2BE2, #6A5ACD) !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        transition: background-color 0.3s ease;
    }

    .stButton button:hover {
        background-color: #4B0082 !important;
        color: #FFFFFF !important;
    }

    /* Cabeçalhos de seção */
    h3 {
        color: #D4D4FF !important;
    }

    /* Rodapé */
    .footer {
        text-align: center;
        padding: 10px;
        margin-top: 20px;
        font-size: 0.9em;
        color: #CCCCFF !important;
        border-top: 1px solid #9159A9;
    }

    /* Mensagens de transcrição */
    .transcription-status {
        color: #FFFFFF !important;
        background-color: #3B136B !important;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }

    /* Ajuste na cor dos textos */
    .stMarkdown, .stMarkdown h3 {
        color: #D4D4FF !important;
    }

    .stTextArea textarea::placeholder {
        color: #CCCCFF !important;
    }

    /* Ajuste da cor do botão de download */
    .stDownloadButton button {
        background-color: #4B0082 !important;
        color: #FFFFFF !important;
        border-radius: 8px;
    }
    
    .stDownloadButton button:hover {
        background-color: #6A5ACD !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Título principal e subtítulo
st.markdown("<h1 class='main-title'>scripto.ai</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Your Azure Video Transcript Assistant</h2>", unsafe_allow_html=True)

# Carregar o logo da IT Valley
logo_path = "it_valley.png"  # Certifique-se de que o logo está no mesmo diretório
st.sidebar.image(logo_path, use_column_width=True)

# Barra lateral com fundo escuro e formulários estilizados
st.sidebar.markdown("<h3>Video Transcription</h3>", unsafe_allow_html=True)

with st.sidebar:
    with st.form(key="my_form"):
        video_identifier = st.text_area(label="Video ID", max_chars=200, help="Enter the Video ID.")
        submit_button = st.form_submit_button(label="Transcribe Video")

# Processamento do vídeo e transcrição
if submit_button and video_identifier:
    # Início do cronômetro para calcular o tempo de processamento
    start_time = time.time()

    with st.spinner(f"Fetching and transcribing video ID {video_identifier}..."):
        # 1. Obter o token do Azure
        access_token_azure = obter_token_azure()
        if not access_token_azure:
            st.error("Erro ao obter o token do Azure.")
            st.stop()

        # 2. Obter o token do Video Indexer
        subscription_id = os.getenv('subscriptionId')
        resource_group = os.getenv('resourceGroupName')
        account_name = os.getenv('accountname')
        location = os.getenv('location')
        account_id = os.getenv('accountId')

        video_indexer_token = obter_token_video_indexer(subscription_id, resource_group, account_name, access_token_azure)
        if not video_indexer_token:
            st.error("Erro ao obter o token do Video Indexer.")
            st.stop()

        # 3. Buscar a transcrição do vídeo e metadados
        transcription, video_info = buscar_transcricao_video(video_identifier, video_indexer_token, location, account_id)

        if transcription:
            # Calculando o tempo de processamento
            end_time = time.time()
            processing_time = end_time - start_time

            # Exibe informações do vídeo
            st.markdown(f"<h3 style='color: #D4D4FF;'>Video Information</h3>", unsafe_allow_html=True)
            st.write(f"**Title:** {video_info['title']}")
            st.write(f"**Duration:** {video_info['duration']} minutes")

            # Exibe a transcrição
            st.markdown("<h3 style='color: #D4D4FF;'>Transcript</h3>", unsafe_allow_html=True)
            st.text_area("", transcription, height=400)

            # Exibe o tempo de processamento
            st.write(f"**Processing Time:** {processing_time:.2f} seconds")

            # Botão para download da transcrição
            st.download_button(
                label="Download Transcript",
                data=transcription,
                file_name=f"transcript_{video_identifier}.txt",
                mime="text/plain",
            )
        else:
            st.error("Transcription not available or an error occurred.")

# Rodapé estilizado
st.markdown(
    """
    <div class="footer">
        © 2024 scripto.ai. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
