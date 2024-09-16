import subprocess
import os

# Função para executar um comando no terminal
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode("utf-8"), error.decode("utf-8")

# Diretório do projeto
project_directory = r'C:/LangChain-Projects/ITValley-Python-Projects/scripto.ai'

# Mensagem padrão de commit
default_commit_message = "Commit automático: Ajustes no projeto."

# Função para obter a mensagem de commit
def get_commit_message():
    print("Por favor, insira uma mensagem de commit adicional (pressione Enter para usar a mensagem padrão):")
    additional_message = input().strip()
    if additional_message:
        return f"{default_commit_message} - {additional_message}"
    return default_commit_message

# Função para realizar o commit e push
def git_commit_push():
    try:
        # Navegar para o diretório do projeto
        os.chdir(project_directory)

        # Verificar o status do repositório
        print("Verificando o status do Git...")
        status_output, status_error = run_command("git status")
        print(status_output)

        if "nada a commitar" in status_output.lower():
            print("Nenhuma alteração detectada. Saindo.")
            return

        # Adicionar todos os arquivos
        print("Adicionando arquivos ao staging...")
        add_output, add_error = run_command("git add .")
        if add_error:
            print(f"Erro ao adicionar arquivos: {add_error}")
            return
        print(add_output)

        # Obter a mensagem de commit
        commit_message = get_commit_message()

        # Fazer o commit
        print(f"Fazendo commit: '{commit_message}'...")
        commit_output, commit_error = run_command(f'git commit -m "{commit_message}"')
        if commit_error:
            print(f"Erro ao fazer commit: {commit_error}")
            return
        print(commit_output)

        # Enviar as alterações para o GitHub
        print("Fazendo push para o GitHub...")
        push_output, push_error = run_command("git push origin dev")
        if push_error:
            print(f"Erro ao fazer push: {push_error}")
            return
        print(push_output)

        print("Commit e push realizados com sucesso!")
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Executa a função
if __name__ == "__main__":
    git_commit_push()
