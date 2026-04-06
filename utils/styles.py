import streamlit as st

def aplicar_estilo_mell():
    """Aplica o tema corporativo da Mell Internet - Versão Empresarial"""
    
    st.markdown(f"""
    <style>
        /* Cores corporativas */
        :root {{
            --primary: #1e3a5f;        /* Azul escuro corporativo */
            --secondary: #2b4c7c;       /* Azul médio */
            --accent: #c8102e;           /* Vermelho sutil para destaques */
            --background: #f0f2f5;       /* Fundo cinza muito suave */
            --card-bg: #ffffff;          /* Branco para cards */
            --text-primary: #1e293b;     /* Texto principal - quase preto */
            --text-secondary: #475569;   /* Texto secundário - cinza escuro */
            --text-muted: #64748b;       /* Texto suave - cinza médio */
            --border: #e2e8f0;           /* Bordas suaves */
            --sidebar-bg: #1e3a5f;       /* Sidebar com azul escuro */
            --sidebar-text: #ffffff;      /* Texto branco na sidebar */
            --success: #0f7b6b;          /* Verde mais sério */
            --warning: #b45309;           /* Laranja queimado */
            --danger: #b91c1c;            /* Vermelho sério */
            --info: #2563eb;              /* Azul info */
        }}
        
        /* Fundo principal */
        .stApp {{
            background-color: var(--background) !important;
        }}
        
        /* Container principal */
        .main .block-container {{
            background-color: var(--background) !important;
            padding: 2rem !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
        }}
        
        /* Títulos - mais contidos */
        h1, h2, h3, h4 {{
            color: var(--text-primary) !important;
            font-weight: 500 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}
        
        h1 {{
            font-size: 1.8rem !important;
            border-bottom: 2px solid var(--border);
            padding-bottom: 0.8rem;
            margin-bottom: 1.5rem;
            font-weight: 600 !important;
        }}
        
        h2 {{
            font-size: 1.5rem !important;
            margin-bottom: 1.2rem;
        }}
        
        h3 {{
            font-size: 1.2rem !important;
            color: var(--text-secondary) !important;
        }}
        
        /* Cards - estilo corporate */
        div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"],
        .stCard {{
            background: var(--card-bg) !important;
            border-radius: 8px !important;
            padding: 1.2rem !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1) !important;
            margin: 0.8rem 0 !important;
            border: 1px solid var(--border) !important;
            transition: all 0.2s ease;
        }}
        
        div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"]:hover {{
            box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
            border-color: var(--secondary) !important;
        }}
        
        /* Botões - estilo empresarial */
        .stButton > button {{
            border-radius: 6px !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease !important;
            border: 1px solid transparent !important;
        }}
        
        /* Botão primário */
        .stButton > button[kind="primary"] {{
            background-color: var(--primary) !important;
            color: white !important;
            border: none !important;
        }}
        
        .stButton > button[kind="primary"]:hover {{
            background-color: var(--secondary) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }}
        
        /* Botão secundário */
        .stButton > button:not([kind="primary"]) {{
            background-color: white !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
        }}
        
        .stButton > button:not([kind="primary"]):hover {{
            background-color: var(--background) !important;
            border-color: var(--secondary) !important;
        }}
        
        /* Sidebar - profissional */
        section[data-testid="stSidebar"] {{
            background: var(--sidebar-bg) !important;
        }}
        
        section[data-testid="stSidebar"] .stMarkdown {{
            color: var(--sidebar-text) !important;
        }}
        
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {{
            color: white !important;
            opacity: 0.95;
            font-weight: 400 !important;
        }}
        
        /* Menu na sidebar */
        section[data-testid="stSidebar"] .stRadio > div {{
            background: rgba(255,255,255,0.05) !important;
            border-radius: 6px;
            padding: 0.5rem;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        section[data-testid="stSidebar"] .stRadio label {{
            color: rgba(255,255,255,0.9) !important;
            font-size: 0.95rem !important;
            padding: 0.5rem 0.8rem !important;
            border-radius: 4px !important;
            transition: all 0.2s ease;
        }}
        
        section[data-testid="stSidebar"] .stRadio label:hover {{
            background: rgba(255,255,255,0.1) !important;
        }}
        
        section[data-testid="stSidebar"] .stRadio div[data-testid="stMarkdownContainer"] {{
            padding: 0 !important;
        }}
        
        /* Tabs - estilo mais sério */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
            background: transparent;
            padding: 0;
            border-bottom: 1px solid var(--border);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 0 !important;
            padding: 0.6rem 1.2rem !important;
            background: transparent !important;
            border: none !important;
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            border-bottom: 2px solid transparent !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            color: var(--primary) !important;
            border-bottom: 2px solid var(--primary) !important;
            background: transparent !important;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            color: var(--primary) !important;
            border-bottom: 2px solid var(--secondary) !important;
        }}
        
        /* Métricas - clean */
        div[data-testid="stMetric"] {{
            background: white !important;
            padding: 1.2rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}
        
        div[data-testid="stMetric"] label {{
            color: var(--text-secondary) !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        div[data-testid="stMetric"] div {{
            color: var(--text-primary) !important;
            font-size: 1.8rem !important;
            font-weight: 600 !important;
            line-height: 1.2;
        }}
        
        /* DataFrames */
        .stDataFrame {{
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        
        /* Expanders */
        .streamlit-expanderHeader {{
            background: white !important;
            border-radius: 6px !important;
            color: var(--text-primary) !important;
            font-weight: 500 !important;
            border: 1px solid var(--border) !important;
            font-size: 0.95rem !important;
        }}
        
        .streamlit-expanderHeader:hover {{
            border-color: var(--secondary) !important;
        }}
        
        /* Inputs e selects */
        .stTextInput input, .stSelectbox select, .stNumberInput input {{
            border-radius: 6px !important;
            border: 1px solid var(--border) !important;
            padding: 0.5rem 0.75rem !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease !important;
        }}
        
        .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus {{
            border-color: var(--secondary) !important;
            box-shadow: 0 0 0 3px rgba(43,76,124,0.1) !important;
        }}
        
        /* Alertas - mais suaves */
        .stAlert {{
            border-radius: 6px !important;
            border: none !important;
            border-left: 4px solid transparent !important;
            padding: 1rem !important;
        }}
        
        .stAlert[data-baseweb="notification"][kind="success"] {{
            background: #ecfdf5 !important;
            color: var(--success) !important;
            border-left-color: var(--success) !important;
        }}
        
        .stAlert[data-baseweb="notification"][kind="error"] {{
            background: #fef2f2 !important;
            color: var(--danger) !important;
            border-left-color: var(--danger) !important;
        }}
        
        .stAlert[data-baseweb="notification"][kind="warning"] {{
            background: #fffbeb !important;
            color: var(--warning) !important;
            border-left-color: var(--warning) !important;
        }}
        
        .stAlert[data-baseweb="notification"][kind="info"] {{
            background: #eff6ff !important;
            color: var(--info) !important;
            border-left-color: var(--info) !important;
        }}
        
        /* Divisor */
        hr {{
            border: none !important;
            height: 1px !important;
            background: var(--border) !important;
            margin: 2rem 0 !important;
        }}
        
        /* Badges - mais discretos */
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}
        
        /* Loading spinner */
        .stSpinner > div {{
            border-color: var(--secondary) transparent transparent transparent !important;
        }}
        
        /* Tooltips */
        [data-testid="stTooltip"] {{
            background: var(--text-primary) !important;
            color: white !important;
            border-radius: 4px !important;
            font-size: 0.8rem !important;
            padding: 0.3rem 0.6rem !important;
        }}
        
        /* Rodapé */
        .footer {{
            background: white;
            color: var(--text-muted);
            text-align: center;
            padding: 1rem;
            font-size: 0.8rem;
            border-top: 1px solid var(--border);
            margin-top: 3rem;
        }}
    </style>
    """, unsafe_allow_html=True)

def card_corporativo(titulo, conteudo, variante='normal'):
    """Cria um card no estilo corporativo"""
    
    return f"""
    <div style="
        background: white;
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin: 0.8rem 0;
        border: 1px solid #e2e8f0;
    ">
        <h4 style="color: #1e3a5f; margin: 0 0 1rem 0; font-weight: 500; font-size: 1.1rem;">{titulo}</h4>
        <div style="color: #475569; line-height: 1.5;">{conteudo}</div>
    </div>
    """

def badge_corporativo(status, texto):
    """Cria um badge no estilo corporativo"""
    
    cores = {
        'aprovado': {'bg': '#ecfdf5', 'text': '#0f7b6b'},
        'pendente': {'bg': '#fffbeb', 'text': '#b45309'},
        'reprovado': {'bg': '#fef2f2', 'text': '#b91c1c'},
        'ativo': {'bg': '#ecfdf5', 'text': '#0f7b6b'},
        'inativo': {'bg': '#f1f5f9', 'text': '#475569'},
        'info': {'bg': '#eff6ff', 'text': '#2563eb'}
    }
    
    cor = cores.get(status.lower(), cores['info'])
    
    return f"""
    <span style="
        background: {cor['bg']};
        color: {cor['text']};
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
        letter-spacing: 0.3px;
    ">{texto}</span>
    """