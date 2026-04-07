from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# --- FUNÇÃO DE CONEXÃO COM O BANCO ---
def conectar():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, 'voluntarios.db')
    return sqlite3.connect(caminho_banco)

# ==========================================
# 1. READ (Lê todos os voluntários na tela inicial)
# ==========================================
@app.route('/')
def index():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_voluntario, nome, email, habilidade_principal, disponibilidade, telefone, cpf FROM voluntarios")
    dados = cursor.fetchall()
    conn.close()
    return render_template('index.html', lista_voluntarios=dados)

# ==========================================
# 2. CREATE (Cadastra um novo voluntário)
# ==========================================
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        habilidade = request.form['habilidade']
        disponibilidade = request.form['disponibilidade']

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO voluntarios 
                              (nome, email, habilidade_principal, disponibilidade, telefone, cpf) 
                              VALUES (?, ?, ?, ?, ?, ?)''', 
                           (nome, email, habilidade, disponibilidade, telefone, cpf))
            conn.commit()
        except Exception as e:
            print(f"Erro ao salvar: {e}")
        finally:
            conn.close()
        
        return redirect(url_for('index'))
    
    # Se for GET, só mostra o formulário vazio
    return render_template('cadastro.html')

# ==========================================
# 3. UPDATE (Atualiza os dados de um voluntário)
# ==========================================
@app.route('/editar/<int:id_voluntario>', methods=['GET', 'POST'])
def editar(id_voluntario):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Se for POST, pega os novos dados digitados e salva
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        habilidade = request.form['habilidade']
        disponibilidade = request.form['disponibilidade']

        cursor.execute('''UPDATE voluntarios 
                          SET nome=?, email=?, habilidade_principal=?, disponibilidade=?, telefone=?, cpf=?
                          WHERE id_voluntario=?''', 
                       (nome, email, habilidade, disponibilidade, telefone, cpf, id_voluntario))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    # Se for GET, busca os dados da pessoa e preenche a tela
    cursor.execute("SELECT id_voluntario, nome, email, habilidade_principal, disponibilidade, telefone, cpf FROM voluntarios WHERE id_voluntario = ?", (id_voluntario,))
    voluntario_atual = cursor.fetchone()
    conn.close()

    return render_template('editar.html', voluntario=voluntario_atual)

# ==========================================
# 4. DELETE (Remove um voluntário)
# ==========================================
@app.route('/deletar/<int:id_voluntario>')
def deletar(id_voluntario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM voluntarios WHERE id_voluntario = ?", (id_voluntario,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- LIGA O SERVIDOR ---
if __name__ == '__main__':
    app.run(debug=True)