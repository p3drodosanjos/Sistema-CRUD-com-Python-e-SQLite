import sqlite3

# Conecta no seu banco
conn = sqlite3.connect('voluntarios.db')
cursor = conn.cursor()

# O comando mágico do SQL para adicionar a coluna
cursor.execute("ALTER TABLE voluntarios ADD COLUMN telefone TEXT")
cursor.execute("ALTER TABLE voluntarios ADD COLUMN CPF TEXT")

conn.commit()
conn.close()

print("✅ Nova coluna adicionada com sucesso no banco de dados!")