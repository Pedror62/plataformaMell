# modulos/supervisor_televendas.py
import streamlit as st
import pandas as pd
from database.queries import get_db_cursor, registrar_log
from datetime import datetime
import time

def format_brl(val):
    """Formata valores para R$"""
    try:
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def buscar_vendas_televendas_para_aprovacao(mes_num, ano_sel):
    """Busca vendas pendentes do televendas"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                v.id_venda,
                v.codigo_cliente,
                v.valor_venda,
                DATE_FORMAT(v.data_venda, '%%d/%%m/%%Y') as data_venda_br,
                u.nome_usuario as vendedor,
                t.descricao as operacao,
                s.descricao as status
            FROM venda v
            JOIN users u ON v.id_usuario_vendedor = u.id_usuario
            JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
            JOIN status s ON v.id_status = s.id_status
            WHERE v.setor = 'televendas'
              AND v.id_status = 1
              AND v.ativo = 1
              AND MONTH(v.data_venda) = %s
              AND YEAR(v.data_venda) = %s
            ORDER BY v.data_venda DESC
        """, (mes_num, ano_sel))
        return cursor.fetchall()

def buscar_ranking_televendas(mes_num, ano_sel):
    """Busca ranking dos operadores"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                u.nome_usuario,
                COUNT(v.id_venda) as total_vendas,
                SUM(v.valor_venda) as total_faturamento
            FROM users u
            LEFT JOIN venda v ON u.id_usuario = v.id_usuario_vendedor 
                AND v.setor = 'televendas'
                AND v.id_status = 2
                AND v.ativo = 1
                AND MONTH(v.data_venda) = %s
                AND YEAR(v.data_venda) = %s
            WHERE u.setor = 'televendas' AND u.ativo = 1
            GROUP BY u.nome_usuario
            HAVING total_vendas > 0
            ORDER BY total_vendas DESC
        """, (mes_num, ano_sel))
        return cursor.fetchall()

def buscar_resumo_televendas(mes_num, ano_sel):
    """Busca resumo do setor"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_vendas,
                SUM(CASE WHEN id_status = 2 THEN 1 ELSE 0 END) as aprovadas,
                SUM(CASE WHEN id_status = 1 THEN 1 ELSE 0 END) as pendentes,
                SUM(CASE WHEN id_status = 2 THEN valor_venda ELSE 0 END) as faturamento
            FROM venda
            WHERE setor = 'televendas'
              AND MONTH(data_venda) = %s
              AND YEAR(data_venda) = %s
              AND ativo = 1
        """, (mes_num, ano_sel))
        return cursor.fetchone()

def atualizar_status_venda(id_venda, novo_status):
    """Atualiza status da venda"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("""
                UPDATE venda 
                SET id_status = %s,
                    data_aprovacao = CASE WHEN %s = 2 THEN NOW() ELSE NULL END
                WHERE id_venda = %s
            """, (novo_status, novo_status, id_venda))
            return cursor.rowcount > 0
    except Exception as e:
        st.error(f"Erro: {e}")
        return False

def exibir_tela_supervisor_televendas():
    """Tela principal do supervisor"""
    
    if "id_usuario" not in st.session_state:
        st.error("Sessão encerrada.")
        return

    st.title("📞 Supervisor de Televendas")
    st.caption(f"Supervisor: {st.session_state.get('user_nome', '')}")

    # Filtros
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    col1, col2 = st.columns(2)
    with col1:
        mes_sel = st.selectbox("Mês", meses, index=datetime.now().month - 1)
        mes_num = meses.index(mes_sel) + 1
    with col2:
        ano_sel = st.selectbox("Ano", [2025, 2026], index=1)

    # Resumo
    resumo = buscar_resumo_televendas(mes_num, ano_sel)
    if resumo:
        st.subheader("📊 Resumo do Setor")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", int(resumo['total_vendas'] or 0))
        c2.metric("✅ Aprovadas", int(resumo['aprovadas'] or 0))
        c3.metric("⏳ Pendentes", int(resumo['pendentes'] or 0))
        c4.metric("💰 Faturamento", format_brl(float(resumo['faturamento'] or 0)))

    st.divider()

    # Ranking
    ranking = buscar_ranking_televendas(mes_num, ano_sel)
    if ranking:
        st.subheader("🏆 Ranking dos Operadores")
        df_rank = pd.DataFrame(ranking)
        df_rank['total_faturamento'] = df_rank['total_faturamento'].apply(format_brl)
        df_rank.columns = ['Operador', 'Vendas', 'Faturamento']
        st.dataframe(df_rank, use_container_width=True, hide_index=True)

    st.divider()

    # Vendas Pendentes
    st.subheader("⏳ Vendas Pendentes")
    vendas = buscar_vendas_televendas_para_aprovacao(mes_num, ano_sel)
    
    if not vendas:
        st.success("✅ Nenhuma venda pendente!")
        return

    for venda in vendas:
        with st.container(border=True):
            st.markdown(f"### Venda #{venda['id_venda']}")
            
            info1, info2, info3 = st.columns(3)
            with info1:
                st.markdown(f"**👤 Operador:** {venda['vendedor']}")
                st.markdown(f"**📋 Cliente:** {venda['codigo_cliente']}")
            with info2:
                st.markdown(f"**💰 Valor:** {format_brl(venda['valor_venda'])}")
                st.markdown(f"**📅 Data:** {venda['data_venda_br']}")
            with info3:
                st.markdown(f"**🔄 Operação:** {venda['operacao']}")
                st.markdown(f"**📌 Status:** {venda['status']}")
            
            st.markdown("---")
            
            b1, b2, _ = st.columns([1, 1, 2])
            with b1:
                if st.button("✅ APROVAR", key=f"apr_{venda['id_venda']}", use_container_width=True):
                    if atualizar_status_venda(venda['id_venda'], 2):
                        registrar_log(st.session_state.id_usuario, "APROVACAO_TV", 
                                    f"Venda {venda['id_venda']} aprovada")
                        st.success("✅ Aprovada!")
                        st.rerun()
            with b2:
                if st.button("❌ REPROVAR", key=f"rep_{venda['id_venda']}", use_container_width=True):
                    if atualizar_status_venda(venda['id_venda'], 3):
                        registrar_log(st.session_state.id_usuario, "REPROVACAO_TV", 
                                    f"Venda {venda['id_venda']} reprovada")
                        st.success("❌ Reprovada!")
                        st.rerun()