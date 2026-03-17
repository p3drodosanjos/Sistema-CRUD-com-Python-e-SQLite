import sqlite3
import os


def conectar():
   
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, 'voluntarios.db')
    
    return sqlite3.connect(caminho_banco)

# Testando a conexão
try:
    conn = conectar()
    print("🚀 Conexão com o banco do SQLite Online estabelecida com sucesso!")
    
   
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
        
        cursor.execute("SELECT id_voluntario, nome, email, habilidade_principal, disponibilidade FROM voluntarios")
        
        
        lista_voluntarios = cursor.fetchall()

      
        if len(lista_voluntarios) == 0:
            print("Nenhum voluntário cadastrado ainda.")
        else:
           
            for vol in lista_voluntarios:
                
                print(f"ID: {vol[0]}")
                print(f"Nome: {vol[1]} | E-mail: {vol[2]}")
                print(f"Habilidade: {vol[3]} | Disp: {vol[4]}")
                print("-" * 40) 

    except Exception as e:
        print(f"\n❌ Erro ao buscar os dados: {e}")
    finally:
        conn.close()

        # --- FUNÇÃO UPDATE (U) ---
def atualizar_voluntario():
    print("\n" + "="*40)
    print(" ATUALIZAR DADOS DO VOLUNTÁRIO ")
    print("="*40)

    # Chamamos a função de listar para o usuário ver os IDs disponíveis
    listar_voluntarios()

    id_alvo = input("\nDigite o ID do voluntário que deseja editar (ou 0 para cancelar): ")
    
    if id_alvo == '0':
        print("Atualização cancelada.")
        return # Sai da função e volta pro menu

    conn = conectar()
    cursor = conn.cursor()

    try:
       
        cursor.execute("SELECT nome, email, habilidade_principal, disponibilidade FROM voluntarios WHERE id_voluntario = ?", (id_alvo,))
        voluntario_atual = cursor.fetchone() # fetchone() pega só 1 resultado

        if voluntario_atual is None:
            print(f"\n❌ Erro: Nenhum voluntário encontrado com o ID {id_alvo}.")
        else:
            nome_atual, email_atual, hab_atual, disp_atual = voluntario_atual
            
            print(f"\nEditando: {nome_atual}")
            print("Dica: Deixe em branco e aperte ENTER para não alterar o campo.")

            # Pede os novos dados. Se o usuário der só Enter, salva uma string vazia ("")
            novo_email = input(f"Novo E-mail [{email_atual}]: ")
            nova_hab = input(f"Nova Habilidade [{hab_atual}]: ")
            nova_disp = input(f"Nova Disp. [{disp_atual}]: ")

            # Lógica para manter o dado antigo se o novo for vazio
            email_final = novo_email if novo_email != "" else email_atual
            hab_final = nova_hab if nova_hab != "" else hab_atual
            disp_final = nova_disp if nova_disp != "" else disp_atual

            # O comando SQL de UPDATE
            sql = '''UPDATE voluntarios 
                     SET email = ?, habilidade_principal = ?, disponibilidade = ?
                     WHERE id_voluntario = ?'''
            
            cursor.execute(sql, (email_final, hab_final, disp_final, id_alvo))
            conn.commit()
            print("\n✅ Cadastro atualizado com sucesso!")

    except sqlite3.IntegrityError:
        print("\n❌ Erro: Este novo e-mail já pertence a outro voluntário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    finally:
        conn.close()


   # --- FUNÇÃO DELETE (D) ---
def remover_voluntario():
    print("\n" + "="*40)
    print(" EXCLUIR CADASTRO DE VOLUNTÁRIO ")
    print("="*40)

    
    listar_voluntarios()

    id_alvo = input("\nDigite o ID do voluntário que deseja remover (ou 0 para cancelar): ")
    
    if id_alvo == '0':
        print("Operação cancelada.")
        return

    conn = conectar()
    cursor = conn.cursor()

    try:
      
        cursor.execute("SELECT nome FROM voluntarios WHERE id_voluntario = ?", (id_alvo,))
        voluntario = cursor.fetchone()

        if voluntario is None:
            print(f"\n❌ Erro: Nenhum voluntário encontrado com o ID {id_alvo}.")
        else:
            nome_voluntario = voluntario[0]
            
            
            print(f"\n⚠️ ATENÇÃO: Você está prestes a excluir o cadastro de '{nome_voluntario}'.")
            confirmacao = input("Tem certeza disso? (S para Sim / N para Não): ").strip().upper()

            if confirmacao == 'S':
                
                cursor.execute("DELETE FROM voluntarios WHERE id_voluntario = ?", (id_alvo,))
                conn.commit()
                print(f"\n🗑️ Cadastro de '{nome_voluntario}' removido com sucesso!")
            else:
                print("\nExclusão cancelada. O cadastro foi mantido.")

    except Exception as e:
        print(f"\n❌ Erro inesperado ao tentar excluir: {e}")
    finally:
        conn.close()

# --- MENU PRINCIPAL ---
def menu():
    while True:
        print("\n--- SISTEMA DE GESTÃO DE VOLUNTÁRIOS ---")
        print("1. Cadastrar Voluntário (Create)")
        print("2. Listar Voluntários (Read)")
        print("3. Atualizar Voluntário (Update)")
        print("4. Remover Voluntário (Delete) -")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            cadastrar_voluntario()
        elif opcao == '2':
            listar_voluntarios()
        elif opcao == '3':
            atualizar_voluntario()
        elif opcao == '4':
            remover_voluntario()
        elif opcao == '0':
            print("Saindo do sistema... Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Iniciar o programa
if __name__ == "__main__":
    menu()