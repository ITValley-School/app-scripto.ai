from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Verifica se as variáveis estão sendo carregadas corretamente
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
tenant_id = os.getenv('AZURE_TENANT_ID')

if client_id and client_secret and tenant_id:
    print("As variáveis de ambiente foram carregadas corretamente:")
    print(f"AZURE_CLIENT_ID: {client_id}")
    print(f"AZURE_CLIENT_SECRET: {client_secret}")
    print(f"AZURE_TENANT_ID: {tenant_id}")
else:
    print("Erro: algumas variáveis de ambiente não estão configuradas.")
