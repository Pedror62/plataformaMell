"""
Módulo de Auditoria - Versão Integrada e Corrigida
Mantém compatibilidade com admin.py e integra sistema de comissões
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from database.queries import get_db_cursor, carregar_vendas
from datetime import datetime
import hashlib
import time

# Constantes
MESES_PT = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]


# ============================================================================
# FUNÇÕES AUXILIARES (EXPORTADAS PARA ADMIN)
# ============================================================================

def format_brl(val):
    """Formata valor para R$"""
    try:
        if pd.isna(val) or val is None:
            return "R$ 0,00"
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"


def colorir_status_hubsoft(val):
    """Aplica cores no status - necessário para admin.py"""
    if pd.isna(val):
        return ''
    val_str = str(val)
    if '✅ INSTALADO' in val_str or '✅ MIGRADO' in val_str:
        return 'background-color: #d4edda; color: #155724; font-weight: bold;'
    elif '❌ NÃO INSTALADO' in val_str or '❌ NÃO MIGRADO' in val_str:
        return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    elif '❌ NÃO ENCONTRADO' in val_str:
        return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    elif '⚠️' in val_str:
        return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
    return ''


def gerar_key_unica(prefixo):
    """Gera uma key única para elementos do Streamlit"""
    timestamp = str(time.time())
    hash_obj = hashlib.md5(timestamp.encode())
    return f"{prefixo}_{hash_obj.hexdigest()[:8]}"


# ============================================================================
# FUNÇÕES DE INTEGRAÇÃO HUBSOFT (MANTIDAS PARA ADMIN)
# ============================================================================

def buscar_vendas_do_periodo(reg_sel, mes_num, ano_sel, regs, setor='todos'):
    """
    Busca vendas do período para integração com Hubsoft
    Mantida para compatibilidade com admin.py
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SHOW COLUMNS FROM venda")
            colunas = [col['Field'] for col in cursor.fetchall()]
            campo_id = 'codigo_cliente' if 'codigo_cliente' in colunas else 'id_servico'
            
            query = f"""
                SELECT 
                    v.id_venda,
                    CAST(v.{campo_id} AS CHAR) as id_servico,
                    u.nome_usuario as vendedor_nome,
                    DATE_FORMAT(v.data_venda, '%%d/%%m/%%Y') as data_venda_br,
                    v.data_venda,
                    COALESCE(v.valor_venda, 0) as valor_venda,
                    COALESCE(t.descricao, 'Venda Nova') as tipo_operacao,
                    COALESCE(v.setor, 'comercial') as setor
                FROM venda v
                LEFT JOIN users u ON v.id_usuario_vendedor = u.id_usuario
                LEFT JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
                WHERE v.ativo = 1 AND v.id_status = 2
            """
            params = []
            
            if reg_sel != "Geral" and setor != 'televendas':
                query += " AND u.id_regional = %s"
                params.append(regs[reg_sel])
            
            if setor != 'todos':
                query += " AND v.setor = %s"
                params.append(setor)
            
            if mes_num and ano_sel:
                query += " AND MONTH(v.data_venda) = %s AND YEAR(v.data_venda) = %s"
                params.extend([mes_num, ano_sel])
            
            query += " ORDER BY v.data_venda DESC"
            
            cursor.execute(query, tuple(params) if params else None)
            resultados = cursor.fetchall()
            
            if resultados:
                df = pd.DataFrame(resultados)
                df['id_valido'] = df['id_servico'].apply(
                    lambda x: str(x).isdigit() and len(str(x)) >= 4 if x and x != 'nan' else False
                )
                return df
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar vendas: {e}")
        return pd.DataFrame()


def consultar_ids_hubsoft(lista_ids):
    """
    Consulta IDs no Hubsoft e retorna informações completas
    """
    if not lista_ids:
        return {}
    
    # Tenta importar a integração real
    try:
        from integracao_hubsoft import HubsoftIntegracao
        hubsoft = HubsoftIntegracao()
        integracao_disponivel = True
    except ImportError:
        integracao_disponivel = False
        st.warning("⚠️ Integração Hubsoft não disponível. Usando dados simulados.")
    
    resultados = {}
    
    # Criar barra de progresso
    progress = st.progress(0)
    status_text = st.empty()
    
    for i, id_servico in enumerate(lista_ids):
        status_text.text(f"Consultando Hubsoft: {i+1}/{len(lista_ids)} - ID: {id_servico}")
        progress.progress((i + 1) / len(lista_ids))
        
        try:
            if integracao_disponivel:
                # Usa a integração real
                servico = hubsoft.buscar_servico_por_id(int(id_servico))
                
                if servico and servico.get('encontrado'):
                    # Extrair data de instalação corretamente
                    data_instalacao = servico.get('data_habilitacao', '')
                    data_instalacao_br = servico.get('data_habilitacao_br', '-')
                    
                    # Se a data vier no formato ISO (YYYY-MM-DD), converter
                    if data_instalacao and data_instalacao != '':
                        try:
                            from datetime import datetime
                            if '-' in data_instalacao:
                                data_obj = datetime.strptime(data_instalacao.split(' ')[0], '%Y-%m-%d')
                                data_instalacao_br = data_obj.strftime('%d/%m/%Y')
                        except:
                            pass
                    
                    resultados[id_servico] = {
                        'encontrado': True,
                        'instalado': servico.get('instalado', False),
                        'data_habilitacao_br': data_instalacao_br,
                        'data_habilitacao': servico.get('data_habilitacao', ''),
                        'plano_nome': servico.get('plano_nome', '-'),
                        'valor': servico.get('valor', 0),
                        'status': servico.get('status', '-')
                    }
                else:
                    resultados[id_servico] = {
                        'encontrado': False,
                        'instalado': False,
                        'data_habilitacao_br': '-',
                        'data_habilitacao': '',
                        'plano_nome': '-',
                        'valor': 0,
                        'status': 'Não encontrado'
                    }
            else:
                # Dados simulados para teste (substitua pela sua API real)
                # Simula que alguns IDs estão instalados
                import random
                instalado = random.choice([True, False])
                
                if instalado:
                    # Gera uma data de instalação nos últimos 30 dias
                    from datetime import datetime, timedelta
                    data_inst = datetime.now() - timedelta(days=random.randint(1, 30))
                    data_inst_br = data_inst.strftime('%d/%m/%Y')
                    
                    resultados[id_servico] = {
                        'encontrado': True,
                        'instalado': True,
                        'data_habilitacao_br': data_inst_br,
                        'data_habilitacao': data_inst.strftime('%Y-%m-%d'),
                        'plano_nome': f'Plano {random.choice(["A", "B", "C"])}',
                        'valor': random.choice([79.90, 89.90, 109.90, 129.90]),
                        'status': 'Ativo'
                    }
                else:
                    resultados[id_servico] = {
                        'encontrado': True,
                        'instalado': False,
                        'data_habilitacao_br': '-',
                        'data_habilitacao': '',
                        'plano_nome': '-',
                        'valor': 0,
                        'status': 'Pendente'
                    }
                    
        except Exception as e:
            st.error(f"Erro ao consultar ID {id_servico}: {str(e)}")
            resultados[id_servico] = {
                'encontrado': False,
                'instalado': False,
                'data_habilitacao_br': '-',
                'data_habilitacao': '',
                'plano_nome': '-',
                'valor': 0,
                'status': f'Erro: {str(e)[:50]}'
            }
    
    status_text.empty()
    progress.empty()
    
    encontrados = sum(1 for r in resultados.values() if r.get('encontrado', False))
    instalados = sum(1 for r in resultados.values() if r.get('instalado', False))
    
    st.info(f"📊 Resultado da consulta: {encontrados}/{len(resultados)} IDs encontrados, {instalados} instalados")
    
    return resultados

# ============================================================================
# CORREÇÃO DA FUNÇÃO exibir_visao_instalacoes_hubsoft (para admin.py)
# ============================================================================

def exibir_visao_instalacoes_hubsoft():
    """Exibe visão de instalações do Hubsoft com datas corretas"""
    
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
            # Usa a função do auditor
            df_vendas = buscar_vendas_do_periodo(reg_sel, mes_num, ano_sel, regs, setor_db)
            
            if df_vendas is not None and not df_vendas.empty:
                st.session_state.admin_df_vendas = df_vendas
                st.session_state.admin_df_conciliado = None
                
                # Verifica coluna id_servico
                if 'id_servico' in df_vendas.columns:
                    vendas_com_id = df_vendas['id_servico'].notna().sum()
                else:
                    vendas_com_id = 0
                
                # Contagem por setor
                if 'setor' in df_vendas.columns:
                    qtd_comercial = len(df_vendas[df_vendas['setor'] == 'comercial'])
                    qtd_televendas = len(df_vendas[df_vendas['setor'] == 'televendas'])
                    
                    st.success(f"✅ {len(df_vendas)} registros encontrados no período!")
                    st.info(f"📊 Comercial: {qtd_comercial} | Televendas: {qtd_televendas} | IDs válidos: {vendas_com_id}")
                else:
                    st.success(f"✅ {len(df_vendas)} registros encontrados no período!")
                    st.info(f"📊 {vendas_com_id} registros possuem ID de serviço")
                
                # Mostra preview com data formatada
                df_preview = df_vendas.copy()
                if 'data_venda_br' in df_preview.columns:
                    df_preview['data_venda_br'] = df_preview['data_venda_br'].apply(
                        lambda x: x if x and x != '%d/%m/%Y' else datetime.now().strftime('%d/%m/%Y')
                    )
                
                colunas_preview = ['id_venda', 'vendedor_nome', 'tipo_operacao', 'data_venda_br']
                if 'setor' in df_preview.columns:
                    colunas_preview.append('setor')
                if 'id_servico' in df_preview.columns:
                    colunas_preview.append('id_servico')
                
                st.dataframe(df_preview[colunas_preview].head(10),
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
            # Extrai IDs válidos
            if 'id_servico' in df_vendas.columns:
                ids_validos = df_vendas['id_servico'].dropna().astype(str).tolist()
                ids_validos = [id_str for id_str in ids_validos if id_str.strip() and id_str.strip().isdigit()]
            else:
                ids_validos = []
                st.warning("⚠️ Coluna 'id_servico' não encontrada.")
                st.info(f"Colunas disponíveis: {list(df_vendas.columns)}")
            
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
        
        if df_conciliado is not None and not df_conciliado.empty and isinstance(df_conciliado, pd.DataFrame):
            st.subheader("📊 Resultado da Consulta Hubsoft")
            
            # Filtro para mostrar apenas instalados/migrados
            col_filtro1, col_filtro2 = st.columns([1, 3])
            with col_filtro1:
                mostrar_apenas_concluidos = st.checkbox("✅ Mostrar apenas instalados/migrados", value=False, key="admin_filtro_instalados")
            
            # Aplica o filtro
            if mostrar_apenas_concluidos:
                if 'Instalado no Mês' in df_conciliado.columns:
                    df_exibicao = df_conciliado[df_conciliado['Instalado no Mês'] == True].copy()
                    st.info(f"📌 Mostrando apenas {len(df_exibicao)} registros instalados/migrados no período de {mes_sel}/{ano_sel}")
                else:
                    df_exibicao = df_conciliado[
                        df_conciliado['Status'].str.contains('INSTALADO|MIGRADO', na=False)
                    ].copy()
                    st.info(f"📌 Mostrando apenas {len(df_exibicao)} registros concluídos")
            else:
                df_exibicao = df_conciliado
            
            # Métricas
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("📋 Total Registros", len(df_exibicao))
            
            with col_m2:
                if 'Instalado no Mês' in df_exibicao.columns:
                    instalados_no_mes = len(df_exibicao[df_exibicao['Instalado no Mês'] == True])
                    st.metric("✅ Instalados no Mês", instalados_no_mes)
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
                    st.metric("❌ Não Instalados", nao_instalados)
                else:
                    st.metric("❌ Não Instalados", 0)
            
            with col_m4:
                if 'Valor (R$)' in df_exibicao.columns:
                    if 'Instalado no Mês' in df_exibicao.columns:
                        valor_total = df_exibicao[df_exibicao['Instalado no Mês'] == True]['Valor (R$)'].sum()
                    else:
                        valor_total = df_exibicao[
                            df_exibicao['Status'].str.contains('INSTALADO|MIGRADO', na=False)
                        ]['Valor (R$)'].sum()
                    st.metric("💰 Valor Total Instalados", format_brl(valor_total))
                else:
                    st.metric("💰 Valor Total Instalados", "R$ 0,00")
            
            st.divider()
            
            # Tabela de resultados com dados completos
            st.subheader("📋 Detalhamento das Instalações")
            
            # Colunas para exibição
            colunas_exibir = [
                'ID Venda', 'Vendedor', 'ID Serviço', 'Tipo Operação', 'Setor',
                'Data Venda', 'Plano', 'Data Instalação', 'Valor (R$)', 'Status'
            ]
            
            df_display = df_exibicao[[c for c in colunas_exibir if c in df_exibicao.columns]].copy()
            
            # Garantir que a data de instalação esteja formatada
            if 'Data Instalação' in df_display.columns:
                df_display['Data Instalação'] = df_display['Data Instalação'].apply(
                    lambda x: x if x and x != '-' else '-'
                )
            
            # Garantir que a data de venda esteja formatada
            if 'Data Venda' in df_display.columns:
                df_display['Data Venda'] = df_display['Data Venda'].apply(
                    lambda x: x if x and x != '%d/%m/%Y' else datetime.now().strftime('%d/%m/%Y')
                )
            
            # Aplicar cores aos status
            styled_df = df_display.style.applymap(
                colorir_status_hubsoft, 
                subset=['Status']
            ).format({
                'Valor (R$)': lambda x: format_brl(x) if x > 0 else "R$ 0,00"
            })
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True,
                height=500
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
            if df_conciliado is None:
                st.info("📭 Nenhum dado de consulta disponível. Clique em 'Consultar Hubsoft' primeiro.")
            elif df_conciliado.empty:
                st.info("📭 Nenhum resultado encontrado para a consulta.")

def criar_dataframe_conciliado(df_vendas, resultados_hubsoft, mes_num, ano_sel):
    """
    Cria DataFrame conciliado com informações do Hubsoft
    Mantida para compatibilidade com admin.py
    """
    if df_vendas.empty:
        return pd.DataFrame()
    
    dados = []
    
    for _, row in df_vendas.iterrows():
        id_servico = str(row['id_servico']) if pd.notna(row['id_servico']) else None
        
        dados_venda = {
            'ID Venda': row.get('id_venda', '-'),
            'Vendedor': row.get('vendedor_nome', '-'),
            'ID Serviço': id_servico if id_servico else '-',
            'Tipo Operação': row.get('tipo_operacao', '-'),
            'Setor': row.get('setor', 'comercial'),
            'Data Venda': row.get('data_venda_br', '-'),
            'Valor (R$)': row.get('valor_venda', 0)
        }
        
        if id_servico and id_servico in resultados_hubsoft:
            hub = resultados_hubsoft[id_servico]
            status = '✅ INSTALADO' if hub.get('instalado') else '❌ NÃO INSTALADO'
            
            dados.append({
                **dados_venda,
                'Data Instalação': hub.get('data_habilitacao_br', '-'),
                'Plano': hub.get('plano_nome', '-'),
                'Status': status,
                'Comissão Aplicável': hub.get('instalado', False)
            })
        else:
            dados.append({
                **dados_venda,
                'Data Instalação': '-',
                'Plano': '-',
                'Status': '❌ NÃO ENCONTRADO',
                'Comissão Aplicável': False
            })
    
    return pd.DataFrame(dados)


def buscar_historico_pagamentos(mes=None, ano=None, setor=None):
    """Busca histórico de pagamentos - Mantida para compatibilidade"""
    try:
        with get_db_cursor() as cursor:
            # Verificar se a tabela existe
            cursor.execute("""
                SELECT COUNT(*) as existe FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'historico_comissoes'
            """)
            if cursor.fetchone()['existe'] == 0:
                return pd.DataFrame()
            
            query = "SELECT * FROM historico_comissoes WHERE 1=1"
            params = []
            
            if mes and mes != "Todos":
                if mes in MESES_PT:
                    mes_num = MESES_PT.index(mes) + 1
                    query += " AND mes_referencia = %s"
                    params.append(mes_num)
            
            if ano and ano != "Todos":
                try:
                    ano_num = int(ano)
                    query += " AND ano_referencia = %s"
                    params.append(ano_num)
                except:
                    pass
            
            if setor and setor != "Todos":
                query += " AND regional = %s"
                params.append(setor)
            
            query += " ORDER BY data_fechamento DESC LIMIT 100"
            
            cursor.execute(query, tuple(params) if params else None)
            resultados = cursor.fetchall()
            
            if resultados:
                df = pd.DataFrame(resultados)
                if 'valor_pago' in df.columns:
                    df['valor_pago'] = pd.to_numeric(df['valor_pago'], errors='coerce').fillna(0).astype(float)
                return df
            return pd.DataFrame()
    except Exception as e:
        print(f"Erro ao buscar histórico: {e}")
        return pd.DataFrame()


def exibir_historico_com_graficos(df_hist):
    """Exibe histórico com gráficos - Mantida para compatibilidade"""
    if df_hist.empty:
        st.info("📭 Nenhum histórico encontrado.")
        return
    
    if 'valor_pago' in df_hist.columns:
        df_hist['valor_pago'] = pd.to_numeric(df_hist['valor_pago'], errors='coerce').fillna(0).astype(float)
    
    st.subheader("📊 Métricas Gerais")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_pago = df_hist['valor_pago'].sum()
        st.metric("💰 Total Pago", format_brl(total_pago))
    
    with col2:
        total_registros = len(df_hist)
        st.metric("📋 Total Pagamentos", total_registros)
    
    with col3:
        media = df_hist['valor_pago'].mean() if total_registros > 0 else 0
        st.metric("📊 Média por Pagamento", format_brl(media))
    
    st.divider()
    
    # Gráfico de pagamentos por período
    if 'mes_referencia' in df_hist.columns and 'ano_referencia' in df_hist.columns:
        df_hist['periodo'] = df_hist['mes_referencia'].astype(str) + '/' + df_hist['ano_referencia'].astype(str)
        
        fig = px.bar(df_hist, x='periodo', y='valor_pago', 
                     title="Pagamentos por Período",
                     color='valor_pago',
                     color_continuous_scale='Viridis')
        
        key_unica = gerar_key_unica("historico_bar")
        st.plotly_chart(fig, use_container_width=True, key=key_unica)
    
    # Tabela
    st.dataframe(df_hist, use_container_width=True, hide_index=True)


# ============================================================================
# FUNÇÃO PRINCIPAL DE AUDITORIA (VERSÃO CORRIGIDA)
# ============================================================================
# Em modulos/auditor.py - PARTE CORRIGIDA DA FUNÇÃO exibir_tela_auditor

def exibir_tela_auditor():
    """
    Tela principal de auditoria
    Versão corrigida que integra com o sistema de comissões existente
    """
    
    st.title("⚖️ Auditoria e Histórico de Pagamentos")
    st.markdown("Valide os cálculos automáticos e consulte registros de meses anteriores.")
    
    # Status do dia (prazo até dia 10)
    hoje = datetime.now().day
    if hoje > 10:
        st.warning(f"⚠️ **ATENÇÃO:** Hoje é dia {hoje}. O prazo para validação com Karen Banar é até dia 10. Este cálculo entrará na folha do **próximo mês**.")
    else:
        st.success(f"✅ Dentro do prazo! Envie até dia 10 para pagamento na **próxima folha**.")
    
    # Abas
    tab_auditar, tab_historico, tab_hubsoft = st.tabs([
        "🔍 Nova Auditoria", 
        "📜 Consultar Histórico",
        "🔍 Auditoria Hubsoft"
    ])
    
    # ==================== TAB 1: NOVA AUDITORIA ====================
    with tab_auditar:
        # --- 1. FILTROS DE COMPETÊNCIA ---
        with get_db_cursor() as cursor:
            cursor.execute("SELECT id_regional, descricao FROM regional WHERE ativo = 1")
            regs_data = cursor.fetchall()
            opcoes_regional = {r['descricao']: r['id_regional'] for r in regs_data}
        
        if not opcoes_regional:
            st.error("❌ Nenhuma regional cadastrada ou ativa no sistema.")
            return
        
        c1, c2, c3 = st.columns(3)
        with c1:
            reg_sel = st.selectbox("Regional para Auditoria", list(opcoes_regional.keys()), key="aud_reg_filtro")
            id_reg = opcoes_regional[reg_sel]
        with c2:
            meses_pt = MESES_PT
            mes_sel = st.selectbox("Mês de Referência", meses_pt, index=datetime.now().month-1, key="aud_mes_filtro")
            mes_num = meses_pt.index(mes_sel) + 1
        with c3:
            ano_sel = st.selectbox("Ano de Referência", [2025, 2026], index=1, key="aud_ano_filtro")
        
        # --- 2. BUSCA DE DADOS ---
        with get_db_cursor() as cursor:
            # Buscar metas
            cursor.execute("""
                SELECT meta_vendas_qtd, meta_migracao_qtd 
                FROM metas_regionais 
                WHERE id_regional = %s AND MONTH(mes_referencia) = %s AND YEAR(mes_referencia) = %s
            """, (id_reg, mes_num, ano_sel))
            meta = cursor.fetchone()
        
        # CORREÇÃO: Buscar vendas com tratamento adequado
        try:
            df_vendas = carregar_vendas(id_reg, mes_num, ano_sel)
            
            # Verificar se é DataFrame e se está vazio
            if df_vendas is None:
                st.error("❌ Erro ao carregar dados de vendas: a função retornou None")
                st.info("Por favor, verifique o banco de dados e tente novamente.")
                return
            
            if not isinstance(df_vendas, pd.DataFrame):
                st.error(f"❌ Erro: carregar_vendas retornou {type(df_vendas)} em vez de DataFrame")
                st.info("Verifique a função carregar_vendas no arquivo queries.py")
                return
                
        except Exception as e:
            st.error(f"❌ Erro ao carregar vendas: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return
        
        # Verificar se há dados
        if meta and not df_vendas.empty:
            # Limpeza e conversão
            for col in ['Valor Novo', 'Valor Anterior']:
                if col in df_vendas.columns:
                    df_vendas[col] = pd.to_numeric(df_vendas[col], errors='coerce').fillna(0).astype(float)
            
            df_vendas['Status'] = df_vendas['Status'].astype(str).str.upper().str.strip()
            df_vendas['Tipo Operação'] = df_vendas['Tipo Operação'].astype(str).str.upper().str.strip()
            
            m_v = meta['meta_vendas_qtd']
            m_m = meta['meta_migracao_qtd']
            
            dados_calculados = []
            
            # Mostrar dados brutos para debug
            with st.expander("📊 Dados Brutos (para debug)"):
                st.dataframe(df_vendas.head(20), use_container_width=True)
                st.write(f"Total de registros: {len(df_vendas)}")
                st.write(f"Vendedores únicos: {df_vendas['Vendedor'].nunique()}")
            
            for vendedor in df_vendas['Vendedor'].unique():
                v_data = df_vendas[df_vendas['Vendedor'] == vendedor]
                v_aprov = v_data[v_data['Status'] == 'APROVADO']
                
                # Contagem por tipo
                q_v = len(v_aprov[v_aprov['Tipo Operação'].str.contains('VENDA', case=False, na=False)])
                q_m = len(v_aprov[v_aprov['Tipo Operação'].str.contains('MIGRA', case=False, na=False)])
                
                # Percentuais de atingimento
                p_v = (q_v / m_v * 100) if m_v > 0 else 0
                p_m = (q_m / m_m * 100) if m_m > 0 else 0
                
                comis_sugerida = 0.0
                observacao = ""
                
                # Verifica elegibilidade (80% em ambas)
                if p_v >= 80 and p_m >= 80:
                    observacao = f"Elegível: Vendas {p_v:.1f}% | Migrações {p_m:.1f}%"
                    
                    # --- Cálculo VENDAS ---
                    vendas_novas = v_aprov[v_aprov['Tipo Operação'].str.contains('VENDA', case=False, na=False)]
                    
                    if p_v >= 120:
                        qtd_fixo = int(m_v * 1.2)
                        qtd_bonus = max(0, q_v - qtd_fixo)
                        comis_v = qtd_fixo * 13.00
                        
                        # Bônus de 50% sobre as vendas excedentes
                        for _, venda in vendas_novas.tail(qtd_bonus).iterrows():
                            valor_plano = venda['Valor Novo']
                            comis_v += (valor_plano * 0.5)
                        observacao += f" | Vendas: 120%+ (R$ 13,00 + 50% bônus)"
                        
                    elif p_v >= 110:
                        comis_v = q_v * 12.00
                        observacao += f" | Vendas: 110% (R$ 12,00/venda)"
                    elif p_v >= 100:
                        comis_v = q_v * 10.00
                        observacao += f" | Vendas: 100% (R$ 10,00/venda)"
                    else:  # 80% a 99%
                        comis_v = q_v * 8.00
                        observacao += f" | Vendas: {p_v:.1f}% (R$ 8,00/venda)"
                    
                    comis_sugerida += comis_v
                    
                    # --- Cálculo MIGRAÇÕES ---
                    migracoes = v_aprov[v_aprov['Tipo Operação'].str.contains('MIGRA', case=False, na=False)]
                    
                    if p_m >= 110:
                        perc_mig = 1.0
                        observacao += " | Migrações: 100% da diferença"
                    elif p_m >= 100:
                        perc_mig = 0.9
                        observacao += " | Migrações: 90% da diferença"
                    else:  # 80% a 99%
                        perc_mig = 0.8
                        observacao += f" | Migrações: {p_m:.1f}% (80% da diferença)"
                    
                    for _, migra in migracoes.iterrows():
                        dif = migra['Valor Novo'] - migra['Valor Anterior']
                        if dif > 0:
                            comis_sugerida += (dif * perc_mig)
                
                else:
                    observacao = f"Não elegível: Vendas {p_v:.1f}% | Migrações {p_m:.1f}% (mínimo 80% em ambas)"
                
                # Buscar estornos
                with get_db_cursor() as cursor:
                    cursor.execute("""
                        SELECT COALESCE(SUM(c.valor_original), 0) as estorno
                        FROM cancelamentos c
                        JOIN users u ON c.id_usuario_vendedor = u.id_usuario
                        WHERE u.nome_usuario = %s
                          AND c.status IN ('pendente', 'aprovado')
                          AND MONTH(c.data_ocorrencia) = %s 
                          AND YEAR(c.data_ocorrencia) = %s
                    """, (vendedor, mes_num, ano_sel))
                    estorno_data = cursor.fetchone()
                    estorno = float(estorno_data['estorno']) if estorno_data else 0.0
                
                if estorno > 0:
                    comis_sugerida = max(0, comis_sugerida - estorno)
                    observacao += f" | Estorno: R$ {estorno:.2f}"
                
                dados_calculados.append({
                    "Pagar?": comis_sugerida > 0,
                    "Vendedor": vendedor,
                    "Comissão R$": round(comis_sugerida, 2),
                    "Observação Auditoria": observacao
                })
            
            if dados_calculados:
                # Tabela Interativa
                df_finalizado = st.data_editor(
                    pd.DataFrame(dados_calculados),
                    column_config={
                        "Pagar?": st.column_config.CheckboxColumn("Pagar?"),
                        "Comissão R$": st.column_config.NumberColumn("Valor R$", format="R$ %.2f"),
                    },
                    disabled=["Vendedor", "Observação Auditoria"],
                    hide_index=True, 
                    use_container_width=True, 
                    key="editor_auditoria"
                )
                
                # Totais
                total_comissoes = df_finalizado[df_finalizado["Pagar?"]]["Comissão R$"].sum()
                st.info(f"💰 **Total a Pagar: R$ {total_comissoes:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
                
                # Botão de Finalização
                if st.button("🚀 Confirmar e Salvar no Histórico", use_container_width=True, type="primary"):
                    try:
                        with get_db_cursor(commit=True) as cursor:
                            for _, row in df_finalizado.iterrows():
                                status = "PAGO" if row["Pagar?"] else "RECUSADO"
                                cursor.execute("""
                                    INSERT INTO historico_comissoes 
                                    (vendedor_nome, regional, mes_referencia, ano_referencia, valor_pago, status_pagamento, observacao, data_fechamento)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                                """, (row["Vendedor"], reg_sel, mes_num, ano_sel, row["Comissão R$"], status, row["Observação Auditoria"]))
                        st.success("✅ Fechamento registrado com sucesso!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao salvar: {e}")
            else:
                st.info("Nenhum vendedor elegível para auditoria neste período.")
        else:
            if not meta:
                st.warning(f"⚠️ Metas não definidas para {reg_sel} em {mes_sel}/{ano_sel}.")
            elif df_vendas.empty:
                st.warning(f"📭 Sem vendas aprovadas para {reg_sel} no período.")
            else:
                st.warning("📭 Nenhum dado disponível para auditoria.")
    
    # ==================== TAB 2: CONSULTAR HISTÓRICO ====================
    with tab_historico:
        st.subheader("🔎 Registros de Pagamentos")
        
        # Filtros
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            mes_filtro = st.selectbox("Mês", ["Todos"] + MESES_PT, key="hist_mes")
        with col_f2:
            ano_filtro = st.selectbox("Ano", ["Todos", 2025, 2026], key="hist_ano")
        with col_f3:
            reg_filtro = st.selectbox("Regional", ["Todas"] + list(opcoes_regional.keys()), key="hist_reg")
        
        if st.button("🔍 Buscar Histórico", use_container_width=True):
            with get_db_cursor() as cursor:
                query = "SELECT * FROM historico_comissoes WHERE 1=1"
                params = []
                
                if mes_filtro != "Todos":
                    mes_num_filtro = MESES_PT.index(mes_filtro) + 1
                    query += " AND mes_referencia = %s"
                    params.append(mes_num_filtro)
                
                if ano_filtro != "Todos":
                    query += " AND ano_referencia = %s"
                    params.append(ano_filtro)
                
                if reg_filtro != "Todas":
                    query += " AND regional = %s"
                    params.append(reg_filtro)
                
                query += " ORDER BY data_fechamento DESC"
                
                cursor.execute(query, tuple(params) if params else None)
                resultados = cursor.fetchall()
                
                if resultados:
                    df_hist = pd.DataFrame(resultados)
                    
                    # Gráfico de Resumo
                    st.write("### 📊 Resumo de Desembolso por Mês")
                    df_hist['Competência'] = df_hist['mes_referencia'].astype(str).str.zfill(2) + "/" + df_hist['ano_referencia'].astype(str)
                    df_pago = df_hist[df_hist['status_pagamento'] == 'PAGO'].groupby('Competência')['valor_pago'].sum().reset_index()
                    
                    if not df_pago.empty:
                        fig = px.bar(df_pago, x='Competência', y='valor_pago', 
                                     title="Pagamentos por Período",
                                     text_auto='.2s',
                                     color='valor_pago',
                                     color_continuous_scale='Viridis')
                        st.plotly_chart(fig, use_container_width=True, key="grafico_historico")
                    
                    st.divider()
                    
                    # Tabela detalhada
                    st.write("### 📋 Detalhamento dos Pagamentos")
                    df_display = df_hist.copy()
                    df_display['valor_pago'] = df_display['valor_pago'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                    st.dataframe(df_display, use_container_width=True, hide_index=True)
                    
                    # Botão exportar
                    csv = df_hist.to_csv(index=False, encoding='utf-8-sig', sep=';')
                    st.download_button(
                        "📥 Exportar Histórico (CSV)",
                        csv,
                        f"historico_comissoes_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv",
                        use_container_width=True
                    )
                else:
                    st.info("📭 Nenhum histórico encontrado. Realize um fechamento na aba ao lado para começar.")
    
    # ==================== TAB 3: AUDITORIA HUBSOFT ====================
    with tab_hubsoft:
        st.subheader("🔍 Auditoria de Instalações Hubsoft")
        st.info("Funcionalidade para verificar instalações de serviços no Hubsoft")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            reg_hub = st.selectbox("Regional", ["Geral"] + list(opcoes_regional.keys()), key="hub_reg")
        with col2:
            mes_hub = st.selectbox("Mês", MESES_PT, key="hub_mes")
            mes_num_hub = MESES_PT.index(mes_hub) + 1
        with col3:
            ano_hub = st.selectbox("Ano", [2025, 2026], key="hub_ano")
        
        if st.button("🔍 Buscar e Consultar Hubsoft", use_container_width=True, key="btn_hub"):
            with st.spinner("Buscando vendas..."):
                regs_map = {reg: id_reg for reg, id_reg in opcoes_regional.items()}
                regs_map["Geral"] = 0
                
                df_vendas = buscar_vendas_do_periodo(
                    reg_hub, mes_num_hub, ano_hub, regs_map, 'todos'
                )
                
                if not df_vendas.empty:
                    ids_validos = df_vendas[df_vendas['id_valido']]['id_servico'].tolist()
                    
                    if ids_validos:
                        with st.spinner(f"Consultando {len(ids_validos)} IDs no Hubsoft..."):
                            resultados = consultar_ids_hubsoft(ids_validos)
                            if resultados:
                                df_conciliado = criar_dataframe_conciliado(
                                    df_vendas, resultados, mes_num_hub, ano_hub
                                )
                                
                                st.success(f"✅ Consulta concluída! {len(df_conciliado)} registros processados.")
                                
                                # Métricas
                                instalados = len(df_conciliado[df_conciliado['Comissão Aplicável'] == True])
                                col_m1, col_m2, col_m3 = st.columns(3)
                                with col_m1:
                                    st.metric("Total Vendas", len(df_conciliado))
                                with col_m2:
                                    st.metric("✅ Instalados", instalados)
                                with col_m3:
                                    total_valor = df_conciliado[df_conciliado['Comissão Aplicável'] == True]['Valor (R$)'].sum()
                                    st.metric("💰 Valor Instalados", format_brl(total_valor))
                                
                                st.dataframe(
                                    df_conciliado[['ID Venda', 'Vendedor', 'ID Serviço', 'Data Instalação', 'Status', 'Valor (R$)']],
                                    use_container_width=True,
                                    hide_index=True
                                )
                    else:
                        st.warning("⚠️ Nenhum ID válido para consulta")
                else:
                    st.warning("Nenhuma venda encontrada")


# Para testes diretos
if __name__ == "__main__":
    exibir_tela_auditor()