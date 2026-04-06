import sqlite3
import pandas as pd

DB_PATH = 'plataforma_testes.db'

def get_db_cursor():
    """Retorna uma conexão com o banco SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    """Cria as tabelas necessárias para teste"""
    conn = get_db_cursor()
    cursor = conn.cursor()
    
    # Criar tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT NOT NULL,
            cpf TEXT,
            id_regional INTEGER,
            id_tipo_usuario INTEGER,
            setor TEXT,
            senha TEXT,
            ativo INTEGER DEFAULT 1
        )
    ''')
    
    # Criar tabela de regionais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS regional (
            id_regional INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            ativo INTEGER DEFAULT 1
        )
    ''')
    
    # Criar tabela de tipos de usuário
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tipo_usuario (
            id_tipo_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            ativo INTEGER DEFAULT 1
        )
    ''')
    
    # Criar tabela de vendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS venda (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario_vendedor INTEGER,
            id_tipo_operacao INTEGER,
            id_status INTEGER,
            valor_venda REAL,
            data_venda DATE,
            ativo INTEGER DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Tabelas criadas com sucesso!")

def inserir_dados_teste():
    """Insere dados de teste"""
    conn = get_db_cursor()
    cursor = conn.cursor()
    
    # Inserir regionais
    cursor.execute("INSERT OR IGNORE INTO regional (id_regional, descricao) VALUES (1, 'Curvelo')")
    cursor.execute("INSERT OR IGNORE INTO regional (id_regional, descricao) VALUES (2, 'Moc')")
    cursor.execute("INSERT OR IGNORE INTO regional (id_regional, descricao) VALUES (3, 'Salinas')")
    
    # Inserir tipos de usuário
    cursor.execute("INSERT OR IGNORE INTO tipo_usuario (id_tipo_usuario, descricao) VALUES (1, 'Admin')")
    cursor.execute("INSERT OR IGNORE INTO tipo_usuario (id_tipo_usuario, descricao) VALUES (2, 'Vendedor')")
    cursor.execute("INSERT OR IGNORE INTO tipo_usuario (id_tipo_usuario, descricao) VALUES (3, 'Supervisor')")
    
    # Inserir usuário admin
    cursor.execute("""
        INSERT OR IGNORE INTO users (id_usuario, nome_usuario, senha, id_tipo_usuario, ativo) 
        VALUES (1, 'ADMINISTRADOR', 'admin123', 1, 1)
    """)
    
    conn.commit()
    conn.close()
    print("✅ Dados de teste inseridos!")

# Executar
if __name__ == "__main__":
    criar_tabelas()
    inserir_dados_teste()
    print("✅ Banco de testes criado: plataforma_testes.db")

import sqlite3

conn = sqlite3.connect('plataforma_testes.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

conn.close()