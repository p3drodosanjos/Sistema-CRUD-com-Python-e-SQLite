from flask import Flask, render_template
import sqlite3
import os

# 1. Inicializa o aplicativo web Flask
app = Flask(__name__)

# 2. Função para conectar ao banco de dados (você já conhece essa!)
def conectar():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, 'voluntarios.db')
    return sqlite3.connect(caminho_banco)

# 3. Cria a rota principal (a página inicial do seu site)
@app.route('/')
def index():
    conn = conectar()
    cursor = conn.cursor()
    
    # Executa o "R" do CRUD: Lê todos os voluntários salvos
    cursor.execute("SELECT id_voluntario, nome, email, habilidade_principal, disponibilidade FROM voluntarios")
    dados = cursor.fetchall()
    
    conn.close()
    
    # Envia a lista de dados para o arquivo HTML
    return render_template('index.html', lista_voluntarios=dados)

# 4. Liga o servidor web
if __name__ == '__main__':
    # debug=True faz o site atualizar sozinho quando você salva o código!
    app.run(debug=True)