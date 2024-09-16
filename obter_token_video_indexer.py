import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Certifique-se de que a configuração da página seja a primeira função Streamlit
st.set_page_config(
    page_title="Your Azure Video Transcript Assistant",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carrega as variáveis do arquivo .env
load_dotenv()

# Função para obter o token do Azure AD
def obter_token_azure():
    url = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("AZURE_CLIENT_ID"),
        "client_secret": os.getenv("AZURE_CLIENT_SECRET"),
        "scope": "https://management.azure.com/.default"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        st.error("Erro ao obter token do Azure AD.")
        return None

# Função para obter o token do Video Indexer
def obter_token_video_indexer(subscription_id, resource_group, account_name, access_token):
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.VideoIndexer/accounts/{account_name}/generateAccessToken?api-version=2024-01-01"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    body = {
        "permissionType": "Contributor",
        "scope": "Account"
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        token = response.json().get("accessToken")
        return token
    else:
        st.error("Erro ao obter token do Video Indexer.")
        return None

# Função para buscar o thumbnail do vídeo
def buscar_thumbnail_video(video_id, thumbnail_id, access_token, location, account_id):
    url_thumbnail = f"https://api.videoindexer.ai/{location}/Accounts/{account_id}/Videos/{video_id}/Thumbnails/{thumbnail_id}?format=Jpeg&accessToken={access_token}"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url_thumbnail, headers=headers)

    if response.status_code == 200:
        return response.content  # Retorna o conteúdo da imagem
    else:
        st.error(f"Erro ao buscar o thumbnail: {response.status_code}")
        return None

# Função para buscar a transcrição do vídeo e metadados
def buscar_transcricao_video(video_id, access_token, location, account_id):
    # URL para obter a transcrição
    url_transcription = f"https://api.videoindexer.ai/{location}/Accounts/{account_id}/Videos/{video_id}/Captions"
    
    params = {
        "format": "srt",
        "language": "pt-BR",
        "accessToken": access_token
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url_transcription, headers=headers, params=params)

    if response.status_code == 200:
        response.encoding = 'utf-8'
        transcription = response.text
    else:
        st.error(f"Erro ao buscar a transcrição: {response.status_code}")
        return None, None

    # URL para obter os metadados do vídeo
    url_metadata = f"https://api.videoindexer.ai/{location}/Accounts/{account_id}/Videos/{video_id}/Index"
    metadata_response = requests.get(url_metadata, headers=headers)

    if metadata_response.status_code == 200:
        video_metadata = metadata_response.json()
        video_info = {
            'title': video_metadata.get('name', 'N/A'),
            'duration': round(video_metadata.get('durationInSeconds', 0) / 60, 2),  # Convertendo de segundos para minutos e arredondando
            'thumbnail_url': f"https://api.videoindexer.ai/{location}/Accounts/{account_id}/Videos/{video_id}/Thumbnails/{video_metadata.get('thumbnailId', '')}?format=Jpeg&accessToken={access_token}",  # Certificando-se que é .jpeg
            'thumbnail_id': video_metadata.get('thumbnailId', '')
        }
    else:
        st.error(f"Erro ao buscar os metadados do vídeo: {metadata_response.status_code}")
        return transcription, None

    return transcription, video_info

# Interface Streamlit
st.title("Your Azure Video Transcript Assistant")
video_identifier = st.text_input("Enter Video ID")

if st.button("Transcribe Video"):
    subscription_id = os.getenv('subscriptionId')
    resource_group = os.getenv('resourceGroupName')
    account_name = os.getenv('accountname')
    location = os.getenv('location')
    account_id = os.getenv('accountId')

    azure_access_token = obter_token_azure()
    if azure_access_token:
        video_indexer_token = obter_token_video_indexer(subscription_id, resource_group, account_name, azure_access_token)
        if video_indexer_token:
            transcricao, video_info = buscar_transcricao_video(video_identifier, video_indexer_token, location, account_id)

            if transcricao:
                st.markdown(f"**Title:** {video_info['title']}")
                st.markdown(f"**Duration:** {video_info['duration']} minutes")

                # Buscar e exibir o thumbnail
                if video_info['thumbnail_id']:
                    thumbnail_image = buscar_thumbnail_video(video_identifier, video_info['thumbnail_id'], video_indexer_token, location, account_id)
                    if thumbnail_image:
                        st.image(thumbnail_image, caption="Thumbnail", use_column_width=True)
                    else:
                        st.error("Erro ao carregar o thumbnail.")
                else:
                    st.error("Thumbnail não disponível.")

                st.text_area("Transcript", transcricao, height=300)