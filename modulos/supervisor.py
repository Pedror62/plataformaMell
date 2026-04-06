import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.queries import (
    get_db_cursor, 
    atualizar_status_venda, 
    registrar_log,
    buscar_vendas_por_supervisor,
    buscar_metas_regionais
)
from datetime import datetime
from decimal import Decimal
import time
import numpy as np

def format_brl(val):
    """Formata valores para R$"""
    try:
        if val is None:
            return "R$ 0,00"
        if isinstance(val, Decimal):
            val = float(val)
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def determinar_tipo_migracao(valor_novo, valor_antigo):
    """Determina se é Upgrade ou Downgrade baseado na diferença"""
    if valor_novo > valor_antigo:
        return "Migração (Upgrade)"
    elif valor_novo < valor_antigo:
        return "Migração (Downgrade)"
    else:
        return "Migração (mesmo valor)"

def calcular_comissoes_equipe(id_regional, mes_num, ano_sel):
    """
    Calcula as comissões dos vendedores da equipe
    Retorna apenas quem está dentro da meta
    """
    try:
        with get_db_cursor() as cursor:
            # Busca a meta da regional para quantidade de vendas
            metas = buscar_metas_regionais(id_regional, mes_num, ano_sel)
            meta_qtd = int(metas[0]['meta_vendas_qtd']) if metas and len(metas) > 0 else 10
            
            # Busca todos os vendedores da regional
            cursor.execute("""
                SELECT 
                    u.id_usuario,
                    u.nome_usuario,
                    COUNT(v.id_venda) as total_vendas,
                    SUM(v.valor_venda) as faturamento_total,
                    SUM(CASE WHEN v.id_tipo_operacao IN (2,3) THEN 1 ELSE 0 END) as migracoes,
                    SUM(CASE WHEN v.id_tipo_operacao = 1 THEN 1 ELSE 0 END) as vendas_novas
                FROM users u
                LEFT JOIN venda v ON u.id_usuario = v.id_usuario_vendedor 
                    AND MONTH(v.data_venda) = %s 
                    AND YEAR(v.data_venda) = %s 
                    AND v.id_status = 2 
                    AND v.ativo = 1
                WHERE u.id_regional = %s 
                    AND u.id_tipo_usuario = 2
                    AND u.ativo = 1
                GROUP BY u.id_usuario, u.nome_usuario
                ORDER BY total_vendas DESC
            """, (mes_num, ano_sel, id_regional))
            
            vendedores = cursor.fetchall()
            
            if not vendedores:
                return [], meta_qtd
            
            # Lista para armazenar comissões
            comissoes = []
            
            for v in vendedores:
                total_vendas = int(v['total_vendas'] or 0)
                
                # Verifica se bateu a meta
                if total_vendas >= meta_qtd:
                    # Cálculo da comissão: R$ 50 por venda acima da meta
                    vendas_acima_meta = total_vendas - meta_qtd
                    comissao_vendedor = vendas_acima_meta * 50
                    
                    # Comissão adicional por migrações: R$ 10 por migração
                    migracoes = int(v['migracoes'] or 0)
                    comissao_migracoes = migracoes * 10
                    
                    comissao_total = comissao_vendedor + comissao_migracoes
                    
                    comissoes.append({
                        'id_vendedor': v['id_usuario'],
                        'vendedor': v['nome_usuario'],
                        'total_vendas': total_vendas,
                        'meta': meta_qtd,
                        'vendas_acima_meta': vendas_acima_meta,
                        'migracoes': migracoes,
                        'comissao_base': comissao_vendedor,
                        'comissao_migracoes': comissao_migracoes,
                        'comissao_total': comissao_total,
                        'faturamento': float(v['faturamento_total'] or 0)
                    })
            
            return comissoes, meta_qtd
            
    except Exception as e:
        st.error(f"Erro ao calcular comissões: {str(e)}")
        return [], 0

def calcular_comissao_supervisor(id_regional, mes_num, ano_sel):
    """
    Calcula a comissão do supervisor baseada no desempenho da equipe
    """
    try:
        comissoes_equipe, meta_qtd = calcular_comissoes_equipe(id_regional, mes_num, ano_sel)
        
        if not comissoes_equipe:
            return 0, 0, 0
        
        # Total de comissões pagas à equipe
        total_comissoes_equipe = sum(c['comissao_total'] for c in comissoes_equipe)
        
        # Comissão do supervisor: 10% do total das comissões da equipe
        comissao_supervisor = total_comissoes_equipe * 0.10
        
        # Número de vendedores que bateram a meta
        vendedores_meta = len(comissoes_equipe)
        
        return comissao_supervisor, total_comissoes_equipe, vendedores_meta
        
    except Exception as e:
        st.error(f"Erro ao calcular comissão do supervisor: {str(e)}")
        return 0, 0, 0

def exibir_grafico_performance_vendedores(df, nome_regional):
    """Exibe gráfico detalhado de performance dos vendedores da regional"""
    
    st.subheader(f"📊 Performance dos Vendedores - {nome_regional}")
    
    if df.empty:
        st.info("Sem dados para exibir no período selecionado.")
        return
    
    # Prepara dados por vendedor
    df_vendedores = df.groupby('vendedor').agg({
        'id_venda': 'count',
        'valor_venda': 'sum',
        'id_status': [
            ('aprovadas', lambda x: sum(x == 2)),
            ('pendentes', lambda x: sum(x == 1)),
            ('reprovadas', lambda x: sum(x == 3))
        ]
    }).reset_index()
    
    # Ajusta os nomes das colunas
    df_vendedores.columns = ['vendedor', 'total_vendas', 'faturamento_total', 
                            'aprovadas', 'pendentes', 'reprovadas']
    
    # Calcula taxas
    df_vendedores['taxa_aprovacao'] = (df_vendedores['aprovadas'] / df_vendedores['total_vendas'] * 100).fillna(0).round(1)
    df_vendedores['ticket_medio'] = df_vendedores.apply(
        lambda row: row['faturamento_total'] / row['aprovadas'] if row['aprovadas'] > 0 else 0, 
        axis=1
    ).round(2)
    
    # Ordena por faturamento
    df_vendedores = df_vendedores.sort_values('faturamento_total', ascending=False).reset_index(drop=True)
    
    # Métricas gerais
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    total_vendedores_ativos = len(df_vendedores[df_vendedores['total_vendas'] > 0])
    total_vendas = df_vendedores['total_vendas'].sum()
    total_aprovadas = df_vendedores['aprovadas'].sum()
    taxa_geral = (total_aprovadas / total_vendas * 100) if total_vendas > 0 else 0
    
    col_m1.metric("Vendedores Ativos", total_vendedores_ativos)
    col_m2.metric("Total de Vendas", int(total_vendas))
    col_m3.metric("Total Aprovadas", int(total_aprovadas))
    col_m4.metric("Taxa de Aprovação", f"{taxa_geral:.1f}%")
    
    st.divider()
    
    # Gráficos
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        if not df_vendedores.empty:
            fig_faturamento = px.bar(
                df_vendedores.head(10),
                x='vendedor',
                y='faturamento_total',
                title=f"💰 Faturamento por Vendedor - {nome_regional} (R$)",
                text_auto='.2s',
                color='faturamento_total',
                color_continuous_scale='Blues',
                labels={'faturamento_total': 'Faturamento (R$)', 'vendedor': 'Vendedor'}
            )
            fig_faturamento.update_traces(textposition='outside')
            fig_faturamento.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_faturamento, use_container_width=True)
    
    with col_g2:
        if not df_vendedores.empty:
            fig_vendas = px.bar(
                df_vendedores.head(10),
                x='vendedor',
                y=['aprovadas', 'pendentes', 'reprovadas'],
                title=f"📊 Volume de Vendas por Vendedor - {nome_regional}",
                labels={'value': 'Quantidade', 'variable': 'Status', 'vendedor': 'Vendedor'},
                color_discrete_map={
                    'aprovadas': '#28a745',
                    'pendentes': '#ffc107',
                    'reprovadas': '#dc3545'
                },
                barmode='stack'
            )
            fig_vendas.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_vendas, use_container_width=True)

def exibir_tela_supervisor(id_regional=None):
    """Tela do supervisor - com comissões da equipe"""
    
    if "id_usuario" not in st.session_state:
        st.error("Sessão encerrada. Faça login novamente.")
        return

    # Define a regional
    if id_regional is None:
        id_regional = st.session_state.get('id_regional')
    
    if not id_regional:
        st.error("Regional não identificada.")
        return
    
    # Busca nome da regional
    with get_db_cursor() as cursor:
        cursor.execute("SELECT descricao FROM regional WHERE id_regional = %s", (id_regional,))
        reg = cursor.fetchone()
        nome_reg = reg['descricao'] if reg else "Minha Regional"
    
    st.title(f"🛡️ Gestão da Regional: {nome_reg}")
    st.caption(f"Supervisor: {st.session_state.get('user_nome', '')}")

    # Filtros de data
    meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        mes_sel = st.selectbox("📅 Mês", meses_pt, index=datetime.now().month - 1)
        mes_num = meses_pt.index(mes_sel) + 1
    with col_f2:
        ano_sel = st.selectbox("📅 Ano", [2025, 2026], index=1)

    # ===== SEÇÃO DE COMISSÕES =====
    st.divider()
    st.subheader("💰 Comissões da Equipe")
    
    # Busca comissões
    comissoes_equipe, meta_qtd = calcular_comissoes_equipe(id_regional, mes_num, ano_sel)
    comissao_supervisor, total_comissoes_equipe, vendedores_meta = calcular_comissao_supervisor(id_regional, mes_num, ano_sel)
    
    # Métricas gerais de comissões
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    
    with col_c1:
        st.metric(
            "🎯 Meta da Regional", 
            f"{meta_qtd} vendas",
            help="Quantidade mínima de vendas para bater a meta"
        )
    
    with col_c2:
        st.metric(
            "👥 Vendedores com Meta Batida", 
            f"{vendedores_meta}",
            delta=f"{vendedores_meta} vendedores",
            help="Vendedores que atingiram ou superaram a meta"
        )
    
    with col_c3:
        st.metric(
            "💰 Total Comissões Equipe", 
            format_brl(total_comissoes_equipe),
            help="Total de comissões a pagar para a equipe"
        )
    
    with col_c4:
        st.metric(
            "👔 Sua Comissão", 
            format_brl(comissao_supervisor),
            delta=f"10% do total da equipe",
            help="Sua comissão é 10% do total das comissões da equipe"
        )
    
    # Tabela de comissões da equipe (apenas quem bateu a meta)
    if comissoes_equipe:
        st.markdown("### 📊 Detalhamento por Vendedor (Apenas quem bateu a meta)")
        
        df_comissoes = pd.DataFrame(comissoes_equipe)
        
        # Formata valores
        df_comissoes['comissao_base'] = df_comissoes['comissao_base'].apply(format_brl)
        df_comissoes['comissao_migracoes'] = df_comissoes['comissao_migracoes'].apply(format_brl)
        df_comissoes['comissao_total'] = df_comissoes['comissao_total'].apply(format_brl)
        df_comissoes['faturamento'] = df_comissoes['faturamento'].apply(format_brl)
        
        # Renomeia colunas para exibição
        df_exibir = df_comissoes[[
            'vendedor', 'total_vendas', 'meta', 'vendas_acima_meta', 
            'migracoes', 'comissao_base', 'comissao_migracoes', 'comissao_total', 'faturamento'
        ]].copy()
        
        df_exibir.columns = [
            'Vendedor', 'Total Vendas', 'Meta', 'Vendas Acima', 
            'Migrações', 'Comissão Base', 'Comissão Migrações', 'Comissão Total', 'Faturamento'
        ]
        
        st.dataframe(
            df_exibir,
            column_config={
                "Vendedor": st.column_config.TextColumn("Vendedor", width="medium"),
                "Total Vendas": st.column_config.NumberColumn("Total Vendas", format="%d"),
                "Meta": st.column_config.NumberColumn("Meta", format="%d"),
                "Vendas Acima": st.column_config.NumberColumn("Vendas Acima", format="%d"),
                "Migrações": st.column_config.NumberColumn("Migrações", format="%d"),
                "Comissão Base": st.column_config.TextColumn("Comissão Base"),
                "Comissão Migrações": st.column_config.TextColumn("Comissão Migrações"),
                "Comissão Total": st.column_config.TextColumn("Comissão Total"),
                "Faturamento": st.column_config.TextColumn("Faturamento")
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Gráfico de comissões
        df_comissoes_numeric = pd.DataFrame(comissoes_equipe)
        fig_comissoes = px.bar(
            df_comissoes_numeric,
            x='vendedor',
            y='comissao_total',
            title="💰 Comissões por Vendedor",
            text_auto='.2s',
            color='comissao_total',
            color_continuous_scale='Greens'
        )
        fig_comissoes.update_traces(textposition='outside')
        fig_comissoes.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_comissoes, use_container_width=True)
        
    else:
        st.info(f"📭 Nenhum vendedor bateu a meta de {meta_qtd} vendas em {mes_sel}/{ano_sel}.")
    
    st.divider()

    # Busca vendas APENAS da regional do supervisor
    vendas = buscar_vendas_por_supervisor(id_regional, mes_num, ano_sel)
    
    if not vendas:
        st.info(f"📭 Nenhuma venda encontrada para {nome_reg} em {mes_sel}/{ano_sel}.")
        return

    # Converte para DataFrame
    df = pd.DataFrame(vendas)
    
    # Converte valores decimais
    for col in ['valor_venda', 'valor_venda_antiga']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: float(x) if pd.notna(x) else 0.0)
    
    # ===== CORREÇÃO: ADICIONAR COLUNA COM OPERAÇÃO DETALHADA =====
    def get_operacao_detalhada(row):
        operacao = str(row.get('operacao', ''))
        # Verifica se é migração pelo nome da operação ou pelo ID do tipo
        if 'Migra' in operacao or row.get('id_tipo_operacao') in [2, 3]:  # IDs de migração
            valor_novo = row.get('valor_venda', 0)
            valor_antigo = row.get('valor_venda_antiga', 0)
            if valor_novo > valor_antigo and valor_antigo > 0:
                return "Migração (Upgrade)"
            elif valor_novo < valor_antigo and valor_antigo > 0:
                return "Migração (Downgrade)"
            elif valor_antigo > 0:
                return "Migração (mesmo valor)"
            else:
                return "Migração"
        # Se não for migração, retorna o nome da operação ou "Venda Nova"
        return operacao if operacao and operacao != 'nan' else "Venda Nova"
    
    df['operacao_detalhada'] = df.apply(get_operacao_detalhada, axis=1)
    
    # Adiciona também a coluna de impacto financeiro
    def get_impacto(row):
        if 'Migração' in str(row.get('operacao_detalhada', '')):
            return row.get('valor_venda', 0) - row.get('valor_venda_antiga', 0)
        return row.get('valor_venda', 0)
    
    df['impacto'] = df.apply(get_impacto, axis=1)

    # ===== SEÇÃO DE APROVAÇÕES COM DESTAQUE PARA DOWNGRADES =====
    st.divider()
    st.subheader(f"⏳ Vendas Pendentes de Aprovação - {nome_reg}")

    df_pendentes = df[df['id_status'] == 1].copy()

    if not df_pendentes.empty:
        # Inicializa controle de vendas processadas
        if 'vendas_processadas' not in st.session_state:
            st.session_state.vendas_processadas = set()
        
        # Processa cada venda
        for idx, (_, row) in enumerate(df_pendentes.iterrows()):
            id_venda = row['id_venda']
            
            # Se esta venda já foi processada, não mostrar os botões
            if id_venda in st.session_state.vendas_processadas:
                continue
            
            # DETECTAR SE É DOWNGRADE OU UPGRADE
            is_downgrade = False
            is_upgrade = False
            diferenca = 0
            operacao_detalhada = row.get('operacao_detalhada', row.get('operacao', 'Venda Nova'))
            
            if 'Downgrade' in operacao_detalhada:
                is_downgrade = True
                if row.get('valor_venda_antiga', 0) > 0:
                    diferenca = row['valor_venda_antiga'] - row['valor_venda']
            elif 'Upgrade' in operacao_detalhada:
                is_upgrade = True
                if row.get('valor_venda_antiga', 0) > 0:
                    diferenca = row['valor_venda'] - row['valor_venda_antiga']
            
            # ESCOLHER A COR DO CONTAINER BASEADO NO TIPO
            if is_downgrade:
                # DESTAQUE VERMELHO PARA DOWNGRADE
                container_color = "#ffebee"  # Vermelho claro
                border_color = "#f44336"     # Vermelho forte
                icon = "🔻🔴"
                alerta = f"⚠️ **ATENÇÃO: DOWNGRADE DETECTADO** - Redução de {format_brl(diferenca)} ⚠️"
            elif is_upgrade:
                # DESTAQUE VERDE PARA UPGRADE
                container_color = "#e8f5e9"  # Verde claro
                border_color = "#4caf50"     # Verde forte
                icon = "📈🟢"
                alerta = f"✨ **UPGRADE DETECTADO** - Aumento de {format_brl(diferenca)} ✨"
            else:
                # Azul claro para vendas normais
                container_color = "#e3f2fd"
                border_color = "#2196f3"
                icon = "📦"
                alerta = ""
            
            # CONTAINER COM COR DE FUNDO
            with st.container(border=True):
                # Usar HTML para cor de fundo
                st.markdown(f"""
                <div style="background-color: {container_color}; padding: 15px; border-radius: 10px; border-left: 5px solid {border_color}; margin-bottom: 10px;">
                """, unsafe_allow_html=True)
                
                # CABEÇALHO COM ÍCONE E TIPO
                if is_downgrade:
                    st.markdown(f"### {icon} **DOWNGRADE** {icon}")
                elif is_upgrade:
                    st.markdown(f"### {icon} **UPGRADE** {icon}")
                else:
                    st.markdown(f"### {icon} **VENDA NOVA**")
                
                # ALERTA ESPECIAL
                if alerta:
                    if is_downgrade:
                        st.error(alerta)
                    elif is_upgrade:
                        st.success(alerta)
                    st.markdown("---")
                
                # INFORMAÇÕES DA VENDA
                col_info1, col_info2 = st.columns(2)
                
                with col_info1:
                    st.markdown(f"**👤 Vendedor:** {row['vendedor']}")
                    st.markdown(f"**📋 Cliente:** {row['codigo_cliente']}")
                    st.markdown(f"**🔄 Operação:** {operacao_detalhada}")
                
                with col_info2:
                    if pd.notna(row['data_venda']):
                        if hasattr(row['data_venda'], 'strftime'):
                            data_str = row['data_venda'].strftime('%d/%m/%Y')
                        else:
                            data_str = str(row['data_venda'])
                        st.markdown(f"**📅 Data:** {data_str}")
                    
                    # VALORES COM DESTAQUE
                    if is_downgrade:
                        st.markdown(f"**💰 Valor Antigo:** {format_brl(row['valor_venda_antiga'])}")
                        st.markdown(f"**💰💰 Valor Novo:** {format_brl(row['valor_venda'])}")
                        st.markdown(f"**📉 REDUÇÃO:** {format_brl(diferenca)}")
                    elif is_upgrade:
                        st.markdown(f"**💰 Valor Antigo:** {format_brl(row['valor_venda_antiga'])}")
                        st.markdown(f"**💰💰 Valor Novo:** {format_brl(row['valor_venda'])}")
                        st.markdown(f"**📈 AUMENTO:** {format_brl(diferenca)}")
                    else:
                        st.markdown(f"**💰 Valor:** {format_brl(row['valor_venda'])}")
                        if row.get('valor_venda_antiga', 0) > 0:
                            st.markdown(f"**💰 Valor Antigo:** {format_brl(row['valor_venda_antiga'])}")
                
                st.markdown("---")
                
                # BOTÕES EM COLUNAS
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("✅ APROVAR", 
                                key=f"aprov_{id_venda}", 
                                use_container_width=True,
                                type="primary" if not is_downgrade else "secondary"):
                        with st.spinner("Processando aprovação..."):
                            try:
                                resultado = atualizar_status_venda(id_venda, 2)
                                if resultado:
                                    registrar_log(
                                        st.session_state.id_usuario, 
                                        "APROVAÇÃO", 
                                        f"Venda {id_venda} aprovada - {operacao_detalhada} - R$ {row['valor_venda']}"
                                    )
                                    st.session_state.vendas_processadas.add(id_venda)
                                    st.success(f"✅ Venda {id_venda} aprovada com sucesso!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(f"❌ Erro ao aprovar venda {id_venda}")
                            except Exception as e:
                                st.error(f"❌ Erro: {str(e)}")
                
                with col2:
                    button_type = "primary" if is_downgrade else "secondary"
                    button_label = "❌ REPROVAR (DOWNGRADE)" if is_downgrade else "❌ REPROVAR"
                    
                    if st.button(button_label, 
                                key=f"reprov_{id_venda}", 
                                use_container_width=True,
                                type=button_type):
                        with st.spinner("Processando reprovação..."):
                            try:
                                resultado = atualizar_status_venda(id_venda, 3)
                                if resultado:
                                    registrar_log(
                                        st.session_state.id_usuario, 
                                        "REPROVAÇÃO", 
                                        f"Venda {id_venda} reprovada - {operacao_detalhada}"
                                    )
                                    st.session_state.vendas_processadas.add(id_venda)
                                    st.success(f"❌ Venda {id_venda} reprovada!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(f"❌ Erro ao reprovar venda {id_venda}")
                            except Exception as e:
                                st.error(f"❌ Erro: {str(e)}")
                
                with col3:
                    if st.button("🔍 VER DETALHES", 
                                key=f"detalhes_{id_venda}", 
                                use_container_width=True):
                        with st.expander("Detalhes completos", expanded=True):
                            st.json({
                                "ID Venda": id_venda,
                                "Vendedor": row['vendedor'],
                                "Cliente": row['codigo_cliente'],
                                "Operação": operacao_detalhada,
                                "Tipo": "DOWNGRADE" if is_downgrade else ("UPGRADE" if is_upgrade else "VENDA NOVA"),
                                "Valor": row['valor_venda'],
                                "Valor Antigo": row.get('valor_venda_antiga', 0),
                                "Diferença": diferenca,
                                "Data": str(row['data_venda']),
                                "Status Atual": row['status']
                            })
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("")  # Espaço entre containers
        
        # Se todas as vendas foram processadas, limpa o set
        if len(st.session_state.vendas_processadas) == len(df_pendentes):
            st.session_state.vendas_processadas = set()
            st.rerun()
            
    else:
        st.success(f"✅ Nenhuma venda pendente de aprovação em {nome_reg}!")
        # Limpa vendas processadas quando não há pendentes
        if 'vendas_processadas' in st.session_state:
            st.session_state.vendas_processadas = set()

    st.divider()

    # ===== GRÁFICO DE PERFORMANCE DOS VENDEDORES =====
    exibir_grafico_performance_vendedores(df, nome_reg)

    st.divider()

    # ===== RESUMO DA REGIONAL COM RECEITA LÍQUIDA =====
    st.subheader(f"📊 Resumo da Regional - {nome_reg}")

    # Métricas básicas
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    total_vendas = len(df)
    vendedores_unicos = df['vendedor'].nunique()
    vendas_aprovadas = len(df[df['id_status'] == 2])
    faturamento_bruto = df[df['id_status'] == 2]['valor_venda'].sum()
    
    col_m1.metric("Total de Vendas", total_vendas)
    col_m2.metric("Vendedores Ativos", vendedores_unicos)
    col_m3.metric("✅ Aprovadas", vendas_aprovadas)
    col_m4.metric("💰 Faturamento Bruto", format_brl(faturamento_bruto))
    
    # Receita Líquida com cancelamentos
    from database.queries import calcular_receita_liquida_regional
    
    receita_info = calcular_receita_liquida_regional(id_regional, mes_num, ano_sel)
    
    if receita_info and receita_info['total_cancelamentos'] > 0:
        st.divider()
        st.subheader("📉 Impacto dos Cancelamentos")
        
        col_n1, col_n2, col_n3 = st.columns(3)
        
        col_n1.metric(
            "📉 Cancelamentos (≤3m)", 
            format_brl(receita_info['total_cancelamentos']),
            delta_color="inverse"
        )
        
        col_n2.metric(
            "💵 Receita Líquida", 
            format_brl(receita_info['receita_liquida']),
            delta=f"{(receita_info['receita_liquida']/faturamento_bruto*100 - 100):.1f}%" if faturamento_bruto > 0 else None
        )
        
        percentual_perda = (receita_info['total_cancelamentos'] / faturamento_bruto * 100) if faturamento_bruto > 0 else 0
        col_n3.metric(
            "📊 Impacto %", 
            f"-{percentual_perda:.1f}%",
            delta_color="inverse"
        )

    # ===== TABELA DE VENDAS COM OPERAÇÃO DETALHADA =====
    st.divider()
    st.subheader(f"📋 Detalhamento das Vendas - {nome_reg}")
    
    colunas_exibir = ['data_venda', 'vendedor', 'codigo_cliente', 'operacao_detalhada', 'valor_venda', 'status', 'impacto']
    colunas_existentes = [col for col in colunas_exibir if col in df.columns]
    
    if colunas_existentes:
        # Prepara DataFrame para exibição
        df_exibir = df[colunas_existentes].copy()
        
        # Formata valores
        df_exibir['valor_venda'] = df_exibir['valor_venda'].apply(format_brl)
        if 'impacto' in df_exibir.columns:
            df_exibir['impacto'] = df_exibir['impacto'].apply(format_brl)
        
        # Aplica cores condicionais para os status
        def color_status(val):
            if val == 'APROVADO':
                return 'background-color: #90ee90'
            elif val == 'EM ANÁLISE':
                return 'background-color: #fff3cd'
            elif val == 'REPROVADO':
                return 'background-color: #f8d7da'
            return ''
        
        # Aplica estilo na coluna de status
        styled_df = df_exibir.style.applymap(color_status, subset=['status'])
        
        st.dataframe(
            styled_df,
            column_config={
                "data_venda": "Data",
                "vendedor": "Vendedor",
                "codigo_cliente": "Cliente",
                "operacao_detalhada": "Operação",
                "valor_venda": "Valor",
                "status": "Status",
                "impacto": "Impacto"
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Resumo por tipo de operação
        st.divider()
        with st.expander("📊 Resumo por Tipo de Operação", expanded=False):
            # Agrupa por operação detalhada
            resumo_operacao = df.groupby('operacao_detalhada').agg({
                'id_venda': 'count',
                'valor_venda': 'sum',
                'impacto': 'sum'
            }).reset_index()
            resumo_operacao.columns = ['Operação', 'Quantidade', 'Valor Total', 'Impacto Total']
            resumo_operacao['Valor Total'] = resumo_operacao['Valor Total'].apply(format_brl)
            resumo_operacao['Impacto Total'] = resumo_operacao['Impacto Total'].apply(format_brl)
            st.dataframe(resumo_operacao, use_container_width=True, hide_index=True)

def exibir_cancelamentos_regionais(id_regional, nome_reg, mes_num, ano_sel):
    """
    Exibe os cancelamentos da regional para o supervisor
    Permite registrar novos cancelamentos
    """
    
    st.subheader(f"📉 Cancelamentos - {nome_reg}")
    
    # Abas: Visualizar e Registrar
    tab_ver, tab_registrar = st.tabs(["📋 Visualizar Cancelamentos", "➕ Registrar Cancelamento"])
    
    with tab_ver:
        # ===== RECEITA LÍQUIDA DA REGIONAL =====
        from database.queries import calcular_receita_liquida_regional
        
        receita_info = calcular_receita_liquida_regional(id_regional, mes_num, ano_sel)
        
        if receita_info:
            st.subheader("💰 Receita da Regional")
            
            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            
            col_r1.metric(
                "Receita Bruta", 
                format_brl(receita_info['receita_bruta'])
            )
            
            col_r2.metric(
                "Cancelamentos (≤3m)", 
                format_brl(receita_info['total_cancelamentos']),
                delta_color="inverse"
            )
            
            col_r3.metric(
                "Receita Líquida", 
                format_brl(receita_info['receita_liquida']),
                delta=f"{(receita_info['receita_liquida']/receita_info['receita_bruta']*100 - 100):.1f}%" if receita_info['receita_bruta'] > 0 else None
            )
            
            if receita_info['total_cancelamentos'] > 0:
                percentual_perda = (receita_info['total_cancelamentos'] / receita_info['receita_bruta'] * 100) if receita_info['receita_bruta'] > 0 else 0
                col_r4.metric(
                    "Impacto %", 
                    f"-{percentual_perda:.1f}%",
                    delta_color="inverse"
                )
            else:
                col_r4.metric("Impacto %", "0%")
            
            st.divider()
        
        # Busca cancelamentos
        from database.queries import buscar_cancelamentos_por_regional, calcular_impacto_cancelamentos_comissoes
        
        cancelamentos = buscar_cancelamentos_por_regional(id_regional, mes_num, ano_sel)
        
        if cancelamentos:
            df_cancel = pd.DataFrame(cancelamentos)
            
            # Métricas de cancelamento
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            
            total_cancel = len(df_cancel)
            valor_total = df_cancel['valor_original'].sum()
            ticket_medio = valor_total / total_cancel if total_cancel > 0 else 0
            
            # Conta cancelamentos com menos de 3 meses
            if 'meses_apos_venda' in df_cancel.columns:
                estornos = len(df_cancel[df_cancel['meses_apos_venda'] <= 3])
            else:
                estornos = 0
            
            col_c1.metric("Total Cancelamentos", total_cancel)
            col_c2.metric("Valor Total", format_brl(valor_total))
            col_c3.metric("Ticket Médio", format_brl(ticket_medio))
            col_c4.metric("Com Estorno (<3m)", estornos)
            
            st.divider()
            
            # Gráfico de cancelamentos por motivo
            if 'motivo' in df_cancel.columns:
                df_motivos = df_cancel['motivo'].value_counts().reset_index()
                df_motivos.columns = ['Motivo', 'Quantidade']
                
                fig_motivos = px.pie(df_motivos, values='Quantidade', names='Motivo',
                                     title="Cancelamentos por Motivo",
                                     hole=0.4,
                                     color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig_motivos, use_container_width=True)
                
                st.divider()
            
            # Tabela detalhada com destaque para estornos
            df_display = df_cancel.copy()
            
            # Formata coluna de impacto
            if 'meses_apos_venda' in df_display.columns:
                df_display['impacto'] = df_display['meses_apos_venda'].apply(
                    lambda x: '🔴 ESTORNA' if x <= 3 else '🟢 Mantém'
                )
            
            st.dataframe(
                df_display[['data_ocorrencia', 'vendedor', 'codigo_cliente', 
                           'valor_original', 'motivo', 'impacto', 'status']],
                column_config={
                    "data_ocorrencia": "Data",
                    "vendedor": "Vendedor",
                    "codigo_cliente": "Cliente",
                    "valor_original": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
                    "motivo": "Motivo",
                    "impacto": "Impacto",
                    "status": "Status"
                },
                use_container_width=True,
                hide_index=True
            )
            st.divider()
            
            # Impacto nas comissões
            st.subheader("💰 Impacto nas Comissões")
            
            impacto = calcular_impacto_cancelamentos_comissoes(id_regional, mes_num, ano_sel)
            
            if impacto:
                df_impacto = pd.DataFrame(impacto)
                
                # Separa estornos e manutenções
                df_estorno = df_impacto[df_impacto['impacto_comissao'] == 'ESTORNAR']
                df_manter = df_impacto[df_impacto['impacto_comissao'] == 'MANTER']
                
                col_i1, col_i2 = st.columns(2)
                
                with col_i1:
                    st.warning("**🔴 Cancelamentos que geram ESTORNO**")
                    if not df_estorno.empty:
                        st.dataframe(
                            df_estorno[['vendedor', 'total_cancelamentos', 'valor_total_cancelado']],
                            column_config={
                                "vendedor": "Vendedor",
                                "total_cancelamentos": "Qtd",
                                "valor_total_cancelado": st.column_config.NumberColumn("Valor", format="R$ %.2f")
                            },
                            use_container_width=True,
                            hide_index=True
                        )
                        total_estorno = df_estorno['valor_total_cancelado'].sum()
                        st.error(f"**Total a estornar: {format_brl(total_estorno)}**")
                
                with col_i2:
                    st.success("**🟢 Cancelamentos que NÃO estornam**")
                    if not df_manter.empty:
                        st.dataframe(
                            df_manter[['vendedor', 'total_cancelamentos', 'valor_total_cancelado']],
                            column_config={
                                "vendedor": "Vendedor",
                                "total_cancelamentos": "Qtd",
                                "valor_total_cancelado": st.column_config.NumberColumn("Valor", format="R$ %.2f")
                            },
                            use_container_width=True,
                            hide_index=True
                        )
            else:
                st.info("Nenhum cancelamento com impacto em comissões.")
        else:
            st.success(f"✅ Nenhum cancelamento registrado em {nome_reg} neste período.")
    
    with tab_registrar:
        st.subheader("➕ Registrar Novo Cancelamento")
        
        # Busca vendas aprovadas da regional para vincular
        from database.queries import (
            buscar_vendas_por_supervisor, 
            get_motivos_cancelamento, 
            registrar_cancelamento,
            buscar_cancelamentos_por_regional
        )
        
        # Busca cancelamentos existentes para filtrar
        cancelamentos_existentes = buscar_cancelamentos_por_regional(id_regional, mes_num, ano_sel)
        ids_cancelados = [c['id_venda_original'] for c in cancelamentos_existentes if c.get('id_venda_original')]
        
        vendas_aprovadas = buscar_vendas_por_supervisor(id_regional, mes_num, ano_sel)
        
        if vendas_aprovadas:
            # Filtra apenas vendas aprovadas (id_status = 2) e não canceladas
            df_vendas = pd.DataFrame(vendas_aprovadas)
            df_vendas_aprov = df_vendas[
                (df_vendas['id_status'] == 2) & 
                (~df_vendas['id_venda'].isin(ids_cancelados))
            ].copy() if not df_vendas.empty else pd.DataFrame()
            
            if not df_vendas_aprov.empty:
                with st.form("form_cancelamento"):
                    # Selecionar venda
                    opcoes_venda = []
                    for _, row in df_vendas_aprov.iterrows():
                        data_str = row['data_venda'].strftime('%d/%m/%Y') if hasattr(row['data_venda'], 'strftime') else str(row['data_venda'])
                        opcoes_venda.append((
                            row['id_venda'],
                            f"{data_str} - {row['vendedor']} - R$ {row['valor_venda']:.2f} - {row['codigo_cliente']}"
                        ))
                    
                    venda_sel = st.selectbox(
                        "Selecione a Venda Cancelada *",
                        options=opcoes_venda,
                        format_func=lambda x: x[1],
                        key="venda_cancelamento"
                    )
                    
                    # Buscar motivos
                    motivos = get_motivos_cancelamento()
                    
                    if motivos:
                        opcoes_motivo = [(m['id_motivo'], m['descricao']) for m in motivos]
                        motivo_sel = st.selectbox(
                            "Motivo do Cancelamento *",
                            options=opcoes_motivo,
                            format_func=lambda x: x[1],
                            key="motivo_cancelamento"
                        )
                    else:
                        st.error("Nenhum motivo cadastrado. Configure na tabela 'motivos_cancelamento'.")
                        motivo_sel = None
                    
                    observacoes = st.text_area("Observações", placeholder="Detalhes adicionais...", key="obs_cancelamento")
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        submitted = st.form_submit_button("✅ Registrar Cancelamento", use_container_width=True, type="primary")
                    with col_b2:
                        limpar = st.form_submit_button("🔄 Limpar", use_container_width=True)
                    
                    if submitted:
                        if not venda_sel or not motivo_sel:
                            st.error("❌ Selecione a venda e o motivo do cancelamento.")
                        else:
                            id_venda, desc_venda = venda_sel
                            id_motivo, desc_motivo = motivo_sel
                            
                            # Busca dados completos da venda
                            venda_info = df_vendas_aprov[df_vendas_aprov['id_venda'] == id_venda].iloc[0]
                            
                            # DEBUG: Mostrar dados que serão enviados
                            with st.expander("🔍 Dados do Cancelamento", expanded=False):
                                st.json({
                                    "id_venda_original": id_venda,
                                    "id_usuario_vendedor": int(venda_info['id_vendedor']),
                                    "id_regional": id_regional,
                                    "id_supervisor_cancelamento": st.session_state.id_usuario,
                                    "valor_original": float(venda_info['valor_venda']),
                                    "id_motivo": id_motivo,
                                    "observacoes": observacoes
                                })
                            
                            with st.spinner("Registrando cancelamento..."):
                                try:
                                    cancel_id = registrar_cancelamento(
                                        id_venda_original=id_venda,
                                        id_usuario_vendedor=int(venda_info['id_vendedor']),
                                        id_regional=id_regional,
                                        id_supervisor_cancelamento=st.session_state.id_usuario,
                                        valor_original=float(venda_info['valor_venda']),
                                        id_motivo=id_motivo,
                                        observacoes=observacoes
                                    )
                                    
                                    if cancel_id:
                                        st.success(f"✅ Cancelamento registrado com sucesso! ID: {cancel_id}")
                                        st.balloons()
                                        time.sleep(2)
                                        st.rerun()
                                    else:
                                        st.error("❌ Erro ao registrar cancelamento. Verifique o console para mais detalhes.")
                                except Exception as e:
                                    st.error(f"❌ Erro: {str(e)}")
            else:
                st.warning("Nenhuma venda aprovada disponível para cancelamento neste período.")
        else:
            st.warning("Nenhuma venda encontrada para esta regional no período.")
# Adicione no início do arquivo, depois dos imports
def get_operacao_detalhada(row):
    """
    Determina a operação detalhada (Upgrade/Downgrade)
    Função auxiliar para testes
    """
    try:
        operacao = str(row.get('operacao', ''))
        # Verifica se é migração
        if 'Migra' in operacao or row.get('id_tipo_operacao') in [2, 3]:
            valor_novo = row.get('valor_venda', 0)
            valor_antigo = row.get('valor_venda_antiga', 0)
            if valor_novo > valor_antigo and valor_antigo > 0:
                return "Migração (Upgrade)"
            elif valor_novo < valor_antigo and valor_antigo > 0:
                return "Migração (Downgrade)"
            elif valor_antigo > 0:
                return "Migração (mesmo valor)"
            else:
                return "Migração"
        # Se não for migração
        if operacao and operacao != 'nan':
            return operacao
        return "Venda Nova"
    except:
        return "Venda Nova"

def get_impacto(row):
    """
    Calcula o impacto financeiro da operação
    Função auxiliar para testes
    """
    try:
        if 'Migração' in str(row.get('operacao_detalhada', '')):
            return row.get('valor_venda', 0) - row.get('valor_venda_antiga', 0)
        return row.get('valor_venda', 0)
    except:
        return 0