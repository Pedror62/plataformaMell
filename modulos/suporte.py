# modulos/suporte.py
import streamlit as st
import datetime
import os
import subprocess
import pandas as pd
import glob
from database.queries import get_db_cursor, registrar_log

# ===== FUNÇÕES DE PERMISSÃO (TABELA 4) =====

def get_funcionalidades():
    """Retorna todas as funcionalidades ativas"""
    sql = "SELECT * FROM funcionalidades WHERE ativo = 1 ORDER BY ordem"
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar funcionalidades: {e}")
        return []

def get_permissoes_cargo(id_tipo_usuario):
    """Retorna as permissões de um cargo"""
    sql = """
        SELECT f.*, 
               COALESCE(p.pode_visualizar, 0) as pode_visualizar,
               COALESCE(p.pode_criar, 0) as pode_criar,
               COALESCE(p.pode_editar, 0) as pode_editar,
               COALESCE(p.pode_excluir, 0) as pode_excluir
        FROM funcionalidades f
        LEFT JOIN permissoes_cargo p ON f.id_funcionalidade = p.id_funcionalidade 
            AND p.id_tipo_usuario = %s
        WHERE f.ativo = 1
        ORDER BY f.ordem
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (id_tipo_usuario,))
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar permissões do cargo: {e}")
        return []

def get_permissoes_usuario(id_usuario):
    """Retorna permissões especiais de um usuário"""
    sql = """
        SELECT id_funcionalidade, pode_visualizar, pode_criar, pode_editar, pode_excluir
        FROM permissoes_usuario
        WHERE id_usuario = %s
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (id_usuario,))
            return {p['id_funcionalidade']: p for p in cursor.fetchall()}
    except Exception as e:
        print(f"Erro ao buscar permissões do usuário: {e}")
        return {}

def salvar_permissao_cargo(id_tipo_usuario, id_funcionalidade, permissoes):
    """Salva permissões para um cargo"""
    sql = """
        INSERT INTO permissoes_cargo 
        (id_tipo_usuario, id_funcionalidade, pode_visualizar, pode_criar, pode_editar, pode_excluir)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        pode_visualizar = VALUES(pode_visualizar),
        pode_criar = VALUES(pode_criar),
        pode_editar = VALUES(pode_editar),
        pode_excluir = VALUES(pode_excluir)
    """
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (
                id_tipo_usuario, 
                id_funcionalidade,
                permissoes.get('visualizar', 0),
                permissoes.get('criar', 0),
                permissoes.get('editar', 0),
                permissoes.get('excluir', 0)
            ))
            return True
    except Exception as e:
        print(f"Erro ao salvar permissão do cargo: {e}")
        return False

def salvar_permissao_usuario(id_usuario, id_funcionalidade, permissoes):
    """Salva permissões especiais para um usuário"""
    sql = """
        INSERT INTO permissoes_usuario 
        (id_usuario, id_funcionalidade, pode_visualizar, pode_criar, pode_editar, pode_excluir)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        pode_visualizar = VALUES(pode_visualizar),
        pode_criar = VALUES(pode_criar),
        pode_editar = VALUES(pode_editar),
        pode_excluir = VALUES(pode_excluir)
    """
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (
                id_usuario, 
                id_funcionalidade,
                permissoes.get('visualizar', 0),
                permissoes.get('criar', 0),
                permissoes.get('editar', 0),
                permissoes.get('excluir', 0)
            ))
            return True
    except Exception as e:
        print(f"Erro ao salvar permissão do usuário: {e}")
        return False

def verificar_permissao(id_usuario, id_tipo_usuario, funcionalidade_rota, acao='visualizar'):
    """Verifica se usuário tem permissão para uma ação"""
    try:
        # Primeiro busca a funcionalidade pela rota
        with get_db_cursor() as cursor:
            cursor.execute("SELECT id_funcionalidade FROM funcionalidades WHERE rota = %s", (funcionalidade_rota,))
            func = cursor.fetchone()
            if not func:
                print(f"Funcionalidade com rota '{funcionalidade_rota}' não encontrada")
                return False
            id_funcionalidade = func['id_funcionalidade']
        
        # Verifica permissão especial do usuário
        permissoes_user = get_permissoes_usuario(id_usuario)
        if id_funcionalidade in permissoes_user:
            return permissoes_user[id_funcionalidade].get(f'pode_{acao}', 0) == 1
        
        # Verifica permissão do cargo
        with get_db_cursor() as cursor:
            cursor.execute(f"""
                SELECT pode_{acao} 
                FROM permissoes_cargo 
                WHERE id_tipo_usuario = %s AND id_funcionalidade = %s
            """, (id_tipo_usuario, id_funcionalidade))
            permissao = cursor.fetchone()
            return permissao and permissao[f'pode_{acao}'] == 1
    except Exception as e:
        print(f"Erro ao verificar permissão: {e}")
        return False

def gerenciar_permissoes():
    """Tela para gerenciar permissões do sistema"""
    st.header("🔐 Gestão de Permissões")
    
    tab_cargos, tab_usuarios = st.tabs(["👥 Por Cargo", "👤 Por Usuário"])
    
    with tab_cargos:
        # Busca todos os cargos
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM tipo_usuario WHERE ativo = 1")
            cargos = cursor.fetchall()
        
        # Busca funcionalidades
        funcionalidades = get_funcionalidades()
        
        if not cargos:
            st.warning("Nenhum cargo encontrado.")
            return
        
        # Select de cargo
        cargo_sel = st.selectbox(
            "Selecione o Cargo",
            options=[(c['id_tipo_usuario'], c['descricao']) for c in cargos],
            format_func=lambda x: x[1]
        )
        
        if cargo_sel:
            id_cargo, nome_cargo = cargo_sel
            permissoes_atuais = get_permissoes_cargo(id_cargo)
            
            st.subheader(f"Permissões para {nome_cargo}")
            
            # Tabela de permissões
            with st.form(f"form_permissoes_cargo_{id_cargo}"):
                permissoes_dict = {}
                
                for func in funcionalidades:
                    permissao_atual = next((p for p in permissoes_atuais if p['id_funcionalidade'] == func['id_funcionalidade']), {})
                    
                    with st.container(border=True):
                        st.markdown(f"**{func['icone']} {func['nome']}**")
                        st.caption(func['descricao'] or "")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            visualizar = st.checkbox(
                                "Visualizar", 
                                value=bool(permissao_atual.get('pode_visualizar', 0)),
                                key=f"c_{id_cargo}_{func['id_funcionalidade']}_vis"
                            )
                        with col2:
                            criar = st.checkbox(
                                "Criar", 
                                value=bool(permissao_atual.get('pode_criar', 0)),
                                key=f"c_{id_cargo}_{func['id_funcionalidade']}_criar"
                            )
                        with col3:
                            editar = st.checkbox(
                                "Editar", 
                                value=bool(permissao_atual.get('pode_editar', 0)),
                                key=f"c_{id_cargo}_{func['id_funcionalidade']}_editar"
                            )
                        with col4:
                            excluir = st.checkbox(
                                "Excluir", 
                                value=bool(permissao_atual.get('pode_excluir', 0)),
                                key=f"c_{id_cargo}_{func['id_funcionalidade']}_excluir"
                            )
                        
                        permissoes_dict[func['id_funcionalidade']] = {
                            'visualizar': visualizar,
                            'criar': criar,
                            'editar': editar,
                            'excluir': excluir
                        }
                
                if st.form_submit_button("💾 Salvar Permissões"):
                    sucessos = 0
                    for id_func, permissoes in permissoes_dict.items():
                        if salvar_permissao_cargo(id_cargo, id_func, permissoes):
                            sucessos += 1
                    
                    if sucessos == len(permissoes_dict):
                        st.success(f"✅ Todas as permissões para {nome_cargo} foram salvas!")
                    else:
                        st.warning(f"⚠️ {sucessos} de {len(permissoes_dict)} permissões salvas.")
                    
                    registrar_log(st.session_state.id_usuario, "PERMISSOES", 
                                f"Atualizou permissões do cargo {nome_cargo}")
                    st.rerun()
    
    with tab_usuarios:
        # Busca usuários
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT u.id_usuario, u.nome_usuario, t.descricao as cargo
                FROM users u
                JOIN tipo_usuario t ON u.id_tipo_usuario = t.id_tipo_usuario
                WHERE u.ativo = 1
                ORDER BY u.nome_usuario
            """)
            usuarios = cursor.fetchall()
        
        if not usuarios:
            st.warning("Nenhum usuário encontrado.")
            return
        
        # Busca funcionalidades
        funcionalidades = get_funcionalidades()
        
        # Select de usuário
        usuario_sel = st.selectbox(
            "Selecione o Usuário",
            options=[(u['id_usuario'], f"{u['nome_usuario']} ({u['cargo']})") for u in usuarios],
            format_func=lambda x: x[1]
        )
        
        if usuario_sel:
            id_usuario, nome_usuario = usuario_sel
            permissoes_especiais = get_permissoes_usuario(id_usuario)
            
            st.subheader(f"Permissões Especiais para {nome_usuario}")
            st.caption("Estas permissões sobrescrevem as do cargo")
            
            with st.form(f"form_permissoes_usuario_{id_usuario}"):
                permissoes_dict = {}
                
                for func in funcionalidades:
                    permissao_atual = permissoes_especiais.get(func['id_funcionalidade'], {})
                    
                    with st.expander(f"{func['icone']} {func['nome']}"):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            visualizar = st.checkbox(
                                "Visualizar", 
                                value=bool(permissao_atual.get('pode_visualizar', 0)),
                                key=f"u_{id_usuario}_{func['id_funcionalidade']}_vis"
                            )
                        with col2:
                            criar = st.checkbox(
                                "Criar", 
                                value=bool(permissao_atual.get('pode_criar', 0)),
                                key=f"u_{id_usuario}_{func['id_funcionalidade']}_criar"
                            )
                        with col3:
                            editar = st.checkbox(
                                "Editar", 
                                value=bool(permissao_atual.get('pode_editar', 0)),
                                key=f"u_{id_usuario}_{func['id_funcionalidade']}_editar"
                            )
                        with col4:
                            excluir = st.checkbox(
                                "Excluir", 
                                value=bool(permissao_atual.get('pode_excluir', 0)),
                                key=f"u_{id_usuario}_{func['id_funcionalidade']}_excluir"
                            )
                        
                        permissoes_dict[func['id_funcionalidade']] = {
                            'visualizar': visualizar,
                            'criar': criar,
                            'editar': editar,
                            'excluir': excluir
                        }
                
                if st.form_submit_button("💾 Salvar Permissões Especiais"):
                    sucessos = 0
                    for id_func, permissoes in permissoes_dict.items():
                        if salvar_permissao_usuario(id_usuario, id_func, permissoes):
                            sucessos += 1
                    
                    if sucessos == len(permissoes_dict):
                        st.success(f"✅ Todas as permissões especiais para {nome_usuario} foram salvas!")
                    else:
                        st.warning(f"⚠️ {sucessos} de {len(permissoes_dict)} permissões salvas.")
                    
                    registrar_log(st.session_state.id_usuario, "PERMISSOES", 
                                f"Atualizou permissões do usuário {nome_usuario}")
                    st.rerun()

# Função local para enviar notificações
def enviar_notificacao_local(titulo, mensagem, destinatario):
    """
    Envia uma notificação para um grupo de usuários
    destinatario: "Todos", "Vendedores", "Supervisores", "Admins"
    """
    try:
        # Remove possíveis asteriscos e formatação Markdown
        titulo_limpo = titulo.replace('**', '').replace('__', '').strip() if titulo else ''
        mensagem_limpa = mensagem.replace('**', '').replace('__', '').strip() if mensagem else ''
        
        # Mapeia o destinatário para o formato do banco
        mapa_destinatario = {
            "Todos": "todos",
            "Vendedores": "vendedor",
            "Supervisores": "supervisor",
            "Admins": "admin",
            "Auditores": "auditor"
        }
        
        dest = mapa_destinatario.get(destinatario, destinatario.lower())
        
        sql = "INSERT INTO notificacoes (titulo, mensagem, destinatario, data_envio) VALUES (%s, %s, %s, NOW())"
        
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (titulo_limpo, mensagem_limpa, dest))
        
        return True
        
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")
        return False

def buscar_logs_local(limite=500):
    """Busca os logs do sistema - versão local"""
    sql = """
        SELECT l.id, u.nome_usuario, l.acao, l.detalhes, l.data_hora 
        FROM logs_sistema l
        JOIN users u ON l.id_usuario = u.id_usuario
        ORDER BY l.data_hora DESC 
        LIMIT %s
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (limite,))
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar logs: {e}")
        return []

def realizar_backup():
    """Função de backup original"""
    try:
        db_user = st.secrets["mysql"]["user"]
        db_password = st.secrets["mysql"]["password"]
        db_host = st.secrets["mysql"]["host"]
        db_name = st.secrets["mysql"]["database"]
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        nome_arquivo = f"backup_{db_name}_{timestamp}.sql"
        caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)

        mysqldump_exe = r'"C:\Program Files\MariaDB 12.2\bin\mysqldump.exe"'
        comando = f'{mysqldump_exe} -h {db_host} -u {db_user} -p"{db_password}" --ssl=0 {db_name} > "{caminho_arquivo}"'
        
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            st.error(f"Erro no MariaDB: {resultado.stderr}")
            return None
            
        return caminho_arquivo

    except Exception as e:
        st.error(f"Erro inesperado ao gerar backup: {e}")
        return None

def exibir_copyright():
    """Exibe o rodapé padrão do sistema"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #72767a; font-size: 0.85rem; padding: 10px;'>
            © 2026 Mell Internet - Gestão de Vendas. <br>
            <span style='font-size: 0.75rem;'>Desenvolvido pelo Suporte Interno</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

def verificar_backup_diario():
    """Verifica se já fez backup hoje, se não, faz automaticamente e retorna status"""
    import os
    from datetime import date
    import glob
    
    hoje = date.today().strftime("%Y-%m-%d")
    resultado = {
        'status': 'ok',
        'mensagem': '',
        'arquivo': None,
        'icone': '✅'
    }
    
    try:
        # Verifica se já existe algum backup de hoje
        backups_hoje = glob.glob(f"*{hoje}*.sql")
        
        if backups_hoje:
            resultado['mensagem'] = f"Backup de hoje já existe: {os.path.basename(backups_hoje[0])}"
            resultado['arquivo'] = backups_hoje[0]
            resultado['status'] = 'sucesso'
            resultado['icone'] = '✅'
            print(f"✅ {resultado['mensagem']}")  # APENAS NO CONSOLE
            return resultado
        
        # Se não existe, faz backup automático
        print("🔄 Realizando backup automático diário...")  # APENAS NO CONSOLE
        arquivo = realizar_backup()
        
        if arquivo and os.path.exists(arquivo):
            resultado['mensagem'] = f"Backup automático concluído: {os.path.basename(arquivo)}"
            resultado['arquivo'] = arquivo
            resultado['status'] = 'sucesso'
            resultado['icone'] = '🎉'
            print(f"🎉 {resultado['mensagem']}")  # APENAS NO CONSOLE
            
            # Registra no log
            registrar_log(26, "BACKUP_AUTOMATICO", f"Backup automático: {os.path.basename(arquivo)}")
        else:
            resultado['status'] = 'erro'
            resultado['mensagem'] = "Falha ao gerar backup automático"
            resultado['icone'] = '❌'
            print(f"❌ {resultado['mensagem']}")  # APENAS NO CONSOLE
            
    except Exception as e:
        resultado['status'] = 'erro'
        resultado['mensagem'] = f"Erro na verificação: {str(e)}"
        resultado['icone'] = '⚠️'
        print(f"⚠️ Erro em verificar_backup_diario: {e}")  # APENAS NO CONSOLE
    
    return resultado

def exibir_tela_suporte():
    """Tela exclusiva para Suporte Técnico - SEM MENSAGENS DE BACKUP NA TELA"""
    
    st.markdown(f"<h2 style='color: #01384d;'>🛡️ Central de Controle (Suporte Técnico)</h2>", unsafe_allow_html=True)
    
    # Verifica se é realmente suporte técnico
    if st.session_state.cargo_id != 26:
        st.error("⛔ Acesso negado! Esta área é exclusiva para Suporte Técnico.")
        return
    
    # ===== VERIFICAÇÃO DE BACKUP - COMPLETAMENTE SILENCIOSA =====
    if 'backup_verificado' not in st.session_state:
        st.session_state.backup_verificado = False

    if not st.session_state.backup_verificado:
        resultado_backup = verificar_backup_diario()
        st.session_state.backup_verificado = True
        st.session_state.ultimo_backup = resultado_backup
        # NADA É MOSTRADO NA TELA - NEM SUCESSO, NEM ERRO
    
    # Abas
    aba_notif, aba_logs, aba_manutencao, aba_permissoes = st.tabs([
        "📢 Disparar Notificações", 
        "📜 Logs de Auditoria",
        "🛠️ Manutenção do Sistema",
        "🔐 Gestão de Permissões"
    ])
    
    # ===== ABA 1: NOTIFICAÇÕES =====
    with aba_notif:
        st.subheader("📢 Enviar aviso para o Sino")
        
        with st.form("form_notificacao", clear_on_submit=True):
            titulo = st.text_input("Título do Alerta")
            mensagem = st.text_area("Mensagem detalhada")
            para_quem = st.selectbox("Destinatário", ["Todos", "Vendedores", "Supervisores", "Admins"])
            
            if st.form_submit_button("🔔 Disparar Alerta", use_container_width=True):
                if titulo and mensagem:
                    sucesso = enviar_notificacao_local(titulo, mensagem, para_quem)
                    if sucesso:
                        registrar_log(st.session_state.id_usuario, "NOTIFICACAO_ENVIADA", f"Título: {titulo} | Para: {para_quem}")
                        st.success("✅ Alerta enviado com sucesso!")
                        st.rerun() 
                    else:
                        st.error("❌ Erro técnico ao salvar no banco.")
                else:
                    st.warning("⚠️ Preencha o título e a mensagem.")
    
    # ===== ABA 2: LOGS =====
    with aba_logs:
        st.subheader("📜 Histórico de ações")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            dias_opcoes = {
                "Últimas 24h": 1,
                "Últimos 7 dias": 7,
                "Últimos 30 dias": 30,
                "Todos": None
            }
            periodo = st.selectbox("Período", list(dias_opcoes.keys()))
        
        with col_f2:
            filtro = st.text_input("Filtrar por ação", placeholder="Ex: LOGIN, VENDA, BACKUP")
        
        # Busca logs usando função local
        logs = buscar_logs_local(500)
        
        if logs:
            df_logs = pd.DataFrame(logs)
            
            if 'data_hora' in df_logs.columns:
                df_logs['data_hora'] = pd.to_datetime(df_logs['data_hora']).dt.strftime('%d/%m/%Y %H:%M:%S')
            
            if filtro and 'acao' in df_logs.columns:
                df_logs = df_logs[df_logs['acao'].str.contains(filtro.upper(), na=False)]
            
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
            
            # Estatísticas
            col_e1, col_e2, col_e3 = st.columns(3)
            col_e1.metric("Total de Registros", len(df_logs))
            
            if 'acao' in df_logs.columns:
                col_e2.metric("Ações Únicas", df_logs['acao'].nunique())
                backups_count = len(df_logs[df_logs['acao'].str.contains('BACKUP', na=False)])
                col_e3.metric("Backups Realizados", backups_count)
        else:
            st.info("Nenhum log encontrado.")
    
    # ===== ABA 3: MANUTENÇÃO =====
    with aba_manutencao:
        st.subheader("🛠️ Segurança e Backup")
        st.info("💾 Gere um backup completo (Dump) do banco de dados antes de realizar alterações estruturais.")
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.write(f"**Banco Ativo:** `{st.secrets['mysql']['database']}`")
        with col_info2:
            st.write(f"**Servidor:** `{st.secrets['mysql']['host']}`")
        
        st.divider()
        
        col_btn, col_status = st.columns([1, 2])
        
        with col_btn:
            if st.button("📥 Gerar Backup Agora", use_container_width=True, type="primary"):
                with st.spinner("🔄 Processando Dump MySQL..."):
                    arquivo_sql = realizar_backup()
                    
                    if arquivo_sql and os.path.exists(arquivo_sql):
                        registrar_log(
                            st.session_state.id_usuario, 
                            "BACKUP_MANUAL", 
                            f"Backup gerado: {os.path.basename(arquivo_sql)}"
                        )
                        
                        st.success("✅ Backup gerado com sucesso!")
                        
                        with open(arquivo_sql, "rb") as f:
                            st.download_button(
                                label="📥 Baixar Arquivo SQL",
                                data=f,
                                file_name=os.path.basename(arquivo_sql),
                                mime="application/sql",
                                use_container_width=True
                            )
                    else:
                        st.error("❌ Erro ao gerar backup. Verifique o console.")
        
        with col_status:
            st.markdown("### 📋 Últimos Backups")
            backups_encontrados = []
            
            for arquivo in os.listdir('.'):
                if arquivo.startswith('backup_') and arquivo.endswith('.sql'):
                    caminho = os.path.join('.', arquivo)
                    data_mod = datetime.datetime.fromtimestamp(os.path.getmtime(caminho))
                    tamanho = os.path.getsize(caminho) / (1024*1024)
                    backups_encontrados.append({
                        'Arquivo': arquivo,
                        'Data': data_mod.strftime('%d/%m/%Y %H:%M'),
                        'Tamanho': f'{tamanho:.2f} MB'
                    })
            
            if backups_encontrados:
                backups_encontrados.sort(key=lambda x: x['Data'], reverse=True)
                df_backups = pd.DataFrame(backups_encontrados[:5])
                st.dataframe(df_backups, use_container_width=True, hide_index=True)
                
                # Botão para limpar backups antigos
                if st.button("🧹 Limpar Backups Antigos (manter apenas os últimos 10)"):
                    backups_encontrados.sort(key=lambda x: x['Data'], reverse=True)
                    for backup in backups_encontrados[10:]:
                        try:
                            os.remove(backup['Arquivo'])
                            st.success(f"Removido: {backup['Arquivo']}")
                        except:
                            st.error(f"Erro ao remover: {backup['Arquivo']}")
                    st.rerun()
            else:
                st.info("Nenhum backup encontrado no diretório atual.")
    
    # ===== ABA 4: GESTÃO DE PERMISSÕES =====
    with aba_permissoes:
        gerenciar_permissoes()
    
    exibir_copyright()