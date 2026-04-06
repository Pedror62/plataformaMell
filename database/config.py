import streamlit as st

# O Streamlit lê o arquivo secrets.toml e preenche este dicionário automaticamente
DB_CONFIG = {
    'host': st.secrets["mysql"]["host"],
    'user': st.secrets["mysql"]["user"],
    'password': st.secrets["mysql"]["password"],
    'database': st.secrets["mysql"]["database"],
     'port': st.secrets["mysql"].get("port", 3306), 
}
