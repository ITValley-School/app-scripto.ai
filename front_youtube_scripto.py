import streamlit as st
import ts_videos_youtube as lch  # Importando o módulo para funções do back-end
from datetime import datetime
import time
from fpdf import FPDF
import os

# Dicionário para armazenar transcrições por ID de arquivo
transcription_cache = {}

# Configuração da página
st.set_page_config(
    page_title="scripto.ai",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

    /* Cor do rótulo (label) "YouTube Video URL" */
    label {
        color: #FFFFFF !important;
    }

    /* Cor do ícone de ajuda "?" */
    .stForm .stTextArea label .stHelp {
        color: #FFFFFF !important;  /* Cor branca para o "?" */
    }

    .stForm .stTextArea label .stHelp:hover::before {
        color: #FFFFFF !important;  /* Cor branca para o "?" */
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

# Adicionando o logo no topo da página com largura ajustada
st.image("it_valley.png", width=150)

# Título principal e subtítulo
st.markdown("<h1 class='main-title'>scripto.ai</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Your YouTube Video Transcript Assistant</h2>", unsafe_allow_html=True)

# Barra lateral com fundo escuro e formulários estilizados
st.sidebar.markdown("<h3>Video Transcription</h3>", unsafe_allow_html=True)

with st.sidebar:
    with st.form(key="my_form"):
        video_url = st.text_area(label="YouTube Video URL", max_chars=200, help="Enter the full URL of the YouTube video.")
        submit_button = st.form_submit_button(label="Transcribe Video")

# Processamento do vídeo e transcrição
if video_url:
    # Início do cronômetro para calcular o tempo de processamento
    start_time = time.time()

    # Mostra um spinner enquanto processa o vídeo
    with st.spinner(f"Transcribing video from {video_url}..."):
        video_info = lch.get_video_metadata(video_url)
        
        # Verificando se a thumbnail está disponível
        thumbnail_url = video_info.get('thumbnail_url')
        if thumbnail_url:
            st.image(thumbnail_url, width=200)
            # Adicionar o link para o vídeo abaixo do thumbnail
            st.markdown(f"[Assistir no YouTube]({video_url})", unsafe_allow_html=True)
        else:
            st.warning("Thumbnail not available")

        # Convertendo a data de publicação para o formato dd-mm-aaaa
        publish_date = datetime.strptime(video_info['publish_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        
        st.markdown(f"<div class='transcription-status'>Transcribing '{video_info['title']}' from channel '{video_info['channel']}'...</div>", unsafe_allow_html=True)

        db, transcript = lch.create_vector_from_yt_url(video_url)

        # Calculando o tempo de processamento
        end_time = time.time()
        processing_time = end_time - start_time

        # Formata e exibe a transcrição
        formatted_transcript = lch.format_transcript(transcript)

        st.markdown("<h3>Video Information</h3>", unsafe_allow_html=True)
        st.write(f"**Title:** {video_info['title']}")
        st.write(f"**Channel:** {video_info['channel']}")
        st.write(f"**Duration:** {video_info['duration']} minutes")
        st.write(f"**Published on:** {publish_date}")  # Data no formato dd-mm-aaaa
        st.write(f"**Processing Time:** {processing_time:.2f} seconds")  # Tempo de processamento da transcrição

        st.markdown("<h3>Transcript</h3>", unsafe_allow_html=True)
        st.text_area(label="", value=formatted_transcript, height=300, key="transcript_area")

        # Botão para download da transcrição
        st.download_button(
            label="Download Raw Transcript",
            data=formatted_transcript,
            file_name=f"{video_info['title']}_transcript.txt",
            mime="text/plain",
        )

        # Botão para download do PDF formatado
        if st.button("Download the styled PDF"):
            # Gerando o PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Adicionando o conteúdo ao PDF
            pdf.multi_cell(0, 10, f"Title: {video_info['title']}\n", align="L")
            pdf.multi_cell(0, 10, f"Channel: {video_info['channel']}\n", align="L")
            pdf.multi_cell(0, 10, f"Duration: {video_info['duration']} minutes\n", align="L")
            pdf.multi_cell(0, 10, f"Published on: {publish_date}\n", align="L")
            pdf.multi_cell(0, 10, f"Processing Time: {processing_time:.2f} seconds\n\n", align="L")
            pdf.multi_cell(0, 10, "Transcript:\n", align="L")
            pdf.multi_cell(0, 10, formatted_transcript, align="L")

            # Salvando o PDF em um buffer como bytes
            pdf_output = pdf.output(dest='S').encode('latin1')  # Converta para bytes com a codificação 'latin1'

            # Botão para fazer o download do PDF
            st.download_button(
                label="Download Styled PDF",
                data=pdf_output,
                file_name=f"{video_info['title']}_transcript.pdf",
                mime="application/pdf",
            )


# Rodapé estilizado
st.markdown(
    """
    <div class="footer">
        © 2024 scripto.ai. All rights reserved.
    </div>
    """, 
    unsafe_allow_html=True,
)

# Garantir que a aplicação escute na porta 8080 ao ser implantada no Google Cloud Run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    st._is_running_with_streamlit = False
    os.system(f"streamlit run front_youtube_scripto.py --server.port {port}")
