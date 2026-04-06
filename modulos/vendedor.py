import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from database.queries import (
    get_db_cursor, 
    registrar_log, 
    buscar_vendas_por_vendedor,
    registrar_venda,
    get_tipos_operacao,
    buscar_metas_regionais
)
from datetime import datetime, date
import calendar
from decimal import Decimal
import time

def format_brl(val):
    """Formata valores para R$"""
    try:
        if isinstance(val, Decimal):
            val = float(val)
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def determinar_tipo_migracao(valor_novo, valor_antigo):
    """Determina se é Upgrade ou Downgrade baseado na diferença"""
    if valor_novo > valor_antigo:
        return "Upgrade"
    elif valor_novo < valor_antigo:
        return "Downgrade"
    else:
        return "Migração (mesmo valor)"

def exibir_historico_servico(id_servico):
    """Exibe o histórico completo de um serviço para validação"""
    try:
        from database.queries import get_db_cursor
        
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    v.id_venda,
                    DATE_FORMAT(v.data_venda, '%d/%m/%Y') as data_venda,
                    t.descricao as tipo_operacao,
                    v.valor_venda,
                    u.nome_usuario as vendedor,
                    s.descricao as status,
                    v.codigo_cliente
                FROM venda v
                LEFT JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
                LEFT JOIN users u ON v.id_usuario_vendedor = u.id_usuario
                LEFT JOIN status s ON v.id_status = s.id_status
                WHERE v.codigo_cliente = %s
                AND v.ativo = 1
                ORDER BY v.data_venda ASC
            """, (str(id_servico),))
            
            registros = cursor.fetchall()
            
            if registros:
                df = pd.DataFrame(registros)
                st.subheader(f"📋 Histórico do Serviço: {id_servico}")
                
                # Análise
                tem_venda_nova = any('Venda Nova' in str(r['tipo_operacao']) for r in registros)
                tem_migracao = any('Migra' in str(r['tipo_operacao']) for r in registros)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Venda Nova", "✅" if tem_venda_nova else "❌")
                with col2:
                    st.metric("Migração", "✅" if tem_migracao else "❌")
                
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                if tem_venda_nova and not tem_migracao:
                    st.info("💡 Este serviço pode ser migrado!")
                elif tem_venda_nova and tem_migracao:
                    st.success("✅ Serviço completo: Venda Nova + Migração realizadas")
                elif not tem_venda_nova:
                    st.info("📝 Este serviço aguarda venda nova")
                
                return df
            else:
                st.success(f"✅ Serviço {id_servico} não possui registros anteriores")
                return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erro ao buscar histórico: {e}")
        return pd.DataFrame()

def buscar_meta_vendedor_quantidade(id_vendedor, mes, ano):
    """Busca a meta do vendedor em QUANTIDADE de vendas baseado na regional"""
    with get_db_cursor() as cursor:
        # Primeiro, descobre a regional do vendedor
        cursor.execute("SELECT id_regional FROM users WHERE id_usuario = %s", (id_vendedor,))
        user = cursor.fetchone()
        if not user:
            return 10  # valor padrão se não encontrar
        
        id_regional = user['id_regional']
        
        # Busca a meta da regional para o mês/ano
        metas = buscar_metas_regionais(id_regional, mes, ano)
        
        if metas and len(metas) > 0:
            # Retorna a meta em quantidade de vendas
            return int(metas[0]['meta_vendas_qtd'])
        else:
            # Se não encontrar meta para o período, retorna valor padrão
            return 10

def exibir_posicao_ranking_vendedor(id_vendedor, mes, ano):
    """Exibe a posição do vendedor no ranking da regional"""
    with get_db_cursor() as cursor:
        # Busca regional do vendedor
        cursor.execute("SELECT id_regional FROM users WHERE id_usuario = %s", (id_vendedor,))
        user = cursor.fetchone()
        if not user:
            return
        
        id_regional = user['id_regional']
        
        # Conta total de vendedores ativos na regional
        cursor.execute("""
            SELECT COUNT(DISTINCT u.id_usuario) as total
            FROM users u
            WHERE u.id_regional = %s AND u.ativo = 1
        """, (id_regional,))
        total_vendedores = cursor.fetchone()['total']
        
        # Calcula ranking baseado em quantidade de vendas aprovadas
        query_ranking = """
            SELECT 
                u.id_usuario,
                COUNT(v.id_venda) as total_vendas,
                SUM(v.valor_venda) as total_valor,
                RANK() OVER (ORDER BY COUNT(v.id_venda) DESC) as ranking
            FROM users u
            LEFT JOIN venda v ON u.id_usuario = v.id_usuario_vendedor 
                AND v.id_status = 2 
                AND v.ativo = 1 
                AND MONTH(v.data_venda) = %s 
                AND YEAR(v.data_venda) = %s
            WHERE u.id_regional = %s AND u.ativo = 1
            GROUP BY u.id_usuario
            HAVING total_vendas > 0
        """
        cursor.execute(query_ranking, (mes, ano, id_regional))
        resultados = cursor.fetchall()
        
        # Encontra a posição do vendedor atual
        posicao = None
        total_vendas = 0
        total_valor = 0
        for r in resultados:
            if r['id_usuario'] == id_vendedor:
                posicao = r['ranking']
                total_vendas = r['total_vendas']
                total_valor = r['total_valor']
                break
        
        if posicao and total_vendedores > 1:
            if posicao == 1:
                st.success(f"🥇 **Você é o LÍDER da regional!**")
                st.markdown(f"📊 **{total_vendas} vendas | {format_brl(total_valor)}**")
            else:
                st.info(f"📊 **Sua posição: {int(posicao)}º lugar na regional**")
                st.markdown(f"📈 **{total_vendas} vendas | {format_brl(total_valor)}**")
        else:
            st.warning("📊 **Você ainda não aparece no ranking. Faça vendas aprovadas para entrar!**")

def exibir_resumo_vendas(df, mes, ano):
    """Exibe resumo detalhado das vendas do vendedor"""
    
    st.subheader("📊 Resumo de Vendas/Migrações")
    
    # Filtra apenas vendas aprovadas para alguns cálculos
    df_aprovadas = df[df['id_status'] == 2].copy() if not df.empty else pd.DataFrame()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    total_vendas = len(df) if not df.empty else 0
    col1.metric("Total de Vendas", total_vendas)
    
    total_aprovadas = len(df_aprovadas) if not df_aprovadas.empty else 0
    col2.metric("✅ Aprovadas", total_aprovadas)
    
    total_pendentes = len(df[df['id_status'] == 1]) if not df.empty else 0
    col3.metric("⏳ Pendentes", total_pendentes)
    
    total_reprovadas = len(df[df['id_status'] == 3]) if not df.empty else 0
    col4.metric("❌ Reprovadas", total_reprovadas)
    
    if not df_aprovadas.empty:
        # Métricas financeiras
        col5, col6, col7, col8 = st.columns(4)
        
        faturamento_total = df_aprovadas['valor_venda'].sum()
        col5.metric("💰 Faturamento", format_brl(faturamento_total))
        
        # Calcula ticket médio
        ticket_medio = faturamento_total / len(df_aprovadas) if len(df_aprovadas) > 0 else 0
        col6.metric("🎫 Ticket Médio", format_brl(ticket_medio))
        
        # Conta migrações
        migracoes = len(df_aprovadas[df_aprovadas['operacao'].str.contains('Migra', na=False)])
        col7.metric("🔄 Migrações", migracoes)
        
        # Vendas novas
        vendas_novas = len(df_aprovadas[~df_aprovadas['operacao'].str.contains('Migra', na=False)])
        col8.metric("🆕 Vendas Novas", vendas_novas)
        
        st.divider()
        
        # Análise por tipo de operação
        st.subheader("📈 Análise por Tipo de Operação")
        
        # Agrupa por operação
        df_tipos = df_aprovadas.groupby('operacao').agg({
            'id_venda': 'count',
            'valor_venda': 'sum'
        }).reset_index()
        df_tipos.columns = ['Tipo de Operação', 'Quantidade', 'Valor Total']
        
        # Gráfico de pizza para tipos de operação
        fig_tipos = px.pie(
            df_tipos, 
            values='Quantidade', 
            names='Tipo de Operação',
            title="Distribuição por Tipo de Operação",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_tipos, use_container_width=True)
        
        # Tabela de tipos
        df_tipos['Valor Total'] = df_tipos['Valor Total'].apply(format_brl)
        st.dataframe(df_tipos, use_container_width=True, hide_index=True)

def exibir_progresso_metas_vendedor(id_vendedor, mes, ano):
    """Exibe o progresso das metas do vendedor em QUANTIDADE de vendas"""
    
    # Busca a meta do vendedor em quantidade (definida pelo admin)
    META_QUANTIDADE = buscar_meta_vendedor_quantidade(id_vendedor, mes, ano)
    
    with get_db_cursor() as cursor:
        # Calcula a quantidade de vendas aprovadas
        cursor.execute("""
            SELECT 
                COUNT(*) as quantidade_aprovadas,
                SUM(CASE WHEN id_tipo_operacao IN (2,3,4) THEN 1 ELSE 0 END) as migracoes,
                SUM(CASE WHEN id_tipo_operacao = 1 THEN 1 ELSE 0 END) as vendas_novas
            FROM venda 
            WHERE id_usuario_vendedor = %s 
                AND MONTH(data_venda) = %s 
                AND YEAR(data_venda) = %s 
                AND id_status = 2 
                AND ativo = 1
        """, (id_vendedor, mes, ano))
        
        res = cursor.fetchone()
        
    quantidade_batida = int(res['quantidade_aprovadas'] or 0)
    migracoes = int(res['migracoes'] or 0)
    vendas_novas = int(res['vendas_novas'] or 0)
    percentual = (quantidade_batida / META_QUANTIDADE) * 100 if META_QUANTIDADE > 0 else 0
    falta = max(0, META_QUANTIDADE - quantidade_batida)

    st.subheader("🏁 Minha Meta")
    
    # Mostra informação da regional
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id_regional FROM users WHERE id_usuario = %s", (id_vendedor,))
        user = cursor.fetchone()
        if user:
            cursor.execute("SELECT descricao FROM regional WHERE id_regional = %s", (user['id_regional'],))
            regional = cursor.fetchone()
            if regional:
                st.caption(f"Meta definida para a regional: {regional['descricao']}")
    
    # Cards de meta
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("✅ Vendas Aprovadas", f"{quantidade_batida} vendas", f"{percentual:.1f}%")
    
    with col2:
        if falta > 0:
            st.metric("🎯 Meta", f"{META_QUANTIDADE} vendas", f"Faltam: {falta}", delta_color="inverse")
        else:
            st.metric("🎯 Meta", f"{META_QUANTIDADE} vendas", "✅ META BATIDA!", delta_color="normal")
    
    with col3:
        # Calcula projeção baseada no dia atual
        hoje = datetime.now().day
        dias_no_mes = calendar.monthrange(ano, mes)[1]
        if hoje > 0 and quantidade_batida > 0:
            projecao = int(quantidade_batida / hoje * dias_no_mes)
            diferenca_projecao = projecao - META_QUANTIDADE
            if diferenca_projecao > 0:
                st.metric("📈 Projeção Final", f"{projecao} vendas", f"+{diferenca_projecao}", delta_color="normal")
            else:
                st.metric("📈 Projeção Final", f"{projecao} vendas", f"{diferenca_projecao}", delta_color="inverse")
        else:
            st.metric("📈 Projeção Final", "0 vendas", "Aguardando")

    # Barra de progresso
    progresso = min(1.0, quantidade_batida / META_QUANTIDADE)
    
    # Barra de progresso colorida baseada no percentual
    if percentual >= 100:
        st.success(f"### 🎉 META BATIDA! 🎉")
        st.progress(1.0, text=f"{percentual:.1f}% da meta atingida ({quantidade_batida} de {META_QUANTIDADE} vendas)")
    elif percentual >= 70:
        st.warning(f"### ⚠️ Quase lá! Faltam {falta} vendas")
        st.progress(progresso, text=f"{percentual:.1f}% da meta atingida ({quantidade_batida} de {META_QUANTIDADE} vendas)")
    else:
        st.info(f"### Faltam {falta} vendas para bater a meta")
        st.progress(progresso, text=f"{percentual:.1f}% da meta atingida ({quantidade_batida} de {META_QUANTIDADE} vendas)")
    
    # Calcula quantas vendas por dia são necessárias para bater a meta
    hoje = datetime.now().day
    dias_no_mes = calendar.monthrange(ano, mes)[1]
    dias_restantes = dias_no_mes - hoje + 1
    if falta > 0 and dias_restantes > 0:
        vendas_por_dia = round(falta / dias_restantes, 1)
        st.caption(f"📅 Para bater a meta, você precisa de **{vendas_por_dia}** vendas por dia nos próximos {dias_restantes} dias.")
    
    st.divider()
    
    # Métricas adicionais
    st.markdown("### 📊 Composição das Vendas")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("🆕 Vendas Novas", vendas_novas)
    col_m2.metric("🔄 Migrações", migracoes)
    if quantidade_batida > 0:
        perc_migracoes = (migracoes / quantidade_batida * 100)
        col_m3.metric("📊 % Migrações", f"{perc_migracoes:.1f}%")

def exibir_historico_vendas(vendas):
    """Exibe o histórico detalhado de vendas"""
    
    st.subheader("📋 Histórico de Vendas")
    
    if not vendas:
        st.info("Nenhuma venda encontrada para o período selecionado.")
        return
    
    df = pd.DataFrame(vendas)
    
    # Converte valores
    for col in ['valor_venda', 'valor_venda_antiga']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: float(x) if pd.notna(x) else 0.0)

    # Determina operação detalhada
    def get_operacao_detalhada(row):
        if 'Migra' in str(row['operacao']):
            if row['valor_venda'] > row['valor_venda_antiga']:
                return "Upgrade"
            elif row['valor_venda'] < row['valor_venda_antiga']:
                return "Downgrade"
            else:
                return "Migração"
        return row['operacao']
    
    df['operacao_detalhada'] = df.apply(get_operacao_detalhada, axis=1)
    df['impacto'] = df.apply(
        lambda row: row['valor_venda'] - row['valor_venda_antiga'] if 'Migra' in str(row['operacao']) else row['valor_venda'], 
        axis=1
    )

    # Formata data
    if 'data_venda' in df.columns:
        df['data_venda'] = pd.to_datetime(df['data_venda']).dt.strftime('%d/%m/%Y')

    # Garantir que o status seja exibido corretamente
    if 'status' in df.columns:
        df['status'] = df['status'].fillna('EM ANÁLISE')
        df['status'] = df['status'].apply(lambda x: x.upper() if isinstance(x, str) else 'EM ANÁLISE')
    else:
        df['status'] = 'EM ANÁLISE'

    # Cores para status
    def cor_status(val):
        if val == 'APROVADO':
            return 'background-color: #90ee90; color: black'
        elif val == 'EM ANÁLISE':
            return 'background-color: #fff3cd; color: black'
        elif val == 'REPROVADO':
            return 'background-color: #f8d7da; color: black'
        elif val == 'CANCELADO':
            return 'background-color: #d3d3d3; color: black'
        return ''

    # Tabela de vendas
    colunas_exibir = ['data_venda', 'codigo_cliente', 'operacao_detalhada', 'valor_venda', 'valor_venda_antiga', 'impacto', 'status']
    colunas_existentes = [col for col in colunas_exibir if col in df.columns]
    
    if colunas_existentes:
        # Aplica estilo
        styled_df = df[colunas_existentes].style.applymap(cor_status, subset=['status'])
        
        # Formata números
        styled_df = styled_df.format({
            'valor_venda': 'R$ {:.2f}',
            'valor_venda_antiga': 'R$ {:.2f}',
            'impacto': 'R$ {:.2f}'
        })
        
        st.dataframe(
            styled_df,
            column_config={
                "data_venda": "Data",
                "codigo_cliente": "Cliente",
                "operacao_detalhada": "Operação",
                "valor_venda": "Valor Novo",
                "valor_venda_antiga": "Valor Antigo",
                "impacto": "Impacto",
                "status": "Status"
            },
            use_container_width=True,
            hide_index=True
        )

    # Resumos
    with st.expander("📊 Resumos Detalhados"):
        tab1, tab2, tab3 = st.tabs(["Por Status", "Por Operação", "Evolução"])
        
        with tab1:
            # Resumo por status
            resumo_status = df.groupby('status').agg({
                'id_venda': 'count',
                'valor_venda': 'sum',
                'impacto': 'sum'
            }).reset_index()
            resumo_status.columns = ['Status', 'Quantidade', 'Valor Total', 'Impacto Total']
            resumo_status['Valor Total'] = resumo_status['Valor Total'].apply(format_brl)
            resumo_status['Impacto Total'] = resumo_status['Impacto Total'].apply(format_brl)
            st.dataframe(resumo_status, use_container_width=True, hide_index=True)
        
        with tab2:
            # Resumo por operação
            resumo_op = df.groupby('operacao_detalhada').agg({
                'id_venda': 'count',
                'valor_venda': 'sum',
                'impacto': 'sum'
            }).reset_index()
            resumo_op.columns = ['Operação', 'Quantidade', 'Valor Total', 'Impacto Total']
            resumo_op['Valor Total'] = resumo_op['Valor Total'].apply(format_brl)
            resumo_op['Impacto Total'] = resumo_op['Impacto Total'].apply(format_brl)
            st.dataframe(resumo_op, use_container_width=True, hide_index=True)
        
        with tab3:
            # Evolução por dia
            if 'data_venda' in df.columns:
                df_evolucao = df.groupby('data_venda').agg({
                    'id_venda': 'count',
                    'valor_venda': 'sum'
                }).reset_index()
                df_evolucao.columns = ['Data', 'Vendas', 'Valor']
                fig_evolucao = px.line(df_evolucao, x='Data', y=['Vendas', 'Valor'], 
                                      title="Evolução Diária")
                st.plotly_chart(fig_evolucao, use_container_width=True)

def exibir_grafico_meta_diaria(id_vendedor, mes, ano):
    """Exibe gráfico de acompanhamento diário da meta em quantidade"""
    META_QUANTIDADE = buscar_meta_vendedor_quantidade(id_vendedor, mes, ano)
    num_dias = calendar.monthrange(ano, mes)[1]
    meta_diaria = META_QUANTIDADE / num_dias

    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                DAY(data_venda) as dia,
                COUNT(*) as quantidade_dia,
                SUM(valor_venda) as valor_dia
            FROM venda 
            WHERE id_usuario_vendedor = %s 
                AND MONTH(data_venda) = %s 
                AND YEAR(data_venda) = %s 
                AND id_status = 2 
                AND ativo = 1
            GROUP BY DAY(data_venda)
            ORDER BY dia
        """, (id_vendedor, mes, ano))
        
        df_v = pd.DataFrame(cursor.fetchall())

    # Cria DataFrame com todos os dias do mês
    df_plot = pd.DataFrame({'dia': list(range(1, num_dias + 1))})
    if not df_v.empty and 'quantidade_dia' in df_v.columns:
        df_plot = pd.merge(df_plot, df_v, on='dia', how='left').fillna(0)
    else:
        df_plot['quantidade_dia'] = 0
        df_plot['valor_dia'] = 0
    
    # Calcula acumulados
    df_plot['acumulado_qtd'] = df_plot['quantidade_dia'].cumsum()
    df_plot['acumulado_valor'] = df_plot['valor_dia'].cumsum()
    
    fig = go.Figure()
    
    # Barras da quantidade diária
    fig.add_trace(go.Bar(
        x=df_plot['dia'],
        y=df_plot['quantidade_dia'],
        name='Vendas do Dia',
        marker_color='#169fda',
        yaxis='y'
    ))
    
    # Linha da meta diária
    fig.add_trace(go.Scatter(
        x=df_plot['dia'],
        y=[meta_diaria] * num_dias,
        name='Meta Diária',
        line=dict(color='#f3716c', width=2, dash='dash'),
        yaxis='y'
    ))
    
    # Linha do acumulado de vendas
    fig.add_trace(go.Scatter(
        x=df_plot['dia'],
        y=df_plot['acumulado_qtd'],
        name='Vendas Acumuladas',
        line=dict(color='#28a745', width=3),
        yaxis='y2'
    ))

    fig.update_layout(
        title=f'Acompanhamento Diário da Meta - {mes}/{ano}',
        xaxis=dict(title='Dia do Mês', dtick=1),
        yaxis=dict(title='Vendas por Dia', side='left'),
        yaxis2=dict(title='Vendas Acumuladas', side='right', overlaying='y'),
        legend=dict(x=0, y=1.1, orientation='h'),
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métricas do gráfico
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Total Mês", f"{int(df_plot['acumulado_qtd'].iloc[-1])} vendas")
    col_m2.metric("Média Dia", f"{df_plot['quantidade_dia'].mean():.1f} vendas")
    col_m3.metric("Melhor Dia", f"Dia {df_plot['quantidade_dia'].idxmax()}", 
                  f"{int(df_plot['quantidade_dia'].max())} vendas")
    col_m4.metric("Projeção Final", 
                  f"{int(df_plot['acumulado_qtd'].iloc[-1] / df_plot['dia'].iloc[-1] * num_dias)} vendas")

def exibir_tela_vendedor():
    """Tela do vendedor - vê apenas suas próprias vendas com validação de duplicidade"""
    
    if "id_usuario" not in st.session_state:
        st.error("Por favor, faça login.")
        return

    id_vendedor = st.session_state.id_usuario
    nome_vendedor = st.session_state.get('user_nome', 'Vendedor')

    st.title(f"💰 Painel do Vendedor")
    st.caption(f"Vendedor: {nome_vendedor}")

    # Filtros de data
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        mes_sel = st.selectbox("Mês", meses, index=datetime.now().month - 1)
        mes_num = meses.index(mes_sel) + 1
    with col_f2:
        ano_sel = st.selectbox("Ano", [2025, 2026], index=1)

    # ===== VALIDAÇÃO DE SERVIÇO (EXPANDER) =====
    with st.expander("🔍 Validar Serviço Antes de Registrar", expanded=False):
        col_v1, col_v2 = st.columns([2, 1])
        with col_v1:
            id_servico_validar = st.text_input(
                "ID do Serviço", 
                key="validar_servico",
                placeholder="Digite o código do cliente para verificar histórico"
            )
        with col_v2:
            if st.button("🔍 Verificar", key="btn_validar_servico", use_container_width=True):
                if id_servico_validar:
                    exibir_historico_servico(id_servico_validar)
                else:
                    st.warning("⚠️ Digite um ID de serviço para verificar")
    
    st.divider()

    # ===== RANKING =====
    exibir_posicao_ranking_vendedor(id_vendedor, mes_num, ano_sel)
    st.divider()

    # Busca vendas do período - INICIAL
    vendas = buscar_vendas_por_vendedor(id_vendedor, mes_num, ano_sel)
    df = pd.DataFrame(vendas) if vendas else pd.DataFrame()
    
    if not df.empty:
        # Converte valores
        for col in ['valor_venda', 'valor_venda_antiga']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: float(x) if pd.notna(x) else 0.0)
    
    # ===== RESUMO DE VENDAS =====
    exibir_resumo_vendas(df, mes_num, ano_sel)
    st.divider()

    # ===== PROGRESSO DA META =====
    exibir_progresso_metas_vendedor(id_vendedor, mes_num, ano_sel)
    st.divider()

    # ===== GRÁFICO DE ACOMPANHAMENTO =====
    exibir_grafico_meta_diaria(id_vendedor, mes_num, ano_sel)
    st.divider()

    # ===== NOVA TABULAÇÃO =====
    st.subheader("📝 Nova Tabulação")

    # Busca tipos de operação
    tipos_op = get_tipos_operacao()
    if tipos_op:
        opcoes_operacao = {}
        for t in tipos_op:
            if t['descricao'] == 'Migração (Upgrade)':
                opcoes_operacao["Migração"] = t['id_tipo_operacao']
            else:
                opcoes_operacao[t['descricao']] = t['id_tipo_operacao']
    else:
        opcoes_operacao = {
            "Venda Nova": 1,
            "Migração": 2,
            "Chip Avulsa": 3,
            "B2B": 4
        }

    # Tipo de operação fora do formulário
    tipo_op_nome = st.selectbox(
        "Tipo de Operação",
        list(opcoes_operacao.keys()),
        key="tipo_operacao_principal"
    )
    id_tipo_op = opcoes_operacao[tipo_op_nome]
    
    st.markdown("---")
    
    # Formulário de registro
    with st.form("form_nova_venda"):
        cliente = st.text_input("ID Cliente / Serviço do Cliente *", placeholder="Ex: 123456")
        
        valor_venda = st.number_input(
            "Valor Final / Novo (R$) *", 
            min_value=0.0, 
            step=10.0, 
            format="%.2f"
        )
        
        # Campo condicional para migração
        valor_anterior = 0.0
        if tipo_op_nome == "Migração":
            st.markdown("---")
            st.markdown("##### 📋 Dados da Migração")
            valor_anterior = st.number_input(
                "Valor Anterior (R$)", 
                min_value=0.0, 
                step=10.0, 
                format="%.2f",
                help="Valor que o cliente pagava antes da migração"
            )
            
            # Feedback visual
            if valor_venda > 0 and valor_anterior > 0:
                diferenca = valor_venda - valor_anterior
                if diferenca > 0:
                    st.success(f"📈 **Upgrade detectado** - Diferença: {format_brl(diferenca)}")
                elif diferenca < 0:
                    st.warning(f"📉 **Downgrade detectado** - Diferença: {format_brl(diferenca)}")
                else:
                    st.info(f"🔄 **Migração com mesmo valor**")
        
        observacao = st.text_area("Observações (opcional)", height=100)
        
        submitted = st.form_submit_button("📝 Registrar Venda", use_container_width=True, type="primary")

    if submitted:
        # Validações
        if not cliente:
            st.error("❌ Por favor, informe o ID do cliente/serviço!")
        elif not cliente.strip().isdigit():
            st.error(f"❌ ID do serviço '{cliente}' deve conter apenas números!")
        elif valor_venda <= 0:
            st.error("❌ O valor da venda deve ser maior que zero!")
        elif tipo_op_nome == "Migração" and valor_anterior <= 0:
            st.error("❌ Para migrações, informe o valor anterior!")
        else:
            with st.spinner("Registrando venda..."):
                try:
                    # Registrar venda (agora retorna tupla)
                    sucesso, mensagem = registrar_venda(
                        id_usuario=id_vendedor,
                        cliente=cliente.strip(),
                        id_tipo_operacao=id_tipo_op,
                        valor_venda=valor_venda,
                        valor_anterior=valor_anterior
                    )
                    
                    if sucesso:
                        if tipo_op_nome == "Migração":
                            tipo_migracao = determinar_tipo_migracao(valor_venda, valor_anterior)
                            log_detalhe = f"{tipo_migracao}: {cliente} - R$ {valor_venda} (anterior: R$ {valor_anterior})"
                            st.success(f"✅ {tipo_migracao} registrado com sucesso!")
                        else:
                            log_detalhe = f"{tipo_op_nome}: {cliente} - R$ {valor_venda}"
                            st.success(f"✅ {mensagem}")
                        
                        registrar_log(id_vendedor, "VENDA", log_detalhe)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ {mensagem}")
                        
                        # Se for erro de duplicidade, mostrar histórico
                        if "duplicidade" in mensagem.lower() or "já possui" in mensagem.lower():
                            with st.expander("🔍 Verificar Histórico do Serviço", expanded=True):
                                exibir_historico_servico(cliente)
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")

    st.divider()

    # ===== BUSCAR VENDAS NOVAMENTE PARA O HISTÓRICO =====
    vendas_atualizadas = buscar_vendas_por_vendedor(id_vendedor, mes_num, ano_sel)
    
    # ===== HISTÓRICO DE VENDAS =====
    exibir_historico_vendas(vendas_atualizadas)