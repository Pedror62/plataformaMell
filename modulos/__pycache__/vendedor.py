import streamlit as st
from database.queries import carregar_vendas

def exibir_tela_vendedor():
    st.title(f"Bem-vindo, {st.session_state.user_nome}")
    
    # O vendedor só vê as vendas DELE
    df_vendas = carregar_vendas(id_vendedor=st.session_state.user_id)
    
    st.subheader("Minhas Vendas")
    st.dataframe(df_vendas, use_container_width=True)