import streamlit as st
import os
import glob
import subprocess
from datetime import datetime, date
import hashlib
import hmac
import base64
import platform
from database.queries import (
    login_usuario, 
    atualizar_senha_usuario, 
    registrar_log,           
    buscar_notificacoes,
    marcar_notificacoes_como_lidas,
    get_db_cursor
)
from modulos.supervisor import exibir_tela_supervisor, exibir_cancelamentos_regionais
from modulos.vendedor import exibir_tela_vendedor
from modulos.admin import (
    exibir_dashboard_admin, 
    gerenciar_usuarios, 
    exibir_gestao_metas, 
    exibir_dashboard_cancelamentos,
    exibir_visao_instalacoes_hubsoft,
    exibir_todas_vendas_hubsoft
)
from modulos.auditor import exibir_tela_auditor
from modulos.suporte import exibir_tela_suporte
from modulos.treinamento import exibir_tela_treinamentos, gerenciar_treinamentos_admin

# ===== FUNÇÃO PARA CARREGAR LOGO =====
def carregar_logo():
    """Carrega a logo do sistema"""
    import os
    import base64
    from PIL import Image
    import io
    
    nomes_arquivo = [
        "MELL beacons.png",
        "logo.png",
        "assets/LOGO MELL.png"
    ]
    
    pastas = [".", "src", "./src", os.path.dirname(__file__), 
              os.path.join(os.path.dirname(__file__), "assets"),
              os.path.join(os.path.dirname(__file__), "src", "assets")]
    
    arquivo_encontrado = None
    
    for nome in nomes_arquivo:
        for pasta in pastas:
            caminho = os.path.join(pasta, nome)
            if os.path.exists(caminho):
                arquivo_encontrado = caminho
                break
        if arquivo_encontrado:
            break
    
    if not arquivo_encontrado:
        return None, None
    
    try:
        img = Image.open(arquivo_encontrado)
        
        max_width = 300
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        
        encoded = base64.b64encode(buffer.read()).decode()
        
        return encoded, arquivo_encontrado
        
    except Exception as e:
        return None, None

# ===== FUNÇÃO PARA CRIAR TOKEN DE SESSÃO =====
def criar_token_sessao(id_usuario, user_nome, cargo_id):
    """Cria um token simples baseado nos dados do usuário"""
    try:
        secret_key = st.secrets.get("session", {}).get("secret_key", "mell_internet_secret_key_2026")
    except:
        secret_key = "mell_internet_secret_key_2026"
    
    dados = f"{id_usuario}|{user_nome}|{cargo_id}|{datetime.now().strftime('%Y-%m-%d')}"
    token = hmac.new(
        key=secret_key.encode(),
        msg=dados.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    
    return token, dados

def verificar_login_url():
    """Verifica se há parâmetros de login na URL e restaura a sessão"""
    
    if st.session_state.get('auth', False):
        return True
    
    query_params = st.query_params
    
    if 'token' in query_params and 'user_data' in query_params:
        token = query_params['token']
        user_data = query_params['user_data']
        
        if verificar_token_sessao(token, user_data):
            partes = user_data.split('|')
            if len(partes) >= 4:
                id_usuario = int(partes[0])
                user_nome = partes[1]
                cargo_id = int(partes[2])
                data_token = partes[3]
                
                if data_token == datetime.now().strftime('%Y-%m-%d'):
                    st.session_state.auth = True
                    st.session_state.id_usuario = id_usuario
                    st.session_state.user_nome = user_nome
                    st.session_state.cargo_id = cargo_id
                    
                    with get_db_cursor() as cursor:
                        cursor.execute("""
                            SELECT u.id_regional, r.descricao as regional_nome
                            FROM users u
                            LEFT JOIN regional r ON u.id_regional = r.id_regional
                            WHERE u.id_usuario = %s
                        """, (id_usuario,))
                        user_info = cursor.fetchone()
                        
                        if user_info:
                            st.session_state.id_regional = user_info.get('id_regional')
                            st.session_state.regional_nome = user_info.get('regional_nome', 'Geral')
                        
                        perfis = {
                            1: 'admin', 2: 'vendedor', 3: 'supervisor',
                            4: 'auditor', 24: 'gestor_treinamento', 26: 'suporte'
                        }
                        st.session_state.perfil = perfis.get(cargo_id, 'vendedor')
                    
                    st.query_params.clear()
                    
                    return True
    
    return False

def verificar_token_sessao(token, dados):
    """Verifica se o token é válido"""
    try:
        secret_key = st.secrets.get("session", {}).get("secret_key", "mell_internet_secret_key_2026")
    except:
        secret_key = "mell_internet_secret_key_2026"
    
    token_esperado = hmac.new(
        key=secret_key.encode(),
        msg=dados.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(token, token_esperado)

# ===== BACKUP AUTOMÁTICO CORRIGIDO =====
def realizar_backup_automatico():
    """Função de backup automático que roda silenciosamente - CORRIGIDA PARA LINUX"""
    try:
        # Detectar sistema operacional
        if platform.system() == "Windows":
            mysqldump_exe = r'"C:\Program Files\MariaDB 12.2\bin\mysqldump.exe"'
        else:
            mysqldump_exe = "mysqldump"
        
        db_user = st.secrets["mysql"]["user"]
        db_password = st.secrets["mysql"]["password"]
        db_host = st.secrets["mysql"]["host"]
        db_name = st.secrets["mysql"]["database"]
        
        pasta_backup = "backups_automaticos"
        if not os.path.exists(pasta_backup):
            os.makedirs(pasta_backup)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nome_arquivo = f"backup_auto_{db_name}_{timestamp}.sql"
        caminho_arquivo = os.path.join(pasta_backup, nome_arquivo)

        comando = f'{mysqldump_exe} -h {db_host} -u {db_user} -p"{db_password}" {db_name} > "{caminho_arquivo}"'
        
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0 and os.path.exists(caminho_arquivo):
            with open("backup_log.txt", "a") as log_file:
                log_file.write(f"{datetime.now()} - Backup: {nome_arquivo}\n")
            return True, caminho_arquivo
        else:
            return False, resultado.stderr
            
    except Exception as e:
        return False, str(e)

def verificar_e_executar_backup():
    """Verifica se já existe backup de hoje e executa se necessário"""
    try:
        pasta_backup = "backups_automaticos"
        if not os.path.exists(pasta_backup):
            os.makedirs(pasta_backup)
        
        hoje = date.today().strftime("%Y-%m-%d")
        backups_hoje = glob.glob(os.path.join(pasta_backup, f"*{hoje}*.sql"))
        
        if not backups_hoje:
            return realizar_backup_automatico()
        else:
            return True, backups_hoje[0]
    except Exception as e:
        # Não para o sistema se o backup falhar
        print(f"Backup não executado: {e}")
        return True, None

# Executar backup (não crítico)
try:
    verificar_e_executar_backup()
except:
    pass

# ===== CARREGA A LOGO =====
logo_base64, caminho_logo = carregar_logo()

# ===== CONFIGURAÇÃO GLOBAL =====
if logo_base64:
    favicon = f"data:image/png;base64,{logo_base64}"
else:
    try:
        with open("assets/LOGO MELL.png", "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
            favicon = f"data:image/png;base64,{img_base64}"
    except:
        favicon = "💰"

st.set_page_config(
    page_title="PROSALES - Gestão Profissional de Vendas", 
    layout="wide", 
    page_icon=favicon,
    initial_sidebar_state="collapsed"
)

# ===== INICIALIZAÇÃO DE ESTADO =====
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'id_usuario' not in st.session_state:
    st.session_state.id_usuario = None
if 'user_nome' not in st.session_state:
    st.session_state.user_nome = ""
if 'cargo_id' not in st.session_state:
    st.session_state.cargo_id = None
if 'perfil' not in st.session_state:
    st.session_state.perfil = None
if 'id_regional' not in st.session_state:
    st.session_state.id_regional = None
if 'regional_nome' not in st.session_state:
    st.session_state.regional_nome = ""
if 'trocando_senha' not in st.session_state:
    st.session_state.trocando_senha = False
if 'backup_verificado_hoje' not in st.session_state:
    st.session_state.backup_verificado_hoje = False
if 'ultimo_backup' not in st.session_state:
    st.session_state.ultimo_backup = None

# ===== VERIFICAÇÃO DE LOGIN VIA URL =====
if not st.session_state.auth:
    verificar_login_url()

# ===== TELA DE LOGIN =====
if not st.session_state.auth:
    cor_primaria = "#169fda"
    cor_secundaria = "#0d7ab3"
    cor_fundo = "#01384d"
    
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, {cor_fundo} 0%, #1a5f7a 100%);
            overflow: hidden !important;
            height: 100vh !important;
            width: 100vw !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        
        html, body {{
            overflow: hidden !important;
            height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            position: fixed !important;
            width: 100% !important;
        }}
        
        .stAppViewContainer {{
            overflow: hidden !important;
            height: 100vh !important;
        }}
        
        .stAppViewBlockContainer {{
            overflow: hidden !important;
            height: 100vh !important;
            padding: 0 !important;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}
        
        .main .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
            height: 100vh !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}
        
        [data-testid="stSidebar"] {{
            display: none !important;
        }}
        
        header {{
            display: none !important;
        }}
        
        ::-webkit-scrollbar {{
            display: none !important;
        }}
        
        .login-card {{
            background: #ffffff;
            border-radius: 28px;
            padding: 2rem 1.8rem;
            width: 100%;
            max-width: 400px;
            margin: 0 auto;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(22, 159, 218, 0.15);
            text-align: center;
        }}
        
        .logo-icon {{
            background: linear-gradient(135deg, {cor_primaria}, {cor_secundaria});
            width: 70px;
            height: 70px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem auto;
            box-shadow: 0 10px 20px rgba(22, 159, 218, 0.3);
        }}
        
        .logo-icon img {{
            width: 45px;
            height: 45px;
            object-fit: contain;
        }}
        
        .logo-icon span {{
            font-size: 32px;
        }}
        
        .login-title {{
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, {cor_primaria}, {cor_secundaria});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 0.25rem 0;
        }}
        
        .login-subtitle {{
            font-size: 0.75rem;
            color: #6c757d;
            margin-bottom: 1.5rem;
        }}
        
        .form-group {{
            margin-bottom: 1rem;
            text-align: left;
        }}
        
        .form-label {{
            display: block;
            font-size: 0.75rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 0.3rem;
        }}
        
        .input-wrapper {{
            position: relative;
        }}
        
        .input-icon {{
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: #9ca3af;
            font-size: 0.9rem;
            z-index: 1;
        }}
        
        .stTextInput > div > div > input {{
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 0.65rem 1rem 0.65rem 2.2rem !important;
            font-size: 0.85rem !important;
            background: #ffffff !important;
            color: #1a1a1a !important;
            width: 100%;
        }}
        
        .stTextInput > div > div > input::placeholder {{
            color: #4a4a4a !important;
            opacity: 0.7 !important;
            font-weight: normal !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {cor_primaria} !important;
            box-shadow: 0 0 0 2px rgba(22, 159, 218, 0.1) !important;
            background: #ffffff !important;
        }}
        
        .forgot-link {{
            text-align: right;
            margin: 0.5rem 0 1rem 0;
        }}
        
        .forgot-link a {{
            color: {cor_primaria};
            text-decoration: none;
            font-size: 0.7rem;
        }}
        
        .forgot-link a:hover {{
            text-decoration: underline;
        }}
        
        .stButton > button {{
            width: 100%;
            background: linear-gradient(135deg, {cor_primaria}, {cor_secundaria}) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.65rem !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            margin-top: 0.25rem;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 5px 15px rgba(22, 159, 218, 0.3);
        }}
        
        .login-footer {{
            text-align: center;
            font-size: 0.6rem;
            color: #adb5bd;
            margin-top: 1.2rem;
            padding-top: 0.8rem;
            border-top: 1px solid #e9ecef;
        }}
        
        .stAlert {{
            margin-top: 0.5rem;
            padding: 0.4rem;
            font-size: 0.75rem;
            border-radius: 8px;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if logo_base64:
            st.markdown(f"""
                <div class="login-card">
                    <div class="logo-icon">
                        <img src='data:image/png;base64,{logo_base64}' alt='Logo'>
                    </div>
                    <div class="login-title">PROSALES</div>
                    <div class="login-subtitle">Mell Internet · Gestão Profissional de Vendas</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="login-card">
                    <div class="logo-icon">
                        <span>💰</span>
                    </div>
                    <div class="login-title">PROSALES</div>
                    <div class="login-subtitle">Mell Internet · Gestão Profissional de Vendas</div>
                </div>
            """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<label class="form-label">Usuário</label>', unsafe_allow_html=True)
            st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
            st.markdown('<span class="input-icon">👤</span>', unsafe_allow_html=True)
            usuario = st.text_input("", placeholder="Digite seu usuário", label_visibility="collapsed")
            st.markdown('</div></div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<label class="form-label">Senha</label>', unsafe_allow_html=True)
            st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
            st.markdown('<span class="input-icon">🔒</span>', unsafe_allow_html=True)
            senha = st.text_input("", type="password", placeholder="Digite sua senha", label_visibility="collapsed")
            st.markdown('</div></div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="forgot-link">
                    <a href="#">Esqueceu a senha?</a>
                </div>
            """, unsafe_allow_html=True)
            
            submitted = st.form_submit_button("ENTRAR", use_container_width=True)
            
            if submitted:
                if not usuario or not senha:
                    st.error("❌ Preencha todos os campos!")
                else:
                    user = login_usuario(usuario, senha)
                    if user:
                        st.session_state.auth = True
                        st.session_state.id_usuario = user['id_usuario']
                        st.session_state.user_nome = user['nome_usuario']
                        st.session_state.cargo_id = user['id_tipo_usuario']
                        st.session_state.perfil = user.get('nivel_acesso', 'vendedor')
                        st.session_state.id_regional = user['id_regional']
                        st.session_state.regional_nome = user.get('regional_nome', 'Geral')
                        
                        token, user_data = criar_token_sessao(
                            user['id_usuario'], 
                            user['nome_usuario'], 
                            user['id_tipo_usuario']
                        )
                        
                        st.query_params['token'] = token
                        st.query_params['user_data'] = user_data
                        
                        registrar_log(user['id_usuario'], "LOGIN", "Acesso realizado")
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha inválidos!")
        
        st.markdown(f"""
            <div class="login-footer">
                © {datetime.now().year} PROSALES · Gestão Profissional de Vendas
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ===== TELA PRINCIPAL APÓS LOGIN =====
else:
    # --- VERIFICAÇÃO DE BACKUP ---
    if st.session_state.cargo_id == 26 and not st.session_state.backup_verificado_hoje:
        try:
            from modulos.suporte import verificar_backup_diario
            resultado = verificar_backup_diario()
            st.session_state.backup_verificado_hoje = True
            st.session_state.ultimo_backup = resultado
        except Exception as e:
            st.session_state.backup_verificado_hoje = True
            st.session_state.ultimo_backup = {
                'status': 'erro',
                'mensagem': f'Erro: {str(e)}',
                'arquivo': None
            }

    # --- INTERFACE LOGADA ---
    col_notif, col_empty = st.columns([1.5, 4])
    
    with col_notif:
        notificacoes = buscar_notificacoes(st.session_state.perfil, st.session_state.id_usuario)
        qtd_notif = len(notificacoes)
        
        with st.popover(f"🔔 Notificações ({qtd_notif})", use_container_width=True):
            if notificacoes:
                for n in notificacoes:
                    titulo_limpo = n['titulo'].replace('**', '').replace('__', '').strip() if n['titulo'] else ''
                    mensagem_limpa = n['mensagem'].replace('**', '').replace('__', '').strip() if n['mensagem'] else ''
                    
                    st.markdown(f"""
                    <div style='background: #f8f9fa; border-radius: 10px; padding: 10px; margin-bottom: 10px; border-left: 3px solid #169fda;'>
                        <div style='font-weight: bold; color: #169fda;'>{titulo_limpo}</div>
                        <div style='color: #333; font-size: 0.8rem;'>{mensagem_limpa}</div>
                        <div style='font-size: 0.65rem; color: #999; margin-top: 5px;'>🕐 {n['data_envio']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.button("✓ Marcar todas como lidas", key="marcar_lidas", use_container_width=True):
                    ids = [n['id'] for n in notificacoes if 'id' in n]
                    if ids:
                        marcar_notificacoes_como_lidas(st.session_state.id_usuario, ids)
                        st.success("Notificações marcadas como lidas!")
                        st.rerun()
            else:
                st.info("📭 Nenhuma notificação não lida")
    
    # Sidebar
    with st.sidebar:
        if logo_base64:
            st.markdown(f"""
                <div style='text-align: center; padding: 10px 0; margin-bottom: 20px; border-bottom: 1px solid #e0e0e0;'>
                    <img src='data:image/png;base64,{logo_base64}' 
                         style='width: 100%; max-width: 120px; height: auto; margin: 0 auto;' alt='Logo'>
                    <p style='color: #169fda; font-size: 0.65rem; margin-top: 5px;'>A internet sempre feliz.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='text-align: center; padding: 10px 0;'>
                    <div style='font-size: 2rem;'>💰</div>
                    <h3 style='margin: 0;'>PRO SALES</h3>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown(f"### 👤 {st.session_state.user_nome}")
        st.markdown(f"📍 {st.session_state.regional_nome}")
        st.divider()
        
        cargo_id = st.session_state.cargo_id
        menu_options = []
        
        if cargo_id == 1:
            menu_options = [
                "📊 Dashboard Estratégico",
                "📉 Desistências",
                "👥 Gestão de Usuários",
                "🎯 Metas Regionais",
                "🛡️ Visão de Supervisor",
                "📚 Gestão de Treinamentos",
            ]
        elif cargo_id == 24:
            menu_options = [
                "📚 Gestão de Treinamentos",
                "📊 Dashboard Estratégico",
                "📑 Auditoria"
            ]
        elif cargo_id == 26:
            menu_options = [
                "📊 Dashboard Estratégico",
                "👥 Gestão de Usuários",
                "🎯 Metas Regionais",
                "📚 Meus Treinamentos",
                "📑 Auditoria",
                "🛠️ Painel Suporte"
            ]
        elif cargo_id == 3:
            menu_options = [
                "🛡️ Visão de Supervisor",
                "📉 Desistências",
                "📚 Meus Treinamentos"
                
            ]
        elif cargo_id == 2:
            menu_options = [
                "💰 Minhas Vendas",
                "📚 Meus Treinamentos"
            ]
        elif cargo_id == 4:
            menu_options = [
                "📑 Auditoria",
                "📚 Meus Treinamentos",
                "📊 Visão de Instalações Hubsoft",
                "🌐 Todas as Vendas Hubsoft"
            ]
        else:
            menu_options = ["ℹ️ Sem Acesso"]
        
        if menu_options:
            escolha = st.radio("📌 Menu Principal", menu_options, key="menu_principal")
        else:
            st.warning("Nenhuma opção disponível")
            escolha = None
            
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 Trocar Senha", use_container_width=True):
                st.session_state.trocando_senha = True
                st.rerun()
        with col2:
            if st.button("🔴 Sair", use_container_width=True):
                st.query_params.clear()
                registrar_log(st.session_state.id_usuario, "LOGOUT", "Saiu do sistema")
                st.session_state.clear()
                st.rerun()

    # ===== CONTEÚDO PRINCIPAL =====
    try:
        if st.session_state.get('trocando_senha', False):
            st.title("🔐 Alterar Senha")
            with st.form("form_troca_senha"):
                senha_atual = st.text_input("Senha Atual", type="password")
                nova_senha = st.text_input("Nova Senha", type="password")
                confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Atualizar Senha", use_container_width=True):
                        if nova_senha != confirmar_senha:
                            st.error("As senhas não coincidem!")
                        elif atualizar_senha_usuario(st.session_state.id_usuario, senha_atual, nova_senha):
                            st.success("Senha alterada com sucesso!")
                            registrar_log(st.session_state.id_usuario, "SENHA", "Senha alterada")
                            st.session_state.trocando_senha = False
                            st.rerun()
                        else:
                            st.error("Senha atual incorreta!")
                
                with col2:
                    if st.form_submit_button("🔙 Voltar", use_container_width=True):
                        st.session_state.trocando_senha = False
                        st.rerun()
        
        elif escolha == "📊 Dashboard Estratégico":
            exibir_dashboard_admin()
        elif escolha == "📉 Desistências":
            if cargo_id == 1:
                exibir_dashboard_cancelamentos()
            elif cargo_id == 3:
                meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                           "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
                
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    mes_sel = st.selectbox("Mês", meses_pt, index=datetime.now().month - 1)
                    mes_num = meses_pt.index(mes_sel) + 1
                with col_f2:
                    ano_sel = st.selectbox("Ano", [2025, 2026], index=1)
                
                exibir_cancelamentos_regionais(
                    st.session_state.id_regional,
                    st.session_state.regional_nome,
                    mes_num, 
                    ano_sel
                )
        elif escolha == "👥 Gestão de Usuários":
            gerenciar_usuarios()
        elif escolha == "🎯 Metas Regionais":
            exibir_gestao_metas()
        elif escolha == "📚 Gestão de Treinamentos":
            st.header("📚 Painel do Gestor de Treinamentos")
            gerenciar_treinamentos_admin()
        elif escolha == "📚 Meus Treinamentos":
            exibir_tela_treinamentos()
        elif escolha == "🛡️ Visão de Supervisor":
            exibir_tela_supervisor(id_regional=st.session_state.id_regional)
        elif escolha == "💰 Minhas Vendas":
            exibir_tela_vendedor()
        elif escolha == "📑 Auditoria":
            exibir_tela_auditor()
        elif escolha == "🛠️ Painel Suporte":
            exibir_tela_suporte()
        elif escolha == "📊 Visão de Instalações Hubsoft":  
            exibir_visao_instalacoes_hubsoft()
        elif escolha == "🌐 Todas as Vendas Hubsoft":   
            exibir_todas_vendas_hubsoft()
        elif escolha == "ℹ️ Sem Acesso":
            st.warning("Seu perfil não tem acesso a nenhuma funcionalidade no momento.")
    
    except Exception as e:
        st.error(f"Erro ao carregar página: {str(e)}")
        import traceback
        with st.expander("Ver detalhes do erro"):
            st.code(traceback.format_exc())
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown(
        f"""
        <div style='text-align: center; color: #6C757D; font-size: 0.7rem; padding: 5px;'>
            © {datetime.now().year} PRO SALES - Gestão Profissional de Vendas
        </div>
        """, 
        unsafe_allow_html=True
    )