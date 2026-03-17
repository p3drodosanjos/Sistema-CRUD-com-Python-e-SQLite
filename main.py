import sqlite3
import os

# Essa função garante que o Python encontre o arquivo na pasta correta
def conectar():
    # Pega o caminho absoluto da pasta onde o script está rodando
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, 'voluntarios.db')
    
    return sqlite3.connect(caminho_banco)

# Testando a conexão
try:
    conn = conectar()
    print("🚀 Conexão com o banco do SQLite Online estabelecida com sucesso!")
    
    # Vamos listar as tabelas que você criou no site para confirmar
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    
    print(f"Tabelas encontradas: {tabelas}")
    
    conn.close()
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")


# --- CONFIGURAÇÃO DE CONEXÃO ---
def conectar():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, 'voluntarios.db')
    return sqlite3.connect(caminho_banco)

# --- FUNÇÃO CREATE (C) ---
def cadastrar_voluntario():
    print("\n" + "="*30)
    print(" NOVO CADASTRO ")
    print("="*30)
    
    nome = input("Nome completo: ")
    email = input("E-mail: ")
    habilidade = input("Habilidade (ex: TI, Cozinha): ")
    disponibilidade = input("Disponibilidade (ex: Manhã): ")

    conn = conectar()
    cursor = conn.cursor()

    try:
        sql = '''INSERT INTO voluntarios (nome, email, habilidade_principal, disponibilidade)
                 VALUES (?, ?, ?, ?)'''
        cursor.execute(sql, (nome, email, habilidade, disponibilidade))
        conn.commit()
        print(f"\n✅ {nome} cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("\n❌ Erro: Este e-mail já existe no sistema.")
    finally:
        conn.close()

        # --- FUNÇÃO READ (R) ---
def listar_voluntarios():
    print("\n" + "="*40)
    print(" LISTA DE VOLUNTÁRIOS CADASTRADOS ")
    print("="*40)

    conn = conectar()
    cursor = conn.cursor()

    try:
        # Comando SQL para buscar todos os dados da tabela
        cursor.execute("SELECT id_voluntario, nome, email, habilidade_principal, disponibilidade FROM voluntarios")
        
        # Pega todos os resultados que o cursor achou e guarda numa lista
        lista_voluntarios = cursor.fetchall()

        # Verifica se a lista está vazia
        if len(lista_voluntarios) == 0:
            print("Nenhum voluntário cadastrado ainda.")
        else:
            # Passa por cada voluntário na lista e imprime na tela
            for vol in lista_voluntarios:
                # vol[0] é o id, vol[1] é o nome, e assim por diante...
                print(f"ID: {vol[0]}")
                print(f"Nome: {vol[1]} | E-mail: {vol[2]}")
                print(f"Habilidade: {vol[3]} | Disp: {vol[4]}")
                print("-" * 40) # Linha separadora para ficar organizado

    except Exception as e:
        print(f"\n❌ Erro ao buscar os dados: {e}")
    finally:
        conn.close()

# --- MENU PRINCIPAL ---
def menu():
    while True:
        print("\n--- SISTEMA DE GESTÃO DE VOLUNTÁRIOS ---")
        print("1. Cadastrar Voluntário (Create)")
        print("2. Listar Voluntários (Read)")
        print("3. Atualizar Voluntário (Update) - Em breve")
        print("4. Remover Voluntário (Delete) - Em breve")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            cadastrar_voluntario()
        elif opcao == '2':
            listar_voluntarios()
        elif opcao == '0':
            print("Saindo do sistema... Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Iniciar o programa
if __name__ == "__main__":
    menu()