import streamlit as st
import pandas as pd
from database.connection import get_db_cursor
from datetime import datetime

def diagnosticar_banco():
    st.title("🔍 Diagnóstico do Banco de Dados")
    st.caption("Visualize o conteúdo real das tabelas para ajustar as queries")

    # Lista de tabelas para diagnosticar
    tabelas = [
        "regional",
        "tipo_usuario",
        "users",
        "tipo_operacao",
        "status",
        "venda",
        "metas_regionais",
        "notificacoes",
        "logs_sistema"
    ]

    # Seletor de tabela
    tabela_sel = st.selectbox("Selecione a tabela para visualizar", tabelas)

    if st.button("🔍 Ver Estrutura e Dados", type="primary"):
        with get_db_cursor() as cursor:
            # Ver estrutura da tabela
            st.subheader(f"📋 Estrutura da tabela: {tabela_sel}")
            cursor.execute(f"DESCRIBE {tabela_sel}")
            estrutura = cursor.fetchall()
            df_estrutura = pd.DataFrame(estrutura)
            st.dataframe(df_estrutura, use_container_width=True)

            # Ver dados da tabela
            st.subheader(f"📊 Dados da tabela: {tabela_sel} (primeiros 50 registros)")
            cursor.execute(f"SELECT * FROM {tabela_sel} LIMIT 50")
            dados = cursor.fetchall()
            
            if dados:
                df_dados = pd.DataFrame(dados)
                st.dataframe(df_dados, use_container_width=True)
                
                # Estatísticas básicas
                st.subheader("📈 Estatísticas")
                st.write(f"Total de registros: {len(dados)}")
                st.write("Colunas:", list(df_dados.columns))
            else:
                st.warning("Tabela vazia - nenhum registro encontrado")

    # Diagnóstico específico para vendas
    st.divider()
    st.subheader("🎯 Diagnóstico de Vendas por Período")

    col1, col2 = st.columns(2)
    with col1:
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        mes_sel = st.selectbox("Mês", meses, index=datetime.now().month - 1)
        mes_num = meses.index(mes_sel) + 1
    with col2:
        ano_sel = st.selectbox("Ano", [2024, 2025, 2026], index=1)

    if st.button("🔍 Ver Vendas do Período"):
        with get_db_cursor() as cursor:
            # Query detalhada de vendas
            query = """
                SELECT 
                    v.id_venda,
                    v.data_venda,
                    u.nome_usuario as vendedor,
                    u.id_regional,
                    r.descricao as regional,
                    t.descricao as tipo_operacao,
                    v.valor_venda,
                    v.valor_venda_antiga,
                    s.descricao as status,
                    v.id_status,
                    v.codigo_cliente,
                    v.ativo
                FROM venda v
                LEFT JOIN users u ON v.id_usuario_vendedor = u.id_usuario
                LEFT JOIN regional r ON u.id_regional = r.id_regional
                LEFT JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
                LEFT JOIN status s ON v.id_status = s.id_status
                WHERE MONTH(v.data_venda) = %s AND YEAR(v.data_venda) = %s
                ORDER BY v.data_venda DESC
                LIMIT 100
            """
            cursor.execute(query, (mes_num, ano_sel))
            vendas = cursor.fetchall()
            
            if vendas:
                df_vendas = pd.DataFrame(vendas)
                st.success(f"Encontradas {len(vendas)} vendas!")
                st.dataframe(df_vendas, use_container_width=True)
                
                # Resumo por regional
                st.subheader("📊 Resumo por Regional")
                resumo = df_vendas.groupby('regional').agg({
                    'id_venda': 'count',
                    'valor_venda': 'sum',
                    'id_status': lambda x: list(x)
                }).reset_index()
                st.dataframe(resumo)
                
                # Resumo por status
                st.subheader("📊 Resumo por Status")
                resumo_status = df_vendas.groupby('status').agg({
                    'id_venda': 'count',
                    'valor_venda': 'sum'
                }).reset_index()
                st.dataframe(resumo_status)
            else:
                st.warning(f"Nenhuma venda encontrada para {mes_sel}/{ano_sel}")

    # Query personalizada
    st.divider()
    st.subheader("🔧 Query SQL Personalizada")
    
    query_personalizada = st.text_area(
        "Digite sua query SQL:",
        height=150,
        value="SELECT * FROM venda LIMIT 10"
    )
    
    if st.button("Executar Query"):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query_personalizada)
                resultados = cursor.fetchall()
                
                if resultados:
                    df_result = pd.DataFrame(resultados)
                    st.success(f"Query executada com sucesso! {len(resultados)} registros.")
                    st.dataframe(df_result, use_container_width=True)
                else:
                    st.info("Query executada mas não retornou resultados.")
        except Exception as e:
            st.error(f"Erro na query: {str(e)}")

# Para executar diretamente
if __name__ == "__main__":
    st.set_page_config(page_title="Diagnóstico do Banco", layout="wide")
    diagnosticar_banco()