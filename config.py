# config.py
import streamlit as st

# ===== CONFIGURAÇÃO DE TESTE =====
# Banco de dados SQLite LOCAL
DB_CONFIG = {
    "type": "sqlite",
    "database": "plataforma_testes.db",
    "porta_streamlit": 8504  # ← mudar para 8501
}

def get_db_config():
    """Retorna configuração do banco de dados de TESTE"""
    return DB_CONFIG

def get_streamlit_port():
    """Retorna a porta do Streamlit"""
    return DB_CONFIG.get("porta_streamlit", 8504)

# Debug
print(f"🔧 AMBIENTE: TESTE LOCAL (SQLite)")
print(f"📁 Banco: {DB_CONFIG['database']}")
print(f"🌐 Porta: {DB_CONFIG['porta_streamlit']}")