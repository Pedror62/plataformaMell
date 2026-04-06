import streamlit as st
import pandas as pd
from database.queries import carregar_vendas, get_db_cursor
from datetime import datetime

def exibir_tela_comissoes():
    st.markdown("<h1 style='color: #004AAD;'>💰 Gestão de Comissões e Metas</h1>", unsafe_allow_html=True)
    st.caption("Apuração oficial baseada na Política de Remuneração Variável 2025.")
    st.divider()

    # --- AVISO DE PRAZO (até dia 10) ---
    hoje = datetime.now().day
    if hoje > 10:
        st.warning(f"⚠️ **ATENÇÃO:** Hoje é dia {hoje}. O prazo para validação com Karen Banar é até dia 10. Este cálculo entrará na folha do **próximo mês**.")
    else:
        st.success(f"✅ Dentro do prazo! Envie até dia 10 para pagamento na **próxima folha**.")

    # --- 1. FILTROS DE BUSCA ---
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id_regional, descricao FROM regional WHERE ativo = 1")
        regs_data = cursor.fetchall()
        opcoes_regional = {r['descricao']: r['id_regional'] for r in regs_data}

    if not opcoes_regional:
        st.error("❌ Nenhuma regional cadastrada ou ativa no sistema.")
        return

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        reg_padrao = st.session_state.get('regional_nome', list(opcoes_regional.keys())[0] if opcoes_regional else None)
        lista_regs = list(opcoes_regional.keys())
        idx_reg = lista_regs.index(reg_padrao) if reg_padrao in lista_regs else 0
        regional_sel = st.selectbox("📍 Selecionar Regional", lista_regs, index=idx_reg, key="comissoes_regional")
        id_reg = opcoes_regional[regional_sel]
    
    with col_f2:
        meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        mes_sel = st.selectbox("📅 Mês", meses_pt, index=datetime.now().month - 1, key="comissoes_mes")
        mes_num = meses_pt.index(mes_sel) + 1
        
    with col_f3:
        ano_sel = st.selectbox("📅 Ano", [2025, 2026], index=0, key="comissoes_ano")

    # --- 2. BUSCA DE METAS DA REGIONAL ---
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT meta_vendas_qtd, meta_migracao_qtd 
            FROM metas_regionais 
            WHERE id_regional = %s AND MONTH(mes_referencia) = %s AND YEAR(mes_referencia) = %s
        """, (id_reg, mes_num, ano_sel))
        meta_data = cursor.fetchone()
    
    if not meta_data:
        st.warning(f"⚠️ Metas não definidas para {regional_sel} em {mes_sel}/{ano_sel}. Vá em 'Metas das Regionais' para configurar.")
        return

    meta_venda_qtd = meta_data['meta_vendas_qtd']
    meta_migra_qtd = meta_data['meta_migracao_qtd']

    if meta_venda_qtd <= 0 or meta_migra_qtd <= 0:
        st.warning(f"⚠️ Metas inválidas: Vendas={meta_venda_qtd}, Migrações={meta_migra_qtd}. Verifique a configuração.")
        return

    st.info(f"🎯 Metas do Período: **{meta_venda_qtd} Vendas** | **{meta_migra_qtd} Migrações**")

    # --- 3. CARGA E TRATAMENTO DE DADOS ---
    with st.spinner("Carregando dados de vendas..."):
        df_vendas = carregar_vendas(id_reg, mes_num, ano_sel) 

    if df_vendas is None or df_vendas.empty:
        st.warning(f"📭 Sem vendas aprovadas para {regional_sel} no período.")
        return

    # Limpeza e conversão financeira
    for col in ['Valor Novo', 'Valor Anterior']:
        if col in df_vendas.columns:
            df_vendas[col] = pd.to_numeric(df_vendas[col], errors='coerce').fillna(0).astype(float)

    df_vendas['Status'] = df_vendas['Status'].astype(str).str.upper().str.strip()
    df_vendas['Tipo Operação'] = df_vendas['Tipo Operação'].astype(str).str.upper().str.strip()
    
    # Identifica tipos especiais de venda
    df_vendas['É Telefonia'] = df_vendas['Tipo Operação'].str.contains('TELEFONIA|FONE|VOIP', case=False, na=False)
    df_vendas['É B2B'] = df_vendas['Tipo Operação'].str.contains('B2B|EMPRESARIAL|CORPORATIVO', case=False, na=False)
    df_vendas['É Pague em Dia'] = df_vendas['Tipo Operação'].str.contains('PAGUE DIA|PAGUE EM DIA', case=False, na=False)

    # --- 4. APURAÇÃO POR VENDEDOR (POLÍTICA 2025 COMPLETA) ---
    apuracao_vendedores = []      # Vendedores normais
    apuracao_recepcao = []        # Recepção/Cobrança
    apuracao_telefonia = []       # Vendas de telefonia avulsa
    apuracao_b2b = []             # Vendas B2B
    
    vendedores = df_vendas['Vendedor'].unique()

    # Busca cargos dos vendedores
    cargos_vendedores = {}
    with get_db_cursor() as cursor:
        for v in vendedores:
            cursor.execute("""
                SELECT id_tipo_usuario 
                FROM users 
                WHERE nome_usuario = %s AND ativo = 1
            """, (v,))
            cargo = cursor.fetchone()
            if cargo:
                cargos_vendedores[v] = cargo['id_tipo_usuario']

    for v in vendedores:
        # Apenas vendas APROVADAS contam para comissão
        vendas_v = df_vendas[(df_vendas['Vendedor'] == v) & (df_vendas['Status'] == 'APROVADO')]
        
        if vendas_v.empty:
            continue
            
        # Separa por tipo de operação
        telefonia = vendas_v[vendas_v['É Telefonia']]
        b2b = vendas_v[vendas_v['É B2B']]
        vendas_normais = vendas_v[~vendas_v['É Telefonia'] & ~vendas_v['É B2B']]
        
        # Dentro das vendas normais, separa vendas novas e migrações
        vendas_novas = vendas_normais[vendas_normais['Tipo Operação'].str.contains('VENDA', case=False, na=False)]
        migracoes = vendas_normais[vendas_normais['Tipo Operação'].str.contains('MIGRA', case=False, na=False)]
        
        # Quantidades
        qtd_v = len(vendas_novas)
        qtd_m = len(migracoes)
        qtd_tel = len(telefonia)
        qtd_b2b = len(b2b)
        
        # --- COMISSÃO DE TELEFONIA (R$13 fixo, não conta na meta) ---
        comissao_telefonia = qtd_tel * 13.00
        if qtd_tel > 0:
            apuracao_telefonia.append({
                "Vendedor": v,
                "Vendas Telefonia": qtd_tel,
                "Comissão Telefonia (R$13)": comissao_telefonia
            })
        
        # --- COMISSÃO B2B (50% do valor, não conta na meta) ---
        comissao_b2b = b2b['Valor Novo'].sum() * 0.5 if not b2b.empty else 0
        if not b2b.empty:
            apuracao_b2b.append({
                "Vendedor": v,
                "Vendas B2B": qtd_b2b,
                "Valor Total B2B": b2b['Valor Novo'].sum(),
                "Comissão B2B (50%)": comissao_b2b
            })
        
        # --- CÁLCULO PARA VENDAS NORMAIS E MIGRAÇÕES ---
        ating_v = (qtd_v / meta_venda_qtd) * 100 if meta_venda_qtd > 0 else 0
        ating_m = (qtd_m / meta_migra_qtd) * 100 if meta_migra_qtd > 0 else 0
        
        comis_v = 0.0
        comis_m = 0.0
        
        # Verifica se é recepção/cobrança (IDs 5 e 6 - ajuste conforme seu banco)
        cargo_id = cargos_vendedores.get(v)
        is_recepcao = cargo_id in [5, 6] if cargo_id else False
        
        if is_recepcao:
            # Recepção/Cobrança: R$ 3,00 por venda (inclui todos os tipos)
            comis_v = (qtd_v + qtd_tel + qtd_b2b) * 3.00
            apuracao_recepcao.append({
                "Vendedor": v,
                "Vendas": qtd_v + qtd_tel + qtd_b2b,
                "Comissão (R$ 3,00)": comis_v
            })
        else:
            # VENDEDORES NORMAIS: REGRA DE ELEGIBILIDADE (80% em ambas as metas)
            if ating_v >= 80 and ating_m >= 80:
                
                # --- CÁLCULO VENDAS (Seção 2.1 e 3) ---
                if ating_v >= 120:
                    qtd_fixo = int(meta_venda_qtd * 1.2)
                    qtd_bonus = max(0, qtd_v - qtd_fixo)
                    # R$ 13,00 até 120% + 50% do valor do plano no excedente
                    comis_v = qtd_fixo * 13.00
                    
                    # Bônus de 50% sobre o valor do plano (primeira mensalidade)
                    for _, venda in vendas_novas.tail(qtd_bonus).iterrows():
                        # Se for "Pague em Dia", usar valor menor? Por enquanto usa o padrão
                        valor_plano = venda['Valor Novo']
                        comis_v += (valor_plano * 0.5)
                        
                elif ating_v >= 110:
                    comis_v = qtd_v * 12.00
                elif ating_v >= 100:
                    comis_v = qtd_v * 10.00
                else:  # 80% a 99%
                    comis_v = qtd_v * 8.00

                # --- CÁLCULO MIGRAÇÃO (Seção 2.2) ---
                perc_m = 0.0
                if ating_m >= 110:
                    perc_m = 1.0   # 100% da diferença
                elif ating_m >= 100:
                    perc_m = 0.9   # 90% da diferença
                elif ating_m >= 80:
                    perc_m = 0.8   # 80% da diferença

                for _, migra in migracoes.iterrows():
                    # Para migrações, usar valor "Pague em Dia" se disponível
                    if migra['É Pague em Dia']:
                        valor_base = migra['Valor Novo']  # Ajustar se houver campo específico
                    else:
                        valor_base = migra['Valor Novo']  # Valor cheio
                    
                    dif = valor_base - migra['Valor Anterior']
                    if dif > 0:
                        comis_m += (dif * perc_m)

            # --- ESTORNOS por cancelamento (≤3 meses) ---
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT COALESCE(SUM(c.valor_original), 0) as estorno
                    FROM cancelamentos c
                    JOIN users u ON c.id_usuario_vendedor = u.id_usuario
                    JOIN venda v ON c.id_venda_original = v.id_venda
                    WHERE u.nome_usuario = %s
                      AND c.status IN ('pendente', 'aprovado')
                      AND TIMESTAMPDIFF(MONTH, v.data_venda, c.data_ocorrencia) <= 3
                      AND MONTH(c.data_ocorrencia) = %s
                      AND YEAR(c.data_ocorrencia) = %s
                """, (v, mes_num, ano_sel))
                estorno_data = cursor.fetchone()
                estorno = float(estorno_data['estorno']) if estorno_data else 0.0
            
            # --- TOTAL DO VENDEDOR ---
            total_comissao = comis_v + comis_m + comissao_telefonia + comissao_b2b - estorno
            total_comissao = max(0, total_comissao)  # Não negativar

            # Só adiciona se tiver alguma comissão a receber
            if total_comissao > 0 or qtd_v > 0 or qtd_m > 0:
                apuracao_vendedores.append({
                    "Vendedor": v,
                    "Vendas": qtd_v,
                    "Migrações": qtd_m,
                    "Telefonia": qtd_tel,
                    "B2B": qtd_b2b,
                    "Ating. Venda": f"{ating_v:.1f}%",
                    "Ating. Migra": f"{ating_m:.1f}%",
                    "Comis. Vendas": comis_v,
                    "Comis. Migra": comis_m,
                    "Comis. Telefonia": comissao_telefonia,
                    "Comis. B2B": comissao_b2b,
                    "Estornos": estorno,
                    "Total Geral": total_comissao
                })

    # --- 5. EXIBIÇÃO DOS RESULTADOS - EQUIPE DE VENDAS ---
    st.subheader("📊 Resumo de Pagamentos - Equipe de Vendas")
    if apuracao_vendedores:
        df_final = pd.DataFrame(apuracao_vendedores)
        
        # Seleciona colunas para exibição
        colunas_exibir = ['Vendedor', 'Vendas', 'Migrações', 'Telefonia', 'B2B', 
                         'Ating. Venda', 'Ating. Migra', 'Comis. Vendas', 
                         'Comis. Migra', 'Estornos', 'Total Geral']
        
        df_exibicao = df_final[[c for c in colunas_exibir if c in df_final.columns]]
        
        st.dataframe(
            df_exibicao.style.format({
                'Comis. Vendas': 'R$ {:,.2f}', 
                'Comis. Migra': 'R$ {:,.2f}',
                'Comis. Telefonia': 'R$ {:,.2f}',
                'Comis. B2B': 'R$ {:,.2f}',
                'Estornos': 'R$ {:,.2f}',
                'Total Geral': 'R$ {:,.2f}'
            }), 
            use_container_width=True, 
            hide_index=True
        )
        
        # Totais gerais
        col_t1, col_t2, col_t3, col_t4 = st.columns(4)
        with col_t1:
            st.metric("💰 Total Comissões", f"R$ {df_final['Total Geral'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        with col_t2:
            st.metric("📊 Total Vendedores", len(df_final))
        with col_t3:
            st.metric("📉 Total Estornos", f"R$ {df_final['Estornos'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        with col_t4:
            media = df_final['Total Geral'].mean()
            st.metric("📈 Média por Vendedor", f"R$ {media:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    else:
        st.info("Nenhum vendedor atingiu os critérios de elegibilidade (80/80) neste período.")

    # --- 6. EXIBIÇÃO DOS RESULTADOS - TELEFONIA ---
    if apuracao_telefonia:
        st.subheader("📞 Comissões de Telefonia Avulsa (R$13 por venda)")
        df_telefonia = pd.DataFrame(apuracao_telefonia)
        st.dataframe(
            df_telefonia.style.format({'Comissão Telefonia (R$13)': 'R$ {:,.2f}'}),
            use_container_width=True,
            hide_index=True
        )

    # --- 7. EXIBIÇÃO DOS RESULTADOS - B2B ---
    if apuracao_b2b:
        st.subheader("🏢 Comissões B2B (50% do valor)")
        df_b2b = pd.DataFrame(apuracao_b2b)
        st.dataframe(
            df_b2b.style.format({
                'Valor Total B2B': 'R$ {:,.2f}',
                'Comissão B2B (50%)': 'R$ {:,.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )

    # --- 8. EXIBIÇÃO DOS RESULTADOS - RECEPÇÃO/COBRANÇA ---
    if apuracao_recepcao:
        st.subheader("📋 Resumo de Pagamentos - Recepção/Cobrança (R$3 por venda)")
        df_recepcao = pd.DataFrame(apuracao_recepcao)
        st.dataframe(
            df_recepcao.style.format({'Comissão (R$ 3,00)': 'R$ {:,.2f}'}),
            use_container_width=True,
            hide_index=True
        )

    # --- 9. CÁLCULO PARA LÍDERES (10% da receita líquida) ---
    st.divider()
    st.subheader("👔 Comissão da Liderança (10% da Receita Líquida)")

    with get_db_cursor() as cursor:
        # Busca líderes da regional (Supervisores - id_tipo_usuario = 3)
        cursor.execute("""
            SELECT id_usuario, nome_usuario 
            FROM users 
            WHERE id_regional = %s AND id_tipo_usuario = 3 AND ativo = 1
        """, (id_reg,))
        lideres = cursor.fetchall()

    if lideres:
        # Calcula receita bruta (apenas vendas aprovadas de todos os tipos)
        df_aprovadas = df_vendas[df_vendas['Status'] == 'APROVADO']
        receita_bruta = df_aprovadas['Valor Novo'].sum() if not df_aprovadas.empty else 0
        
        # Busca cancelamentos no período que impactam a receita
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT COALESCE(SUM(v.valor_venda), 0) as cancelamentos
                FROM venda v
                JOIN users u ON v.id_usuario_vendedor = u.id_usuario
                WHERE u.id_regional = %s 
                  AND v.id_status = 4  -- Cancelado
                  AND MONTH(v.data_venda) = %s 
                  AND YEAR(v.data_venda) = %s
            """, (id_reg, mes_num, ano_sel))
            cancel_data = cursor.fetchone()
            cancelamentos = float(cancel_data['cancelamentos']) if cancel_data else 0.0
        
        receita_liquida = max(0, receita_bruta - cancelamentos)
        comissao_lider = receita_liquida * 0.10  # 10%
        
        dados_lideres = []
        for lider in lideres:
            dados_lideres.append({
                "Líder": lider['nome_usuario'],
                "Receita Bruta": receita_bruta,
                "Cancelamentos": cancelamentos,
                "Receita Líquida": receita_liquida,
                "Comissão (10%)": comissao_lider
            })
        
        df_lideres = pd.DataFrame(dados_lideres)
        st.dataframe(
            df_lideres.style.format({
                'Receita Bruta': 'R$ {:,.2f}',
                'Cancelamentos': 'R$ {:,.2f}',
                'Receita Líquida': 'R$ {:,.2f}',
                'Comissão (10%)': 'R$ {:,.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        st.metric("💰 Total Liderança", f"R$ {comissao_lider:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    else:
        st.info("ℹ️ Nenhum líder encontrado para esta regional.")

    st.divider()

    # --- 10. DOWNLOAD DO RELATÓRIO COMPLETO ---
    if any([apuracao_vendedores, apuracao_recepcao, apuracao_telefonia, apuracao_b2b, lideres]):
        # Combina todos os dados para download
        relatorio_completo = []
        
        # Vendedores
        for item in apuracao_vendedores:
            relatorio_completo.append({
                "Tipo": "Vendedor",
                "Nome": item["Vendedor"],
                "Vendas": item.get("Vendas", 0),
                "Migrações": item.get("Migrações", 0),
                "Telefonia": item.get("Telefonia", 0),
                "B2B": item.get("B2B", 0),
                "% Vendas": item.get("Ating. Venda", "-"),
                "% Migrações": item.get("Ating. Migra", "-"),
                "Comissão Vendas": item.get("Comis. Vendas", 0),
                "Comissão Migrações": item.get("Comis. Migra", 0),
                "Comissão Telefonia": item.get("Comis. Telefonia", 0),
                "Comissão B2B": item.get("Comis. B2B", 0),
                "Estornos": item.get("Estornos", 0),
                "Total": item.get("Total Geral", 0)
            })
        
        # Telefonia
        for item in apuracao_telefonia:
            relatorio_completo.append({
                "Tipo": "Telefonia",
                "Nome": item["Vendedor"],
                "Vendas": 0,
                "Migrações": 0,
                "Telefonia": item.get("Vendas Telefonia", 0),
                "B2B": 0,
                "% Vendas": "-",
                "% Migrações": "-",
                "Comissão Vendas": 0,
                "Comissão Migrações": 0,
                "Comissão Telefonia": item.get("Comissão Telefonia (R$13)", 0),
                "Comissão B2B": 0,
                "Estornos": 0,
                "Total": item.get("Comissão Telefonia (R$13)", 0)
            })
        
        # B2B
        for item in apuracao_b2b:
            relatorio_completo.append({
                "Tipo": "B2B",
                "Nome": item["Vendedor"],
                "Vendas": 0,
                "Migrações": 0,
                "Telefonia": 0,
                "B2B": item.get("Vendas B2B", 0),
                "% Vendas": "-",
                "% Migrações": "-",
                "Comissão Vendas": 0,
                "Comissão Migrações": 0,
                "Comissão Telefonia": 0,
                "Comissão B2B": item.get("Comissão B2B (50%)", 0),
                "Estornos": 0,
                "Total": item.get("Comissão B2B (50%)", 0)
            })
        
        # Recepção
        for item in apuracao_recepcao:
            relatorio_completo.append({
                "Tipo": "Recepção",
                "Nome": item["Vendedor"],
                "Vendas": item.get("Vendas", 0),
                "Migrações": 0,
                "Telefonia": 0,
                "B2B": 0,
                "% Vendas": "-",
                "% Migrações": "-",
                "Comissão Vendas": item.get("Comissão (R$ 3,00)", 0),
                "Comissão Migrações": 0,
                "Comissão Telefonia": 0,
                "Comissão B2B": 0,
                "Estornos": 0,
                "Total": item.get("Comissão (R$ 3,00)", 0)
            })
        
        # Líderes
        if lideres:
            for item in dados_lideres:
                relatorio_completo.append({
                    "Tipo": "Líder",
                    "Nome": item["Líder"],
                    "Vendas": 0,
                    "Migrações": 0,
                    "Telefonia": 0,
                    "B2B": 0,
                    "% Vendas": "-",
                    "% Migrações": "-",
                    "Comissão Vendas": item["Comissão (10%)"],
                    "Comissão Migrações": 0,
                    "Comissão Telefonia": 0,
                    "Comissão B2B": 0,
                    "Estornos": 0,
                    "Total": item["Comissão (10%)"]
                })
        
        if relatorio_completo:
            df_relatorio = pd.DataFrame(relatorio_completo)
            
            # Formatação para CSV
            for col in ['Comissão Vendas', 'Comissão Migrações', 'Comissão Telefonia', 
                       'Comissão B2B', 'Estornos', 'Total']:
                if col in df_relatorio.columns:
                    df_relatorio[col] = df_relatorio[col].apply(lambda x: f"{x:,.2f}".replace(",", "@").replace(".", ",").replace("@", "."))
            
            csv = df_relatorio.to_csv(index=False, encoding='utf-8-sig', sep=';')
            
            col_d1, col_d2, col_d3 = st.columns(3)
            with col_d1:
                st.download_button(
                    "📥 Download Relatório Completo (CSV)",
                    csv,
                    f"comissoes_completas_{regional_sel}_{mes_sel}_{ano_sel}.csv",
                    "text/csv",
                    use_container_width=True
                )
    else:
        st.info("📭 Nenhum dado disponível para exportar neste período.")

    # --- 11. INFORMAÇÕES ADICIONAIS DA POLÍTICA ---
    with st.expander("📋 Resumo da Política de Remuneração 2025", expanded=False):
        st.markdown("""
        ### Regras Principais:
        
        **Elegibilidade:** Mínimo 80% nas duas metas (vendas e migrações)
        
        **Comissões Vendas:**
        - 80% → R$ 8,00 por venda
        - 100% → R$ 10,00 por venda  
        - 110% → R$ 12,00 por venda
        - 120% → R$ 13,00 por venda + 50% do valor do plano nas vendas excedentes
        
        **Comissões Migração:**
        - 80% → 80% da diferença do plano
        - 100% → 90% da diferença do plano
        - 110%+ → 100% da diferença do plano
        
        **Casos Especiais:**
        - Telefonia avulsa: R$ 13,00 (não conta na meta)
        - B2B: 50% do valor (não conta na meta)
        - Recepção/Cobrança: R$ 3,00 por venda (sem meta)
        - Liderança: 10% da receita líquida da regional
        
        **Estornos:** Cancelamentos em até 3 meses são descontados
        """)