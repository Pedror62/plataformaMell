# modulos/supervisor_tv.py
import streamlit as st
import pandas as pd
import plotly.express as px
from database.queries import get_db_cursor, registrar_log
from datetime import datetime

def format_brl(val):
    """Formata valores para R$"""
    try:
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def buscar_pendentes(mes, ano):
    """Busca vendas pendentes do televendas"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                v.id_venda,
                v.codigo_cliente,
                v.valor_venda,
                DATE_FORMAT(v.data_venda, '%d/%m/%Y') as data,  -- ALTERADO: %d (um %) não %%d
                u.nome_usuario as vendedor,
                t.descricao as operacao
            FROM venda v
            JOIN users u ON v.id_usuario_vendedor = u.id_usuario
            JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
            WHERE v.setor = 'televendas'
              AND v.id_status = 1
              AND v.ativo = 1
              AND MONTH(v.data_venda) = %s
              AND YEAR(v.data_venda) = %s
            ORDER BY v.data_venda DESC
        """, (mes, ano))
        return cursor.fetchall()
def buscar_resumo(mes, ano):
    """Busca resumo completo do setor de televendas"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_vendas,
                SUM(CASE WHEN id_status = 2 THEN 1 ELSE 0 END) as aprovadas,
                SUM(CASE WHEN id_status = 1 THEN 1 ELSE 0 END) as pendentes,
                SUM(CASE WHEN id_status = 3 THEN 1 ELSE 0 END) as reprovadas,
                SUM(CASE WHEN id_status = 2 THEN valor_venda ELSE 0 END) as faturamento_aprovado,
                SUM(CASE WHEN id_status = 1 THEN valor_venda ELSE 0 END) as faturamento_pendente,
                AVG(CASE WHEN id_status = 2 THEN valor_venda ELSE NULL END) as ticket_medio
            FROM venda
            WHERE setor = 'televendas'
              AND MONTH(data_venda) = %s
              AND YEAR(data_venda) = %s
              AND ativo = 1
        """, (mes, ano))
        return cursor.fetchone()

def buscar_ranking(mes, ano):
    """Busca ranking completo dos operadores de televendas"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                u.nome_usuario,
                COUNT(v.id_venda) as total_vendas,
                SUM(CASE WHEN v.id_status = 2 THEN 1 ELSE 0 END) as aprovadas,
                SUM(CASE WHEN v.id_status = 1 THEN 1 ELSE 0 END) as pendentes,
                SUM(CASE WHEN v.id_status = 2 THEN v.valor_venda ELSE 0 END) as faturamento
            FROM users u
            LEFT JOIN venda v ON u.id_usuario = v.id_usuario_vendedor 
                AND v.setor = 'televendas'
                AND v.ativo = 1
                AND MONTH(v.data_venda) = %s
                AND YEAR(v.data_venda) = %s
            WHERE u.setor = 'televendas' AND u.ativo = 1
            GROUP BY u.nome_usuario
            HAVING total_vendas > 0
            ORDER BY aprovadas DESC, faturamento DESC
        """, (mes, ano))
        return cursor.fetchall()

def buscar_evolucao_diaria(mes, ano):
    """Busca evolução diária de vendas"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                DAY(data_venda) as dia,
                COUNT(*) as total,
                SUM(CASE WHEN id_status = 2 THEN 1 ELSE 0 END) as aprovadas,
                SUM(CASE WHEN id_status = 2 THEN valor_venda ELSE 0 END) as faturamento
            FROM venda
            WHERE setor = 'televendas'
              AND MONTH(data_venda) = %s
              AND YEAR(data_venda) = %s
              AND ativo = 1
            GROUP BY DAY(data_venda)
            ORDER BY dia
        """, (mes, ano))
        return cursor.fetchall()
def buscar_operadores_ativos():
    """Busca total de operadores ativos no televendas"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM users
            WHERE setor = 'televendas' AND ativo = 1
        """)
        return cursor.fetchone()['total']

def aprovar_venda(id_venda):
    """Aprova uma venda"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("""
                UPDATE venda 
                SET id_status = 2, data_aprovacao = NOW()
                WHERE id_venda = %s
            """, (id_venda,))
            return True
    except Exception as e:
        st.error(f"Erro ao aprovar: {e}")
        return False

def reprovar_venda(id_venda):
    """Reprova uma venda"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("""
                UPDATE venda 
                SET id_status = 3
                WHERE id_venda = %s
            """, (id_venda,))
            return True
    except Exception as e:
        st.error(f"Erro ao reprovar: {e}")
        return False

def exibir_tela_supervisor_televendas():
    """Tela principal do supervisor de televendas"""
    
    if "id_usuario" not in st.session_state:
        st.error("Sessão encerrada. Faça login novamente.")
        return

    st.title("📞 Supervisor de Televendas")
    st.caption(f"Supervisor: {st.session_state.get('user_nome', '')}")

    # Filtros de data
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    col1, col2 = st.columns(2)
    with col1:
        mes_sel = st.selectbox("📅 Mês", meses, index=datetime.now().month - 1)
        mes_num = meses.index(mes_sel) + 1
    with col2:
        ano_sel = st.selectbox("📅 Ano", [2025, 2026], index=1)

    # Informações gerais do setor
    total_operadores = buscar_operadores_ativos()
    st.sidebar.metric("👥 Operadores Ativos", total_operadores)

    # ===== RESUMO COMPLETO DO SETOR =====
    resumo = buscar_resumo(mes_num, ano_sel)
    
    if resumo:
        st.subheader("📊 Resumo do Setor")
        
        # Métricas principais
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("📋 Total de Vendas", int(resumo['total_vendas'] or 0))
        col_m2.metric("✅ Aprovadas", int(resumo['aprovadas'] or 0))
        col_m3.metric("⏳ Pendentes", int(resumo['pendentes'] or 0))
        col_m4.metric("❌ Reprovadas", int(resumo['reprovadas'] or 0))
        
        # Métricas financeiras
        st.markdown("---")
        col_f1, col_f2, col_f3 = st.columns(3)
        
        if resumo['faturamento_aprovado']:
            col_f1.metric("💰 Faturamento Aprovado", format_brl(float(resumo['faturamento_aprovado'])))
        else:
            col_f1.metric("💰 Faturamento Aprovado", "R$ 0,00")
            
        if resumo['faturamento_pendente']:
            col_f2.metric("⏳ Faturamento Pendente", format_brl(float(resumo['faturamento_pendente'])))
        else:
            col_f2.metric("⏳ Faturamento Pendente", "R$ 0,00")
            
        if resumo['ticket_medio']:
            col_f3.metric("🎫 Ticket Médio", format_brl(float(resumo['ticket_medio'])))
        else:
            col_f3.metric("🎫 Ticket Médio", "R$ 0,00")

    st.divider()

    # ===== GRÁFICO DE EVOLUÇÃO DIÁRIA =====
    evolucao = buscar_evolucao_diaria(mes_num, ano_sel)
    if evolucao:
        st.subheader("📈 Evolução Diária")
        df_evolucao = pd.DataFrame(evolucao)
        
        # Garantir que as colunas são numéricas
        df_evolucao['dia'] = pd.to_numeric(df_evolucao['dia'])
        df_evolucao['aprovadas'] = pd.to_numeric(df_evolucao['aprovadas'], errors='coerce').fillna(0)
        df_evolucao['total'] = pd.to_numeric(df_evolucao['total'], errors='coerce').fillna(0)
        df_evolucao['faturamento'] = pd.to_numeric(df_evolucao['faturamento'], errors='coerce').fillna(0)
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            # Versão corrigida: dois gráficos separados em vez de um com barmode='group'
            fig_vendas = px.line(
                df_evolucao, 
                x='dia', 
                y=['aprovadas', 'total'],
                title="Vendas por Dia",
                labels={'dia': 'Dia do Mês', 'value': 'Quantidade', 'variable': 'Tipo'},
                markers=True
            )
            st.plotly_chart(fig_vendas, use_container_width=True)
        
        with col_g2:
            fig_faturamento = px.line(
                df_evolucao, 
                x='dia', 
                y='faturamento',
                title="Faturamento Diário",
                labels={'dia': 'Dia do Mês', 'faturamento': 'Faturamento (R$)'},
                markers=True
            )
            fig_faturamento.update_traces(line_color='#28a745', line_width=3)
            st.plotly_chart(fig_faturamento, use_container_width=True)

    st.divider()

    # ===== RANKING DOS OPERADORES =====
    ranking = buscar_ranking(mes_num, ano_sel)
    if ranking:
        st.subheader("🏆 Ranking dos Operadores")
        
        # Cards para o Top 3
        if len(ranking) >= 3:
            col_p1, col_p2, col_p3 = st.columns(3)
            
            # 2º lugar
            with col_p1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #C0C0C0 0%, #A0A0A0 100%); 
                            padding: 1.2rem; border-radius: 15px; text-align: center; color: white;
                            box-shadow: 0 8px 15px rgba(0,0,0,0.2);">
                    <span style="font-size: 2.5rem;">🥈</span>
                    <h3 style="margin: 0;">{ranking[1]['nome_usuario']}</h3>
                    <p style="font-size: 1.2rem; margin: 0;">{ranking[1]['aprovadas']} vendas</p>
                    <p style="margin: 0;">{format_brl(ranking[1]['faturamento'])}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 1º lugar
            with col_p2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                            padding: 1.5rem; border-radius: 15px; text-align: center; color: white;
                            box-shadow: 0 10px 20px rgba(0,0,0,0.2);">
                    <span style="font-size: 3rem;">🥇</span>
                    <h2 style="margin: 0;">{ranking[0]['nome_usuario']}</h2>
                    <p style="font-size: 1.5rem; margin: 0;">{ranking[0]['aprovadas']} vendas</p>
                    <p style="margin: 0;">{format_brl(ranking[0]['faturamento'])}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 3º lugar
            with col_p3:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #CD7F32 0%, #B87333 100%); 
                            padding: 1.2rem; border-radius: 15px; text-align: center; color: white;
                            box-shadow: 0 8px 15px rgba(0,0,0,0.2);">
                    <span style="font-size: 2.5rem;">🥉</span>
                    <h3 style="margin: 0;">{ranking[2]['nome_usuario']}</h3>
                    <p style="font-size: 1.2rem; margin: 0;">{ranking[2]['aprovadas']} vendas</p>
                    <p style="margin: 0;">{format_brl(ranking[2]['faturamento'])}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Tabela completa do ranking
        df_rank = pd.DataFrame(ranking)
        df_rank.columns = ['Operador', 'Total', 'Aprovadas', 'Pendentes', 'Faturamento']
        
        # Converter para numérico
        df_rank['Total'] = pd.to_numeric(df_rank['Total'], errors='coerce').fillna(0).astype(int)
        df_rank['Aprovadas'] = pd.to_numeric(df_rank['Aprovadas'], errors='coerce').fillna(0).astype(int)
        df_rank['Pendentes'] = pd.to_numeric(df_rank['Pendentes'], errors='coerce').fillna(0).astype(int)
        df_rank['Faturamento'] = pd.to_numeric(df_rank['Faturamento'], errors='coerce').fillna(0)
        
        # Calcular taxa de aprovação
        df_rank['Taxa Aprovação'] = (df_rank['Aprovadas'] / df_rank['Total'] * 100).round(1).astype(str) + '%'
        df_rank['Faturamento'] = df_rank['Faturamento'].apply(format_brl)
        
        st.dataframe(
            df_rank[['Operador', 'Total', 'Aprovadas', 'Pendentes', 'Taxa Aprovação', 'Faturamento']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Operador": "👤 Operador",
                "Total": "📋 Total",
                "Aprovadas": "✅ Aprovadas",
                "Pendentes": "⏳ Pendentes",
                "Taxa Aprovação": "📊 Taxa",
                "Faturamento": "💰 Faturamento"
            }
        )

    st.divider()

    # ===== VENDAS PENDENTES =====
    st.subheader("⏳ Vendas Pendentes de Aprovação")
    
    vendas = buscar_pendentes(mes_num, ano_sel)
    
    if not vendas:
        st.success("✅ Nenhuma venda pendente no período!")
        return

    st.info(f"📌 **{len(vendas)}** venda(s) aguardando aprovação")

    for venda in vendas:
        with st.container(border=True):
            col_h1, col_h2 = st.columns([3, 1])
            with col_h1:
                st.markdown(f"### 📦 Venda #{venda['id_venda']}")
            with col_h2:
                st.markdown(f"**📅 {venda['data']}**")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(f"**👤 Operador:** {venda['vendedor']}")
                st.markdown(f"**📋 Cliente:** {venda['codigo_cliente']}")
            with col_b:
                st.markdown(f"**💰 Valor:** {format_brl(venda['valor_venda'])}")
                st.markdown(f"**🔄 Operação:** {venda['operacao']}")
            with col_c:
                st.markdown("**⚡ Ações**")
            
            st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            with col_btn1:
                if st.button("✅ APROVAR", key=f"apr_{venda['id_venda']}", use_container_width=True, type="primary"):
                    if aprovar_venda(venda['id_venda']):
                        registrar_log(st.session_state.id_usuario, "APROVACAO_TV", 
                                    f"Venda {venda['id_venda']} aprovada - R$ {venda['valor_venda']}")
                        st.success("✅ Venda aprovada!")
                        st.rerun()
            with col_btn2:
                if st.button("❌ REPROVAR", key=f"rep_{venda['id_venda']}", use_container_width=True):
                    if reprovar_venda(venda['id_venda']):
                        registrar_log(st.session_state.id_usuario, "REPROVACAO_TV", 
                                    f"Venda {venda['id_venda']} reprovada")
                        st.success("❌ Venda reprovada!")
                        st.rerun()
            with col_btn3:
                with st.expander("🔍 Ver detalhes completos"):
                    st.json({
                        "ID Venda": int(venda['id_venda']),
                        "Operador": venda['vendedor'],
                        "Cliente": venda['codigo_cliente'],
                        "Valor": float(venda['valor_venda']),
                        "Data": venda['data'],
                        "Operação": venda['operacao']
                    })