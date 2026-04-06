# modulos/televendas.py
import streamlit as st
import pandas as pd
import plotly.express as px
from database.queries import get_db_cursor, registrar_log
from datetime import datetime
from modulos.admin import MESES_PT, format_brl

# ===== FUNÇÕES AUXILIARES =====
def buscar_vendas_televendas_por_operador(id_operador, mes_num, ano_sel):
    """Busca as vendas de um operador do televendas no período"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                v.id_venda,
                v.codigo_cliente as cliente,
                v.valor_venda,
                v.data_venda,
                DATE_FORMAT(v.data_venda, '%d/%m/%Y') as data_venda_br,
                t.descricao as tipo_operacao,
                s.descricao as status
            FROM venda v
            JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
            JOIN status s ON v.id_status = s.id_status
            WHERE v.id_usuario_vendedor = %s
              AND v.setor = 'televendas'
              AND v.ativo = 1
              AND MONTH(v.data_venda) = %s
              AND YEAR(v.data_venda) = %s
            ORDER BY v.data_venda DESC
        """, (id_operador, mes_num, ano_sel))
        return cursor.fetchall()

def registrar_venda_televendas(id_usuario, cliente, valor_venda, id_tipo_operacao=1):
    """Registra uma nova venda para o televendas (começa como PENDENTE)"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("""
                INSERT INTO venda (
                    id_usuario_vendedor,
                    codigo_cliente,
                    data_venda,
                    valor_venda,
                    id_tipo_operacao,
                    id_status,  -- 1 = PENDENTE (aguardando aprovação)
                    setor,
                    ativo
                ) VALUES (%s, %s, NOW(), %s, %s, 1, 'televendas', 1)
            """, (id_usuario, cliente, valor_venda, id_tipo_operacao))
            return True
    except Exception as e:
        st.error(f"Erro ao registrar venda: {e}")
        return False

def buscar_meta_televendas(mes_num, ano_sel):
    """Busca a meta do televendas para o período"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT meta_vendas_qtd, meta_faturamento
            FROM metas_televendas
            WHERE MONTH(mes_referencia) = %s AND YEAR(mes_referencia) = %s
        """, (mes_num, ano_sel))
        resultado = cursor.fetchone()
        
        if resultado:
            return {
                'meta_vendas_qtd': float(resultado['meta_vendas_qtd']) if resultado['meta_vendas_qtd'] else 0,
                'meta_faturamento': float(resultado['meta_faturamento']) if resultado['meta_faturamento'] else 0
            }
        return None

def calcular_progresso_meta(id_operador, mes_num, ano_sel):
    """Calcula o progresso individual do operador em relação à meta do setor"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_vendas,
                SUM(CASE WHEN id_status = 2 THEN valor_venda ELSE 0 END) as faturamento_aprovado
            FROM venda
            WHERE id_usuario_vendedor = %s
              AND setor = 'televendas'
              AND MONTH(data_venda) = %s
              AND YEAR(data_venda) = %s
              AND ativo = 1
        """, (id_operador, mes_num, ano_sel))
        result = cursor.fetchone()
        
        return {
            'vendas': int(result['total_vendas'] or 0),
            'faturamento': float(result['faturamento_aprovado'] or 0)
        }

def exibir_posicao_ranking_televendas(id_operador, mes_num, ano_sel):
    """Exibe a posição do operador no ranking do televendas (apenas vendas aprovadas)"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                u.id_usuario,
                u.nome_usuario,
                COUNT(v.id_venda) as total_vendas,
                SUM(v.valor_venda) as total_faturamento
            FROM users u
            LEFT JOIN venda v ON u.id_usuario = v.id_usuario_vendedor 
                AND v.setor = 'televendas'
                AND v.id_status = 2  -- APENAS APROVADAS
                AND v.ativo = 1
                AND MONTH(v.data_venda) = %s
                AND YEAR(v.data_venda) = %s
            WHERE u.setor = 'televendas' AND u.ativo = 1
            GROUP BY u.id_usuario, u.nome_usuario
            ORDER BY total_vendas DESC
        """, (mes_num, ano_sel))
        
        ranking = cursor.fetchall()
        
        if ranking:
            # Encontra a posição do operador
            posicao = None
            for i, r in enumerate(ranking):
                if r['id_usuario'] == id_operador:
                    posicao = i + 1
                    break
            
            total_operadores = len(ranking)
            
            if posicao:
                col_r1, col_r2, col_r3 = st.columns(3)
                
                with col_r1:
                    if posicao == 1:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                            <span style="font-size: 2rem;">🥇</span>
                            <h3 style="margin: 0;">1º Lugar!</h3>
                            <p style="margin: 0;">Parabéns, você é o líder!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif posicao == 2:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #C0C0C0 0%, #A0A0A0 100%); padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                            <span style="font-size: 2rem;">🥈</span>
                            <h3 style="margin: 0;">2º Lugar</h3>
                            <p style="margin: 0;">Muito bem, continue assim!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif posicao == 3:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #CD7F32 0%, #B87333 100%); padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                            <span style="font-size: 2rem;">🥉</span>
                            <h3 style="margin: 0;">3º Lugar</h3>
                            <p style="margin: 0;">No pódio, parabéns!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                            <span style="font-size: 2rem;">#{posicao}</span>
                            <h3 style="margin: 0;">{posicao}º de {total_operadores}</h3>
                            <p style="margin: 0;">Continue melhorando!</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col_r2:
                    stats = calcular_progresso_meta(id_operador, mes_num, ano_sel)
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; text-align: center; border: 1px solid #e9ecef;">
                        <span style="font-size: 1.5rem;">📊</span>
                        <h3 style="margin: 0; color: #2d3748;">{stats['vendas']} vendas</h3>
                        <p style="margin: 0; color: #666;">suas vendas aprovadas</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_r3:
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; text-align: center; border: 1px solid #e9ecef;">
                        <span style="font-size: 1.5rem;">💰</span>
                        <h3 style="margin: 0; color: #2d3748;">{format_brl(stats['faturamento'])}</h3>
                        <p style="margin: 0; color: #666;">faturamento aprovado</p>
                    </div>
                    """, unsafe_allow_html=True)

def exibir_resumo_vendas_televendas(df, mes_num, ano_sel):
    """Exibe o resumo das vendas do operador"""
    if df.empty:
        st.info("📭 Nenhuma venda encontrada no período.")
        return
    
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    
    with col_r1:
        total_vendas = len(df)
        st.metric("Total de Vendas", total_vendas)
    
    with col_r2:
        total_aprovadas = len(df[df['status'] == 'APROVADO']) if 'status' in df.columns else 0
        st.metric("✅ Aprovadas", total_aprovadas)
    
    with col_r3:
        total_pendentes = len(df[df['status'] == 'EM ANÁLISE']) if 'status' in df.columns else 0
        st.metric("⏳ Pendentes", total_pendentes)
    
    with col_r4:
        valor_total = df[df['status'] == 'APROVADO']['valor_venda'].sum() if 'valor_venda' in df.columns else 0
        st.metric("💰 Faturamento Aprovado", format_brl(valor_total))

def exibir_progresso_meta_televendas(id_operador, mes_num, ano_sel):
    """Exibe o progresso do operador em relação à meta do setor"""
    meta = buscar_meta_televendas(mes_num, ano_sel)
    stats = calcular_progresso_meta(id_operador, mes_num, ano_sel)
    
    if not meta:
        st.info("📊 Meta não definida para este período.")
        return
    
    st.subheader("🎯 Progresso da Meta do Setor")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        perc_vendas = (stats['vendas'] / meta['meta_vendas_qtd'] * 100) if meta['meta_vendas_qtd'] > 0 else 0
        st.markdown(f"**Vendas Aprovadas:** {stats['vendas']} / {int(meta['meta_vendas_qtd'])}")
        st.progress(min(perc_vendas / 100, 1.0))
        st.caption(f"{perc_vendas:.1f}% da meta de vendas")
    
    with col_p2:
        perc_faturamento = (stats['faturamento'] / meta['meta_faturamento'] * 100) if meta['meta_faturamento'] > 0 else 0
        st.markdown(f"**Faturamento Aprovado:** {format_brl(stats['faturamento'])} / {format_brl(meta['meta_faturamento'])}")
        st.progress(min(perc_faturamento / 100, 1.0))
        st.caption(f"{perc_faturamento:.1f}% da meta de faturamento")

def exibir_grafico_vendas_diarias_televendas(id_operador, mes_num, ano_sel):
    """Exibe gráfico de vendas diárias do operador (apenas aprovadas)"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT 
                DAY(data_venda) as dia,
                COUNT(*) as quantidade,
                SUM(valor_venda) as valor_total
            FROM venda
            WHERE id_usuario_vendedor = %s
              AND setor = 'televendas'
              AND id_status = 2  -- APENAS APROVADAS
              AND MONTH(data_venda) = %s
              AND YEAR(data_venda) = %s
              AND ativo = 1
            GROUP BY DAY(data_venda)
            ORDER BY dia
        """, (id_operador, mes_num, ano_sel))
        
        dados = cursor.fetchall()
    
    if not dados:
        st.info("📊 Nenhuma venda aprovada para gerar gráfico.")
        return
    
    df = pd.DataFrame(dados)
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        fig_qtd = px.bar(
            df, 
            x='dia', 
            y='quantidade',
            title="Vendas Aprovadas por Dia",
            labels={'dia': 'Dia do Mês', 'quantidade': 'Nº de Vendas'},
            color='quantidade',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_qtd, use_container_width=True)
    
    with col_g2:
        fig_valor = px.bar(
            df, 
            x='dia', 
            y='valor_total',
            title="Faturamento Aprovado por Dia",
            labels={'dia': 'Dia do Mês', 'valor_total': 'Valor (R$)'},
            color='valor_total',
            color_continuous_scale='Greens'
        )
        fig_valor.update_traces(texttemplate='R$ %{y:.0f}', textposition='outside')
        st.plotly_chart(fig_valor, use_container_width=True)

def exibir_historico_vendas_televendas(vendas):
    """Exibe o histórico de vendas do operador"""
    if not vendas:
        st.info("📭 Nenhuma venda registrada no período.")
        return
    
    df = pd.DataFrame(vendas)
    
    # CORREÇÃO: Formata a data corretamente se necessário
    if 'data_venda_br' not in df.columns and 'data_venda' in df.columns:
        df['data_venda_br'] = pd.to_datetime(df['data_venda']).dt.strftime('%d/%m/%Y')
    
    colunas = {
        'id_venda': 'ID',
        'data_venda_br': 'Data',
        'cliente': 'Cliente',
        'tipo_operacao': 'Operação',
        'valor_venda': 'Valor',
        'status': 'Status'
    }
    
    df_display = df[[c for c in colunas.keys() if c in df.columns]].copy()
    df_display = df_display.rename(columns={k: v for k, v in colunas.items() if k in df_display.columns})
    
    if 'Valor' in df_display.columns:
        df_display['Valor'] = df_display['Valor'].apply(format_brl)
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

# ===== FUNÇÃO PRINCIPAL DO DASHBOARD =====
def exibir_dashboard_televendas():
    """Tela do operador de televendas"""
    
    if "id_usuario" not in st.session_state:
        st.error("Por favor, faça login.")
        return

    id_operador = st.session_state.id_usuario
    nome_operador = st.session_state.get('user_nome', 'Operador')

    st.title(f"📞 Painel do Televendas")
    st.caption(f"Operador: {nome_operador}")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        meses = MESES_PT
        mes_sel = st.selectbox("Mês", meses, index=datetime.now().month - 1)
        mes_num = meses.index(mes_sel) + 1
    with col_f2:
        ano_sel = st.selectbox("Ano", [2025, 2026], index=1)

    # ===== RANKING =====
    exibir_posicao_ranking_televendas(id_operador, mes_num, ano_sel)
    st.divider()

    # Busca vendas do período
    vendas = buscar_vendas_televendas_por_operador(id_operador, mes_num, ano_sel)
    df = pd.DataFrame(vendas) if vendas else pd.DataFrame()
    
    # ===== RESUMO DE VENDAS =====
    exibir_resumo_vendas_televendas(df, mes_num, ano_sel)
    st.divider()

    # ===== PROGRESSO DA META =====
    exibir_progresso_meta_televendas(id_operador, mes_num, ano_sel)
    st.divider()

    # ===== GRÁFICO DE ACOMPANHAMENTO =====
    exibir_grafico_vendas_diarias_televendas(id_operador, mes_num, ano_sel)
    st.divider()

    # ===== NOVA VENDA =====
    st.subheader("📝 Nova Venda")

    with st.form("form_nova_venda_televendas"):
        st.info("⏳ Após o registro, a venda ficará pendente de aprovação do supervisor.")
        
        cliente = st.text_input("Código do Cliente *", placeholder="Digite o código do cliente")
        
        valor_venda = st.number_input(
            "Valor da Venda (R$) *", 
            min_value=0.0, 
            step=10.0, 
            format="%.2f"
        )
        
        submitted = st.form_submit_button("📝 Registrar Venda", use_container_width=True, type="primary")

    if submitted:
        if not cliente:
            st.error("❌ Por favor, informe o código do cliente!")
        elif valor_venda <= 0:
            st.error("❌ O valor da venda deve ser maior que zero!")
        else:
            with st.spinner("Registrando venda..."):
                try:
                    sucesso = registrar_venda_televendas(
                        id_usuario=id_operador,
                        cliente=cliente.strip(),
                        valor_venda=valor_venda
                    )
                    
                    if sucesso:
                        st.success(f"✅ Venda registrada com sucesso e enviada para aprovação!")
                        registrar_log(
                            id_operador, 
                            "VENDA_TELEVENDAS", 
                            f"Venda: {cliente} - R$ {valor_venda:,.2f} (aguardando aprovação)"
                        )
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Erro ao registrar venda.")
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")

    st.divider()

    # ===== HISTÓRICO =====
    vendas_atualizadas = buscar_vendas_televendas_por_operador(id_operador, mes_num, ano_sel)
    st.subheader("📋 Histórico de Vendas")
    exibir_historico_vendas_televendas(vendas_atualizadas)

# ===== FUNÇÃO DE METAS =====
def exibir_metas_televendas():
    """Gestão de metas do televendas"""
    
    st.subheader("🎯 Metas do Televendas")
    st.caption("Defina as metas mensais para o setor de televendas")
    
    col1, col2 = st.columns(2)
    with col1:
        mes_sel = st.selectbox("Mês", MESES_PT, index=datetime.now().month - 1, key="meta_tv_mes")
        mes_num = MESES_PT.index(mes_sel) + 1
    with col2:
        ano_sel = st.selectbox("Ano", [2025, 2026], index=1, key="meta_tv_ano")
    
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT * FROM metas_televendas
            WHERE MONTH(mes_referencia) = %s AND YEAR(mes_referencia) = %s
        """, (mes_num, ano_sel))
        meta = cursor.fetchone()
    
    with st.form("form_meta_televendas"):
        col1, col2 = st.columns(2)
        
        with col1:
            meta_vendas = st.number_input(
                "Meta de Vendas (quantidade)",
                min_value=1,
                value=int(meta['meta_vendas_qtd']) if meta and meta['meta_vendas_qtd'] else 50,
                step=5
            )
        with col2:
            meta_faturamento = st.number_input(
                "Meta de Faturamento (R$)",
                min_value=0.0,
                value=float(meta['meta_faturamento']) if meta and meta['meta_faturamento'] else 50000.0,
                step=1000.0,
                format="%.2f"
            )
        
        if st.form_submit_button("💾 Salvar Meta", use_container_width=True, type="primary"):
            try:
                with get_db_cursor(commit=True) as cursor:
                    cursor.execute("""
                        INSERT INTO metas_televendas 
                        (mes_referencia, meta_vendas_qtd, meta_faturamento)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        meta_vendas_qtd = VALUES(meta_vendas_qtd),
                        meta_faturamento = VALUES(meta_faturamento)
                    """, (
                        f"{ano_sel}-{mes_num:02d}-01",
                        meta_vendas,
                        meta_faturamento
                    ))
                st.success("✅ Meta salva com sucesso!")
                registrar_log(st.session_state.id_usuario, "META_TELEVENDAS", f"Meta {mes_sel}/{ano_sel}: {meta_vendas} vendas, R$ {meta_faturamento:,.2f}")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")