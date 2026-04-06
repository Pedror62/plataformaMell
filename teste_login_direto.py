# teste_login_direto.py
import sqlite3

# Conectar no banco
conn = sqlite3.connect('plataforma_testes.db')
cursor = conn.cursor()

# Teste direto
usuario = "ADMINISTRADOR"
senha = "admin123"

print("=" * 50)
print("TESTE DE LOGIN DIRETO NO BANCO")
print("=" * 50)

# Consulta simples
cursor.execute("SELECT * FROM users WHERE nome_usuario = ? AND senha = ?", (usuario, senha))
resultado = cursor.fetchone()

if resultado:
    print(f"✅ Usuário encontrado!")
    print(f"   ID: {resultado[0]}")
    print(f"   Nome: {resultado[1]}")
    print(f"   Tipo: {resultado[4]}")
else:
    print("❌ Usuário NÃO encontrado!")
    
    # Mostrar todos os usuários
    print("\nUsuários no banco:")
    cursor.execute("SELECT id_usuario, nome_usuario, senha, id_tipo_usuario FROM users")
    for row in cursor.fetchall():
        print(f"   ID: {row[0]} | Nome: '{row[1]}' | Senha: '{row[2]}' | Tipo: {row[3]}")

conn.close()