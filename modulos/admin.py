import streamlit as st
import pandas as pd
import plotly.express as px
from database.queries import get_db_cursor, registrar_log
from datetime import datetime
import io

from integracao_hubsoft import HubsoftIntegracao, buscar_data_habilitacao

# ============================================================================
# IMPORTAÇÕES DO MÓDULO AUDITOR (para funções Hubsoft)
# ============================================================================
from modulos.auditor import (
    buscar_vendas_do_periodo,
    consultar_ids_hubsoft,
    criar_dataframe_conciliado,
    colorir_status_hubsoft,
    format_brl,
    MESES_PT
)

# ============================================================================
# CONSTANTES
# ============================================================================
MESES_PT = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

# ============================================================================
# FUNÇÃO AUXILIAR PARA FORMATAR VALORES
# ============================================================================
def format_brl(val):
    """Formata valores para o padrão monetário brasileiro."""
    try:
        if pd.isna(val) or val is None:
            return "R$ 0,00"
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def colorir_status_hubsoft(val):
    """Aplica cores de fundo baseado no status do Hubsoft"""
    if pd.isna(val):
        return ''
    if '✅ INSTALADO' in str(val) or '✅ MIGRADO' in str(val):
        return 'background-color: #d4edda; color: #155724; font-weight: bold;'
    elif '❌ NÃO INSTALADO' in str(val) or '❌ NÃO MIGRADO' in str(val):
        return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    elif '❌ NÃO ENCONTRADO' in str(val):
        return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    elif '⚠️ ERRO' in str(val):
        return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
    elif '⏳ FORA DO PERÍODO' in str(val):
        return 'background-color: #e2e3e5; color: #383d41; font-weight: bold;'
    elif '⚠️ PENDENTE' in str(val) or '⏳ PENDENTE' in str(val):
        return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
    else:
        return ''

# ============================================================================
# 1. DASHBOARD ESTRATÉGICO (INSIGHTS) - VERSÃO COM FILTRO DE SETOR
# ============================================================================
def exibir_insights_gerenciais(setor='todos'):
    """
    Exibe insights gerenciais filtrando por setor
    setor: 'comercial', 'televendas', ou 'todos' (para admin)
    """
    
    # Determina o título baseado no setor
    if setor == 'televendas':
        st.header("📞 Inteligência de Negócio - Televendas")
        st.info("Visualizando dados do setor de Televendas")
    elif setor == 'comercial':
        st.header("🏢 Inteligência de Negócio - Comercial")
        st.info("Visualizando dados do setor Comercial")
    else:
        st.header("💡 Inteligência de Negócio - Consolidado")
        st.info("Visualizando dados consolidados (Comercial + Televendas - Em Desenvolvimento)")
    
    # Filtros de Tempo
    c1, c2 = st.columns(2)
    meses_pt = MESES_PT
    mes_sel = c1.selectbox("Mês de Análise", meses_pt, index=datetime.now().month - 1)
    ano_sel = c2.selectbox("Ano de Análise", [2025, 2026], index=1)
    mes_num = meses_pt.index(mes_sel) + 1

    with get_db_cursor() as cursor:
        # Query base com filtro de setor
        query = """
            SELECT 
                u.nome_usuario as Vendedor,
                COALESCE(r.descricao, 'Vendas Online') as Regional,
                v.valor_venda,
                t.descricao as Operacao,
                s.descricao as Status,
                v.setor
            FROM venda v
            JOIN users u ON v.id_usuario_vendedor = u.id_usuario
            LEFT JOIN regional r ON u.id_regional = r.id_regional
            JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
            JOIN status s ON v.id_status = s.id_status
            WHERE v.ativo = 1 
              AND MONTH(v.data_venda) = %s 
              AND YEAR(v.data_venda) = %s
        """
        params = [mes_num, ano_sel]
        
        # Aplica filtro de setor
        if setor != 'todos':
            query += " AND v.setor = %s"
            params.append(setor)
        
        cursor.execute(query, params)
        vendas = cursor.fetchall()

    # Cria DataFrame mesmo se vazio
    df_vendas = pd.DataFrame(vendas) if vendas else pd.DataFrame()
    
    if df_vendas.empty:
        st.warning(f"Nenhuma venda encontrada para {mes_sel}/{ano_sel}.")
        return

    df_vendas['valor_venda'] = df_vendas['valor_venda'].astype(float)

    # --- MÉTRICAS PRINCIPAIS ---
    total_faturamento = df_vendas[df_vendas['Status'] == 'APROVADO']['valor_venda'].sum()
    total_vendas = len(df_vendas)
    aprovadas = len(df_vendas[df_vendas['Status'] == 'APROVADO'])
    pendentes = len(df_vendas[df_vendas['Status'] == 'EM ANÁLISE'])
    
    st.subheader("📊 Visão Geral")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Faturamento Total", format_brl(total_faturamento))
    m2.metric("Total de Vendas", total_vendas)
    m3.metric("Aprovadas", aprovadas)
    m4.metric("Pendentes", pendentes)

    st.divider()

    # --- ANÁLISE DE STATUS ---
    st.subheader("📈 Análise de Status das Vendas")
    
    # Agrupa por status (só executa se houver dados)
    if not df_vendas.empty:
        df_status = df_vendas.groupby('Status').agg(
            Quantidade=('Vendedor', 'count'),
            Valor=('valor_venda', 'sum')
        ).reset_index()
    else:
        df_status = pd.DataFrame(columns=['Status', 'Quantidade', 'Valor'])
    
    # Gráficos lado a lado
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        if not df_status.empty:
            # Gráfico de pizza - Quantidade
            fig_pizza_qtd = px.pie(
                df_status, 
                values='Quantidade', 
                names='Status',
                title="Distribuição por Quantidade",
                hole=0.4,
                color='Status',
                color_discrete_map={
                    'APROVADO': '#28a745',
                    'EM ANÁLISE': '#ffc107',
                    'REPROVADO': '#dc3545',
                    'CANCELADO': '#6c757d'
                }
            )
            fig_pizza_qtd.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                texttemplate='%{label}<br>%{percent:.1%}'
            )
            fig_pizza_qtd.update_layout(showlegend=False)
            st.plotly_chart(fig_pizza_qtd, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    
    with col_s2:
        if not df_status.empty:
            # Gráfico de pizza - Valor
            fig_pizza_valor = px.pie(
                df_status, 
                values='Valor', 
                names='Status',
                title="Distribuição por Valor (R$)",
                hole=0.4,
                color='Status',
                color_discrete_map={
                    'APROVADO': '#28a745',
                    'EM ANÁLISE': '#ffc107',
                    'REPROVADO': '#dc3545',
                    'CANCELADO': '#6c757d'
                }
            )
            
            # Formatação para mostrar os valores em R$
            fig_pizza_valor.update_traces(
                textposition='inside', 
                textinfo='label+value',
                texttemplate='%{label}<br>R$ %{value:,.0f}'.replace(',', '.'),
                hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Percentual: %{percent}<extra></extra>'
            )
            
            fig_pizza_valor.update_layout(
                showlegend=False,
                uniformtext_minsize=10,
                uniformtext_mode='hide'
            )
            
            st.plotly_chart(fig_pizza_valor, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    
    st.divider()
    
    # --- RANKING POR REGIONAL (APENAS PARA COMERCIAL) ---
    if setor != 'televendas':
        st.subheader("🏆 Performance por Regional")
        
        if not df_vendas.empty:
            df_regional = df_vendas.groupby('Regional').agg(
                Vendas=('Vendedor', 'count'),
                Faturamento=('valor_venda', 'sum')
            ).reset_index()
            
            fig_regional = px.bar(
                df_regional, 
                x='Regional', 
                y='Faturamento',
                title="Faturamento por Regional",
                text_auto='.2s',
                color='Faturamento',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_regional, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    else:
        st.info("📞 Televendas não possui regionais")
    
    st.divider()
    
    # --- MIX DE OPERAÇÕES ---
    st.subheader("🔄 Mix de Operações")
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        if not df_vendas.empty:
            df_operacao = df_vendas.groupby('Operacao').agg(
                Quantidade=('Vendedor', 'count'),
                Valor=('valor_venda', 'sum')
            ).reset_index()
            
            fig_operacao = px.pie(
                df_operacao, 
                values='Quantidade', 
                names='Operacao',
                title="Distribuição por Tipo de Operação",
                hole=0.4
            )
            fig_operacao.update_traces(textposition='inside', textinfo='percent+label')
            fig_operacao.update_layout(showlegend=False)
            st.plotly_chart(fig_operacao, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    
    with col_m2:
        if not df_status.empty:
            # Funil de Status
            df_funil = df_status.sort_values('Quantidade', ascending=False)
            fig_funil = px.funnel(
                df_funil, 
                x='Quantidade', 
                y='Status',
                title="Funil de Aprovação"
            )
            st.plotly_chart(fig_funil, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    
    st.divider()
    
    # --- TICKET MÉDIO POR VENDEDOR ---
    st.subheader("💰 Ticket Médio por Vendedor")
    
    if not df_vendas.empty:
        df_vendedor = df_vendas.groupby('Vendedor').agg(
            Vendas=('Vendedor', 'count'),
            Ticket_Medio=('valor_venda', 'mean')
        ).reset_index()
        
        df_vendedor = df_vendedor.sort_values('Ticket_Medio', ascending=True)
        
        fig_ticket = px.bar(
            df_vendedor,
            x='Ticket_Medio',
            y='Vendedor',
            orientation='h',
            title="Ticket Médio (R$) - Ordem Crescente",
            text_auto='.2f',
            color='Ticket_Medio',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_ticket, use_container_width=True)
    else:
        st.info("Sem dados para exibir")

# ============================================================================
# 2. GESTÃO DE METAS (COMERCIAL)
# ============================================================================
def exibir_gestao_metas():
    st.header("🎯 Metas das Regionais - Comercial")
    
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id_regional, descricao FROM regional WHERE ativo = 1")
        regionais = {row['descricao']: row['id_regional'] for row in cursor.fetchall()}

    if not regionais:
        st.warning("Nenhuma regional cadastrada.")
        return

    col1, col2 = st.columns(2)
    with col1:
        reg_nome = st.selectbox("Selecione a Regional", list(regionais.keys()))
    with col2:
        data_meta = st.date_input("Mês de Referência", value=datetime.today().replace(day=1))
    
    # Busca metas existentes
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT meta_vendas_qtd, meta_migracao_qtd 
            FROM metas_regionais 
            WHERE id_regional = %s AND MONTH(mes_referencia) = %s AND YEAR(mes_referencia) = %s
        """, (regionais[reg_nome], data_meta.month, data_meta.year))
        metas_existentes = cursor.fetchone()

    valor_padrao_vendas = int(metas_existentes['meta_vendas_qtd']) if metas_existentes else 10
    valor_padrao_migra = int(metas_existentes['meta_migracao_qtd']) if metas_existentes else 5

    c1, c2 = st.columns(2)
    with c1:
        meta_vendas = st.number_input("Meta de Vendas", min_value=1, value=valor_padrao_vendas)
    with c2:
        meta_migra = st.number_input("Meta de Migrações", min_value=1, value=valor_padrao_migra)

    if st.button("💾 Salvar Metas", use_container_width=True):
        try:
            with get_db_cursor(commit=True) as cursor:
                sql = """
                    INSERT INTO metas_regionais (id_regional, mes_referencia, meta_vendas_qtd, meta_migracao_qtd)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    meta_vendas_qtd = VALUES(meta_vendas_qtd),
                    meta_migracao_qtd = VALUES(meta_migracao_qtd)
                """
                cursor.execute(sql, (
                    regionais[reg_nome], 
                    data_meta.replace(day=1), 
                    int(meta_vendas), 
                    int(meta_migra)
                ))
            st.success(f"✅ Metas de {reg_nome} salvas com sucesso!")
            registrar_log(st.session_state.id_usuario, "META", f"Metas salvas para {reg_nome}")
        except Exception as e:
            st.error(f"❌ Erro ao salvar: {e}")

# ============================================================================
# 3. PROGRESSO DE METAS (COMERCIAL)
# ============================================================================
def exibir_progresso_metas_regionais():
    """Exibe o progresso das metas por regional (apenas Comercial)"""
    
    st.subheader("🎯 Progresso das Metas Regionais - Comercial")
    
    # Filtros de tempo
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        meses_pt = MESES_PT
        mes_sel = st.selectbox("📅 Mês", meses_pt, index=datetime.now().month - 1, key="meta_mes")
        mes_num = meses_pt.index(mes_sel) + 1
    with col_f2:
        ano_sel = st.selectbox("📅 Ano", [2025, 2026], index=1, key="meta_ano")
    
    with get_db_cursor() as cursor:
        # Busca todas as regionais
        cursor.execute("SELECT id_regional, descricao FROM regional WHERE ativo = 1")
        regionais = cursor.fetchall()
        
        # Para cada regional, calcula as métricas
        dados_metas = []
        
        for reg in regionais:
            id_reg = reg['id_regional']
            nome_reg = reg['descricao']
            
            # Busca a meta da regional
            cursor.execute("""
                SELECT meta_vendas_qtd, meta_migracao_qtd 
                FROM metas_regionais 
                WHERE id_regional = %s AND MONTH(mes_referencia) = %s AND YEAR(mes_referencia) = %s
            """, (id_reg, mes_num, ano_sel))
            meta = cursor.fetchone()
            
            meta_vendas = int(meta['meta_vendas_qtd']) if meta else 10
            meta_migracoes = int(meta['meta_migracao_qtd']) if meta else 5
            
            # Busca vendas realizadas - apenas COMERCIAL
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_vendas,
                    SUM(CASE WHEN id_status = 2 THEN 1 ELSE 0 END) as vendas_aprovadas,
                    SUM(CASE WHEN id_tipo_operacao = 2 AND id_status = 2 THEN 1 ELSE 0 END) as migracoes_aprovadas,
                    SUM(CASE WHEN id_status = 2 THEN valor_venda ELSE 0 END) as faturamento
                FROM venda v
                JOIN users u ON v.id_usuario_vendedor = u.id_usuario
                WHERE u.id_regional = %s 
                  AND v.setor = 'comercial'
                  AND MONTH(v.data_venda) = %s 
                  AND YEAR(v.data_venda) = %s
                  AND v.ativo = 1
            """, (id_reg, mes_num, ano_sel))
            
            res = cursor.fetchone()
            
            vendas_total = int(res['total_vendas'] or 0)
            vendas_aprovadas = int(res['vendas_aprovadas'] or 0)
            migracoes_aprovadas = int(res['migracoes_aprovadas'] or 0)
            faturamento = float(res['faturamento'] or 0)
            
            # Calcula percentuais
            perc_vendas = (vendas_aprovadas / meta_vendas * 100) if meta_vendas > 0 else 0
            perc_migracoes = (migracoes_aprovadas / meta_migracoes * 100) if meta_migracoes > 0 else 0
            
            falta_vendas = max(0, meta_vendas - vendas_aprovadas)
            falta_migracoes = max(0, meta_migracoes - migracoes_aprovadas)
            
            # Define status visual
            status_vendas = "✅ ACIMA" if perc_vendas >= 100 else "⚠️ PARCIAL" if perc_vendas >= 70 else "❌ ABAIXO"
            status_migra = "✅ ACIMA" if perc_migracoes >= 100 else "⚠️ PARCIAL" if perc_migracoes >= 70 else "❌ ABAIXO"
            
            # Dados para exportação
            status_vendas_export = "ACIMA DA META" if perc_vendas >= 100 else "PARCIAL" if perc_vendas >= 70 else "ABAIXO DA META"
            status_migra_export = "ACIMA DA META" if perc_migracoes >= 100 else "PARCIAL" if perc_migracoes >= 70 else "ABAIXO DA META"
            
            dados_metas.append({
                'regional': nome_reg,
                'meta_vendas': meta_vendas,
                'vendas_aprovadas': vendas_aprovadas,
                'perc_vendas': perc_vendas,
                'status_vendas': status_vendas,
                'status_vendas_export': status_vendas_export,
                'falta_vendas': falta_vendas,
                'meta_migracoes': meta_migracoes,
                'migracoes_aprovadas': migracoes_aprovadas,
                'perc_migracoes': perc_migracoes,
                'status_migra': status_migra,
                'status_migra_export': status_migra_export,
                'falta_migracoes': falta_migracoes,
                'faturamento': faturamento,
                'faturamento_formatado': format_brl(faturamento),
                'total_vendas': vendas_total
            })
    
    if dados_metas:
        df_metas = pd.DataFrame(dados_metas)
        
        # Métricas gerais
        total_meta_vendas = sum(d['meta_vendas'] for d in dados_metas)
        total_vendas_aprovadas = sum(d['vendas_aprovadas'] for d in dados_metas)
        total_meta_migracoes = sum(d['meta_migracoes'] for d in dados_metas)
        total_migracoes_aprovadas = sum(d['migracoes_aprovadas'] for d in dados_metas)
        total_faturamento = sum(d['faturamento'] for d in dados_metas)
        total_vendas_geral = sum(d['total_vendas'] for d in dados_metas)
        
        perc_geral_vendas = (total_vendas_aprovadas / total_meta_vendas * 100) if total_meta_vendas > 0 else 0
        perc_geral_migracoes = (total_migracoes_aprovadas / total_meta_migracoes * 100) if total_meta_migracoes > 0 else 0
        
        # Cards de resumo geral
        st.markdown("### 📊 Resumo Geral")
        col_g1, col_g2, col_g3, col_g4 = st.columns(4)
        
        with col_g1:
            st.metric("🎯 Total Meta Vendas", f"{total_vendas_aprovadas}/{total_meta_vendas}", 
                     f"{perc_geral_vendas:.1f}%")
        with col_g2:
            st.metric("🔄 Total Meta Migrações", f"{total_migracoes_aprovadas}/{total_meta_migracoes}", 
                     f"{perc_geral_migracoes:.1f}%")
        with col_g3:
            st.metric("💰 Faturamento Total", format_brl(total_faturamento))
        with col_g4:
            st.metric("📊 Vendas Totais", f"{total_vendas_geral}")
        
        st.divider()
        
        # Tabela de detalhamento
        st.markdown("### 📋 Detalhamento por Regional")
        
        df_metas['perc_vendas'] = df_metas['perc_vendas'].round(1)
        df_metas['perc_migracoes'] = df_metas['perc_migracoes'].round(1)
        
        def color_percent(val):
            if isinstance(val, (int, float)):
                if val >= 100:
                    return 'background-color: #00cc66; color: white; font-weight: bold'
                elif val >= 70:
                    return 'background-color: #ffaa00; color: white; font-weight: bold'
                else:
                    return 'background-color: #ff4444; color: white; font-weight: bold'
            return ''
        
        df_display = df_metas[['regional', 'meta_vendas', 'vendas_aprovadas', 'perc_vendas', 
                               'status_vendas', 'falta_vendas', 'meta_migracoes', 
                               'migracoes_aprovadas', 'perc_migracoes', 'status_migra', 
                               'falta_migracoes', 'faturamento_formatado', 'total_vendas']].copy()
        
        df_display.columns = ['Regional', 'Meta', 'Feito', '%', 'Status', 'Falta', 
                              'Meta Mig', 'Migrações', '% Mig', 'Status Mig', 'Falta Mig', 
                              'Faturamento', 'Total Vendas']
        
        styled_df = df_display.style.applymap(color_percent, subset=['%', '% Mig'])
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Botões de exportação
        st.divider()
        col_exp1, col_exp2 = st.columns([1, 1])
        
        with col_exp1:
            df_export = df_metas[['regional', 'meta_vendas', 'vendas_aprovadas', 'perc_vendas',
                                   'status_vendas_export', 'falta_vendas', 'meta_migracoes',
                                   'migracoes_aprovadas', 'perc_migracoes', 'status_migra_export',
                                   'falta_migracoes', 'faturamento', 'total_vendas']].copy()
            
            df_export.columns = ['Regional', 'Meta Vendas', 'Vendas Aprovadas', '% Vendas',
                                  'Status Vendas', 'Faltam Vendas', 'Meta Migrações',
                                  'Migrações Aprovadas', '% Migrações', 'Status Migrações',
                                  'Faltam Migrações', 'Faturamento (R$)', 'Total Vendas']
            
            df_export['% Vendas'] = df_export['% Vendas'].apply(lambda x: f"{x:.1f}%")
            df_export['% Migrações'] = df_export['% Migrações'].apply(lambda x: f"{x:.1f}%")
            df_export['Faturamento (R$)'] = df_export['Faturamento (R$)'].apply(format_brl)
            
            csv = df_export.to_csv(index=False, sep=';', encoding='utf-8-sig')
            st.download_button("📥 Exportar CSV", csv, f"metas_comercial_{mes_sel}_{ano_sel}.csv", "text/csv")
        
        with col_exp2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_export.to_excel(writer, sheet_name='Metas Comercial', index=False)
            st.download_button("📊 Exportar Excel", output.getvalue(), 
                              f"metas_comercial_{mes_sel}_{ano_sel}.xlsx", 
                              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        # Gráficos
        st.divider()
        st.markdown("### 📈 Gráficos de Progresso")
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            fig_vendas = px.bar(df_metas, x='regional', y=['vendas_aprovadas', 'meta_vendas'],
                               title="Progresso das Metas de Vendas",
                               barmode='group', color_discrete_map={'vendas_aprovadas': '#28a745', 'meta_vendas': '#ffc107'})
            fig_vendas.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig_vendas, use_container_width=True)
        
        with col_g2:
            fig_migra = px.bar(df_metas, x='regional', y=['migracoes_aprovadas', 'meta_migracoes'],
                              title="Progresso das Metas de Migrações",
                              barmode='group', color_discrete_map={'migracoes_aprovadas': '#17a2b8', 'meta_migracoes': '#ffc107'})
            fig_migra.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig_migra, use_container_width=True)
        
    else:
        st.info("ℹ️ Nenhuma meta encontrada para o período selecionado.")

# ============================================================================
# 4. GESTÃO DE USUÁRIOS (COMPLETA)
# ============================================================================
def gerenciar_usuarios():
    """Gestão completa de usuários com visual moderno e troca de senha"""
    
    # CSS personalizado
    st.markdown("""
    <style>
    .user-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .stat-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid; transition: transform 0.3s; margin-bottom: 1rem; }
    .stat-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
    .badge-ativo { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); color: #1a5a1a; padding: 0.4rem 1rem; border-radius: 25px; font-weight: 600; font-size: 0.85rem; display: inline-block; }
    .badge-inativo { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: #8b0000; padding: 0.4rem 1rem; border-radius: 25px; font-weight: 600; font-size: 0.85rem; display: inline-block; }
    .filter-container { background: #f8fafc; padding: 1.5rem; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 2rem; }
    .user-row { background: white; padding: 1rem; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 0.5rem; transition: all 0.2s; }
    .user-row:hover { background: #f7fafc; border-color: #667eea; }
    div[data-testid="stExpander"] { border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .stButton > button { border-radius: 8px; font-weight: 600; transition: all 0.3s; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="user-header">
        <div style="display: flex; align-items: center; gap: 2rem;">
            <div style="background: rgba(255,255,255,0.2); width: 80px; height: 80px; border-radius: 20px; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 40px;">👥</span>
            </div>
            <div>
                <h1 style="margin: 0; font-size: 2.5rem;">Gestão de Usuários</h1>
                <p style="margin: 0; opacity: 0.9; font-size: 1.1rem;">Gerencie acessos, permissões e senhas do sistema</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_refresh, col_info = st.columns([1, 5])
    with col_refresh:
        if st.button("🔄 Atualizar Dados", use_container_width=True, type="secondary"):
            st.rerun()
    with col_info:
        st.caption("⚡ As alterações são aplicadas em tempo real")

    st.divider()

    tab_lista, tab_cadastro_individual, tab_cadastro_massa, tab_alterar_senha = st.tabs([
        "📋 **Lista de Usuários**", 
        "➕ **Cadastro Individual**",
        "📦 **Cadastro em Massa**",
        "🔐 **Alterar Senha**"
    ])

    # ===== ABA 1: LISTA DE USUÁRIOS =====
    with tab_lista:
        with st.container():
            st.markdown('<div class="filter-container">', unsafe_allow_html=True)
            st.markdown("##### 🔍 Filtros de Busca")
            
            with get_db_cursor() as cursor:
                cursor.execute("SELECT id_regional, descricao FROM regional WHERE ativo = 1 ORDER BY descricao")
                regionais_lista = [("Todas", None)] + [(r['descricao'], r['id_regional']) for r in cursor.fetchall()]
                
                cursor.execute("SELECT id_tipo_usuario, descricao FROM tipo_usuario WHERE ativo = 1 ORDER BY descricao")
                cargos_lista = [("Todos", None)] + [(c['descricao'], c['id_tipo_usuario']) for c in cursor.fetchall()]

            col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([2, 2, 2, 1, 1])
            
            with col_f1:
                filtro_nome = st.text_input("🔤 Nome", placeholder="Digite para buscar...", label_visibility="collapsed")
            with col_f2:
                filtro_regional = st.selectbox("📍 Regional", options=[r[0] for r in regionais_lista], label_visibility="collapsed")
            with col_f3:
                filtro_cargo = st.selectbox("👤 Cargo", options=[c[0] for c in cargos_lista], label_visibility="collapsed")
            with col_f4:
                filtro_setor = st.selectbox("📞 Setor", ["Todos", "comercial", "televendas"], label_visibility="collapsed")
            with col_f5:
                filtro_status = st.selectbox("⚡ Status", ["Todos", "Ativos", "Inativos"], label_visibility="collapsed")
            
            st.markdown('</div>', unsafe_allow_html=True)

        with get_db_cursor() as cursor:
            query = """
                SELECT 
                    u.id_usuario,
                    u.nome_usuario,
                    u.cpf,
                    u.ativo,
                    COALESCE(r.descricao, 'Sem Regional') as regional,
                    COALESCE(t.descricao, 'Sem Cargo') as cargo,
                    u.setor,
                    DATE_FORMAT(u.ultimo_acesso, '%d/%m/%Y %H:%i') as ultimo_acesso_formatado
                FROM users u
                LEFT JOIN regional r ON u.id_regional = r.id_regional
                LEFT JOIN tipo_usuario t ON u.id_tipo_usuario = t.id_tipo_usuario
                WHERE 1=1
            """
            params = []
            
            if filtro_nome:
                query += " AND u.nome_usuario LIKE %s"
                params.append(f"%{filtro_nome}%")
            if filtro_regional and filtro_regional != "Todas":
                query += " AND r.descricao = %s"
                params.append(filtro_regional)
            if filtro_cargo and filtro_cargo != "Todos":
                query += " AND t.descricao = %s"
                params.append(filtro_cargo)
            if filtro_setor and filtro_setor != "Todos":
                query += " AND u.setor = %s"
                params.append(filtro_setor)
            if filtro_status == "Ativos":
                query += " AND u.ativo = 1"
            elif filtro_status == "Inativos":
                query += " AND u.ativo = 0"
            
            query += " ORDER BY u.id_usuario DESC"
            cursor.execute(query, params)
            usuarios = cursor.fetchall()

        if usuarios:
            df_usuarios = pd.DataFrame(usuarios)
            total_ativos = df_usuarios['ativo'].sum()
            total_inativos = len(df_usuarios) - total_ativos
            
            col_stats = st.columns(4)
            with col_stats[0]:
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #667eea;">
                    <p style="color: #718096; margin: 0; font-size: 0.9rem;">TOTAL DE USUÁRIOS</p>
                    <p style="color: #2d3748; font-size: 2.5rem; font-weight: 700; margin: 0;">{len(df_usuarios)}</p>
                    <p style="color: #a0aec0; margin: 0; font-size: 0.8rem;">cadastrados</p>
                </div>
                """, unsafe_allow_html=True)
            with col_stats[1]:
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #48bb78;">
                    <p style="color: #718096; margin: 0; font-size: 0.9rem;">ATIVOS</p>
                    <p style="color: #2f855a; font-size: 2.5rem; font-weight: 700; margin: 0;">{total_ativos}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_stats[2]:
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #f56565;">
                    <p style="color: #718096; margin: 0; font-size: 0.9rem;">INATIVOS</p>
                    <p style="color: #c53030; font-size: 2.5rem; font-weight: 700; margin: 0;">{total_inativos}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_stats[3]:
                qtd_televendas = len(df_usuarios[df_usuarios['setor'] == 'televendas'])
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #ed8936;">
                    <p style="color: #718096; margin: 0; font-size: 0.9rem;">TELEVENDAS</p>
                    <p style="color: #c05621; font-size: 2.5rem; font-weight: 700; margin: 0;">{qtd_televendas}</p>
                </div>
                """, unsafe_allow_html=True)

            st.divider()
            st.markdown("##### 📋 Lista de Usuários")
            
            for idx, user in enumerate(usuarios):
                with st.container():
                    status_class = "badge-ativo" if user['ativo'] else "badge-inativo"
                    status_text = "ATIVO" if user['ativo'] else "INATIVO"
                    
                    # Melhoria na exibição do setor
                    if user['setor'] == 'televendas':
                        setor_display = "📞 Operador TV"
                    else:
                        setor_display = "🏢 Vendedor"
                    
                    cpf = user['cpf']
                    if cpf and len(str(cpf)) == 11:
                        cpf_str = str(cpf)
                        cpf_formatado = f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"
                    else:
                        cpf_formatado = cpf
                    
                    col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 2, 2, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{user['nome_usuario']}**")
                        st.caption(f"ID: {user['id_usuario']}")
                    with col2:
                        st.markdown(f"📋 {cpf_formatado}")
                    with col3:
                        st.markdown(f"📍 {user['regional']}")
                    with col4:
                        st.markdown(f"👤 {user['cargo']}")
                    with col5:
                        st.markdown(f"{setor_display}")
                    with col6:
                        st.markdown(f"🕐 {user['ultimo_acesso_formatado'] or 'Nunca'}")
                    with col7:
                        st.markdown(f'<span class="{status_class}">{status_text}</span>', unsafe_allow_html=True)
                    
                    with st.expander(f"⚙️ Ações para {user['nome_usuario']}"):
                        col_a1, col_a2, col_a3, col_a4 = st.columns(4)
                        with col_a1:
                            if st.button(f"🔐 Nova Senha", key=f"senha_{user['id_usuario']}"):
                                st.session_state['reset_user_id'] = user['id_usuario']
                                st.session_state['reset_user_nome'] = user['nome_usuario']
                                st.rerun()
                        with col_a2:
                            if user['ativo']:
                                if st.button(f"❌ Desativar", key=f"desativar_{user['id_usuario']}"):
                                    with get_db_cursor(commit=True) as cursor:
                                        cursor.execute("UPDATE users SET ativo = 0 WHERE id_usuario = %s", (user['id_usuario'],))
                                    st.success(f"Usuário desativado!")
                                    st.rerun()
                            else:
                                if st.button(f"✅ Ativar", key=f"ativar_{user['id_usuario']}"):
                                    with get_db_cursor(commit=True) as cursor:
                                        cursor.execute("UPDATE users SET ativo = 1 WHERE id_usuario = %s", (user['id_usuario'],))
                                    st.success(f"Usuário ativado!")
                                    st.rerun()
                        with col_a3:
                            st.info("Email em desenvolvimento")
                        with col_a4:
                            st.warning("Contate o suporte para excluir")
                    
                    st.markdown("---" if idx < len(usuarios) - 1 else "")
        else:
            st.warning("⚠️ Nenhum usuário encontrado.")

    # ===== ABA 2: CADASTRO INDIVIDUAL =====
    with tab_cadastro_individual:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f6f9fc 0%, #e6f0f9 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <h3 style="margin: 0; color: #2d3748;">➕ Novo Cadastro</h3>
            <p style="margin: 0; color: #4a5568;">Preencha os dados para criar um novo usuário</p>
        </div>
        """, unsafe_allow_html=True)
        
        with get_db_cursor() as cursor:
            cursor.execute("SELECT id_regional, descricao FROM regional WHERE ativo = 1 ORDER BY descricao")
            regionais_cad = {r['descricao']: r['id_regional'] for r in cursor.fetchall()}
            cursor.execute("SELECT id_tipo_usuario, descricao FROM tipo_usuario WHERE ativo = 1 ORDER BY descricao")
            cargos_cad = {c['descricao']: c['id_tipo_usuario'] for c in cursor.fetchall()}
        
        with st.form("form_cadastro_usuario", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📋 Dados Pessoais")
                nome = st.text_input("Nome Completo *", placeholder="Ex: João Silva (nome real, não use o cargo)")
                cpf = st.text_input("CPF *", max_chars=14, placeholder="000.000.000-00")
            
            with col2:
                st.markdown("##### 🏢 Dados Profissionais")
                regional_sel = st.selectbox("Regional *", options=list(regionais_cad.keys()))
                cargo_sel = st.selectbox("Cargo *", options=list(cargos_cad.keys()))
                setor_sel = st.selectbox("Setor *", options=["comercial", "televendas"])
                senha = st.text_input("Senha *", type="password", value="Mell@2026")
                ativo_sel = st.checkbox("Usuário Ativo", value=True)
            
            st.divider()
            
            if st.form_submit_button("✅ Cadastrar Usuário", use_container_width=True, type="primary"):
                if not nome or not cpf:
                    st.error("❌ Nome e CPF são obrigatórios!")
                else:
                    cpf_limpo = ''.join(filter(str.isdigit, cpf))
                    if len(cpf_limpo) != 11:
                        st.error("❌ CPF deve ter 11 dígitos!")
                    else:
                        try:
                            with get_db_cursor(commit=True) as cursor:
                                cursor.execute("SELECT id_usuario FROM users WHERE cpf = %s", (cpf_limpo,))
                                if cursor.fetchone():
                                    st.error("❌ CPF já cadastrado!")
                                else:
                                    sql = """
                                        INSERT INTO users 
                                        (nome_usuario, cpf, id_regional, id_tipo_usuario, setor, senha, ativo, ultimo_acesso)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)
                                    """
                                    cursor.execute(sql, (
                                        nome.upper().strip(),
                                        cpf_limpo,
                                        regionais_cad[regional_sel],
                                        cargos_cad[cargo_sel],
                                        setor_sel,
                                        senha,
                                        1 if ativo_sel else 0
                                    ))
                                    st.success(f"✅ Usuário {nome.upper()} cadastrado com sucesso!")
                                    registrar_log(st.session_state.id_usuario, "USUÁRIO", f"Cadastrou: {nome}")
                                    st.balloons()
                        except Exception as e:
                            st.error(f"❌ Erro ao cadastrar: {str(e)}")

    # ===== ABA 3: CADASTRO EM MASSA =====
    with tab_cadastro_massa:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f6f9fc 0%, #e6f0f9 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <h3 style="margin: 0; color: #2d3748;">📦 Cadastro em Massa</h3>
            <p style="margin: 0; color: #4a5568;">Cadastre múltiplos usuários de uma vez</p>
        </div>
        """, unsafe_allow_html=True)
        
        with get_db_cursor() as cursor:
            cursor.execute("SELECT id_regional, descricao FROM regional WHERE ativo = 1")
            regionais_massa = {r['descricao']: r['id_regional'] for r in cursor.fetchall()}
            cursor.execute("SELECT id_tipo_usuario, descricao FROM tipo_usuario WHERE ativo = 1")
            cargos_massa = {c['descricao']: c['id_tipo_usuario'] for c in cursor.fetchall()}
        
        with st.container(border=True):
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                regional_massa = st.selectbox("📍 Regional", list(regionais_massa.keys()), key="reg_massa")
            with col_m2:
                cargo_padrao = st.selectbox("👤 Cargo", list(cargos_massa.keys()), key="cargo_massa")
            with col_m3:
                setor_massa = st.selectbox("📞 Setor", ["comercial", "televendas"], key="setor_massa")
            
            senha_padrao = st.text_input("🔐 Senha padrão", value="Mell@2026", type="password")
            st.info("💡 Todos os usuários receberão esta senha inicial")
        
        st.markdown("##### 📝 Lista de Usuários (Nome;CPF)")
        st.caption("Formato: **Nome;CPF** (um por linha) - Use nomes reais, não cargos")
        
        with st.expander("📋 Ver exemplo"):
            st.code("João Silva;123.456.789-00\nMaria Santos;987.654.321-00")
        
        texto_usuarios = st.text_area("Cole a lista aqui:", height=150, key="texto_usuarios_massa")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        
        with col_b1:
            if st.button("📋 Validar Lista", use_container_width=True):
                if texto_usuarios:
                    usuarios_validos, usuarios_invalidos = [], []
                    for linha in texto_usuarios.strip().split('\n'):
                        if ';' in linha:
                            partes = linha.split(';', 1)
                            nome, cpf = partes[0].strip(), ''.join(filter(str.isdigit, partes[1].strip()))
                            if nome and len(cpf) == 11:
                                usuarios_validos.append({"nome": nome, "cpf": cpf})
                            else:
                                usuarios_invalidos.append(linha)
                    
                    st.session_state['usuarios_validados'] = usuarios_validos
                    if usuarios_validos:
                        st.success(f"✅ {len(usuarios_validos)} válidos")
                    if usuarios_invalidos:
                        st.warning(f"⚠️ {len(usuarios_invalidos)} inválidos")
        
        with col_b2:
            if st.button("🚀 Cadastrar Todos", use_container_width=True, type="primary"):
                if 'usuarios_validados' in st.session_state:
                    sucessos, erros = 0, 0
                    for user in st.session_state['usuarios_validados']:
                        try:
                            with get_db_cursor(commit=True) as cursor:
                                cursor.execute("SELECT id_usuario FROM users WHERE cpf = %s", (user['cpf'],))
                                if not cursor.fetchone():
                                    sql = """
                                        INSERT INTO users 
                                        (nome_usuario, cpf, id_regional, id_tipo_usuario, setor, senha, ativo, ultimo_acesso)
                                        VALUES (%s, %s, %s, %s, %s, %s, 1, NULL)
                                    """
                                    cursor.execute(sql, (
                                        user['nome'].upper(), user['cpf'],
                                        regionais_massa[regional_massa], cargos_massa[cargo_padrao],
                                        setor_massa, senha_padrao
                                    ))
                                    sucessos += 1
                                else:
                                    erros += 1
                        except:
                            erros += 1
                    
                    st.success(f"✅ {sucessos} cadastros realizados, {erros} erros")
                    if sucessos > 0:
                        registrar_log(st.session_state.id_usuario, "USUÁRIO", f"Cadastro em massa: {sucessos} ok, {erros} erros")
                    del st.session_state['usuarios_validados']
                    st.rerun()
        
        with col_b3:
            if st.button("🧹 Limpar", use_container_width=True):
                st.session_state.pop('usuarios_validados', None)
                st.rerun()

    # ===== ABA 4: ALTERAR SENHA =====
    with tab_alterar_senha:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f6f9fc 0%, #e6f0f9 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <h3 style="margin: 0; color: #2d3748;">🔐 Alteração de Senha</h3>
            <p style="margin: 0; color: #4a5568;">Altere a senha de um usuário específico</p>
        </div>
        """, unsafe_allow_html=True)
        
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT id_usuario, nome_usuario, cpf, setor 
                FROM users 
                WHERE ativo = 1 
                ORDER BY nome_usuario
            """)
            usuarios_ativos = cursor.fetchall()
        
        if usuarios_ativos:
            # Criar opções com indicação do setor
            opcoes = {}
            for u in usuarios_ativos:
                setor_icon = "📞" if u['setor'] == 'televendas' else "🏢"
                opcoes[f"{setor_icon} {u['nome_usuario']} - {u['cpf']}"] = u['id_usuario']
            
            usuario_sel = st.selectbox("👤 Selecione o Usuário", options=list(opcoes.keys()))
            user_id = opcoes[usuario_sel]
            
            with st.form("form_alterar_senha"):
                nova_senha = st.text_input("Nova Senha", type="password", placeholder="Mínimo 6 caracteres")
                confirmar = st.text_input("Confirmar Nova Senha", type="password")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✅ Alterar Senha", use_container_width=True):
                        if not nova_senha:
                            st.error("❌ Digite a nova senha!")
                        elif len(nova_senha) < 6:
                            st.error("❌ A senha deve ter no mínimo 6 caracteres!")
                        elif nova_senha != confirmar:
                            st.error("❌ As senhas não conferem!")
                        else:
                            try:
                                with get_db_cursor(commit=True) as cursor:
                                    cursor.execute("UPDATE users SET senha = %s WHERE id_usuario = %s", (nova_senha, user_id))
                                st.success("✅ Senha alterada com sucesso!")
                                registrar_log(st.session_state.id_usuario, "SENHA", f"Senha alterada para usuário ID: {user_id}")
                                st.balloons()
                            except Exception as e:
                                st.error(f"❌ Erro ao alterar senha: {str(e)}")
                with col2:
                    if st.form_submit_button("🔙 Cancelar", use_container_width=True):
                        st.rerun()
        else:
            st.warning("⚠️ Nenhum usuário ativo encontrado para alterar senha.")
# 5. DASHBOARD DE CANCELAMENTOS
def exibir_dashboard_cancelamentos():
    """Dashboard consolidado de cancelamentos"""
    
    st.header("📉 Análise de Desistências")
    
    with get_db_cursor() as cursor:
        cursor.execute("DESCRIBE cancelamentos")
        colunas_cancel = [col['Field'] for col in cursor.fetchall()]
        
        cursor.execute("SHOW COLUMNS FROM cancelamentos WHERE Field = 'status'")
        status_info = cursor.fetchone()
        valores_status = []
        if status_info and status_info['Type'].startswith("enum('"):
            valores_status = [v.strip("'") for v in status_info['Type'][6:-2].split("','")]
    
    possiveis_colunas = ['id_vendedor', 'id_usuario_vendedor', 'vendedor_id', 'usuario_id']
    coluna_vendedor = next((col for col in possiveis_colunas if col in colunas_cancel), None)
    
    if not coluna_vendedor:
        st.error("❌ Não foi possível identificar a coluna de relacionamento com o vendedor")
        return
    
    coluna_observacao = 'observacao' if 'observacao' in colunas_cancel else None
    
    tab_pendentes, tab_historico, tab_analise = st.tabs(["⏳ Pendentes", "📋 Histórico", "📊 Análise"])
    
    with tab_pendentes:
        st.subheader("Cancelamentos Pendentes")
        
        with get_db_cursor() as cursor:
            # CORREÇÃO: usar %d/%m/%Y com um % apenas
            query = f"""
                SELECT 
                    c.id_cancelamento,
                    DATE_FORMAT(c.data_ocorrencia, '%d/%m/%Y') as data,
                    COALESCE(r.descricao, 'Sem Regional') as regional,
                    COALESCE(u.nome_usuario, 'Vendedor não encontrado') as vendedor,
                    c.valor_original
                FROM cancelamentos c
                LEFT JOIN users u ON c.{coluna_vendedor} = u.id_usuario
                LEFT JOIN regional r ON u.id_regional = r.id_regional
                WHERE c.status = 'pendente'
                ORDER BY c.data_ocorrencia DESC
            """
            cursor.execute(query)
            pendentes = cursor.fetchall()
        
        if pendentes:
            total_valor = sum(p['valor_original'] for p in pendentes)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Pendentes", len(pendentes))
            col2.metric("Valor Total", format_brl(total_valor))
            col3.metric("Média", format_brl(total_valor/len(pendentes) if pendentes else 0))
            
            st.divider()
            
            for cancel in pendentes:
                with st.container():
                    col_id, col_status, _ = st.columns([1, 1, 4])
                    with col_id:
                        st.markdown(f"**#{cancel['id_cancelamento']}**")
                    with col_status:
                        st.markdown("`PENDENTE`")
                    
                    col_v, col_r, col_d, col_val = st.columns(4)
                    with col_v:
                        st.markdown("VENDEDOR")
                        st.markdown(f"**{cancel['vendedor']}**")
                    with col_r:
                        st.markdown("REGIONAL")
                        st.markdown(f"**{cancel['regional']}**")
                    with col_d:
                        st.markdown("DATA")
                        st.markdown(f"**{cancel['data']}**")
                    with col_val:
                        st.markdown("VALOR")
                        cor = "#dc3545" if cancel['valor_original'] > 500 else "#fd7e14" if cancel['valor_original'] > 200 else "#ffc107"
                        st.markdown(f"**{format_brl(cancel['valor_original'])}**")
                    
                    col_btn1, col_btn2, _ = st.columns([1, 1, 4])
                    with col_btn1:
                        if 'aprovado' in valores_status:
                            if st.button(f"✅ Aprovar", key=f"apr_{cancel['id_cancelamento']}"):
                                with get_db_cursor(commit=True) as cursor:
                                    cursor.execute("UPDATE cancelamentos SET status = 'aprovado' WHERE id_cancelamento = %s", (cancel['id_cancelamento'],))
                                st.success("Aprovado!")
                                st.rerun()
                    with col_btn2:
                        if 'revisado' in valores_status:
                            with st.popover(f"📝 Revisar"):
                                motivo = st.text_area("Motivo", key=f"motivo_{cancel['id_cancelamento']}")
                                if st.button("Confirmar", key=f"conf_{cancel['id_cancelamento']}"):
                                    if motivo:
                                        with get_db_cursor(commit=True) as cursor:
                                            cursor.execute("UPDATE cancelamentos SET status = 'revisado' WHERE id_cancelamento = %s", (cancel['id_cancelamento'],))
                                            if coluna_observacao:
                                                cursor.execute(f"UPDATE cancelamentos SET {coluna_observacao} = %s WHERE id_cancelamento = %s", (motivo, cancel['id_cancelamento']))
                                        st.success("Revisado!")
                                        st.rerun()
                    
                    st.divider()
        else:
            st.info("✅ Nenhum cancelamento pendente!")
            st.balloons()
    
    with tab_historico:
        st.subheader("Histórico de Cancelamentos")
        with get_db_cursor() as cursor:
            # CORREÇÃO: usar %d/%m/%Y com um % apenas
            query = f"""
                SELECT 
                    c.id_cancelamento,
                    DATE_FORMAT(c.data_ocorrencia, '%d/%m/%Y') as data,
                    COALESCE(u.nome_usuario, 'Desconhecido') as vendedor,
                    c.valor_original,
                    c.status
                FROM cancelamentos c
                LEFT JOIN users u ON c.{coluna_vendedor} = u.id_usuario
                WHERE c.status != 'pendente'
                ORDER BY c.data_ocorrencia DESC
                LIMIT 100
            """
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall())
        
        if not df.empty:
            # Converte valores para float
            if 'valor_original' in df.columns:
                df['valor_original'] = df['valor_original'].astype(float)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False, encoding='utf-8-sig', sep=';')
            st.download_button("📥 Exportar CSV", csv, "historico_cancelamentos.csv", "text/csv")
        else:
            st.info("Nenhum registro encontrado")
    
    with tab_analise:
        st.subheader("Análise de Cancelamentos")
        with get_db_cursor() as cursor:
            cursor.execute("SELECT status, COUNT(*) as qtd, SUM(valor_original) as total FROM cancelamentos GROUP BY status")
            df = pd.DataFrame(cursor.fetchall())
        
        if not df.empty:
            df['total'] = df['total'].apply(format_brl)
            st.dataframe(df, use_container_width=True, hide_index=True)
            fig = px.pie(df, values='total', names='status', title="Distribuição por Valor")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum dado disponível")

# ============================================================================
# 6. VISÃO DE INSTALAÇÕES HUBSOFT (CORRIGIDA - SEM ERRO KeyError)
# ============================================================================

def exibir_visao_instalacoes_hubsoft():
    """Exibe visão de instalações do Hubsoft para o admin"""
    
    st.markdown("<h1 style='color: #01384d;'>📊 Visão de Instalações Hubsoft</h1>", unsafe_allow_html=True)
    st.caption("Visão geral de todas as vendas e status de instalação")
    
    # --- VERIFICA REGIONAIS PARA FILTRO ---
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id_regional, descricao FROM regional WHERE ativo = 1")
        regionais = {r['descricao']: r['id_regional'] for r in cursor.fetchall()}
        regs = {"Geral": 0, **regionais}
    
    # Filtros
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        reg_sel = st.selectbox("📍 Regional", list(regs.keys()), key="admin_reg_filtro", index=0)
    with col_f2:
        setor_sel = st.selectbox(
            "📍 Setor", 
            ["Todos", "Comercial", "Televendas"],
            key="admin_setor_filtro",
            index=0
        )
        if setor_sel == "Comercial":
            setor_db = "comercial"
        elif setor_sel == "Televendas":
            setor_db = "televendas"
        else:
            setor_db = "todos"
    with col_f3:
        mes_sel = st.selectbox("📅 Mês", MESES_PT, index=datetime.now().month-1, key="admin_mes_filtro")
        mes_num = MESES_PT.index(mes_sel) + 1
    with col_f4:
        ano_sel = st.selectbox("📅 Ano", [2025, 2026], index=1, key="admin_ano_filtro")
    
    st.divider()
    
    # === PASSO 1: BUSCAR VENDAS DO PERÍODO ===
    if st.button("📊 1. Buscar Vendas e Migrações do Período", use_container_width=True, type="secondary"):
        with st.spinner(f"Buscando vendas de {mes_sel}/{ano_sel}..."):
            # Usa a função importada do auditor
            df_vendas = buscar_vendas_do_periodo(reg_sel, mes_num, ano_sel, regs, setor_db)
            
            if df_vendas is not None and not df_vendas.empty:
                st.session_state.admin_df_vendas = df_vendas
                st.session_state.admin_df_conciliado = None
                
                # ========== CORREÇÃO: Verificação segura da coluna 'id_servico' ==========
                # Verifica se a coluna 'id_servico' existe
                if 'id_servico' in df_vendas.columns:
                    vendas_com_id = df_vendas['id_servico'].notna().sum()
                else:
                    vendas_com_id = 0
                    st.warning("⚠️ A coluna 'id_servico' não está presente no DataFrame retornado.")
                    st.info(f"Colunas disponíveis: {list(df_vendas.columns)}")
                # ========== FIM DA CORREÇÃO ==========
                
                # Contagem por setor
                if 'setor' in df_vendas.columns:
                    qtd_comercial = len(df_vendas[df_vendas['setor'] == 'comercial'])
                    qtd_televendas = len(df_vendas[df_vendas['setor'] == 'televendas'])
                    
                    st.success(f"✅ {len(df_vendas)} registros encontrados no período!")
                    st.info(f"📊 Comercial: {qtd_comercial} | Televendas: {qtd_televendas} | IDs válidos: {vendas_com_id}")
                else:
                    st.success(f"✅ {len(df_vendas)} registros encontrados no período!")
                    st.info(f"📊 {vendas_com_id} registros possuem ID de serviço")
                
                # Mostra preview
                colunas_preview = ['id_venda', 'vendedor_nome', 'tipo_operacao', 'data_venda_br']
                if 'setor' in df_vendas.columns:
                    colunas_preview.append('setor')
                if 'id_servico' in df_vendas.columns:
                    colunas_preview.append('id_servico')
                
                st.dataframe(df_vendas[colunas_preview].head(10),
                           use_container_width=True, hide_index=True)
            else:
                st.warning("⚠️ Nenhuma venda encontrada no período selecionado.")
                st.session_state.admin_df_vendas = pd.DataFrame()
                st.session_state.admin_df_conciliado = None
    
    st.divider()
    
    # === PASSO 2: CONSULTAR HUBSOFT ===
    if "admin_df_vendas" in st.session_state:
        df_vendas = st.session_state.admin_df_vendas
        
        if df_vendas is None:
            df_vendas = pd.DataFrame()
            st.session_state.admin_df_vendas = df_vendas
        
        if not df_vendas.empty and isinstance(df_vendas, pd.DataFrame):
            # ========== CORREÇÃO: Extração segura dos IDs ==========
            # Verifica se a coluna existe antes de acessar
            if 'id_servico' in df_vendas.columns:
                ids_validos = df_vendas['id_servico'].dropna().astype(str).tolist()
                ids_validos = [id_str for id_str in ids_validos if id_str.strip() and id_str.strip().isdigit()]
            else:
                ids_validos = []
                st.warning("⚠️ Coluna 'id_servico' não encontrada no DataFrame. Não é possível consultar o Hubsoft.")
                st.info(f"Colunas disponíveis: {list(df_vendas.columns)}")
            # ========== FIM DA CORREÇÃO ==========
            
            st.subheader("📋 Vendas Carregadas")
            st.write(f"**Total de registros:** {len(df_vendas)}")
            st.write(f"**IDs válidos para consulta:** {len(ids_validos)}")
            
            if st.button("🔍 2. Consultar Hubsoft", use_container_width=True, type="primary"):
                if ids_validos:
                    with st.spinner(f"Consultando {len(ids_validos)} IDs no Hubsoft..."):
                        resultados_hub = consultar_ids_hubsoft(ids_validos)
                        
                        if resultados_hub:
                            df_conciliado = criar_dataframe_conciliado(df_vendas, resultados_hub, mes_num, ano_sel)
                            
                            if df_conciliado is not None and not df_conciliado.empty:
                                st.session_state.admin_df_conciliado = df_conciliado
                                st.success(f"✅ Consulta concluída! {len(df_conciliado)} registros processados.")
                                st.rerun()
                            else:
                                st.session_state.admin_df_conciliado = None
                                st.warning("⚠️ Nenhum dado válido retornado da consulta.")
                else:
                    st.warning("⚠️ Nenhum ID válido para consulta")
                    st.session_state.admin_df_conciliado = None
        else:
            if df_vendas is not None and df_vendas.empty:
                st.info("📭 Nenhuma venda encontrada. Clique em 'Buscar Vendas do Período'.")
            st.session_state.admin_df_conciliado = None
    
    st.divider()
    
    # === PASSO 3: EXIBIR RESULTADOS ===
    if "admin_df_conciliado" in st.session_state:
        df_conciliado = st.session_state.admin_df_conciliado
        
        # Verifica se df_conciliado não é None antes de acessar .empty
        if df_conciliado is not None and not df_conciliado.empty and isinstance(df_conciliado, pd.DataFrame):
            st.subheader("📊 Resultado da Consulta Hubsoft")
            
            # === FILTRO PARA MOSTRAR APENAS INSTALADOS/MIGRADOS ===
            col_filtro1, col_filtro2 = st.columns([1, 3])
            with col_filtro1:
                mostrar_apenas_concluidos = st.checkbox("✅ Mostrar apenas instalados/migrados", value=False, key="admin_filtro_instalados")
            
            # Aplica o filtro corretamente
            if mostrar_apenas_concluidos:
                if 'Instalado no Mês' in df_conciliado.columns:
                    df_exibicao = df_conciliado[
                        (df_conciliado['Instalado no Mês'] == True)
                    ].copy()
                    st.info(f"📌 Mostrando apenas {len(df_exibicao)} registros instalados/migrados no período de {mes_sel}/{ano_sel}")
                else:
                    df_exibicao = df_conciliado[
                        (df_conciliado['Status'].str.contains('INSTALADO|MIGRADO', na=False))
                    ].copy()
                    st.info(f"📌 Mostrando apenas {len(df_exibicao)} registros concluídos")
            else:
                df_exibicao = df_conciliado
            
            # Verifica se a coluna Status existe
            if 'Status' not in df_exibicao.columns:
                df_exibicao['Status'] = '⚠️ SEM STATUS'
            
            # Métricas com validação de mês
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("📋 Total Registros", len(df_exibicao))
            
            with col_m2:
                if 'Instalado no Mês' in df_exibicao.columns:
                    instalados_no_mes = len(df_exibicao[df_exibicao['Instalado no Mês'] == True])
                    st.metric("✅ Concluídos no Mês", instalados_no_mes)
                else:
                    instalados = len(df_exibicao[
                        df_exibicao['Status'].str.contains('INSTALADO|MIGRADO', na=False)
                    ])
                    st.metric("✅ Concluídos", instalados)
            
            with col_m3:
                if not mostrar_apenas_concluidos:
                    if 'Instalado no Mês' in df_exibicao.columns:
                        nao_instalados = len(df_exibicao[df_exibicao['Instalado no Mês'] == False])
                    else:
                        nao_instalados = len(df_exibicao[~df_exibicao['Status'].str.contains('INSTALADO|MIGRADO', na=False)])
                    st.metric("❌ Não Concluídos/Fora do Período", nao_instalados)
                else:
                    st.metric("❌ Não Concluídos", 0)
            
            with col_m4:
                if 'Valor (R$)' in df_exibicao.columns:
                    if 'Instalado no Mês' in df_exibicao.columns:
                        valor_total = df_exibicao[
                            df_exibicao['Instalado no Mês'] == True
                        ]['Valor (R$)'].sum()
                    else:
                        valor_total = df_exibicao[
                            df_exibicao['Status'].str.contains('INSTALADO|MIGRADO', na=False)
                        ]['Valor (R$)'].sum()
                    st.metric("💰 Valor Total Concluído no Mês", format_brl(valor_total))
                else:
                    st.metric("💰 Valor Total Concluído", "R$ 0,00")
            
            st.divider()
            
            # Tabela de resultados
            st.subheader("📋 Detalhamento das Instalações")
            
            # Define as colunas para exibição
            colunas_exibir = [
                'ID Venda', 'Vendedor', 'ID Serviço', 'Tipo Operação', 'Setor',
                'Data Venda', 'Plano', 'Data Instalação', 'Valor (R$)', 'Status'
            ]
            
            df_display = df_exibicao[[c for c in colunas_exibir if c in df_exibicao.columns]]
            
            # Aplica cores
            styled_df = df_display.style.applymap(
                colorir_status_hubsoft, 
                subset=['Status']
            )
            
            # Formata valores
            if 'Valor (R$)' in df_display.columns:
                styled_df = styled_df.format({
                    'Valor (R$)': lambda x: format_brl(x) if x > 0 else "R$ 0,00"
                })
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Botão exportar
            csv_data = df_exibicao.to_csv(index=False, encoding='utf-8-sig', sep=';')
            st.download_button(
                "📥 Exportar Relatório",
                csv_data,
                f"instalacoes_hubsoft_{mes_sel}_{ano_sel}.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            # Mensagem quando não há dados
            if df_conciliado is None:
                st.info("📭 Nenhum dado de consulta disponível. Clique em 'Consultar Hubsoft' primeiro.")
            elif df_conciliado.empty:
                st.info("📭 Nenhum resultado encontrado para a consulta.")

# ============================================================================
# 7. CÁLCULO DE COMISSÕES (COM FILTRO DE SETOR OPCIONAL)
# ============================================================================
def exibir_comissoes(setor='todos'):
    """Cálculo de comissões por vendedor e liderança"""
    
    titulo = "💰 Cálculo de Comissões"
    if setor == 'televendas':
        titulo = "📞 Cálculo de Comissões - Televendas"
    elif setor == 'comercial':
        titulo = "🏢 Cálculo de Comissões - Comercial"
    st.header(titulo)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        meses_pt = MESES_PT
        mes_sel = st.selectbox("Mês", meses_pt, index=datetime.now().month - 1)
        mes_num = meses_pt.index(mes_sel) + 1
    with col_f2:
        ano_sel = st.selectbox("Ano", [2025, 2026], index=1)
    
    query = """
        SELECT 
            u.id_usuario, u.nome_usuario, COALESCE(t.descricao, 'Sem Cargo') as cargo,
            SUM(CASE WHEN v.id_tipo_operacao = 1 THEN 1 ELSE 0 END) as total_vendas,
            SUM(CASE WHEN v.id_tipo_operacao = 2 THEN 1 ELSE 0 END) as total_migracoes,
            SUM(CASE WHEN v.id_tipo_operacao = 1 THEN v.valor_venda ELSE 0 END) as valor_vendas,
            SUM(CASE WHEN v.id_tipo_operacao = 2 THEN v.valor_venda ELSE 0 END) as valor_migracoes,
            SUM(v.valor_venda) as valor_total
        FROM venda v
        JOIN users u ON v.id_usuario_vendedor = u.id_usuario
        LEFT JOIN tipo_usuario t ON u.id_tipo_usuario = t.id_tipo_usuario
        WHERE v.id_status = 2 
          AND MONTH(v.data_venda) = %s 
          AND YEAR(v.data_venda) = %s
          AND v.ativo = 1
    """
    params = [mes_num, ano_sel]
    
    if setor != 'todos':
        query += " AND v.setor = %s"
        params.append(setor)
    
    query += " GROUP BY u.id_usuario, u.nome_usuario, t.descricao ORDER BY valor_total DESC"
    
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        vendas = cursor.fetchall()
        cursor.execute("""
            SELECT c.id_vendedor, SUM(c.valor_original) as total_estornos
            FROM cancelamentos c
            WHERE c.status = 'aprovado'
              AND MONTH(c.data_ocorrencia) = %s 
              AND YEAR(c.data_ocorrencia) = %s
            GROUP BY c.id_vendedor
        """, (mes_num, ano_sel))
        estornos = cursor.fetchall()
    
    if not vendas:
        st.warning("Nenhuma venda encontrada")
        return
    
    df_vendas = pd.DataFrame(vendas)
    df_estornos = pd.DataFrame(estornos) if estornos else pd.DataFrame(columns=['id_vendedor', 'total_estornos'])
    
    comissoes = []
    total_calc, total_estornos_geral, total_final = 0, 0, 0
    COMISSAO_VENDA, COMISSAO_MIGRACAO = 0.05, 0.03
    
    for venda in vendas:
        vendedor_id = venda['id_usuario']
        estorno = df_estornos[df_estornos['id_vendedor'] == vendedor_id]['total_estornos'].sum() if not df_estornos.empty else 0
        
        com_vendas = venda['valor_vendas'] * COMISSAO_VENDA
        com_migra = venda['valor_migracoes'] * COMISSAO_MIGRACAO
        com_calc = com_vendas + com_migra
        
        if venda['total_vendas'] >= 30:
            com_calc *= 1.2
        if venda['total_migracoes'] >= 10:
            com_calc *= 1.1
        
        com_final = max(0, com_calc - estorno)
        
        total_calc += com_calc
        total_estornos_geral += estorno
        total_final += com_final
        
        comissoes.append({
            'vendedor': venda['nome_usuario'], 'cargo': venda['cargo'],
            'vendas': venda['total_vendas'], 'migracoes': venda['total_migracoes'],
            'valor_vendas': venda['valor_vendas'], 'valor_migracoes': venda['valor_migracoes'],
            'comissao_vendas': com_vendas, 'comissao_migracoes': com_migra,
            'comissao_calc': com_calc, 'estornos': estorno, 'a_pagar': com_final
        })
    
    st.subheader("📋 Comissões por Vendedor")
    df = pd.DataFrame(comissoes)
    col_config = {
        "vendedor": "Vendedor", "cargo": "Cargo", "vendas": "Vendas",
        "migracoes": "Migrações", "valor_vendas": st.column_config.NumberColumn("Valor Vendas", format="R$ %.2f"),
        "valor_migracoes": st.column_config.NumberColumn("Valor Migrações", format="R$ %.2f"),
        "comissao_vendas": st.column_config.NumberColumn("Comissão Vendas", format="R$ %.2f"),
        "comissao_migracoes": st.column_config.NumberColumn("Comissão Migrações", format="R$ %.2f"),
        "comissao_calc": st.column_config.NumberColumn("Comissão Total", format="R$ %.2f"),
        "estornos": st.column_config.NumberColumn("Estornos", format="R$ %.2f"),
        "a_pagar": st.column_config.NumberColumn("A Pagar", format="R$ %.2f")
    }
    st.dataframe(df, column_config=col_config, use_container_width=True, hide_index=True)
    
    st.divider()
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.metric("Total Calculado", format_brl(total_calc))
    col_t2.metric("Total Estornos", format_brl(total_estornos_geral))
    col_t3.metric("Total Final", format_brl(total_final))
    col_t4.metric("A Pagar", format_brl(total_final), 
                 delta=f"{((total_final/total_calc)*100):.1f}%" if total_calc > 0 else "0%")

# ============================================================================
# 8. FUNÇÕES HUBSOFT (MANTIDAS IGUAIS)
# ============================================================================
def exibir_relatorio_vendas_novas_hubsoft():
    st.subheader("🆕 Vendas Novas - Hubsoft")
    st.caption("Apenas operações do tipo VENDA")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        mes_sel = st.selectbox("Mês", MESES_PT, index=datetime.now().month-1, key="vendas_hub_mes")
        mes_num = MESES_PT.index(mes_sel) + 1
    with col_f2:
        ano_sel = st.selectbox("Ano", [2024, 2025, 2026], index=1, key="vendas_hub_ano")
    
    if st.button("📊 Buscar", key="btn_vendas_hub", use_container_width=True):
        st.info("Funcionalidade em desenvolvimento - dados simulados")
        import random
        from datetime import date, timedelta
        dados = []
        primeiro_dia = date(ano_sel, mes_num, 1)
        ultimo_dia = date(ano_sel, 12, 31) if mes_num == 12 else date(ano_sel, mes_num+1, 1) - timedelta(days=1)
        dias = list(range(1, ultimo_dia.day + 1))
        for i in range(1, 11):
            dia = random.choice(dias)
            data = date(ano_sel, mes_num, dia)
            concluido = random.random() > 0.3
            status = 'INSTALADO' if concluido else random.choice(['PENDENTE', 'NÃO INSTALADO'])
            dados.append({
                'ID Venda': f"VND{2000+i}", 'Vendedor': f"Vendedor {random.randint(1,10)}",
                'ID Serviço': f"{random.randint(10000, 99999)}", 'Tipo Operação': 'VENDA',
                'Data Venda': data.strftime("%d/%m/%Y"), 'Plano': random.choice(['A', 'B', 'C']),
                'Data Instalação': data.strftime("%d/%m/%Y") if concluido else '-',
                'Status': status, 'Valor (R$)': round(random.uniform(1000, 10000), 2)
            })
        df = pd.DataFrame(dados)
        st.success(f"✅ {len(df)} vendas encontradas")
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False, encoding='utf-8-sig', sep=';')
        st.download_button("📥 Exportar", csv, f"vendas_novas_{mes_sel}_{ano_sel}.csv", "text/csv")

def exibir_relatorio_migracoes_hubsoft():
    st.subheader("🔄 Migrações - Hubsoft")
    st.caption("Apenas operações do tipo MIGRAÇÃO")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        mes_sel = st.selectbox("Mês", MESES_PT, index=datetime.now().month-1, key="migra_hub_mes")
        mes_num = MESES_PT.index(mes_sel) + 1
    with col_f2:
        ano_sel = st.selectbox("Ano", [2024, 2025, 2026], index=1, key="migra_hub_ano")
    
    if st.button("📊 Buscar", key="btn_migra_hub", use_container_width=True):
        st.info("Funcionalidade em desenvolvimento - dados simulados")
        import random
        from datetime import date, timedelta
        dados = []
        primeiro_dia = date(ano_sel, mes_num, 1)
        ultimo_dia = date(ano_sel, 12, 31) if mes_num == 12 else date(ano_sel, mes_num+1, 1) - timedelta(days=1)
        dias = list(range(1, ultimo_dia.day + 1))
        for i in range(1, 11):
            dia = random.choice(dias)
            data = date(ano_sel, mes_num, dia)
            concluido = random.random() > 0.3
            status = 'MIGRADO' if concluido else random.choice(['PENDENTE', 'NÃO MIGRADO'])
            dados.append({
                'ID Migração': f"MIG{3000+i}", 'Vendedor': f"Vendedor {random.randint(1,10)}",
                'ID Serviço': f"{random.randint(10000, 99999)}", 'Tipo Operação': 'MIGRAÇÃO',
                'Data Migração': data.strftime("%d/%m/%Y"), 'Plano Novo': random.choice(['A', 'B', 'C']),
                'Data Conclusão': data.strftime("%d/%m/%Y") if concluido else '-',
                'Status': status, 'Valor (R$)': round(random.uniform(500, 5000), 2)
            })
        df = pd.DataFrame(dados)
        st.success(f"✅ {len(df)} migrações encontradas")
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False, encoding='utf-8-sig', sep=';')
        st.download_button("📥 Exportar", csv, f"migracoes_{mes_sel}_{ano_sel}.csv", "text/csv")

def exibir_relatorio_consolidado_hubsoft():
    st.subheader("📊 Consolidado Hubsoft")
    st.caption("Vendas e Migrações com status apropriados")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        mes_sel = st.selectbox("Mês", MESES_PT, index=datetime.now().month-1, key="cons_hub_mes")
        mes_num = MESES_PT.index(mes_sel) + 1
    with col_f2:
        ano_sel = st.selectbox("Ano", [2024, 2025, 2026], index=1, key="cons_hub_ano")
    with col_f3:
        tipo = st.selectbox("Tipo", ["Todos", "Vendas", "Migrações"], key="cons_hub_tipo")
    
    if st.button("📊 Buscar", key="btn_cons_hub", use_container_width=True):
        st.info("Funcionalidade em desenvolvimento - dados simulados")
        import random
        from datetime import date, timedelta
        dados = []
        primeiro_dia = date(ano_sel, mes_num, 1)
        ultimo_dia = date(ano_sel, 12, 31) if mes_num == 12 else date(ano_sel, mes_num+1, 1) - timedelta(days=1)
        dias = list(range(1, ultimo_dia.day + 1))
        for i in range(1, 21):
            dia = random.choice(dias)
            data = date(ano_sel, mes_num, dia)
            tipo_op = random.choice(['VENDA', 'MIGRAÇÃO'])
            concluido = random.random() > 0.3
            status = 'INSTALADO' if concluido and tipo_op == 'VENDA' else 'MIGRADO' if concluido else random.choice(['PENDENTE', 'NÃO INSTALADO'])
            dados.append({
                'ID': f"REG{4000+i}", 'Vendedor': f"Vendedor {random.randint(1,10)}",
                'Tipo': tipo_op, 'Data': data.strftime("%d/%m/%Y"), 'Status': status,
                'Valor (R$)': round(random.uniform(500, 10000), 2)
            })
        df = pd.DataFrame(dados)
        if tipo == "Vendas":
            df = df[df['Tipo'] == 'VENDA']
        elif tipo == "Migrações":
            df = df[df['Tipo'] == 'MIGRAÇÃO']
        
        st.success(f"✅ {len(df)} registros")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Total", len(df))
        with col_m2:
            concluidos = len(df[df['Status'].str.contains('INSTALADO|MIGRADO', na=False)])
            st.metric("Concluídos", concluidos)
        with col_m3:
            pendentes = len(df[df['Status'].str.contains('PENDENTE', na=False)])
            st.metric("Pendentes", pendentes)
        with col_m4:
            valor = df[df['Status'].str.contains('INSTALADO|MIGRADO', na=False)]['Valor (R$)'].sum()
            st.metric("Valor Concluído", format_brl(valor))
        
        st.divider()
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig = px.pie(df, names='Tipo', title="Vendas vs Migrações", color='Tipo',
                        color_discrete_map={'VENDA': '#28a745', 'MIGRAÇÃO': '#17a2b8'})
            st.plotly_chart(fig, use_container_width=True)
        with col_g2:
            df_status = df.groupby(['Tipo', 'Status']).size().reset_index(name='Quantidade')
            fig = px.bar(df_status, x='Tipo', y='Quantidade', color='Status', title="Status por Tipo")
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False, encoding='utf-8-sig', sep=';')
        st.download_button("📥 Exportar", csv, f"consolidado_{mes_sel}_{ano_sel}.csv", "text/csv")

def exibir_todas_vendas_hubsoft():
    st.header("📊 Vendas e Migrações do Sistema")
    st.caption("Dados reais do banco de dados - Vendas e Migrações")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        mes_sel = st.selectbox("📅 Mês", MESES_PT, index=datetime.now().month-1, key="reais_mes")
        mes_num = MESES_PT.index(mes_sel) + 1
    with col_f2:
        ano_sel = st.selectbox("📅 Ano", [2025, 2026], index=1, key="reais_ano")
    with col_f3:
        tipo_filtro = st.selectbox("📌 Tipo", ["Todos", "Vendas", "Migrações"], key="reais_tipo")
    
    st.divider()
    
    if st.button("📊 Buscar Dados", use_container_width=True, type="primary"):
        with st.spinner(f"Buscando dados..."):
            with get_db_cursor() as cursor:
                cursor.execute("SHOW COLUMNS FROM venda")
                colunas_venda = [col['Field'] for col in cursor.fetchall()]
                possiveis = ['id_cliente_servico', 'codigo_cliente', 'cliente_id', 'id_servico', 'cliente']
                campo_id = next((c for c in possiveis if c in colunas_venda), None)
                if not campo_id:
                    campo_id = next((c for c in colunas_venda if 'id' in c.lower() or 'codigo' in c.lower()), None)
                
                if not campo_id:
                    st.error("❌ ID do serviço não encontrado")
                    return
                
                cursor.execute("SHOW COLUMNS FROM cancelamentos")
                colunas_cancel = [col['Field'] for col in cursor.fetchall()]
                relac = next((c for c in ['id_venda', 'venda_id', 'id_venda_original'] if c in colunas_cancel), None)
                
                select = [f"v.{campo_id} as id_servico", "v.id_venda", "u.nome_usuario as vendedor_nome",
                         "DATE_FORMAT(v.data_venda, '%%d/%%m/%%Y') as data_venda_br", "v.data_venda", "v.valor_venda",
                         "t.descricao as tipo_operacao", "CASE WHEN v.id_tipo_operacao = 1 THEN 'VENDA' ELSE 'MIGRAÇÃO' END as tipo",
                         "CASE WHEN v.id_status = 2 THEN 'APROVADO' WHEN v.id_status = 3 THEN 'REPROVADO' WHEN v.id_status = 4 THEN 'CANCELADO' ELSE 'EM ANÁLISE' END as status_sistema",
                         "r.descricao as regional", "v.setor"]
                
                query = f"SELECT {', '.join(select)} FROM venda v LEFT JOIN users u ON v.id_usuario_vendedor = u.id_usuario LEFT JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao LEFT JOIN regional r ON u.id_regional = r.id_regional WHERE v.ativo = 1"
                params = []
                
                if 'data_venda' in colunas_venda:
                    query += " AND MONTH(v.data_venda) = %s AND YEAR(v.data_venda) = %s"
                    params.extend([mes_num, ano_sel])
                if tipo_filtro == "Vendas":
                    query += " AND v.id_tipo_operacao = 1"
                elif tipo_filtro == "Migrações":
                    query += " AND v.id_tipo_operacao = 2"
                
                query += " ORDER BY v.data_venda DESC"
                cursor.execute(query, params)
                vendas = cursor.fetchall()
                
                df_cancel = pd.DataFrame()
                if relac:
                    try:
                        cursor.execute(f"SELECT {relac} as id_venda_relacionado, valor_original, status as status_cancelamento FROM cancelamentos WHERE MONTH(data_ocorrencia) = %s AND YEAR(data_ocorrencia) = %s", (mes_num, ano_sel))
                        df_cancel = pd.DataFrame(cursor.fetchall())
                    except:
                        pass
            
            if vendas:
                df = pd.DataFrame(vendas)
                
                def status_conclusao(row):
                    if not df_cancel.empty and 'id_venda_relacionado' in df_cancel and row['id_venda'] in df_cancel['id_venda_relacionado'].values:
                        return '❌ CANCELADO'
                    if row['status_sistema'] == 'CANCELADO':
                        return '❌ CANCELADO'
                    if pd.notna(row['id_servico']) and str(row['id_servico']).strip():
                        if row['status_sistema'] == 'APROVADO':
                            return '✅ INSTALADO' if row['tipo'] == 'VENDA' else '✅ MIGRADO'
                        elif row['status_sistema'] == 'EM ANÁLISE':
                            return '⏳ PENDENTE'
                        else:
                            return '❌ NÃO INSTALADO'
                    return '⚠️ SEM ID'
                
                df['Status Conclusão'] = df.apply(status_conclusao, axis=1)
                
                st.subheader("📈 Resumo")
                col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
                with col_m1:
                    st.metric("Total", len(df))
                with col_m2:
                    st.metric("Vendas", len(df[df['tipo'] == 'VENDA']))
                with col_m3:
                    st.metric("Migrações", len(df[df['tipo'] == 'MIGRAÇÃO']))
                with col_m4:
                    st.metric("Valor Total", format_brl(df['valor_venda'].sum()))
                with col_m5:
                    valor_cancel = df_cancel['valor_original'].sum() if not df_cancel.empty else 0
                    st.metric("Cancelamentos", format_brl(valor_cancel))
                
                st.divider()
                st.subheader("📋 Detalhamento")
                df_display = df[['id_venda', 'data_venda_br', 'vendedor_nome', 'regional', 'tipo',
                                'id_servico', 'status_sistema', 'Status Conclusão', 'valor_venda']].copy()
                df_display.columns = ['ID', 'Data', 'Vendedor', 'Regional', 'Tipo', 'ID Serviço',
                                     'Status Sis.', 'Status', 'Valor (R$)']
                
                styled = df_display.style.applymap(lambda x: colorir_status_hubsoft(x) if isinstance(x, str) and any(s in x for s in ['✅', '❌', '⚠️']) else '',
                                                  subset=['Status'])
                styled = styled.format({'Valor (R$)': format_brl})
                st.dataframe(styled, use_container_width=True, hide_index=True, height=500)
                
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    fig = px.pie(df, names='tipo', title="Vendas vs Migrações", color='tipo',
                                color_discrete_map={'VENDA': '#28a745', 'MIGRAÇÃO': '#17a2b8'})
                    st.plotly_chart(fig, use_container_width=True)
                with col_g2:
                    df_status = df.groupby(['tipo', 'Status Conclusão']).size().reset_index(name='Quantidade')
                    fig = px.bar(df_status, x='tipo', y='Quantidade', color='Status Conclusão', title="Status por Tipo")
                    st.plotly_chart(fig, use_container_width=True)
                
                csv = df_display.to_csv(index=False, encoding='utf-8-sig', sep=';')
                st.download_button("📥 Exportar CSV", csv, f"vendas_{mes_sel}_{ano_sel}.csv", "text/csv")
            else:
                st.warning("Nenhum registro encontrado")

# ============================================================================
# 9. FUNÇÃO PRINCIPAL DO DASHBOARD ADMIN
# ============================================================================
def exibir_dashboard_admin():
    """Função principal que será chamada pelo App.py"""
    
    if 'menu_option' in st.session_state:
        if st.session_state.menu_option == "🏠 Dashboard Estratégico":
            # Usa o filtro de setor se existir (para admin)
            setor = getattr(st.session_state, 'filtro_setor', 'todos')
            exibir_insights_gerenciais(setor=setor)
            st.divider()
            if setor == 'televendas':
                st.info("📞 Televendas não possui regionais - exibindo apenas dados consolidados")
            else:
                exibir_progresso_metas_regionais()
        elif st.session_state.menu_option == "🎯 Gestão de Metas":
            exibir_gestao_metas()
        elif st.session_state.menu_option == "👥 Gestão de Usuários":
            gerenciar_usuarios()
        elif st.session_state.menu_option == "📉 Análise de Desistências":
            exibir_dashboard_cancelamentos()
        elif st.session_state.menu_option == "💰 Comissões":
            setor = getattr(st.session_state, 'filtro_setor', 'todos')
            exibir_comissoes(setor=setor)
        elif st.session_state.menu_option == "📊 Visão de Instalações Hubsoft":
            exibir_visao_instalacoes_hubsoft()
        elif st.session_state.menu_option == "🌐 Todas as Vendas Hubsoft":
            exibir_todas_vendas_hubsoft()
        else:
            exibir_insights_gerenciais()
            st.divider()
            exibir_progresso_metas_regionais()
    else:
        exibir_insights_gerenciais()
        st.divider()
        exibir_progresso_metas_regionais()
def gerenciar_assinaturas_certificados():
    """Painel para gerenciar assinaturas com upload de imagem"""
    st.subheader("✍️ Assinaturas dos Certificados")
    st.caption("Faça upload das imagens das assinaturas ou use texto")
    
    from database.queries import buscar_assinaturas_certificados, salvar_assinatura_certificado
    
    assinaturas = buscar_assinaturas_certificados()
    
    # Dicionário com os tipos
    tipos = {
        'coordenacao': 'Coordenação',
        'gerencia': 'Gerência',
        'diretor': 'Diretoria'
    }
    
    for tipo, nome_tipo in tipos.items():
        assinatura = next((a for a in assinaturas if a['tipo'] == tipo), None)
        
        with st.expander(f"{nome_tipo}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input(
                    f"Nome do Responsável ({nome_tipo})",
                    value=assinatura['nome'] if assinatura else "",
                    key=f"nome_{tipo}"
                )
                cargo = st.text_input(
                    f"Cargo ({nome_tipo})",
                    value=assinatura['cargo'] if assinatura else "",
                    key=f"cargo_{tipo}"
                )
            
            with col2:
                st.markdown("**🖌️ Imagem da Assinatura**")
                st.caption("PNG com fundo transparente (opcional)")
                
                # Mostrar imagem atual
                if assinatura and assinatura.get('imagem_assinatura'):
                    import base64
                    img_preview = base64.b64encode(assinatura['imagem_assinatura']).decode()
                    st.image(f"data:image/png;base64,{img_preview}", width=150)
                    st.caption("Imagem atual")
                
                imagem_file = st.file_uploader(
                    "Upload da assinatura",
                    type=["png", "jpg", "jpeg"],
                    key=f"img_{tipo}",
                    label_visibility="collapsed"
                )
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                if st.button(f"💾 Salvar", key=f"save_{tipo}", use_container_width=True):
                    if nome and cargo:
                        imagem_bytes = imagem_file.read() if imagem_file else None
                        if salvar_assinatura_certificado(tipo, nome, cargo, imagem_bytes):
                            st.success(f"✅ {nome_tipo} salva com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao salvar")
                    else:
                        st.warning("⚠️ Preencha nome e cargo")
            
            with col_btn2:
                if st.button(f"🗑️ Remover Imagem", key=f"remove_img_{tipo}", use_container_width=True):
                    # Remover apenas a imagem, manter nome e cargo
                    if salvar_assinatura_certificado(tipo, nome if nome else "_________________________", 
                                                     cargo if cargo else nome_tipo, None):
                        st.success(f"✅ Imagem removida para {nome_tipo}")
                        st.rerun()