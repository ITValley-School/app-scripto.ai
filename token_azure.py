import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Função para obter o token do Azure AD
def obter_token_azure():
    url = "https://login.microsoftonline.com/{}/oauth2/v2.0/token".format(os.getenv("AZURE_TENANT_ID"))
    
    # Carregando variáveis do .env
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    scope = "https://management.azure.com/.default"
    
    # Exibindo os logs das variáveis (somente client_id e scope, por segurança)
    print(f"Parâmetros enviados para obter o token:")
    print(f"client_id: {client_id}")
    print(f"scope: {scope}")
    
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    print("Enviando solicitação para obter o token do Azure...")
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        print("Token do Azure obtido com sucesso!")
        print(f"Token: {token}")  # Exibindo o token obtido (cuidado com isso em produção)
        return token
    else:
        print(f"Erro ao obter o token: {response.status_code}, {response.text}")
        return None

# Exemplo de uso
if __name__ == "__main__":
    obter_token_azure()
