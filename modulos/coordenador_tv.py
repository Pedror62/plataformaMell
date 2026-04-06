# modulos/coordenador_tv.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.queries import get_db_cursor, registrar_log
from datetime import datetime
import calendar
from decimal import Decimal

def format_brl(val):
    """Formata valores para R$"""
    try:
        if isinstance(val, Decimal):
            val = float(val)
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def converter_para_float(valor):
    """Converte Decimal para float de forma segura"""
    if isinstance(valor, Decimal):
        return float(valor)
    return float(valor or 0)

def buscar_dashboard_coordenador(mes_num, ano_sel):
    """Busca dados consolidados do televendas para o coordenador"""
    with get_db_cursor() as cursor:
        # Resumo geral do setor
        cursor.execute("""
            SELECT 
                COUNT(*) as total_vendas,
                SUM(CASE WHEN id_status = 2 THEN 1 ELSE 0 END) as aprovadas,
                SUM(CASE WHEN id_status = 1 THEN 1 ELSE 0 END) as pendentes,
                SUM(CASE WHEN id_status = 3 THEN 1 ELSE 0 END) as reprovadas,
                SUM(CASE WHEN id_status = 2 THEN valor_venda ELSE 0 END) as faturamento
            FROM venda
            WHERE setor = 'televendas'
              AND MONTH(data_venda) = %s
              AND YEAR(data_venda) = %s
              AND ativo = 1
        """, (mes_num, ano_sel))
        resumo = cursor.fetchone()
        
        # Performance por operador (APENAS VENDEDORES - cargo_id = 2)
        cursor.execute("""
            SELECT 
                u.id_usuario,
                u.nome_usuario,
                COUNT(v.id_venda) as total_vendas,
                SUM(CASE WHEN v.id_status = 2 THEN 1 ELSE 0 END) as aprovadas,
                SUM(CASE WHEN v.id_status = 1 THEN 1 ELSE 0 END) as pendentes,
                SUM(CASE WHEN v.id_status = 2 THEN v.valor_venda ELSE 0 END) as faturamento
            FROM users u
            LEFT JOIN venda v ON u.id_usuario = v.id_usuario_vendedor 
                AND v.setor = 'televendas'
                AND MONTH(v.data_venda) = %s
                AND YEAR(v.data_venda) = %s
                AND v.ativo = 1
            WHERE u.setor = 'televendas' 
              AND u.ativo = 1
              AND u.id_tipo_usuario = 2  -- APENAS VENDEDORES (cargo_id = 2)
            GROUP BY u.id_usuario, u.nome_usuario
            ORDER BY aprovadas DESC
        """, (mes_num, ano_sel))
        operadores = cursor.fetchall()
        
        # Meta do setor
        cursor.execute("""
            SELECT meta_vendas_qtd, meta_faturamento
            FROM metas_televendas
            WHERE MONTH(mes_referencia) = %s AND YEAR(mes_referencia) = %s
        """, (mes_num, ano_sel))
        meta = cursor.fetchone()
        
        # Evolução diária
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
        """, (mes_num, ano_sel))
        evolucao = cursor.fetchall()
        
        # Converter valores decimais para float
        if resumo:
            resumo['total_vendas'] = int(resumo['total_vendas'] or 0)
            resumo['aprovadas'] = int(resumo['aprovadas'] or 0)
            resumo['pendentes'] = int(resumo['pendentes'] or 0)
            resumo['reprovadas'] = int(resumo['reprovadas'] or 0)
            resumo['faturamento'] = converter_para_float(resumo['faturamento'])
        
        if operadores:
            for op in operadores:
                op['total_vendas'] = int(op['total_vendas'] or 0)
                op['aprovadas'] = int(op['aprovadas'] or 0)
                op['pendentes'] = int(op['pendentes'] or 0)
                op['faturamento'] = converter_para_float(op['faturamento'])
        
        if meta:
            meta['meta_vendas_qtd'] = int(meta['meta_vendas_qtd'] or 0)
            meta['meta_faturamento'] = converter_para_float(meta['meta_faturamento'])
        
        if evolucao:
            for e in evolucao:
                e['total'] = int(e['total'] or 0)
                e['aprovadas'] = int(e['aprovadas'] or 0)
                e['faturamento'] = converter_para_float(e['faturamento'])
        
        return {
            'resumo': resumo,
            'operadores': operadores,
            'meta': meta,
            'evolucao': evolucao
        }

def exibir_dashboard_coordenador():
    """Tela do coordenador de televendas - visão gerencial do setor"""
    
    if "id_usuario" not in st.session_state:
        st.error("Sessão encerrada. Faça login novamente.")
        return

    st.title(f"👔 Painel do Coordenador - Televendas")
    st.caption(f"Coordenador: {st.session_state.get('user_nome', '')}")
    st.info("📊 Visão gerencial completa do setor de televendas")

    # Filtros de data
    meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        mes_sel = st.selectbox("📅 Mês", meses_pt, index=datetime.now().month - 1)
        mes_num = meses_pt.index(mes_sel) + 1
    with col_f2:
        ano_sel = st.selectbox("📅 Ano", [2025, 2026], index=1)

    # Busca dados
    dados = buscar_dashboard_coordenador(mes_num, ano_sel)
    
    if not dados['resumo'] or dados['resumo']['total_vendas'] == 0:
        st.warning(f"Nenhuma venda encontrada para {mes_sel}/{ano_sel}.")
        return

    # ===== MÉTRICAS DO SETOR =====
    st.subheader("📊 Métricas do Setor")
    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    
    with col_m1:
        st.metric("Total de Vendas", dados['resumo']['total_vendas'])
    with col_m2:
        st.metric("✅ Aprovadas", dados['resumo']['aprovadas'])
    with col_m3:
        st.metric("⏳ Pendentes", dados['resumo']['pendentes'])
    with col_m4:
        st.metric("❌ Reprovadas", dados['resumo']['reprovadas'])
    with col_m5:
        st.metric("💰 Faturamento", format_brl(dados['resumo']['faturamento']))

    st.divider()

    # ===== PROGRESSO DA META =====
    if dados['meta']:
        st.subheader("🎯 Progresso da Meta do Setor")
        
        meta_vendas = dados['meta']['meta_vendas_qtd']
        meta_faturamento = dados['meta']['meta_faturamento']
        
        # Converter para float para evitar erros de divisão
        aprovadas_float = float(dados['resumo']['aprovadas'])
        faturamento_float = float(dados['resumo']['faturamento'])
        
        perc_vendas = (aprovadas_float / meta_vendas * 100) if meta_vendas > 0 else 0
        perc_faturamento = (faturamento_float / meta_faturamento * 100) if meta_faturamento > 0 else 0
        
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown(f"**Meta de Vendas:** {dados['resumo']['aprovadas']} / {meta_vendas}")
            st.progress(min(perc_vendas/100, 1.0))
            st.caption(f"{perc_vendas:.1f}% da meta atingida")
        
        with col_p2:
            st.markdown(f"**Meta de Faturamento:** {format_brl(dados['resumo']['faturamento'])} / {format_brl(meta_faturamento)}")
            st.progress(min(perc_faturamento/100, 1.0))
            st.caption(f"{perc_faturamento:.1f}% da meta atingida")
        
        st.divider()

    # ===== EVOLUÇÃO DIÁRIA =====
    if dados['evolucao']:
        st.subheader("📈 Evolução Diária")
        df_evolucao = pd.DataFrame(dados['evolucao'])
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            fig_vendas = px.bar(
                df_evolucao,
                x='dia',
                y=['aprovadas', 'total'],
                title="Vendas por Dia",
                labels={'dia': 'Dia do Mês', 'value': 'Quantidade', 'variable': 'Tipo'},
                barmode='group',
                color_discrete_map={'aprovadas': '#28a745', 'total': '#17a2b8'}
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

    # ===== PERFORMANCE DOS OPERADORES (APENAS VENDEDORES) =====
    if dados['operadores']:
        st.subheader("📊 Performance dos Operadores")
        
        df_ops = pd.DataFrame(dados['operadores'])
        
        if not df_ops.empty:
            # Calcular taxa de aprovação
            df_ops['taxa_aprovacao'] = df_ops.apply(
                lambda row: f"{(row['aprovadas'] / row['total_vendas'] * 100):.1f}%" if row['total_vendas'] > 0 else "0%", 
                axis=1
            )
            df_ops['faturamento_fmt'] = df_ops['faturamento'].apply(format_brl)
            
            # Tabela de desempenho (sem pódio)
            st.dataframe(
                df_ops[['nome_usuario', 'total_vendas', 'aprovadas', 'pendentes', 'taxa_aprovacao', 'faturamento_fmt']],
                column_config={
                    "nome_usuario": "👤 Operador",
                    "total_vendas": "📋 Total",
                    "aprovadas": "✅ Aprovadas",
                    "pendentes": "⏳ Pendentes",
                    "taxa_aprovacao": "📊 Taxa",
                    "faturamento_fmt": "💰 Faturamento"
                },
                use_container_width=True,
                hide_index=True
            )
            
            # Destaque para o melhor operador (apenas um card simples)
            if len(df_ops) > 0:
                st.markdown("---")
                st.markdown("### 🏆 Destaque do Mês")
                
                melhor = df_ops.iloc[0]
                col_d1, col_d2, col_d3 = st.columns(3)
                
                with col_d1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                                padding: 1rem; border-radius: 15px; text-align: center; color: white;
                                box-shadow: 0 10px 20px rgba(0,0,0,0.2);">
                        <span style="font-size: 2.5rem;">👑</span>
                        <h3 style="margin: 0; color: white;">{melhor['nome_usuario']}</h3>
                        <p style="font-size: 1.5rem; margin: 0; font-weight: bold;">{melhor['aprovadas']} vendas</p>
                        <p style="margin: 0;">{melhor['faturamento_fmt']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_d2:
                    st.metric("📊 Taxa de Aprovação", melhor['taxa_aprovacao'])
                
                with col_d3:
                    if len(df_ops) > 1:
                        segundo = df_ops.iloc[1]
                        diferenca = melhor['aprovadas'] - segundo['aprovadas']
                        st.metric("🥇 Vantagem sobre 2º", f"{diferenca} vendas")
        else:
            st.info("Nenhum operador com vendas no período.")
    else:
        st.info("Nenhum operador encontrado.")

    st.divider()

    # ===== VISÃO DO SUPERVISOR (APROVAR VENDAS) =====
    st.subheader("⏳ Aprovações Pendentes")
    
    # Importa a função do supervisor para reutilizar
    from modulos.supervisor_tv import buscar_pendentes, aprovar_venda, reprovar_venda
    
    vendas_pendentes = buscar_pendentes(mes_num, ano_sel)
    
    if not vendas_pendentes:
        st.success("✅ Nenhuma venda pendente no período!")
    else:
        st.info(f"📌 **{len(vendas_pendentes)}** venda(s) aguardando aprovação")
        
        for venda in vendas_pendentes:
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
                    if st.button("✅ APROVAR", key=f"apr_coord_{venda['id_venda']}", use_container_width=True, type="primary"):
                        if aprovar_venda(venda['id_venda']):
                            registrar_log(st.session_state.id_usuario, "APROVACAO_COORD", 
                                        f"Venda {venda['id_venda']} aprovada - R$ {venda['valor_venda']}")
                            st.success("✅ Venda aprovada!")
                            st.rerun()
                with col_btn2:
                    if st.button("❌ REPROVAR", key=f"rep_coord_{venda['id_venda']}", use_container_width=True):
                        if reprovar_venda(venda['id_venda']):
                            registrar_log(st.session_state.id_usuario, "REPROVACAO_COORD", 
                                        f"Venda {venda['id_venda']} reprovada")
                            st.success("❌ Venda reprovada!")
                            st.rerun()
                with col_btn3:
                    with st.expander("🔍 Ver detalhes"):
                        st.json({
                            "ID Venda": int(venda['id_venda']),
                            "Operador": venda['vendedor'],
                            "Cliente": venda['codigo_cliente'],
                            "Valor": float(venda['valor_venda']),
                            "Data": venda['data'],
                            "Operação": venda['operacao']
                        })