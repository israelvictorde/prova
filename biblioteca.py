from pymongo import MongoClient
from datetime import datetime
from tabulate import tabulate

# Conectar ao MongoDB (ajuste a URI se estiver usando um banco de dados na nuvem)
client = MongoClient('mongodb+srv://israel2005:rockacdc19@cluster0.weqoz.mongodb.net/')
db = client['aula']

# Coleções
livros_collection = db['livros']
usuarios_collection = db['usuarios']
emprestimos_collection = db['emprestimos']

# Funções CRUD para Livros

def adicionar_livro():
    isbn = input("Digite o ISBN do livro: ")
    titulo = input("Digite o título do livro: ")
    autor = input("Digite o nome do autor: ")
    ano = int(input("Digite o ano de publicação: "))
    
    livro = {
        "_id": isbn,
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "disponivel": True
    }
    livros_collection.insert_one(livro)
    print(f"Livro '{titulo}' adicionado com sucesso.")

def listar_livros():
    livros = list(livros_collection.find())
    if livros:
        tabela = [[livro['_id'], livro['titulo'], livro['autor'], livro['ano'], "Sim" if livro['disponivel'] else "Não"] for livro in livros]
        print(tabulate(tabela, headers=["ISBN", "Título", "Autor", "Ano", "Disponível"], tablefmt="pretty"))
    else:
        print("Nenhum livro encontrado.")

def atualizar_livro():
    isbn = input("Digite o ISBN do livro que deseja atualizar: ")
    titulo = input("Novo título (ou enter para manter o atual): ")
    autor = input("Novo autor (ou enter para manter o atual): ")
    ano = input("Novo ano (ou enter para manter o atual): ")
    
    atualizacoes = {}
    if titulo:
        atualizacoes["titulo"] = titulo
    if autor:
        atualizacoes["autor"] = autor
    if ano:
        atualizacoes["ano"] = int(ano)

    if atualizacoes:
        livros_collection.update_one({"_id": isbn}, {"$set": atualizacoes})
        print(f"Livro {isbn} atualizado com sucesso.")
    else:
        print("Nenhuma atualização fornecida.")

def remover_livro():
    isbn = input("Digite o ISBN do livro que deseja remover: ")
    livros_collection.delete_one({"_id": isbn})
    print(f"Livro {isbn} removido com sucesso.")

# Funções CRUD para Usuários

def adicionar_usuario():
    user_id = input("Digite o ID do usuário: ")
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o e-mail do usuário: ")
    telefone = input("Digite o telefone do usuário: ")
    
    usuario = {
        "_id": user_id,
        "nome": nome,
        "email": email,
        "telefone": telefone
    }
    usuarios_collection.insert_one(usuario)
    print(f"Usuário '{nome}' adicionado com sucesso.")

def listar_usuarios():
    usuarios = list(usuarios_collection.find())
    if usuarios:
        tabela = [[usuario['_id'], usuario['nome'], usuario['email'], usuario['telefone']] for usuario in usuarios]
        print(tabulate(tabela, headers=["ID Usuário", "Nome", "Email", "Telefone"], tablefmt="pretty"))
    else:
        print("Nenhum usuário encontrado.")

def atualizar_usuario():
    user_id = input("Digite o ID do usuário que deseja atualizar: ")
    nome = input("Novo nome (ou enter para manter o atual): ")
    email = input("Novo email (ou enter para manter o atual): ")
    telefone = input("Novo telefone (ou enter para manter o atual): ")
    
    atualizacoes = {}
    if nome:
        atualizacoes["nome"] = nome
    if email:
        atualizacoes["email"] = email
    if telefone:
        atualizacoes["telefone"] = telefone

    if atualizacoes:
        usuarios_collection.update_one({"_id": user_id}, {"$set": atualizacoes})
        print(f"Usuário {user_id} atualizado com sucesso.")
    else:
        print("Nenhuma atualização fornecida.")

def remover_usuario():
    user_id = input("Digite o ID do usuário que deseja remover: ")
    usuarios_collection.delete_one({"_id": user_id})
    print(f"Usuário {user_id} removido com sucesso.")

# Funções de Empréstimo

def registrar_emprestimo():
    livro_id = input("Digite o ISBN do livro: ")
    usuario_id = input("Digite o ID do usuário: ")

    # Verifica se o livro está disponível
    livro = livros_collection.find_one({"_id": livro_id})
    if not livro or not livro['disponivel']:
        print(f"Livro {livro_id} não está disponível para empréstimo.")
        return
    
    # Cria o registro de empréstimo
    emprestimo = {
        "livro_id": livro_id,
        "usuario_id": usuario_id,
        "data_emprestimo": datetime.now().strftime("%Y-%m-%d"),
        "data_devolucao": None
    }
    emprestimos_collection.insert_one(emprestimo)
    
    # Atualiza o status de disponibilidade do livro
    livros_collection.update_one({"_id": livro_id}, {"$set": {"disponivel": False}})
    print(f"Empréstimo do livro {livro_id} registrado para o usuário {usuario_id}.")

def registrar_devolucao():
    livro_id = input("Digite o ISBN do livro: ")
    
    # Verifica o empréstimo ativo
    emprestimo = emprestimos_collection.find_one({"livro_id": livro_id, "data_devolucao": None})
    if not emprestimo:
        print(f"Não há empréstimo ativo para o livro {livro_id}.")
        return
    
    # Atualiza a data de devolução
    emprestimos_collection.update_one({"_id": emprestimo["_id"]}, {"$set": {"data_devolucao": datetime.now().strftime("%Y-%m-%d")}})
    
    # Marca o livro como disponível novamente
    livros_collection.update_one({"_id": livro_id}, {"$set": {"disponivel": True}})
    print(f"Devolução do livro {livro_id} registrada com sucesso.")

def listar_emprestimos():
    emprestimos = list(emprestimos_collection.find())
    if emprestimos:
        tabela = [[emprestimo['livro_id'], emprestimo['usuario_id'], emprestimo['data_emprestimo'], emprestimo['data_devolucao'] or "Em andamento"] for emprestimo in emprestimos]
        print(tabulate(tabela, headers=["ID Livro", "ID Usuário", "Data Empréstimo", "Data Devolução"], tablefmt="pretty"))
    else:
        print("Nenhum empréstimo encontrado.")

# Menu interativo
def menu():
    while True:
        print("\n Biblioteca")
        print("1. Adicionar Livro")
        print("2. Listar Livros")
        print("3. Atualizar Livro")
        print("4. Remover Livro")
        print("5. Adicionar Usuário")
        print("6. Listar Usuários")
        print("7. Atualizar Usuário")
        print("8. Remover Usuário")
        print("9. Registrar Empréstimo")
        print("10. Registrar Devolução")
        print("11. Listar Empréstimos")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_livro()
        elif opcao == "2":
            listar_livros()
        elif opcao == "3":
            atualizar_livro()
        elif opcao == "4":
            remover_livro()
        elif opcao == "5":
            adicionar_usuario()
        elif opcao == "6":
            listar_usuarios()
        elif opcao == "7":
            atualizar_usuario()
        elif opcao == "8":
            remover_usuario()
        elif opcao == "9":
            registrar_emprestimo()
        elif opcao == "10":
            registrar_devolucao()
        elif opcao == "11":
            listar_emprestimos()
        elif opcao == "0":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executa o menu
menu()