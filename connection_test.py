# database/connection_test.py
import sqlite3
import streamlit as st
from contextlib import contextmanager

DB_PATH = 'plataforma_testes.db'

@contextmanager
def get_db_cursor_test():
    """Context manager para conexão com SQLite de testes"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn.cursor()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()