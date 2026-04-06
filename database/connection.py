# database/connection.py
import mysql.connector
from contextlib import contextmanager
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_db_config

@contextmanager
def get_db_cursor():
    """Conexão com o banco de dados (automático)"""
    config = get_db_config()
    
    conn_config = {
        'host': config['host'],
        'user': config['user'],
        'password': config['password'],
        'database': config['database']
    }
    
    conn = mysql.connector.connect(**conn_config)
    try:
        yield conn.cursor(dictionary=True)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()