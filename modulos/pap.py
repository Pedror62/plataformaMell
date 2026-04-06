import streamlit as st
import pandas as pd
from database.queries import salvar_visita_pap # Você precisará criar esta query

def exibir_tela_pap():
    st.markdown("<h1 style='color: #004AAD;'>🚶 Atividade Porta a Porta (PAP)</h1>", unsafe_allow_html=True)
    st.caption("Registro de prospecção externa e visitas em campo.")

    with st.form("form_pap", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nome_cliente = st.text_input("Nome do Prospect")
            endereco = st.text_input("Endereço/Rua")
            plano_ofertado = st.selectbox("Plano Ofertado", ["Plano 100mb", "Plano 300mb", "Plano 500mb"])
        
        with col2:
            telefone = st.text_input("Telefone de Contato")
            status_visita = st.selectbox("Resultado da Visita", ["Venda Fechada", "Interessado (Retornar)", "Não tem interesse"])
            observacao = st.text_area("Observações")

        submit = st.form_submit_button("Registrar Visita")

        if submit:
            if nome_cliente and telefone:
                # Aqui você chamaria sua função para salvar no banco de dados
                st.success(f"Visita a {nome_cliente} registrada com sucesso!")
                # salvar_visita_pap(nome_cliente, endereco, plano_ofertado, status_visita)
            else:
                st.error("Por favor, preencha o nome e o telefone.")

    # Exibir histórico de visitas do dia do vendedor
    st.divider()
    st.subheader("📋 Suas Visitas de Hoje")
    # df_hoje = carregar_visitas_vendedor(st.session_state.usuario_id)
    # st.dataframe(df_hoje, use_container_width=True)