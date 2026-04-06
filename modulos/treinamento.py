import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import io
import base64
import plotly.express as px
from database.queries import (
    buscar_treinamentos, registrar_conclusao_treinamento, 
    buscar_meus_treinamentos_concluidos, salvar_novo_treinamento,
    buscar_relatorio_treinamentos, enviar_notificacao,
    buscar_historico_conclusoes, buscar_progresso_individual,
    get_db_cursor, registrar_log
)

# ============================================================================
# CONSTANTES E CONFIGURAÇÕES
# ============================================================================

# Categorias de treinamentos para Telecom
CATEGORIAS_TREINAMENTOS = {
    "Obrigatórios (Leis e Normas)": "⚖️",
    "Técnico (Redes e Infraestrutura)": "🔧",
    "Comercial e Vendas": "💰",
    "Atendimento ao Cliente": "📞",
    "Gestão e Liderança": "👔",
    "Segurança e Compliance": "🛡️",
    "Ferramentas e Sistemas": "💻"
}

# Modalidades de treinamento
MODALIDADES = ["EAD", "Presencial", "Híbrido"]

# Periodicidades
PERIODICIDADES = ["Mensal", "Trimestral", "Semestral", "Anual"]

# Áreas responsáveis
AREAS_RESPONSAVEIS = ["RH", "TI", "Comercial", "Operações", "Segurança do Trabalho", "Diretoria"]

TIPOS_USUARIO = {
    1: "Admin",
    2: "Vendedor",
    3: "Supervisor",
    4: "Auditor Financeiro",
    26: "SUPORTE TECNICO"
}

CARGO_PARA_ID = {v: k for k, v in TIPOS_USUARIO.items()}
CARGO_PARA_ID["Todos"] = 0

# ============================================================================
# FUNÇÃO PARA CARREGAR LOGO (MESMA DO APP.PY)
# ============================================================================

def carregar_logo_certificado():
    """Carrega a logo para o certificado usando a mesma lógica do App.py"""
    import os
    import base64
    from PIL import Image
    import io
    
    # Mesmos nomes de arquivo do App.py
    nomes_arquivo = [
        "MELL beacons.png",
        "logo.png",
        "assets/LOGO MELL.png",
        "assets/MELL beacons.png"
    ]
    
    # Mesmas pastas do App.py
    pastas = [".", "src", "./src", os.path.dirname(__file__), 
              os.path.join(os.path.dirname(__file__), "assets"),
              os.path.join(os.path.dirname(__file__), "..", "assets")]
    
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
        return None
    
    try:
        img = Image.open(arquivo_encontrado)
        
        # Redimensionar para largura máxima
        max_width = 200
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Converter para RGB se necessário
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        
        return base64.b64encode(buffer.read()).decode()
        
    except Exception as e:
        print(f"Erro ao carregar logo: {e}")
        return None

# Carregar a logo uma vez no módulo
LOGO_CERTIFICADO = carregar_logo_certificado()

# ============================================================================
# FUNÇÃO PARA VERIFICAR E CRIAR COLUNAS
# ============================================================================

def verificar_e_criar_colunas_treinamentos():
    """Verifica se as colunas necessárias existem e cria se não existirem"""
    try:
        with get_db_cursor() as cursor:
            # Verificar coluna obrigatorio
            cursor.execute("""
                SELECT COUNT(*) as existe FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'treinamentos' AND COLUMN_NAME = 'obrigatorio'
            """)
            if cursor.fetchone()['existe'] == 0:
                cursor.execute("""
                    ALTER TABLE treinamentos 
                    ADD COLUMN obrigatorio TINYINT DEFAULT 0 COMMENT 'Treinamento obrigatório por lei/norma' 
                    AFTER validade_meses
                """)
                print("✅ Coluna 'obrigatorio' criada")
            
            # Verificar coluna carga_horaria
            cursor.execute("""
                SELECT COUNT(*) as existe FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'treinamentos' AND COLUMN_NAME = 'carga_horaria'
            """)
            if cursor.fetchone()['existe'] == 0:
                cursor.execute("""
                    ALTER TABLE treinamentos 
                    ADD COLUMN carga_horaria INT DEFAULT 0 COMMENT 'Carga horária em horas' 
                    AFTER obrigatorio
                """)
                print("✅ Coluna 'carga_horaria' criada")
            
            # Verificar coluna modalidade
            cursor.execute("""
                SELECT COUNT(*) as existe FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'treinamentos' AND COLUMN_NAME = 'modalidade'
            """)
            if cursor.fetchone()['existe'] == 0:
                cursor.execute("""
                    ALTER TABLE treinamentos 
                    ADD COLUMN modalidade VARCHAR(20) DEFAULT 'EAD' 
                    COMMENT 'Modalidade do treinamento' AFTER carga_horaria
                """)
                print("✅ Coluna 'modalidade' criada")
            
            # Verificar coluna area_responsavel
            cursor.execute("""
                SELECT COUNT(*) as existe FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'treinamentos' AND COLUMN_NAME = 'area_responsavel'
            """)
            if cursor.fetchone()['existe'] == 0:
                cursor.execute("""
                    ALTER TABLE treinamentos 
                    ADD COLUMN area_responsavel VARCHAR(50) COMMENT 'Área responsável' 
                    AFTER modalidade
                """)
                print("✅ Coluna 'area_responsavel' criada")
            
            # Verificar coluna periodicidade
            cursor.execute("""
                SELECT COUNT(*) as existe FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'treinamentos' AND COLUMN_NAME = 'periodicidade'
            """)
            if cursor.fetchone()['existe'] == 0:
                cursor.execute("""
                    ALTER TABLE treinamentos 
                    ADD COLUMN periodicidade VARCHAR(20) DEFAULT 'Anual' 
                    COMMENT 'Periodicidade de reciclagem' AFTER area_responsavel
                """)
                print("✅ Coluna 'periodicidade' criada")
            
            # Verificar coluna instrutor
            cursor.execute("""
                SELECT COUNT(*) as existe FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'treinamentos' AND COLUMN_NAME = 'instrutor'
            """)
            if cursor.fetchone()['existe'] == 0:
                cursor.execute("""
                    ALTER TABLE treinamentos 
                    ADD COLUMN instrutor VARCHAR(100) COMMENT 'Nome do instrutor' 
                    AFTER periodicidade
                """)
                print("✅ Coluna 'instrutor' criada")
            
            # Verificar coluna publico_alvo
            cursor.execute("""
                SELECT COUNT(*) as existe FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'treinamentos' AND COLUMN_NAME = 'publico_alvo'
            """)
            if cursor.fetchone()['existe'] == 0:
                cursor.execute("""
                    ALTER TABLE treinamentos 
                    ADD COLUMN publico_alvo TEXT COMMENT 'Descrição do público-alvo' 
                    AFTER instrutor
                """)
                print("✅ Coluna 'publico_alvo' criada")
            
            # Verificar coluna data_vencimento na tabela treinamentos_concluidos
            cursor.execute("""
                SELECT COUNT(*) as existe FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'treinamentos_concluidos' AND COLUMN_NAME = 'data_vencimento'
            """)
            if cursor.fetchone()['existe'] == 0:
                cursor.execute("""
                    ALTER TABLE treinamentos_concluidos 
                    ADD COLUMN data_vencimento DATE COMMENT 'Data de vencimento do certificado' 
                    AFTER data_conclusao
                """)
                print("✅ Coluna 'data_vencimento' criada")
                
                # Atualizar registros existentes
                cursor.execute("""
                    UPDATE treinamentos_concluidos tc
                    JOIN treinamentos t ON tc.id_treinamento = t.id_treinamento
                    SET tc.data_vencimento = DATE_ADD(tc.data_conclusao, INTERVAL t.validade_meses MONTH)
                    WHERE tc.data_vencimento IS NULL AND t.validade_meses IS NOT NULL
                """)
                print("✅ Registros existentes atualizados com data_vencimento")
            
            # Criar índice para performance
            try:
                cursor.execute("""
                    CREATE INDEX idx_treinamentos_vencimento ON treinamentos_concluidos(data_vencimento)
                """)
                print("✅ Índice de vencimento criado")
            except:
                pass  # Índice já existe
                
            return True
            
    except Exception as e:
        print(f"⚠️ Erro ao verificar/criar colunas: {e}")
        return False

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def limpar_texto(texto):
    """Remove marcações Markdown do texto"""
    if not texto or not isinstance(texto, str):
        return texto
    replacements = {
        '**': '',
        '*': '',
        '__': '',
        '_': '',
        '`': '',
        '```': ''
    }
    for old, new in replacements.items():
        texto = texto.replace(old, new)
    return texto.strip()

def calcular_dias_para_vencimento(data_vencimento):
    """Calcula dias restantes para vencimento"""
    if not data_vencimento:
        return None
    hoje = datetime.now().date()
    if isinstance(data_vencimento, datetime):
        data_vencimento = data_vencimento.date()
    dias = (data_vencimento - hoje).days
    return dias

def gerar_certificado_html(titulo, nome_usuario, data_conclusao, validade_meses, 
                           instrutor=None, logo_base64=None, assinaturas=None, selo_base64=None):
    """Gera um certificado em HTML para download com logo no lugar do troféu"""
    from datetime import datetime
    import hashlib
    import base64
    
    data_validade = data_conclusao + timedelta(days=30*validade_meses)
    data_emissao = datetime.now()
    
    # HTML da logo principal (no lugar do troféu)
    logo_principal_html = ""
    if logo_base64:
        logo_principal_html = f"""
        <div class="logo-principal">
            <img src='data:image/png;base64,{logo_base64}' alt='Logo' style='max-height: 120px;'>
        </div>
        """
    else:
        # Se não tiver logo, mantém o troféu
        logo_principal_html = '<div class="selo">🏆</div>'
    
    # HTML do logo da empresa (canto superior)
    logo_cabecalho_html = ""
    if logo_base64:
        logo_cabecalho_html = f"""
        <div class="logo-certificado">
            <img src='data:image/png;base64,{logo_base64}' alt='Logo' style='max-height: 70px;'>
        </div>
        """
    
    # HTML do selo (canto direito)
    selo_html = ""
    if selo_base64:
        selo_html = f"""
        <div class="selo-empresa">
            <img src='data:image/png;base64,{selo_base64}' alt='Selo de Validade' style='max-height: 80px;'>
        </div>
        """
    
    # Gerar HTML das assinaturas
    assinaturas_html = ""
    if assinaturas and len(assinaturas) > 0:
        assinaturas_html = '<div class="assinaturas">'
        for assinatura in assinaturas:
            # Verificar se tem imagem da assinatura
            if assinatura.get('imagem_assinatura') and len(assinatura['imagem_assinatura']) > 0:
                # Converter imagem para base64 dentro do loop
                img_base64_local = base64.b64encode(assinatura['imagem_assinatura']).decode()
                assinaturas_html += f"""
                <div class="assinatura-item">
                    <img src="data:image/png;base64,{img_base64_local}" class="assinatura-imagem" alt="{assinatura['nome']}">
                    <div class="linha-assinatura"></div>
                    <div class="nome-assinante">{assinatura['nome']}</div>
                    <div class="cargo-assinante">{assinatura['cargo']}</div>
                </div>
                """
            else:
                # Assinatura sem imagem (apenas nome e cargo)
                assinaturas_html += f"""
                <div class="assinatura-item">
                    <div class="linha-assinatura"></div>
                    <div class="nome-assinante">{assinatura['nome']}</div>
                    <div class="cargo-assinante">{assinatura['cargo']}</div>
                </div>
                """
        assinaturas_html += '</div>'
    else:
        # Assinaturas padrão (em branco)
        assinaturas_html = """
        <div class="assinaturas">
            <div class="assinatura-item">
                <div class="linha-assinatura"></div>
                <div class="nome-assinante">_________________________</div>
                <div class="cargo-assinante">Coordenação</div>
            </div>
            <div class="assinatura-item">
                <div class="linha-assinatura"></div>
                <div class="nome-assinante">_________________________</div>
                <div class="cargo-assinante">Gerência</div>
            </div>
        </div>
        """
    
    # Gerar código único do certificado
    codigo_certificado = hashlib.md5(f"{nome_usuario}{titulo}{data_conclusao}{data_emissao}".encode()).hexdigest()[:12].upper()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Certificado - {titulo}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
            
            body {{
                font-family: 'Montserrat', 'Arial', sans-serif;
                margin: 0;
                padding: 40px;
                background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .certificado {{
                max-width: 1100px;
                margin: 0 auto;
                background: white;
                border: 2px solid #169fda;
                border-radius: 20px;
                padding: 50px 40px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0,0,0,0.15);
                position: relative;
                overflow: hidden;
            }}
            .certificado::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 8px;
                background: linear-gradient(90deg, #01384d, #169fda, #01384d);
            }}
            .header-certificado {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 20px;
                border-bottom: 2px solid #e9ecef;
            }}
            .logo-certificado {{
                flex: 1;
                text-align: left;
            }}
            .selo-empresa {{
                flex: 1;
                text-align: right;
            }}
            .logo-principal {{
                margin: 20px 0;
                text-align: center;
            }}
            .logo-principal img {{
                max-height: 120px;
                object-fit: contain;
            }}
            .selo {{
                margin: 20px 0;
                font-size: 64px;
            }}
            .titulo {{
                font-size: 32px;
                font-weight: 700;
                color: #01384d;
                margin-bottom: 30px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            .certificado-texto {{
                font-size: 18px;
                color: #495057;
                margin: 20px 0;
                line-height: 1.6;
            }}
            .nome {{
                font-size: 42px;
                font-weight: 700;
                background: linear-gradient(135deg, #01384d, #169fda);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 20px 0;
                padding: 10px 0;
            }}
            .curso {{
                font-size: 26px;
                font-weight: 600;
                color: #169fda;
                margin: 20px 0;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 10px;
            }}
            .detalhes {{
                margin: 30px 0;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 15px;
            }}
            .datas {{
                font-size: 14px;
                color: #6c757d;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #dee2e6;
            }}
            .assinaturas {{
                margin-top: 50px;
                padding-top: 30px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 60px;
            }}
            
            .assinatura-imagem {{
                max-height: 150px;
                max-width: 550px;
                margin-bottom: 15px;
                display: block;
                margin-left: auto;
                margin-right: auto;
                object-fit: contain;
            }}
            .linha-assinatura {{
                width: 220px;
                height: 2px;
                background: #333;
                margin: 15px auto;
                border-radius: 2px;
            }}
            .nome-assinante {{
                font-size: 18px;
                font-weight: 600;
                color: #2c3e50;
                margin-top: 10px;
            }}
            .cargo-assinante {{
                font-size: 14px;
                color: #7f8c8d;
                margin-top: 5px;
            }}
            .codigo {{
                font-size: 10px;
                color: #adb5bd;
                margin-top: 40px;
                font-family: monospace;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .validade {{
                background: #fff3cd;
                border: 1px solid #ffc107;
                border-radius: 8px;
                padding: 8px;
                margin: 10px 0;
                font-size: 12px;
                color: #856404;
            }}
            @media print {{
                body {{
                    background: white;
                    padding: 0;
                }}
                .certificado {{
                    box-shadow: none;
                    border: 1px solid #ddd;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="certificado">
            <div class="header-certificado">
                {logo_cabecalho_html}
                {selo_html}
            </div>
            
            <!-- LOGO NO LUGAR DO TROFÉU -->
            {logo_principal_html}
            
            <div class="titulo">CERTIFICADO DE CONCLUSÃO</div>
            
            <div class="certificado-texto">
                Certificamos que
            </div>
            
            <div class="nome">{nome_usuario}</div>
            
            <div class="certificado-texto">
                concluiu com êxito o treinamento
            </div>
            
            <div class="curso">{titulo}</div>
            
            <div class="detalhes">
                <div class="certificado-texto" style="margin: 0; font-size: 14px;">
                    Carga horária: {validade_meses * 4} horas
                </div>
                <div class="certificado-texto" style="margin: 0; font-size: 14px;">
                    Concluído em: {data_conclusao.strftime('%d/%m/%Y')}
                </div>
                <div class="validade">
                    ⚠️ Este certificado é válido até: {data_validade.strftime('%d/%m/%Y')}
                </div>
            </div>
            
            <div class="datas">
                <p>Emissão: {data_emissao.strftime('%d/%m/%Y %H:%M')}</p>
                <p>PROSALES - Mell Internet</p>
            </div>
            
            {assinaturas_html}
            
            <div class="codigo">
                <span>🔐 Código de Autenticidade: {codigo_certificado}</span>
                <span class="qr-code">✅ Certificado Digital</span>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def exibir_certificado(titulo, nome_usuario, data_conclusao, validade_meses):
    """Exibe botão para download do certificado com a logo do sistema - CORRIGIDO"""
    # Converter data_conclusao para date se for datetime
    from datetime import date
    
    if isinstance(data_conclusao, datetime):
        data_conclusao_date = data_conclusao.date()
    elif hasattr(data_conclusao, 'date'):
        data_conclusao_date = data_conclusao.date()
    else:
        data_conclusao_date = data_conclusao if isinstance(data_conclusao, date) else date.today()
    
    # Tentar importar as funções, se não existirem, usar valores padrão
    assinaturas = []
    selo_base64 = None
    
    try:
        from database.queries import buscar_assinaturas_certificados, buscar_selo_certificado
        
        # Carregar assinaturas e selo
        assinaturas = buscar_assinaturas_certificados()
        selo = buscar_selo_certificado()
        
        # Preparar selo base64
        if selo and selo.get('imagem'):
            selo_base64 = base64.b64encode(selo['imagem']).decode()
    except Exception as e:
        print(f"Erro ao carregar assinaturas/selo: {e}")
    
    # Usar a logo carregada no módulo
    logo_base64 = LOGO_CERTIFICADO
    
    html_certificado = gerar_certificado_html(
        titulo, nome_usuario, data_conclusao_date, validade_meses,
        logo_base64=logo_base64,
        assinaturas=assinaturas,
        selo_base64=selo_base64
    )
    
    b64 = base64.b64encode(html_certificado.encode()).decode()
    
    data_str = data_conclusao_date.strftime('%Y%m%d') if hasattr(data_conclusao_date, 'strftime') else ''
    nome_arquivo = f"certificado_{titulo.replace(' ', '_')}_{data_str}.html"
    
    href = f'<a href="data:text/html;base64,{b64}" download="{nome_arquivo}" style="text-decoration:none; display: inline-block; background: linear-gradient(135deg, #169fda, #0d7ab3); color: white; padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 500;">📜 Baixar Certificado</a>'
    st.markdown(href, unsafe_allow_html=True)
def verificar_treinamentos_vencendo(id_usuario):
    """Verifica treinamentos que vencem nos próximos 30 dias - CORRIGIDO"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    t.titulo,
                    t.carga_horaria,
                    tc.data_vencimento,
                    DATEDIFF(tc.data_vencimento, CURDATE()) as dias_restantes
                FROM treinamentos_concluidos tc
                JOIN treinamentos t ON tc.id_treinamento = t.id_treinamento
                WHERE tc.id_usuario = %s 
                    AND tc.status = 'concluido'
                    AND tc.data_vencimento IS NOT NULL
                    AND DATEDIFF(tc.data_vencimento, CURDATE()) <= 30
                    AND DATEDIFF(tc.data_vencimento, CURDATE()) > 0
                ORDER BY tc.data_vencimento ASC
            """, (id_usuario,))
            resultados = cursor.fetchall()
            
            # Converter datas para date se necessário
            for r in resultados:
                if r.get('data_vencimento') and hasattr(r['data_vencimento'], 'date'):
                    r['data_vencimento'] = r['data_vencimento'].date()
            return resultados
    except Exception as e:
        print(f"Erro ao verificar treinamentos vencendo: {e}")
        return []

def verificar_treinamentos_vencidos(id_usuario):
    """Verifica treinamentos que já venceram - CORRIGIDO"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    t.titulo,
                    t.carga_horaria,
                    tc.data_vencimento,
                    DATEDIFF(CURDATE(), tc.data_vencimento) as dias_atraso
                FROM treinamentos_concluidos tc
                JOIN treinamentos t ON tc.id_treinamento = t.id_treinamento
                WHERE tc.id_usuario = %s 
                    AND tc.status = 'concluido'
                    AND tc.data_vencimento IS NOT NULL
                    AND DATEDIFF(CURDATE(), tc.data_vencimento) > 0
                ORDER BY tc.data_vencimento ASC
            """, (id_usuario,))
            resultados = cursor.fetchall()
            
            # Converter datas para date se necessário
            for r in resultados:
                if r.get('data_vencimento') and hasattr(r['data_vencimento'], 'date'):
                    r['data_vencimento'] = r['data_vencimento'].date()
            return resultados
    except Exception as e:
        print(f"Erro ao verificar treinamentos vencidos: {e}")
        return []

def enviar_notificacao_treinamento(titulo_treinamento, cargo_destino, id_treinamento=None, 
                                    carga_horaria=None, modalidade=None):
    """Envia notificação para os usuários do cargo destino sobre novo treinamento"""
    try:
        mapa_notificacao = {
            0: "Todos",
            1: "Admins",
            2: "Vendedores",
            3: "Supervisores",
            4: "Auditores",
            26: "Suporte"
        }
        
        destinatario = mapa_notificacao.get(cargo_destino, "Todos")
        
        # Remove asteriscos do título
        titulo_limpo = limpar_texto(titulo_treinamento)
        
        # Se não recebeu carga_horaria e modalidade, busca no banco
        if (carga_horaria is None or modalidade is None) and id_treinamento:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    SELECT carga_horaria, modalidade 
                    FROM treinamentos 
                    WHERE id_treinamento = %s
                """, (id_treinamento,))
                treino = cursor.fetchone()
                if treino:
                    carga_horaria = treino.get('carga_horaria', 4)
                    modalidade = treino.get('modalidade', 'EAD')
        
        # Valores padrão
        carga_horaria = carga_horaria or 4
        modalidade = modalidade or 'EAD'
        
        # Título sem asteriscos e formatado
        titulo = f"📚 Novo Treinamento: {titulo_limpo}"
        
        # Mensagem formatada
        mensagem = f"""🎓 **{titulo_limpo}** foi publicado e está disponível para você!

📝 Acesse o Centro de Treinamentos para iniciar o curso.

⏱️ **Carga horária:** {carga_horaria} horas
🎓 **Modalidade:** {modalidade}

✅ Conclua e receba seu certificado!"""
        
        # Envia a notificação (sem id_usuario_destino para grupo)
        resultado = enviar_notificacao(titulo, mensagem, destinatario)
        print(f"📢 Notificação enviada para {destinatario}: {titulo_limpo} - Resultado: {resultado}")
        return resultado
    except Exception as e:
        print(f"Erro ao enviar notificação de treinamento: {e}")
        import traceback
        traceback.print_exc()
        return False

def enviar_lembretes_treinamentos_pendentes():
    """Envia lembretes para usuários com treinamentos pendentes (MANUAL)"""
    try:
        with get_db_cursor() as cursor:
            # Buscar usuários com treinamentos pendentes
            cursor.execute("""
                SELECT 
                    u.id_usuario,
                    u.nome_usuario,
                    t.id_treinamento,
                    t.titulo,
                    t.carga_horaria,
                    DATEDIFF(CURDATE(), t.data_cadastro) as dias_desde_lancamento
                FROM users u
                CROSS JOIN treinamentos t
                LEFT JOIN treinamentos_concluidos tc ON u.id_usuario = tc.id_usuario AND t.id_treinamento = tc.id_treinamento
                WHERE u.ativo = 1
                    AND tc.id_treinamento IS NULL
                    AND t.ativo = 1
                    AND (t.id_tipo_usuario_alvo = 0 OR t.id_tipo_usuario_alvo = u.id_tipo_usuario)
                ORDER BY u.id_usuario, dias_desde_lancamento DESC
            """)
            pendentes = cursor.fetchall()
            
            if not pendentes:
                return 0
            
            # Agrupar por usuário
            usuarios_pendentes = {}
            for p in pendentes:
                if p['id_usuario'] not in usuarios_pendentes:
                    usuarios_pendentes[p['id_usuario']] = {
                        'nome': p['nome_usuario'],
                        'treinamentos': []
                    }
                
                # Determinar prioridade baseado nos dias
                dias = p['dias_desde_lancamento']
                if dias >= 30:
                    prioridade = "🔴 ATRASADO"
                elif dias >= 15:
                    prioridade = "🟠 URGENTE"
                else:
                    prioridade = "🟡 PENDENTE"
                
                usuarios_pendentes[p['id_usuario']]['treinamentos'].append({
                    'titulo': p['titulo'],
                    'dias': dias,
                    'prioridade': prioridade,
                    'carga_horaria': p['carga_horaria']
                })
            
            # Enviar notificações
            total_notificacoes = 0
            for id_usuario, dados in usuarios_pendentes.items():
                # Verificar se tem treinamentos muito atrasados
                tem_atrasado = any(t['prioridade'] == '🔴 ATRASADO' for t in dados['treinamentos'])
                
                if tem_atrasado:
                    titulo = "🔴 ATENÇÃO: Treinamentos ATRASADOS!"
                    icone = "🔴"
                    mensagem_intro = f"⚠️ Você possui treinamentos ATRASADOS que precisam ser concluídos URGENTEMENTE:"
                else:
                    titulo = "📚 Lembrete: Treinamentos Pendentes"
                    icone = "📚"
                    mensagem_intro = f"Olá {dados['nome']}, você tem treinamentos pendentes:"
                
                # Montar lista de treinamentos
                lista_treinamentos = "\n".join([
                    f"   • **{t['titulo']}** - {t['prioridade']} (há {t['dias']} dias) - {t['carga_horaria']}h"
                    for t in dados['treinamentos'][:10]
                ])
                
                if len(dados['treinamentos']) > 10:
                    lista_treinamentos += f"\n   • ... e mais {len(dados['treinamentos']) - 10} treinamentos"
                
                mensagem = f"""{icone} {mensagem_intro}

{lista_treinamentos}

{'🔔 Acesse o Centro de Treinamentos e conclua seus treinamentos ATRASADOS IMEDIATAMENTE!' if tem_atrasado else '📝 Acesse o Centro de Treinamentos e conclua seus treinamentos pendentes!'}

📚 **Centro de Treinamentos PROSALES**
"""
                
                enviar_notificacao(titulo, mensagem, "individual", id_usuario)
                total_notificacoes += 1
                registrar_log(1, "SISTEMA", f"Lembrete manual enviado para {dados['nome']} - {len(dados['treinamentos'])} treinamentos")
            
            return total_notificacoes
            
    except Exception as e:
        print(f"Erro ao enviar lembretes: {e}")
        return 0

def enviar_alertas_vencimento_certificados():
    """Envia alertas para certificados vencidos e próximos do vencimento (MANUAL)"""
    try:
        with get_db_cursor() as cursor:
            # 1. Buscar certificados que JÁ VENCERAM
            cursor.execute("""
                SELECT 
                    u.id_usuario,
                    u.nome_usuario,
                    t.id_treinamento,
                    t.titulo,
                    tc.data_vencimento,
                    DATEDIFF(CURDATE(), tc.data_vencimento) as dias_atraso,
                    'VENCIDO' as tipo
                FROM treinamentos_concluidos tc
                JOIN users u ON tc.id_usuario = u.id_usuario
                JOIN treinamentos t ON tc.id_treinamento = t.id_treinamento
                WHERE tc.status = 'concluido'
                    AND tc.data_vencimento IS NOT NULL
                    AND DATEDIFF(CURDATE(), tc.data_vencimento) > 0
                    AND u.ativo = 1
            """)
            vencidos = cursor.fetchall()
            
            # 2. Buscar certificados que VENCEM NOS PRÓXIMOS 7 DIAS
            cursor.execute("""
                SELECT 
                    u.id_usuario,
                    u.nome_usuario,
                    t.id_treinamento,
                    t.titulo,
                    tc.data_vencimento,
                    DATEDIFF(tc.data_vencimento, CURDATE()) as dias_restantes,
                    'URGENTE' as tipo
                FROM treinamentos_concluidos tc
                JOIN users u ON tc.id_usuario = u.id_usuario
                JOIN treinamentos t ON tc.id_treinamento = t.id_treinamento
                WHERE tc.status = 'concluido'
                    AND tc.data_vencimento IS NOT NULL
                    AND DATEDIFF(tc.data_vencimento, CURDATE()) BETWEEN 1 AND 7
                    AND u.ativo = 1
                ORDER BY dias_restantes ASC
            """)
            urgentes = cursor.fetchall()
            
            # 3. Buscar certificados que VENCEM NOS PRÓXIMOS 30 DIAS
            cursor.execute("""
                SELECT 
                    u.id_usuario,
                    u.nome_usuario,
                    t.id_treinamento,
                    t.titulo,
                    tc.data_vencimento,
                    DATEDIFF(tc.data_vencimento, CURDATE()) as dias_restantes,
                    'AVISO' as tipo
                FROM treinamentos_concluidos tc
                JOIN users u ON tc.id_usuario = u.id_usuario
                JOIN treinamentos t ON tc.id_treinamento = t.id_treinamento
                WHERE tc.status = 'concluido'
                    AND tc.data_vencimento IS NOT NULL
                    AND DATEDIFF(tc.data_vencimento, CURDATE()) BETWEEN 8 AND 30
                    AND u.ativo = 1
                ORDER BY dias_restantes ASC
            """)
            avisos = cursor.fetchall()
            
            todos_alertas = list(vencidos) + list(urgentes) + list(avisos)
            
            if not todos_alertas:
                return 0
            
            # Agrupar por usuário
            usuarios_alertas = {}
            for alerta in todos_alertas:
                if alerta['id_usuario'] not in usuarios_alertas:
                    usuarios_alertas[alerta['id_usuario']] = {
                        'nome': alerta['nome_usuario'],
                        'certificados': []
                    }
                
                if alerta['tipo'] == 'VENCIDO':
                    dias = alerta['dias_atraso']
                    texto = f"🔴 VENCIDO HÁ {dias} DIAS!"
                elif alerta['tipo'] == 'URGENTE':
                    dias = alerta['dias_restantes']
                    texto = f"🟠 VENCE EM {dias} DIAS! (URGENTE)"
                else:
                    dias = alerta['dias_restantes']
                    texto = f"🟡 VENCE EM {dias} DIAS"
                
                usuarios_alertas[alerta['id_usuario']]['certificados'].append({
                    'titulo': alerta['titulo'],
                    'texto': texto,
                    'tipo': alerta['tipo'],
                    'data_vencimento': alerta['data_vencimento']
                })
            
            # Enviar notificações
            total_notificacoes = 0
            for id_usuario, dados in usuarios_alertas.items():
                tem_vencido = any(c['tipo'] == 'VENCIDO' for c in dados['certificados'])
                tem_urgente = any(c['tipo'] == 'URGENTE' for c in dados['certificados'])
                
                if tem_vencido:
                    titulo = "🔴 URGENTÍSSIMO: Certificados VENCIDOS!"
                    icone = "🔴"
                    mensagem_intro = "⚠️ ATENÇÃO! Seus certificados estão VENCIDOS e precisam ser reciclados IMEDIATAMENTE:"
                elif tem_urgente:
                    titulo = "🔴 URGENTE: Certificados Próximos do Vencimento!"
                    icone = "🔴"
                    mensagem_intro = "⚠️ Seus certificados vencerão em breve. Recicle-os o quanto antes:"
                else:
                    titulo = "⚠️ Atenção: Certificados Próximos do Vencimento"
                    icone = "⚠️"
                    mensagem_intro = "📢 Seus certificados estão próximos do vencimento:"
                
                lista_certificados = "\n".join([
                    f"   • **{c['titulo']}** - {c['texto']} (Vencimento: {c['data_vencimento'].strftime('%d/%m/%Y') if c['data_vencimento'] else 'N/A'})"
                    for c in dados['certificados']
                ])
                
                mensagem = f"""{icone} Olá {dados['nome']}!

{mensagem_intro}

{lista_certificados}

{'🔔 Acesse o Centro de Treinamentos e realize a reciclagem IMEDIATAMENTE!' if tem_vencido else '🎓 Acesse o Centro de Treinamentos e realize a reciclagem antes do vencimento!'}

📚 **Centro de Treinamentos PROSALES**
"""
                
                enviar_notificacao(titulo, mensagem, "individual", id_usuario)
                total_notificacoes += 1
                registrar_log(1, "SISTEMA", f"Alerta manual de vencimento enviado para {dados['nome']} - {len(dados['certificados'])} certificados")
            
            return total_notificacoes
            
    except Exception as e:
        print(f"Erro ao enviar alertas de vencimento: {e}")
        return 0

def exibir_metricas_progresso(df, coluna_agrupamento, titulo):
    """Cria uma lista de barras de progresso para cada categoria"""
    st.markdown(f"#### 📈 Progresso por {titulo}")
    
    contagem = df[coluna_agrupamento].value_counts()
    max_valor = contagem.max() if not contagem.empty else 1
    
    for nome, valor in contagem.items():
        percentual_relativo = valor / max_valor
        col_nome, col_bar = st.columns([1, 3])
        with col_nome:
            st.write(f"**{nome}**")
        with col_bar:
            st.progress(percentual_relativo, text=f"{valor} conclusões")

def processar_treinamentos_lista(treinos_brutos):
    """Processa lista de treinamentos com novos campos - CORRIGIDO"""
    if not treinos_brutos:
        return []
    
    processados = []
    for t in treinos_brutos:
        if isinstance(t, dict):
            processados.append({
                'id_treinamento': t.get('id_treinamento'),
                'titulo': limpar_texto(t.get('titulo')),
                'descricao': t.get('descricao'),
                'categoria': t.get('categoria', 'Geral'),
                'data_cadastro': t.get('data_cadastro'),
                'cargo_destino': t.get('id_tipo_usuario_alvo', 0),
                'validade_meses': t.get('validade_meses', 12),
                'url_video': t.get('url_video'),
                'url_documento': t.get('url_documento'),
                'obrigatorio': t.get('obrigatorio', 0),
                'carga_horaria': t.get('carga_horaria', 0),  # CORREÇÃO: campo garantido
                'modalidade': t.get('modalidade', 'EAD'),
                'area_responsavel': t.get('area_responsavel', ''),
                'periodicidade': t.get('periodicidade', 'Anual'),
                'instrutor': t.get('instrutor', ''),
                'publico_alvo': t.get('publico_alvo', '')
            })
        else:
            # Para compatibilidade com tuplas (agora com mais campos)
            processados.append({
                'id_treinamento': t[0] if len(t) > 0 else None,
                'titulo': limpar_texto(t[1]) if len(t) > 1 else '',
                'descricao': t[2] if len(t) > 2 else '',
                'categoria': t[3] if len(t) > 3 else 'Geral',
                'data_cadastro': t[4] if len(t) > 4 else None,
                'cargo_destino': t[5] if len(t) > 5 else 0,
                'validade_meses': t[6] if len(t) > 6 else 12,
                'url_video': t[7] if len(t) > 7 else None,
                'url_documento': t[8] if len(t) > 8 else None,
                'obrigatorio': t[9] if len(t) > 9 else 0,
                'carga_horaria': t[10] if len(t) > 10 else 0,
                'modalidade': t[11] if len(t) > 11 else 'EAD',
                'area_responsavel': t[12] if len(t) > 12 else '',
                'periodicidade': t[13] if len(t) > 13 else 'Anual',
                'instrutor': t[14] if len(t) > 14 else '',
                'publico_alvo': t[15] if len(t) > 15 else ''
            })
    return processados

# COMPONENTES DE INTERFACE
def exibir_alertas_vencimento(id_usuario):
    """Exibe alertas de treinamentos próximos ao vencimento e já vencidos - CORRIGIDO"""
    treinos_vencendo = verificar_treinamentos_vencendo(id_usuario)
    treinos_vencidos = verificar_treinamentos_vencidos(id_usuario)
    
    if treinos_vencidos:
        st.error("🔴 **ATENÇÃO! Treinamentos VENCIDOS:**")
        for t in treinos_vencidos:
            dias = t['dias_atraso']
            # CORREÇÃO: Mostrar carga horária se disponível
            carga_info = f" - {t.get('carga_horaria', 0)}h" if t.get('carga_horaria') else ""
            st.error(f"🔴 **{t['titulo']}**{carga_info} - Vencido há {dias} dias! (RECICLAGEM OBRIGATÓRIA)")
        st.divider()
    
    if treinos_vencendo:
        st.warning("⚠️ **Atenção! Treinamentos próximos ao vencimento:**")
        for t in treinos_vencendo:
            dias = t['dias_restantes']
            # CORREÇÃO: Mostrar carga horária se disponível
            carga_info = f" - {t.get('carga_horaria', 0)}h" if t.get('carga_horaria') else ""
            if dias <= 7:
                st.error(f"🔴 **{t['titulo']}**{carga_info} - Vence em {dias} dias! (URGENTE)")
            elif dias <= 15:
                st.warning(f"🟡 **{t['titulo']}**{carga_info} - Vence em {dias} dias")
            else:
                st.info(f"🔵 **{t['titulo']}**{carga_info} - Vence em {dias} dias")
        st.divider()


def exibir_progresso_individual(df_progresso):
    """Exibe progresso individual com layout melhorado"""
    st.subheader("👥 Monitoramento de Engajamento Individual")
    
    total_users = len(df_progresso)
    ativos = len(df_progresso[df_progresso['Total_Concluidos'] > 0])
    
    # Cards de métricas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total Colaboradores", total_users)
    col2.metric("🎓 Colaboradores Ativos", ativos)
    col3.metric("📊 Taxa de Engajamento", f"{(ativos/total_users)*100:.1f}%" if total_users > 0 else "0%")
    
    # Média de treinamentos por usuário
    media_treinos = df_progresso['Total_Concluidos'].mean()
    col4.metric("📚 Média por Colaborador", f"{media_treinos:.1f} treinamentos")
    
    st.divider()
    
    # Filtros
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cidades = st.multiselect("🏙️ Filtrar por Cidade", options=sorted(df_progresso['Cidade'].dropna().unique()))
    with col_f2:
        cargos = st.multiselect("👔 Filtrar por Cargo", options=sorted(df_progresso['Cargo'].dropna().unique()))

    df_filtrado = df_progresso.copy()
    if cidades: df_filtrado = df_filtrado[df_filtrado['Cidade'].isin(cidades)]
    if cargos: df_filtrado = df_filtrado[df_filtrado['Cargo'].isin(cargos)]
    
    # Tabela estilizada
    st.markdown("### 📋 Detalhamento por Colaborador")
    styled_df = df_filtrado.style.background_gradient(subset=['Total_Concluidos'], cmap='YlOrRd')
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Gráfico de distribuição
    st.markdown("### 📊 Distribuição de Conclusões")
    df_top = df_filtrado.nlargest(10, 'Total_Concluidos')[['nome_usuario', 'Total_Concluidos']]
    if not df_top.empty:
        fig = px.bar(df_top, x='nome_usuario', y='Total_Concluidos', 
                     title="Top 10 Colaboradores por Conclusões",
                     color='Total_Concluidos', color_continuous_scale='Viridis')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

def exibir_aba_treinamentos():
    """Exibe treinamentos para usuário comum - CORRIGIDO COM TRATAMENTO DE DATAS"""
    st.subheader("📖 Meus Treinamentos")
    st.caption("🎯 Complete os treinamentos e conquiste seus certificados!")
    
    id_usuario = st.session_state.id_usuario
    id_tipo = st.session_state.get('cargo_id', 0)
    
    # Verificar treinamentos vencidos e vencendo
    exibir_alertas_vencimento(id_usuario)
    
    treinos = buscar_treinamentos(id_tipo)
    treinos_p = processar_treinamentos_lista(treinos)
    concluidos = buscar_meus_treinamentos_concluidos(id_usuario)

    if not treinos_p:
        st.info("📭 Nenhum treinamento disponível para o seu cargo no momento.")
        return
    
    # Estatísticas do usuário
    total_treinos = len(treinos_p)
    total_concluidos = len([t for t in treinos_p if t['id_treinamento'] in concluidos])
    percentual = (total_concluidos / total_treinos * 100) if total_treinos > 0 else 0
    obrigatorios = len([t for t in treinos_p if t.get('obrigatorio', 0) == 1])
    obrigatorios_concluidos = len([t for t in treinos_p if t.get('obrigatorio', 0) == 1 and t['id_treinamento'] in concluidos])
    
    # Cards de métricas
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📚 Total", total_treinos)
    col2.metric("✅ Concluídos", total_concluidos)
    col3.metric("⏳ Pendentes", total_treinos - total_concluidos)
    col4.metric("📊 Progresso", f"{percentual:.1f}%")
    col5.metric("⚖️ Obrigatórios", f"{obrigatorios_concluidos}/{obrigatorios}")
    
    if percentual > 0:
        st.progress(percentual / 100, text=f"Progresso geral: {percentual:.1f}%")
    
    st.divider()
    
    # Filtros
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        categorias = list(set([t['categoria'] for t in treinos_p]))
        filtro_cat = st.selectbox("🔍 Categoria", ["Todas"] + categorias)
    with col_f2:
        filtro_status = st.selectbox("📌 Status", ["Todos", "Concluídos", "Pendentes", "Obrigatórios"])
    with col_f3:
        filtro_modalidade = st.selectbox("🎓 Modalidade", ["Todas"] + MODALIDADES)
    with col_f4:
        filtro_periodicidade = st.selectbox("🔄 Periodicidade", ["Todas"] + PERIODICIDADES)
    
    # Lista de treinamentos
    for t in treinos_p:
        # Aplicar filtros
        if filtro_cat != "Todas" and t['categoria'] != filtro_cat:
            continue
        if filtro_status == "Concluídos" and t['id_treinamento'] not in concluidos:
            continue
        if filtro_status == "Pendentes" and t['id_treinamento'] in concluidos:
            continue
        if filtro_status == "Obrigatórios" and t.get('obrigatorio', 0) != 1:
            continue
        if filtro_modalidade != "Todas" and t.get('modalidade', 'EAD') != filtro_modalidade:
            continue
        if filtro_periodicidade != "Todas" and t.get('periodicidade', 'Anual') != filtro_periodicidade:
            continue
            
        fez = t['id_treinamento'] in concluidos
        status_icon = "✅" if fez else "⏳"
        obrigatorio_badge = "🔴 OBRIGATÓRIO" if t.get('obrigatorio', 0) == 1 else ""
        
        carga_horaria = t.get('carga_horaria', 0)
        carga_horaria_texto = f"⏱️ **Carga Horária:** {carga_horaria} horas" if carga_horaria > 0 else "⏱️ **Carga Horária:** Não informada"
        
        with st.expander(f"{status_icon} {t['titulo']} {obrigatorio_badge}", expanded=not fez):
            # Layout em colunas melhorado
            col_info1, col_info2, col_info3 = st.columns([2.5, 2.5, 1.5])
            
            with col_info1:
                st.markdown("**📅 Informações**")
                # Converter data para string de forma segura
                if t['data_cadastro']:
                    if hasattr(t['data_cadastro'], 'strftime'):
                        data_str = t['data_cadastro'].strftime('%d/%m/%Y')
                    else:
                        data_str = str(t['data_cadastro'])
                else:
                    data_str = "Não informada"
                    
                st.markdown(f"🗓️ **Lançamento:** {data_str}")
                st.markdown(f"🏷️ **Categoria:** `{t['categoria']}`")
                st.markdown(f"⏱️ **Validade:** {t['validade_meses']} meses")
                st.markdown(carga_horaria_texto)
                st.markdown(f"🎓 **Modalidade:** {t.get('modalidade', 'EAD')}")
                st.markdown(f"🔄 **Periodicidade:** {t.get('periodicidade', 'Anual')}")
                
                if t.get('instrutor') and t['instrutor'].strip():
                    st.markdown(f"👨‍🏫 **Instrutor:** {t['instrutor']}")
                
                if t.get('area_responsavel') and t['area_responsavel'].strip():
                    st.markdown(f"📌 **Área Responsável:** {t['area_responsavel']}")
            
            with col_info2:
                st.markdown("**📋 Descrição**")
                st.markdown(f"{t['descricao']}")
                
                if t.get('publico_alvo') and t['publico_alvo'].strip():
                    st.markdown("**🎯 Público-Alvo:**")
                    st.markdown(f"{t['publico_alvo']}")
                
                if t.get('url_documento'):
                    st.markdown("**📂 Material:**")
                    st.link_button("📄 Acessar Material", t['url_documento'], use_container_width=True)
            
            with col_info3:
                st.markdown("**👤 Status**")
                if fez:
                    data_conclusao = concluidos.get(t['id_treinamento'], '')
                    if data_conclusao:
                        # CORREÇÃO: Converter para date se for datetime
                        if hasattr(data_conclusao, 'date'):
                            data_conclusao_date = data_conclusao.date()
                        elif isinstance(data_conclusao, datetime):
                            data_conclusao_date = data_conclusao.date()
                        else:
                            data_conclusao_date = data_conclusao if hasattr(data_conclusao, 'strftime') else None
                        
                        if data_conclusao_date:
                            data_str = data_conclusao_date.strftime('%d/%m/%Y') if hasattr(data_conclusao_date, 'strftime') else str(data_conclusao_date)
                            st.success(f"✅ Concluído")
                            st.caption(f"📅 {data_str}")
                            
                            # CORREÇÃO: Calcular vencimento com tipos compatíveis
                            try:
                                from datetime import date
                                # Converter para date se for datetime
                                if isinstance(data_conclusao, datetime):
                                    data_conclusao_dt = data_conclusao.date()
                                else:
                                    data_conclusao_dt = data_conclusao if hasattr(data_conclusao, 'date') else data_conclusao
                                
                                # Calcular data de vencimento
                                if isinstance(data_conclusao_dt, date):
                                    data_vencimento = data_conclusao_dt + timedelta(days=30 * t['validade_meses'])
                                    dias_restantes = (data_vencimento - date.today()).days
                                    
                                    if dias_restantes > 0:
                                        if dias_restantes <= 30:
                                            st.warning(f"⚠️ Vence em {dias_restantes} dias")
                                        else:
                                            st.caption(f"📅 Vence em: {data_vencimento.strftime('%d/%m/%Y')}")
                                    else:
                                        st.error(f"🔴 VENCIDO há {abs(dias_restantes)} dias!")
                            except Exception as e:
                                print(f"Erro ao calcular vencimento: {e}")
                                st.caption(f"📅 Validade: {t['validade_meses']} meses")
                        
                        if st.button(f"📜 Baixar Certificado", key=f"cert_{t['id_treinamento']}", use_container_width=True):
                            # Usar a data correta para o certificado
                            data_cert = data_conclusao_date if data_conclusao_date else data_conclusao
                            exibir_certificado(t['titulo'], st.session_state.user_nome, data_cert, t['validade_meses'])
                    else:
                        st.success("✅ Concluído")
                else:
                    st.warning("⏳ Pendente")
                    # Mostrar dias desde lançamento
                    if t.get('data_cadastro'):
                        try:
                            if hasattr(t['data_cadastro'], 'date'):
                                data_cadastro_date = t['data_cadastro'].date()
                            elif isinstance(t['data_cadastro'], datetime):
                                data_cadastro_date = t['data_cadastro'].date()
                            else:
                                data_cadastro_date = t['data_cadastro']
                            
                            if isinstance(data_cadastro_date, date):
                                dias_desde = (date.today() - data_cadastro_date).days
                                if dias_desde > 15:
                                    st.error(f"🔴 Atrasado há {dias_desde} dias")
                                elif dias_desde > 7:
                                    st.warning(f"🟡 Pendente há {dias_desde} dias")
                                else:
                                    st.info(f"📅 Há {dias_desde} dias")
                        except Exception as e:
                            pass
                    
                    if carga_horaria > 0:
                        st.caption(f"⏱️ Duração: {carga_horaria} horas")
            
            st.divider()
            
            # Material de apoio - Vídeo
            if t.get('url_video'):
                st.markdown("**📺 Material em Vídeo**")
                try:
                    url = t['url_video']
                    if 'youtube.com/watch?v=' in url:
                        video_id = url.split('v=')[1].split('&')[0]
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
                    elif 'youtu.be/' in url:
                        video_id = url.split('/')[-1]
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
                    else:
                        st.link_button("▶️ Assistir Vídeo", url, use_container_width=True)
                except:
                    st.link_button("▶️ Assistir Vídeo", t['url_video'], use_container_width=True)
            
            # Botão de conclusão
            if not fez:
                st.divider()
                col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                with col_btn2:
                    if st.button(f"✅ Marcar como Concluído", key=f"btn_{t['id_treinamento']}", use_container_width=True, type="primary"):
                        if registrar_conclusao_treinamento(id_usuario, t['id_treinamento'], t['validade_meses']):
                            st.success("✅ Conclusão registrada com sucesso!")
                            registrar_log(id_usuario, "TREINAMENTO", f"Concluiu: {t['titulo']}")
                            
                            # Enviar notificação de conclusão
                            try:
                                from database.queries import enviar_notificacao
                                enviar_notificacao(
                                    f"🎉 Parabéns!",
                                    f"Você concluiu o treinamento **{t['titulo']}** com sucesso!\n\n📜 Seu certificado já está disponível para download.\n\n⏱️ Carga horária: {carga_horaria} horas\n🎓 Modalidade: {t.get('modalidade', 'EAD')}",
                                    "individual",
                                    id_usuario
                                )
                            except:
                                pass
                            
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Erro ao registrar conclusão. Tente novamente.")

# PAINEL ADMINISTRATIVO
def gerenciar_treinamentos_admin():
    """Painel administrativo com layout melhorado e novos campos"""
    st.header("🎯 Gestão de Treinamentos")
    st.caption("Gerencie, publique e acompanhe o progresso dos treinamentos")
    
    tab_hist, tab_perf, tab_novo, tab_progresso, tab_compliance = st.tabs([
        "📊 Histórico", "🏆 Performance", "➕ Novo Treinamento", "👥 Progresso Individual", "⚖️ Compliance"
    ])

    dados_brutos = buscar_historico_conclusoes()

    with tab_hist:
        st.subheader("📈 Visão Geral de Conclusões")
        
        if dados_brutos:
            df_hist = pd.DataFrame(dados_brutos)
            
            # Métricas
            total_conclusoes = len(df_hist)
            treinos_unicos = df_hist['treinamento'].nunique() if 'treinamento' in df_hist.columns else 0
            regionais_atendidas = df_hist['regional'].nunique() if 'regional' in df_hist.columns else 0
            usuarios_ativos = df_hist['usuario'].nunique() if 'usuario' in df_hist.columns else 0
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📚 Total Conclusões", total_conclusoes)
            col2.metric("🎓 Cursos Realizados", treinos_unicos)
            col3.metric("🌎 Regionais Ativas", regionais_atendidas)
            col4.metric("👥 Usuários Ativos", usuarios_ativos)
            
            st.divider()
            
            # Gráfico de evolução temporal
            if 'data_conclusao' in df_hist.columns:
                st.markdown("#### 📈 Evolução Temporal")
                df_hist['data_conclusao'] = pd.to_datetime(df_hist['data_conclusao'])
                evolucao = df_hist.groupby(df_hist['data_conclusao'].dt.date).size().reset_index(name='quantidade')
                evolucao.columns = ['Data', 'Conclusões']
                
                fig = px.line(evolucao, x='Data', y='Conclusões', title="Conclusões por Dia",
                              markers=True, line_shape='spline')
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.markdown("#### 📋 Detalhamento do Histórico")
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
        else:
            st.info("📭 Nenhuma conclusão registrada ainda.")

    with tab_perf:
        st.subheader("🏆 Performance dos Treinamentos")
        
        if dados_brutos:
            df_perf = pd.DataFrame(dados_brutos)
            
            # Top treinamentos
            if 'treinamento' in df_perf.columns:
                st.markdown("#### 🎯 Top Treinamentos")
                top_treinos = df_perf['treinamento'].value_counts().head(10).reset_index()
                top_treinos.columns = ['Treinamento', 'Conclusões']
                
                fig = px.bar(top_treinos, x='Treinamento', y='Conclusões', 
                            title="Top 10 Treinamentos por Conclusões",
                            color='Conclusões', color_continuous_scale='Viridis')
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            col_reg, col_treino = st.columns(2)
            with col_reg:
                if 'regional' in df_perf.columns:
                    exibir_metricas_progresso(df_perf, 'regional', "Regionais")
            with col_treino:
                if 'treinamento' in df_perf.columns:
                    exibir_metricas_progresso(df_perf, 'treinamento', "Treinamentos")
        else:
            st.info("📭 Sem dados de performance para exibir.")

    with tab_novo:
        st.subheader("➕ Publicar Novo Treinamento")
        st.caption("Preencha os dados abaixo para criar um novo treinamento")
        
        with st.form("form_novo_treinamento", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                titulo = st.text_input("📝 Título do Treinamento *", placeholder="Ex: LGPD - Lei Geral de Proteção de Dados")
                desc = st.text_area("📄 Descrição/Objetivo *", placeholder="Descreva o conteúdo e objetivos do treinamento", height=150)
                
                # Categoria com ícones
                categoria_options = list(CATEGORIAS_TREINAMENTOS.keys())
                cat_selecionada = st.selectbox("🏷️ Categoria", categoria_options)
                icone_categoria = CATEGORIAS_TREINAMENTOS.get(cat_selecionada, "📚")
                st.caption(f"{icone_categoria} {cat_selecionada}")
                
                obrigatorio = st.checkbox("⚖️ Treinamento Obrigatório (por lei ou norma)")
                carga_horaria = st.number_input("⏰ Carga Horária (horas)", min_value=1, value=4)
            
            with col2:
                alvo = st.selectbox("👥 Público-Alvo", list(CARGO_PARA_ID.keys()))
                modalidade = st.selectbox("🎓 Modalidade", MODALIDADES)
                area_responsavel = st.selectbox("📌 Área Responsável", AREAS_RESPONSAVEIS)
                periodicidade = st.selectbox("🔄 Periodicidade", PERIODICIDADES)
                val = st.number_input("⏱️ Validade do Certificado (Meses)", min_value=1, value=12)
                instrutor = st.text_input("👨‍🏫 Instrutor", placeholder="Nome do instrutor responsável")
                publico_alvo = st.text_area("🎯 Público-Alvo Detalhado", placeholder="Descreva o público-alvo específico", height=80)
                url_v = st.text_input("📹 URL do Vídeo", placeholder="https://youtube.com/...")
                url_d = st.text_input("📂 URL do Documento", placeholder="https://drive.google.com/...")
            
            st.divider()
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
            with col_btn2:
                enviar = st.form_submit_button("🚀 Publicar Treinamento", use_container_width=True, type="primary")
            
            if enviar:
                if not titulo or not desc:
                    st.error("❌ Preencha o Título e a Descrição!")
                else:
                    with st.spinner("Publicando treinamento..."):
                        titulo_limpo = limpar_texto(titulo)
                        
                        sucesso = salvar_novo_treinamento_completo(
                            titulo_limpo, desc, url_v, cat_selecionada, url_d, 
                            CARGO_PARA_ID[alvo], val, obrigatorio, carga_horaria,
                            modalidade, area_responsavel, periodicidade, instrutor, publico_alvo
                        )
                        if sucesso:
                            # Envia notificação para os destinatários
                            enviar_notificacao_treinamento(titulo_limpo, CARGO_PARA_ID[alvo])
                            registrar_log(st.session_state.id_usuario, "TREINAMENTO", 
                                        f"Publicou: {titulo_limpo} para {alvo}")
                            
                            st.success(f"✅ Treinamento '{titulo_limpo}' publicado com sucesso!")
                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Erro ao salvar no banco de dados.")

    with tab_progresso:
        st.subheader("👥 Acompanhamento Individual")
        
        dados_p = buscar_progresso_individual()
        if dados_p:
            exibir_progresso_individual(pd.DataFrame(dados_p))
        else:
            st.info("📭 Nenhum dado de progresso individual encontrado.")
    
    with tab_compliance:
        st.subheader("⚖️ Relatório de Compliance")
        st.caption("Acompanhamento de treinamentos obrigatórios por lei e normas regulatórias")
        
        # Botões de notificação em massa (MANUAIS)
        st.markdown("### 📢 Ações em Massa")
        st.info("💡 Clique nos botões abaixo para enviar notificações manualmente")
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("📢 Enviar Lembretes Pendentes", use_container_width=True, type="secondary"):
                with st.spinner("Enviando lembretes..."):
                    qtd = enviar_lembretes_treinamentos_pendentes()
                    if qtd > 0:
                        st.success(f"✅ {qtd} notificações de lembrete enviadas!")
                    else:
                        st.info("📭 Nenhum treinamento pendente encontrado.")
                    time.sleep(2)
                    st.rerun()
        
        with col_btn2:
            if st.button("⚠️ Alertas de Vencimento", use_container_width=True, type="secondary"):
                with st.spinner("Enviando alertas..."):
                    qtd = enviar_alertas_vencimento_certificados()
                    if qtd > 0:
                        st.success(f"✅ {qtd} alertas de vencimento enviados!")
                    else:
                        st.info("📭 Nenhum certificado próximo do vencimento ou vencido encontrado.")
                    time.sleep(2)
                    st.rerun()
        
        with col_btn3:
            if st.button("📊 Relatório de Pendências", use_container_width=True, type="secondary"):
                with st.spinner("Gerando relatório..."):
                    with get_db_cursor() as cursor:
                        cursor.execute("""
                            SELECT 
                                t.titulo,
                                COUNT(DISTINCT u.id_usuario) as total_usuarios,
                                COUNT(DISTINCT tc.id_usuario) as concluintes,
                                (COUNT(DISTINCT u.id_usuario) - COUNT(DISTINCT tc.id_usuario)) as pendentes
                            FROM treinamentos t
                            CROSS JOIN users u
                            LEFT JOIN treinamentos_concluidos tc ON t.id_treinamento = tc.id_treinamento AND u.id_usuario = tc.id_usuario
                            WHERE u.ativo = 1
                                AND (t.id_tipo_usuario_alvo = 0 OR t.id_tipo_usuario_alvo = u.id_tipo_usuario)
                            GROUP BY t.id_treinamento
                            HAVING pendentes > 0
                            ORDER BY pendentes DESC
                        """)
                        dados = cursor.fetchall()
                        
                        if dados:
                            df = pd.DataFrame(dados)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                            
                            # Botão para exportar
                            csv = df.to_csv(index=False, encoding='utf-8-sig', sep=';')
                            st.download_button(
                                "📥 Exportar Relatório de Pendências",
                                csv,
                                f"relatorio_pendencias_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                "text/csv"
                            )
                        else:
                            st.info("🎉 Nenhum treinamento pendente!")
        st.divider()
        
        with get_db_cursor() as cursor:
            # Buscar treinamentos obrigatórios com verificação de colunas
            cursor.execute("""
                SELECT 
                    t.id_treinamento,
                    t.titulo,
                    t.categoria,
                    t.descricao,
                    COALESCE(t.obrigatorio, 0) as obrigatorio,
                    COALESCE(t.periodicidade, 'Anual') as periodicidade,
                    t.carga_horaria,
                    t.modalidade,
                    t.validade_meses,
                    t.data_cadastro,
                    COUNT(DISTINCT tc.id_usuario) as total_concluidos,
                    (SELECT COUNT(*) FROM users WHERE ativo = 1) as total_usuarios
                FROM treinamentos t
                LEFT JOIN treinamentos_concluidos tc ON t.id_treinamento = tc.id_treinamento
                WHERE COALESCE(t.obrigatorio, 0) = 1
                GROUP BY t.id_treinamento
                ORDER BY t.categoria, t.titulo
            """)
            obrigatorios = cursor.fetchall()
            
            if obrigatorios:
                st.markdown("### 📋 Treinamentos Obrigatórios")
                st.markdown("---")
                
                for t in obrigatorios:
                    total_usuarios = t['total_usuarios'] if t['total_usuarios'] > 0 else 1
                    concluidos = t['total_concluidos'] or 0
                    percentual = (concluidos / total_usuarios * 100) if total_usuarios > 0 else 0
                    
                    # Definir cores baseado no percentual
                    if percentual >= 80:
                        cor_progresso = "green"
                        status_icone = "🟢"
                    elif percentual >= 50:
                        cor_progresso = "orange"
                        status_icone = "🟡"
                    else:
                        cor_progresso = "red"
                        status_icone = "🔴"
                    
                    with st.container(border=True):
                        # Cabeçalho com título e categoria
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f"### {status_icone} **{t['titulo']}**")
                            st.caption(f"📂 **Categoria:** {t['categoria']} | 🔄 **Periodicidade:** {t['periodicidade']}")
                        
                        with col2:
                            st.metric("✅ Concluídos", f"{concluidos}/{total_usuarios}")
                        
                        with col3:
                            st.metric("📊 Progresso", f"{percentual:.1f}%", delta=f"{percentual:.1f}%" if percentual > 0 else None)
                        
                        st.divider()
                        
                        # Detalhes do treinamento
                        col_d1, col_d2 = st.columns(2)
                        with col_d1:
                            st.markdown("**📋 Detalhes do Treinamento:**")
                            st.markdown(f"📖 **Descrição:** {t['descricao'] or 'Não informada'}")
                            st.markdown(f"⏱️ **Carga Horária:** {t['carga_horaria'] or 0} horas")
                            st.markdown(f"🎓 **Modalidade:** {t['modalidade'] or 'EAD'}")
                            st.markdown(f"📅 **Validade:** {t['validade_meses'] or 12} meses")
                            st.markdown(f"🗓️ **Data Cadastro:** {t['data_cadastro'].strftime('%d/%m/%Y') if t['data_cadastro'] else 'Não informada'}")
                        
                        with col_d2:
                            st.markdown("**📊 Status de Conclusão:**")
                            st.progress(percentual / 100, text=f"{percentual:.1f}% do público-alvo concluiu")
                            
                            # Mostrar detalhes de quem falta concluir
                            if concluidos < total_usuarios:
                                faltam = total_usuarios - concluidos
                                st.warning(f"⚠️ {faltam} colaboradores ainda não concluíram este treinamento.")
                            else:
                                st.success("✅ Todos os colaboradores concluíram este treinamento!")
                        
                        st.divider()
                        
                        # Botões de ação
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button(f"📊 Ver Detalhes", key=f"detalhes_{t['id_treinamento']}", use_container_width=True):
                                with st.expander(f"Detalhes dos Colaboradores que concluíram", expanded=True):
                                    # Buscar lista de quem concluiu
                                    cursor.execute("""
                                        SELECT u.nome_usuario, u.cpf, r.descricao as regional, tc.data_conclusao
                                        FROM treinamentos_concluidos tc
                                        JOIN users u ON tc.id_usuario = u.id_usuario
                                        LEFT JOIN regional r ON u.id_regional = r.id_regional
                                        WHERE tc.id_treinamento = %s AND tc.status = 'concluido'
                                        ORDER BY tc.data_conclusao DESC
                                    """, (t['id_treinamento'],))
                                    concluintes = cursor.fetchall()
                                    
                                    if concluintes:
                                        df_concluintes = pd.DataFrame(concluintes)
                                        st.dataframe(df_concluintes, use_container_width=True, hide_index=True)
                                    else:
                                        st.info("Nenhum colaborador concluiu este treinamento ainda.")
                        
                        with col_btn2:
                            if st.button(f"📢 Notificar Pendentes", key=f"notificar_{t['id_treinamento']}", use_container_width=True):
                                # Buscar lista de quem NÃO concluiu
                                cursor.execute("""
                                    SELECT u.id_usuario, u.nome_usuario
                                    FROM users u
                                    WHERE u.ativo = 1
                                    AND u.id_usuario NOT IN (
                                        SELECT id_usuario FROM treinamentos_concluidos 
                                        WHERE id_treinamento = %s AND status = 'concluido'
                                    )
                                    LIMIT 10
                                """, (t['id_treinamento'],))
                                pendentes = cursor.fetchall()
                                
                                if pendentes:
                                    st.info(f"📢 Notificação enviada para {len(pendentes)} colaboradores pendentes")
                                    for p in pendentes:
                                        st.write(f"   - {p['nome_usuario']}")
                                else:
                                    st.success("✅ Todos os colaboradores já concluíram este treinamento!")
                        
                        st.markdown("---")
                
                # Resumo geral de compliance
                st.markdown("### 📊 Resumo Geral de Compliance")
                
                # Estatísticas gerais
                total_obrigatorios = len(obrigatorios)
                total_concluidos_geral = sum(t['total_concluidos'] or 0 for t in obrigatorios)
                total_possiveis = total_obrigatorios * total_usuarios if total_usuarios > 0 else 1
                percentual_geral = (total_concluidos_geral / total_possiveis * 100) if total_possiveis > 0 else 0
                
                col_g1, col_g2, col_g3, col_g4 = st.columns(4)
                col_g1.metric("📚 Total Treinamentos Obrigatórios", total_obrigatorios)
                col_g2.metric("👥 Total de Colaboradores", total_usuarios)
                col_g3.metric("✅ Total de Conclusões", f"{total_concluidos_geral}/{total_possiveis}")
                col_g4.metric("📊 Compliance Geral", f"{percentual_geral:.1f}%")
                
                st.progress(percentual_geral / 100, text=f"Nível de Compliance: {percentual_geral:.1f}%")
                
                # Exportar relatório de compliance
                st.divider()
                df_compliance = pd.DataFrame(obrigatorios)
                df_compliance['percentual'] = df_compliance.apply(
                    lambda x: (x['total_concluidos'] / x['total_usuarios'] * 100) if x['total_usuarios'] > 0 else 0, axis=1
                )
                
                # Selecionar colunas para exportação
                colunas_export = ['id_treinamento', 'titulo', 'categoria', 'periodicidade', 
                                  'carga_horaria', 'modalidade', 'total_concluidos', 'total_usuarios', 'percentual']
                df_export = df_compliance[[c for c in colunas_export if c in df_compliance.columns]]
                df_export.columns = ['ID', 'Treinamento', 'Categoria', 'Periodicidade', 
                                     'Carga Horária', 'Modalidade', 'Concluídos', 'Total Usuários', '% Conclusão']
                df_export['% Conclusão'] = df_export['% Conclusão'].apply(lambda x: f"{x:.1f}%")
                
                csv = df_export.to_csv(index=False, encoding='utf-8-sig', sep=';')
                st.download_button(
                    "📥 Exportar Relatório de Compliance",
                    csv,
                    f"relatorio_compliance_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv",
                    use_container_width=True
                )
            else:
                st.info("📭 Nenhum treinamento obrigatório cadastrado.")

# ============================================================================
# FUNÇÃO PARA SALVAR TREINAMENTO COM NOVOS CAMPOS
# ============================================================================

def salvar_novo_treinamento_completo(titulo, descricao, url_video, categoria, url_documento, 
                                      id_tipo_usuario_alvo, validade_meses, obrigatorio, 
                                      carga_horaria, modalidade, area_responsavel, 
                                      periodicidade, instrutor, publico_alvo):
    """Salva um novo treinamento com todos os campos e envia notificação"""
    try:
        sql = """
            INSERT INTO treinamentos 
            (titulo, descricao, url_video, categoria, url_documento, 
             id_tipo_usuario_alvo, validade_meses, data_cadastro, obrigatorio,
             carga_horaria, modalidade, area_responsavel, periodicidade, instrutor, publico_alvo) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s)
        """
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (titulo, descricao, url_video, categoria, url_documento,
                                id_tipo_usuario_alvo, validade_meses, 
                                1 if obrigatorio else 0, carga_horaria, modalidade, 
                                area_responsavel, periodicidade, instrutor, publico_alvo))
            
            id_treinamento = cursor.lastrowid
            
            # Buscar os dados completos do treinamento recém-criado
            cursor.execute("""
                SELECT carga_horaria, modalidade, titulo 
                FROM treinamentos 
                WHERE id_treinamento = %s
            """, (id_treinamento,))
            treino = cursor.fetchone()
            
            if treino:
                # Enviar notificação com os dados corretos
                enviar_notificacao_treinamento(
                    treino['titulo'], 
                    id_tipo_usuario_alvo, 
                    id_treinamento,
                    treino['carga_horaria'],
                    treino['modalidade']
                )
            
            return True
    except Exception as e:
        print(f"Erro ao salvar treinamento: {e}")
        return False

# FUNÇÃO PRINCIPAL
def exibir_tela_treinamentos():
    """Função principal que será chamada pelo sistema"""
    
    if 'id_usuario' not in st.session_state:
        st.error("Sessão expirada. Faça login novamente.")
        return
    
    # Verificar e criar colunas automaticamente
    verificar_e_criar_colunas_treinamentos()
    
    # Cabeçalho com design moderno
    st.markdown("""
        <div style='background: linear-gradient(135deg, #01384d 0%, #169fda 100%); padding: 1.5rem; border-radius: 20px; margin-bottom: 2rem;'>
            <h1 style='color: white; margin: 0;'>📚 Centro de Treinamentos</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;'>Aprenda, evolua e conquiste certificados!</p>
        </div>
    """, unsafe_allow_html=True)
    
    cargo_id = st.session_state.get('cargo_id', 0)
    
    if cargo_id == 1:  # Admin
        gerenciar_treinamentos_admin()
    else:
        exibir_aba_treinamentos()