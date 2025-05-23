import json
import statistics
import hashlib
import re
import shutil
import matplotlib.pyplot as plt
# Funções de segurança

def gerar_grafico():
    usuarios = carregar_dados()

    if not usuarios:
        print("Nenhum usuário cadastrado para gerar gráficos.")
        return
    
    nomes = [user["nome"] for user in usuarios]
    idades = [user["idade"] for user in usuarios]
    acessos = [user["acessos"] for user in usuarios]
    tempos = [user["tempo_uso"] for user in usuarios]

     # Gráfico 1 - Acessos por usuário (barras)
    plt.figure(figsize=(10, 5))
    plt.bar(nomes, acessos, color="blue")
    plt.title("Número de Acessos por Usuário")
    plt.xlabel("Usuário")
    plt.ylabel("Acessos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Gráfico 2 - Tempo de uso por usuário (linha)
    plt.figure(figsize=(10, 5))
    plt.plot(nomes, tempos, marker="o", color="green")
    plt.title("Tempo Médio de Uso por Usuário")
    plt.xlabel("Usuário")
    plt.ylabel("Tempo de Uso (h)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Gráfico 3 - Distribuição das idades (histograma)
    plt.figure(figsize=(8, 5))
    plt.hist(idades, bins=8, color="purple", edgecolor="black")
    plt.title("Distribuição de Idades dos Usuários")
    plt.xlabel("Idade")
    plt.ylabel("Quantidade")
    plt.tight_layout()
    plt.show()

#Função de login: ela verifica se o nome de usuário e a senha (em hash) estão corretos
def login():
    usuarios = carregar_dados()
    usuario_input = input("Digite seu nome de usuário: ")
    senha_input = input("Digite sua senha: ")
    senha_hash = hash_senha(senha_input)

    for usuario in usuarios:
        if usuario["nome"] == usuario_input and usuario["senha"] == senha_hash:
            print(f"\nLogin realizado com sucesso. Bem-vindo(a), {usuario['nome']}!")
            return True
    print("\nUsuário ou senha incorretos.")
    return False

#Função que verifica se a senha atende aos critérios de segurança
def senha_forte(senha):
    return (
        len(senha) >= 8 and
        re.search(r'[A-Z]', senha) and
        re.search(r'[a-z]', senha) and
        re.search(r'[0-9]', senha) and
        re.search(r'[!@#$%^&*()_+-]', senha)
    )

#Função que aplica hash SHA-256 a senha para proteger no armazenamento
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

#Função que exibe uma dica educativa sobre segurança digital
def alerta_pishing():
    print("\nDICA DE SEGURANÇA:")
    print("Nunca compartilhe sua senha e desconfie de e-mails ou mensagens suspeitas pedindo informações pessoais.")

# Arquivos

# Carrega os dados do arquivo JSON com os usuários
def carregar_dados():
    try:
        with open("usuarios.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

# Salva os dados atualizados no arquivo JSON
def salvar_dados(usuarios):
    with open("usuarios.json", "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)

# Cria uma cópia de backup do arquivo de dados dos usuários
def fazer_backup():
    try:
        shutil.copy("usuarios.json", "usuarios_backup.json")
        print("Backup realizado com sucesso!")
    except FileNotFoundError:
        print("Arquivo original não encontrado para backup.")

# Aplicativo

# Adiciona um novo usuário, valida a senha e salva os dados com segurança no JSON
def adicionar_usuario():
    nome = input("Nome de usuário: ")
    idade = int(input("Idade: "))
    tempo_uso = float(input("Tempo médio de uso (horas): "))
    acessos = int(input("Número de acessos: "))

    while True:
        senha = input("Crie uma senha forte: ")
        if senha_forte(senha):
            break
        print("Senha fraca. Use pelo menos 8 caracteres, com letras maiúsculas, minúsculas, números e símbolos.")

    senha_hash = hash_senha(senha)

    usuarios = carregar_dados()
    usuarios.append({
        "nome": nome,
        "senha": senha_hash,
        "idade": idade,
        "tempo_uso": tempo_uso,
        "acessos": acessos,
    })

    salvar_dados(usuarios)
    print("Usuário cadastrado com sucesso!")

#Exibe as estatísticas com base nos dados dos usuários da plataforma
def mostrar_estatísticas():
    usuarios = carregar_dados()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    idades = [user["idade"] for user in usuarios]
    tempos = [user["tempo_uso"] for user in usuarios]
    acessos = [user["acessos"] for user in usuarios]

    print("\nEstatísticas da Plataforma:")
    print(f"Média de Idade: {statistics.mean(idades):.2f}")
    print(f"Moda de Idade: {statistics.mode(idades):.2f}")
    print(f"Médiana de Idade: {statistics.median(idades):.2f}")

    print(f"Média de acessos: {statistics.mean(acessos):.2f}")
    print(f"Moda de acessos: {statistics.mode(acessos):.2f}")
    print(f"Médiana de acessos: {statistics.median(acessos):.2f}")

    print(f"Média de tempo de uso: {statistics.mean(tempos):.2f}")
    print(f"Moda de tempo de uso: {statistics.mode(tempos):.2f}")
    print(f"Médiana de tempo de uso: {statistics.median(tempos):.2f}")

# Menu principal do sistema 
def menu():
    alerta_pishing()
    logado = False

    while True:
        print("\n1. Adicionar Usuário")
        print("2. Login")
        print("3. Mostrar Estatísticas (somente se logado)")
        print("4. Fazer Backup dos Dados (somente se logado)")
        print("5. Visualizar Gráficos (somente logado)")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_usuario()
        elif opcao == "2":
            logado = login()
        elif opcao == "3":
            if logado:
                mostrar_estatísticas()
            else:
                print("Você precisa estar logado para acessar esta área.")
        elif opcao == "4":
            if logado:
                fazer_backup()
            else:
                print("Você precisa estar logado para acessar esta área.")
        elif opcao =="5":
            if logado:
                gerar_grafico()
            else:
                print("Você precisa estar logado para acessar os gráficos.")
        elif opcao == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente!")

# Ponto de entrada
if __name__ == "__main__":
    menu()
