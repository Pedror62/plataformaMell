# teste_conexao_local.py
import sqlite3

# Conectar no banco de testes
conn = sqlite3.connect('plataforma_testes.db')
cursor = conn.cursor()

# Testar uma consulta
cursor.execute("SELECT * FROM users")
usuarios = cursor.fetchall()

print("Usuários no banco de testes:")
for u in usuarios:
    print(u)

conn.close()