import pandas as pd
from datetime import datetime
from .connection import get_db_cursor

# --- LOGIN ---
def login_usuario(usuario, senha):
    """Realiza login do usuário"""
    sql = """
    SELECT u.id_usuario, u.nome_usuario, u.id_regional, u.id_tipo_usuario, u.ativo, u.senha,
           r.descricao as regional_nome
    FROM users u
    LEFT JOIN regional r ON u.id_regional = r.id_regional
    WHERE u.nome_usuario = %s AND u.senha = %s AND u.ativo = 1
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (usuario, senha))
            user = cursor.fetchone()
            if user:
                # Mapeamento de perfis baseado nos IDs do seu banco
                perfis = {
                    1: 'admin',      # ADMINISTRADOR
                    2: 'vendedor',   # Vendedor
                    3: 'supervisor', # Supervisor
                    4: 'auditor',    # Auditor Financeiro
                    26: 'suporte'    # SUPORTE TECNICO
                }
                user['nivel_acesso'] = perfis.get(user['id_tipo_usuario'], 'vendedor')
                return user
    except Exception as e:
        print(f"Erro no login: {e}")
        return None
    return None

# --- VENDAS ---
def registrar_venda(id_usuario, cliente, id_tipo_operacao, valor_venda, valor_anterior=0):
    """Registra uma nova venda com validação de duplicidade"""
    
    from datetime import date
    
    # Buscar o tipo de operação
    with get_db_cursor() as cursor:
        cursor.execute("SELECT descricao FROM tipo_operacao WHERE id_tipo_operacao = %s", (id_tipo_operacao,))
        tipo = cursor.fetchone()
        tipo_operacao = tipo['descricao'] if tipo else 'Venda Nova'
    
    cliente_str = str(cliente).strip()
    
    # Validação: não permitir ID vazio
    if not cliente_str or cliente_str == '':
        return False, "❌ ID do serviço não pode estar vazio!"
    
    # Validação: ID deve ser numérico
    if not cliente_str.isdigit():
        return False, f"❌ ID do serviço '{cliente_str}' não é numérico!"
    
    # Importar funções de validação
    try:
        from modulos.auditor import validar_operacao_servico, verificar_duplicidade_servico
        
        # Validar operação
        valido, msg = validar_operacao_servico(cliente_str, tipo_operacao, date.today())
        if not valido:
            print(f"❌ Validação falhou: {msg}")
            return False, msg
        
        # Verificar duplicidade específica
        tem_dup, dup_msg = verificar_duplicidade_servico(cliente_str, tipo_operacao, date.today())
        if tem_dup:
            print(f"❌ Duplicidade detectada: {dup_msg}")
            return False, dup_msg
            
    except ImportError:
        # Se não conseguir importar, continua sem validação (fallback)
        print("⚠️ Módulo de validação não disponível")
    
    # Query para inserir a venda
    sql = """
        INSERT INTO venda 
        (id_tipo_operacao, 
         id_usuario_vendedor, 
         id_status, 
         id_status_financeiro,
         valor_venda, 
         valor_venda_antiga,
         codigo_cliente,
         valor_anterior,
         ativo, 
         data_venda) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Status 1 = EM ANÁLISE (padrão para novas vendas)
    id_status = 1
    id_status_financeiro = 1
    data_atual = date.today()
    
    try:
        valor_venda_float = float(valor_venda)
        valor_anterior_float = float(valor_anterior)
        
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (
                id_tipo_operacao,
                id_usuario,
                id_status,
                id_status_financeiro,
                valor_venda_float,
                valor_anterior_float,
                cliente_str,
                valor_anterior_float,
                1,
                data_atual
            ))
            
            id_venda = cursor.lastrowid
            print(f"✅ Venda registrada com sucesso! ID: {id_venda}")
            return True, "✅ Venda registrada com sucesso!"
            
    except Exception as e:
        print(f"❌ Erro detalhado ao registrar venda: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, f"❌ Erro ao registrar: {str(e)}"

def atualizar_status_venda(id_venda, novo_status_id):
    """Atualiza o status de uma venda (1-Em análise, 2-Aprovado, 3-Reprovado, 4-Cancelado)"""
    
    try:
        with get_db_cursor(commit=True) as cursor:
            # Primeiro, verifica se a venda existe
            cursor.execute("SELECT id_venda, id_status FROM venda WHERE id_venda = %s", (id_venda,))
            venda = cursor.fetchone()
            
            if not venda:
                return False
            
            # Query para atualizar o status
            sql = "UPDATE venda SET id_status = %s WHERE id_venda = %s"
            cursor.execute(sql, (novo_status_id, id_venda))
            
            if cursor.rowcount > 0:
                # Se aprovado (2), atualiza também a data de aprovação
                if novo_status_id == 2:
                    try:
                        cursor.execute("""
                            UPDATE venda 
                            SET data_aprovacao = CURDATE(), id_status_financeiro = 2 
                            WHERE id_venda = %s
                        """, (id_venda,))
                    except Exception as e:
                        print(f"Erro ao atualizar data de aprovação: {e}")
                return True
            else:
                return False
                
    except Exception as e:
        print(f"Erro ao atualizar status: {e}")
        import traceback
        traceback.print_exc()
        return False

def buscar_vendas_por_supervisor(id_regional, mes, ano):
    """Busca vendas APENAS da regional do supervisor"""
    sql = """
        SELECT 
            v.id_venda,
            v.data_venda,
            u.nome_usuario as vendedor,
            u.id_usuario as id_vendedor,
            t.id_tipo_operacao,
            t.descricao as operacao,
            v.valor_venda,
            v.valor_venda_antiga,
            s.id_status,
            s.descricao as status,
            v.codigo_cliente
        FROM venda v
        INNER JOIN users u ON v.id_usuario_vendedor = u.id_usuario
        INNER JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
        INNER JOIN status s ON v.id_status = s.id_status
        WHERE u.id_regional = %s 
          AND v.ativo = 1
          AND YEAR(v.data_venda) = %s
          AND MONTH(v.data_venda) = %s
        ORDER BY 
            CASE 
                WHEN v.id_status = 1 THEN 0
                ELSE 1 
            END,
            v.data_venda DESC
    """
    try:
        with get_db_cursor() as cursor:
            print(f"🔍 Executando query com: regional={id_regional}, ano={ano}, mes={mes}")
            cursor.execute(sql, (id_regional, ano, mes))
            resultados = cursor.fetchall()
            print(f"✅ Resultados encontrados: {len(resultados)}")
            
            if resultados:
                for r in resultados[:3]:  # Mostra os primeiros 3
                    print(f"   - Venda: {r['id_venda']}, Vendedor: {r['vendedor']}, Valor: {r['valor_venda']}")
            
            return resultados
    except Exception as e:
        print(f"❌ Erro ao buscar vendas: {e}")
        return []

def buscar_todas_vendas(mes, ano):
    """Busca vendas de todas as regionais (para admin)"""
    sql = """
        SELECT 
            v.id_venda,
            v.data_venda,
            u.nome_usuario as vendedor,
            u.id_regional,
            r.descricao as regional,
            t.descricao as operacao,
            v.valor_venda,
            v.valor_venda_antiga,
            s.id_status,
            s.descricao as status,
            v.codigo_cliente
        FROM venda v
        INNER JOIN users u ON v.id_usuario_vendedor = u.id_usuario
        INNER JOIN regional r ON u.id_regional = r.id_regional
        INNER JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
        INNER JOIN status s ON v.id_status = s.id_status
        WHERE MONTH(v.data_venda) = %s 
          AND YEAR(v.data_venda) = %s
          AND v.ativo = 1
        ORDER BY r.descricao, v.data_venda DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (mes, ano))
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar todas vendas: {e}")
        return []

def buscar_vendas_por_vendedor(id_vendedor, mes, ano):
    """Busca vendas de um vendedor específico"""
    sql = """
        SELECT 
            v.id_venda,
            v.data_venda,
            v.codigo_cliente,
            t.descricao as operacao,
            v.valor_venda,
            v.valor_venda_antiga,
            s.descricao as status,
            v.id_status
        FROM venda v
        INNER JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
        INNER JOIN status s ON v.id_status = s.id_status
        WHERE v.id_usuario_vendedor = %s 
          AND MONTH(v.data_venda) = %s 
          AND YEAR(v.data_venda) = %s
          AND v.ativo = 1
        ORDER BY v.data_venda DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (id_vendedor, mes, ano))
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar vendas do vendedor: {e}")
        return []

# --- NOTIFICAÇÕES ---
def buscar_notificacoes(perfil_usuario, id_usuario):
    """Busca notificações não lidas (incluindo individuais)"""
    sql = """
        SELECT n.id, n.titulo, n.mensagem, n.data_envio 
        FROM notificacoes n
        LEFT JOIN notificacoes_lidas nl ON n.id = nl.id_notificacao AND nl.id_usuario = %s
        WHERE nl.id_notificacao IS NULL
          AND (
              -- Notificações individuais para este usuário
              (n.id_usuario_destino = %s)
              OR
              -- Notificações para grupo
              (n.id_usuario_destino IS NULL AND (
                  LOWER(n.destinatario) = 'todos' OR 
                  LOWER(n.destinatario) = %s OR
                  (LOWER(n.destinatario) = 'vendedor' AND %s = 'vendedor') OR
                  (LOWER(n.destinatario) = 'supervisor' AND %s = 'supervisor') OR
                  (LOWER(n.destinatario) = 'admin' AND %s = 'admin') OR
                  (LOWER(n.destinatario) = 'auditor' AND %s = 'auditor')
              ))
          )
        ORDER BY n.data_envio DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (
                id_usuario,           # para o LEFT JOIN
                id_usuario,           # para notificações individuais
                perfil_usuario,       # para grupo
                perfil_usuario,       # para vendedor
                perfil_usuario,       # para supervisor
                perfil_usuario,       # para admin
                perfil_usuario        # para auditor
            ))
            resultados = cursor.fetchall()
            
            # Limpa os asteriscos dos resultados
            for r in resultados:
                if 'titulo' in r:
                    r['titulo'] = r['titulo'].replace('**', '').replace('__', '').strip()
                if 'mensagem' in r:
                    r['mensagem'] = r['mensagem'].replace('**', '').replace('__', '').strip()
            
            return resultados
    except Exception as e:
        print(f"Erro ao buscar notificações: {e}")
        return []

def marcar_notificacoes_como_lidas(id_usuario, ids_notificacoes):
    """Marca notificações como lidas"""
    if not ids_notificacoes:
        return True
    
    sql = "INSERT IGNORE INTO notificacoes_lidas (id_usuario, id_notificacao, data_leitura) VALUES (%s, %s, NOW())"
    try:
        with get_db_cursor(commit=True) as cursor:
            for id_notif in ids_notificacoes:
                cursor.execute(sql, (id_usuario, id_notif))
        return True
    except Exception as e:
        print(f"Erro ao marcar notificações: {e}")
        return False

# --- LOGS ---
def registrar_log(id_usuario, acao, detalhes):
    """Registra ação no log"""
    sql = "INSERT INTO logs_sistema (id_usuario, acao, detalhes, data_hora) VALUES (%s, %s, %s, NOW())"
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (id_usuario, acao, detalhes))
        return True
    except Exception as e:
        print(f"Erro ao registrar log: {e}")
        return False

# --- USUÁRIOS ---
def atualizar_senha_usuario(id_usuario, senha_atual, nova_senha):
    """Atualiza senha do usuário"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("SELECT senha FROM users WHERE id_usuario = %s", (id_usuario,))
            user = cursor.fetchone()
            if user and user['senha'] == senha_atual:
                cursor.execute("UPDATE users SET senha = %s WHERE id_usuario = %s", (nova_senha, id_usuario))
                return cursor.rowcount > 0
            return False
    except Exception as e:
        print(f"Erro ao atualizar senha: {e}")
        return False

def buscar_usuarios():
    """Busca todos os usuários - CORRIGIDO"""
    sql = """
        SELECT 
            u.id_usuario, 
            u.nome_usuario, 
            u.cpf, 
            u.ativo,
            COALESCE(r.descricao, 'Sem Regional') as regional,
            COALESCE(t.descricao, 'Sem Cargo') as cargo,
            u.ultimo_acesso,
            u.id_regional,
            u.id_tipo_usuario
        FROM users u
        LEFT JOIN regional r ON u.id_regional = r.id_regional
        LEFT JOIN tipo_usuario t ON u.id_tipo_usuario = t.id_tipo_usuario
        ORDER BY u.id_usuario DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            resultados = cursor.fetchall()
            print(f"✅ Busca de usuários: {len(resultados)} encontrados")
            return resultados
    except Exception as e:
        print(f"❌ Erro ao buscar usuários: {e}")
        return []

def criar_usuario(nome, cpf, id_regional, id_tipo_usuario, senha):
    """Cria um novo usuário"""
    sql = """
        INSERT INTO users (nome_usuario, cpf, id_regional, id_tipo_usuario, senha, ativo)
        VALUES (%s, %s, %s, %s, %s, 1)
    """
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (nome, cpf, id_regional, id_tipo_usuario, senha))
        return True
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return False

def toggle_usuario_status(id_usuario, ativo):
    """Ativa/desativa usuário"""
    sql = "UPDATE users SET ativo = %s WHERE id_usuario = %s"
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (ativo, id_usuario))
        return True
    except Exception as e:
        print(f"Erro ao alterar status: {e}")
        return False

# --- METAS ---
def buscar_metas_regionais(id_regional=None, mes=None, ano=None):
    """Busca metas regionais"""
    sql = """
        SELECT m.id_meta, r.descricao as regional, 
               m.mes_referencia, m.meta_vendas_qtd, m.meta_migracao_qtd
        FROM metas_regionais m
        JOIN regional r ON m.id_regional = r.id_regional
        WHERE 1=1
    """
    params = []
    
    if id_regional:
        sql += " AND m.id_regional = %s"
        params.append(id_regional)
    if mes and ano:
        sql += " AND MONTH(m.mes_referencia) = %s AND YEAR(m.mes_referencia) = %s"
        params.extend([mes, ano])
    
    sql += " ORDER BY r.descricao, m.mes_referencia DESC"
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar metas: {e}")
        return []

def salvar_meta_regional(id_regional, mes_referencia, meta_vendas, meta_migra):
    """Salva ou atualiza meta regional"""
    sql = """
        INSERT INTO metas_regionais (id_regional, mes_referencia, meta_vendas_qtd, meta_migracao_qtd)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        meta_vendas_qtd = VALUES(meta_vendas_qtd),
        meta_migracao_qtd = VALUES(meta_migracao_qtd)
    """
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (id_regional, mes_referencia, meta_vendas, meta_migra))
        return True
    except Exception as e:
        print(f"Erro ao salvar meta: {e}")
        return False

# --- UTILITÁRIOS ---
def get_tipos_operacao():
    """Retorna todos os tipos de operação ativos"""
    sql = "SELECT id_tipo_operacao, descricao FROM tipo_operacao WHERE ativo = 1 ORDER BY descricao"
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar tipos de operação: {e}")
        return []

def get_status():
    """Retorna todos os status"""
    sql = "SELECT id_status, descricao FROM status WHERE ativo = 1"
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar status: {e}")
        return []

def buscar_logs(limite=500):
    """Busca os logs do sistema"""
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

# ===== FUNÇÃO ENVIAR NOTIFICAÇÃO (ÚNICA VERSÃO) =====
def enviar_notificacao(titulo, mensagem, destinatario, id_usuario_destino=None):
    """
    Envia uma notificação para um grupo de usuários ou um usuário específico
    
    Parâmetros:
    - titulo: Título da notificação
    - mensagem: Conteúdo da notificação
    - destinatario: "Todos", "Vendedores", "Supervisores", "Admins", "individual"
    - id_usuario_destino: ID do usuário (obrigatório se destinatario = "individual")
    """
    try:
        with get_db_cursor(commit=True) as cursor:
            
            # Caso 1: Envio para usuário individual
            if destinatario == "individual" and id_usuario_destino:
                # Verifica se o usuário existe
                cursor.execute("SELECT id_usuario FROM users WHERE id_usuario = %s AND ativo = 1", (id_usuario_destino,))
                if cursor.fetchone():
                    sql = """
                        INSERT INTO notificacoes (titulo, mensagem, destinatario, id_usuario_destino, data_envio) 
                        VALUES (%s, %s, %s, %s, NOW())
                    """
                    cursor.execute(sql, (titulo, mensagem, "individual", id_usuario_destino))
                    print(f"✅ Notificação individual enviada para usuário {id_usuario_destino}")
                    return True
                else:
                    print(f"❌ Usuário {id_usuario_destino} não encontrado ou inativo")
                    return False
            
            # Caso 2: Envio para grupo
            # Mapeia o destinatário para o formato do banco
            mapa_destinatario = {
                "Todos": "todos",
                "Vendedores": "vendedor",
                "Supervisores": "supervisor",
                "Admins": "admin",
                "Auditores": "auditor"
            }
            
            dest = mapa_destinatario.get(destinatario, destinatario.lower())
            
            # Buscar usuários do grupo
            if dest == "todos":
                sql = """
                    INSERT INTO notificacoes (titulo, mensagem, destinatario, data_envio) 
                    VALUES (%s, %s, %s, NOW())
                """
                cursor.execute(sql, (titulo, mensagem, dest))
                print(f"✅ Notificação enviada para TODOS")
                return True
            else:
                # Mapear string para ID do tipo_usuario
                tipo_map = {
                    "vendedor": 2,
                    "supervisor": 3,
                    "admin": 1,
                    "auditor": 4,
                    "suporte": 26
                }
                tipo_id = tipo_map.get(dest)
                
                if tipo_id:
                    # Insere a notificação (será distribuída na busca)
                    sql = """
                        INSERT INTO notificacoes (titulo, mensagem, destinatario, data_envio) 
                        VALUES (%s, %s, %s, NOW())
                    """
                    cursor.execute(sql, (titulo, mensagem, dest))
                    print(f"✅ Notificação enviada para grupo: {destinatario} (tipo_id: {tipo_id})")
                    return True
                else:
                    print(f"❌ Grupo não reconhecido: {destinatario}")
                    return False
            
    except Exception as e:
        print(f"❌ Erro ao enviar notificação: {e}")
        import traceback
        traceback.print_exc()
        return False

# ===== FUNÇÕES DE TREINAMENTO =====
def buscar_treinamentos(id_tipo_usuario):
    """Busca treinamentos disponíveis para o cargo do usuário"""
    sql = """
        SELECT 
            id_treinamento, 
            titulo, 
            descricao, 
            categoria,
            data_cadastro,
            id_tipo_usuario_alvo,
            validade_meses,
            url_video,
            url_documento
        FROM treinamentos 
        WHERE (id_tipo_usuario_alvo = 0 OR id_tipo_usuario_alvo = %s)
        ORDER BY data_cadastro DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (id_tipo_usuario,))
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar treinamentos: {e}")
        return []

def buscar_meus_treinamentos_concluidos(id_usuario):
    """Busca os IDs dos treinamentos já concluídos pelo usuário"""
    sql = """
        SELECT id_treinamento, data_conclusao 
        FROM treinamentos_concluidos 
        WHERE id_usuario = %s
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (id_usuario,))
            resultados = cursor.fetchall()
            return {r['id_treinamento']: r['data_conclusao'] for r in resultados}
    except Exception as e:
        print(f"Erro ao buscar treinamentos concluídos: {e}")
        return {}

def registrar_conclusao_treinamento(id_usuario, id_treinamento, validade_meses):
    """Registra a conclusão de um treinamento pelo usuário"""
    from datetime import datetime, timedelta
    data_vencimento = datetime.now() + timedelta(days=30*validade_meses)
    
    sql = """
        INSERT INTO treinamentos_concluidos 
        (id_usuario, id_treinamento, data_conclusao, data_vencimento, status) 
        VALUES (%s, %s, NOW(), %s, 'concluido')
    """
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (id_usuario, id_treinamento, data_vencimento))
            return True
    except Exception as e:
        print(f"Erro ao registrar conclusão: {e}")
        return False

def salvar_novo_treinamento(titulo, descricao, url_video, categoria, url_documento, id_tipo_usuario_alvo, validade_meses):
    """Salva um novo treinamento no banco"""
    sql = """
        INSERT INTO treinamentos 
        (titulo, descricao, url_video, categoria, url_documento, id_tipo_usuario_alvo, validade_meses, data_cadastro) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (titulo, descricao, url_video, categoria, url_documento, id_tipo_usuario_alvo, validade_meses))
            return True
    except Exception as e:
        print(f"Erro ao salvar treinamento: {e}")
        return False

def buscar_relatorio_treinamentos():
    """Busca relatório geral de treinamentos"""
    sql = """
        SELECT 
            t.id_treinamento,
            t.titulo,
            t.categoria,
            COUNT(c.id_conclusao) as total_conclusoes,
            COUNT(DISTINCT c.id_usuario) as usuarios_unicos,
            MAX(c.data_conclusao) as ultima_conclusao
        FROM treinamentos t
        LEFT JOIN treinamentos_concluidos c ON t.id_treinamento = c.id_treinamento
        GROUP BY t.id_treinamento
        ORDER BY total_conclusoes DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar relatório: {e}")
        return []

def buscar_historico_conclusoes():
    """Busca histórico completo de conclusões para análise"""
    sql = """
        SELECT 
            c.data_conclusao,
            u.nome_usuario as usuario,
            r.descricao as regional,
            t.titulo as treinamento,
            t.categoria
        FROM treinamentos_concluidos c
        JOIN users u ON c.id_usuario = u.id_usuario
        LEFT JOIN regional r ON u.id_regional = r.id_regional
        JOIN treinamentos t ON c.id_treinamento = t.id_treinamento
        WHERE c.status = 'concluido'
        ORDER BY c.data_conclusao DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar histórico: {e}")
        return []

def buscar_progresso_individual():
    """Busca progresso individual de cada usuário nos treinamentos"""
    sql = """
        SELECT 
            u.nome_usuario,
            COALESCE(r.descricao, 'Sem Regional') as Cidade,
            COALESCE(tp.descricao, 'Sem Cargo') as Cargo,
            COUNT(DISTINCT c.id_treinamento) as Total_Concluidos,
            GROUP_CONCAT(DISTINCT t.titulo SEPARATOR ', ') as Treinamentos_Concluidos
        FROM users u
        LEFT JOIN regional r ON u.id_regional = r.id_regional
        LEFT JOIN tipo_usuario tp ON u.id_tipo_usuario = tp.id_tipo_usuario
        LEFT JOIN treinamentos_concluidos c ON u.id_usuario = c.id_usuario AND c.status = 'concluido'
        LEFT JOIN treinamentos t ON c.id_treinamento = t.id_treinamento
        WHERE u.ativo = 1
        GROUP BY u.id_usuario
        ORDER BY Total_Concluidos DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar progresso individual: {e}")
        return []

# ===== FUNÇÕES DE PERMISSÃO =====
def get_funcionalidades():
    """Retorna todas as funcionalidades ativas"""
    sql = "SELECT * FROM funcionalidades WHERE ativo = 1 ORDER BY ordem"
    with get_db_cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()

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
    with get_db_cursor() as cursor:
        cursor.execute(sql, (id_tipo_usuario,))
        return cursor.fetchall()

def get_permissoes_usuario(id_usuario):
    """Retorna permissões especiais de um usuário"""
    sql = """
        SELECT id_funcionalidade, pode_visualizar, pode_criar, pode_editar, pode_excluir
        FROM permissoes_usuario
        WHERE id_usuario = %s
    """
    with get_db_cursor() as cursor:
        cursor.execute(sql, (id_usuario,))
        return {p['id_funcionalidade']: p for p in cursor.fetchall()}

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

def verificar_permissao(id_usuario, id_tipo_usuario, funcionalidade_rota, acao='visualizar'):
    """Verifica se usuário tem permissão para uma ação"""
    
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id_funcionalidade FROM funcionalidades WHERE rota = %s", (funcionalidade_rota,))
        func = cursor.fetchone()
        if not func:
            return False
        id_funcionalidade = func['id_funcionalidade']
    
    permissoes_user = get_permissoes_usuario(id_usuario)
    if id_funcionalidade in permissoes_user:
        return permissoes_user[id_funcionalidade].get(f'pode_{acao}', 0) == 1
    
    with get_db_cursor() as cursor:
        cursor.execute(f"""
            SELECT pode_{acao} 
            FROM permissoes_cargo 
            WHERE id_tipo_usuario = %s AND id_funcionalidade = %s
        """, (id_tipo_usuario, id_funcionalidade))
        permissao = cursor.fetchone()
        return permissao and permissao[f'pode_{acao}'] == 1

# ===== FUNÇÕES DE COMISSÕES =====
# Em database/queries.py - CORREÇÃO DA FUNÇÃO carregar_vendas

def carregar_vendas(id_regional, mes, ano):
    """
    Carrega vendas aprovadas do período
    Retorna um DataFrame com os dados
    """
    try:
        with get_db_cursor() as cursor:
            query = """
                SELECT 
                    v.id_venda,
                    v.data_venda,
                    u.nome_usuario as Vendedor,
                    u.id_regional,
                    r.descricao as Regional,
                    t.descricao as "Tipo Operação",
                    v.valor_venda as "Valor Novo",
                    v.valor_venda_antiga as "Valor Anterior",
                    s.descricao as Status,
                    v.codigo_cliente
                FROM venda v
                INNER JOIN users u ON v.id_usuario_vendedor = u.id_usuario
                INNER JOIN regional r ON u.id_regional = r.id_regional
                INNER JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
                INNER JOIN status s ON v.id_status = s.id_status
                WHERE v.ativo = 1 
                    AND u.id_regional = %s
                    AND MONTH(v.data_venda) = %s 
                    AND YEAR(v.data_venda) = %s
                ORDER BY v.data_venda DESC
            """
            cursor.execute(query, (id_regional, mes, ano))
            resultados = cursor.fetchall()
            
            print(f"✅ carregar_vendas: {len(resultados)} vendas encontradas para regional {id_regional} em {mes}/{ano}")
            
            if resultados:
                return pd.DataFrame(resultados)
            else:
                # Retorna DataFrame vazio, não None
                print("⚠️ Nenhuma venda encontrada, retornando DataFrame vazio")
                return pd.DataFrame()
                
    except Exception as e:
        print(f"❌ Erro em carregar_vendas: {e}")
        import traceback
        traceback.print_exc()
        # Retorna DataFrame vazio em caso de erro
        return pd.DataFrame()

def carregar_todas_vendas(mes, ano):
    """Carrega vendas de todas as regionais"""
    sql = """
        SELECT 
            v.id_venda,
            v.data_venda,
            u.nome_usuario as Vendedor,
            u.id_regional,
            r.descricao as Regional,
            t.descricao as "Tipo Operação",
            v.valor_venda as "Valor Novo",
            v.valor_venda_antiga as "Valor Anterior",
            s.descricao as Status,
            v.codigo_cliente
        FROM venda v
        INNER JOIN users u ON v.id_usuario_vendedor = u.id_usuario
        INNER JOIN regional r ON u.id_regional = r.id_regional
        INNER JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
        INNER JOIN status s ON v.id_status = s.id_status
        WHERE MONTH(v.data_venda) = %s 
          AND YEAR(v.data_venda) = %s
          AND v.ativo = 1
        ORDER BY r.descricao, v.data_venda DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (mes, ano))
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro em carregar_todas_vendas: {e}")
        return None

# ===== FUNÇÕES DE CANCELAMENTO =====
def registrar_cancelamento(id_venda_original, id_usuario_vendedor, id_regional, 
                          id_supervisor_cancelamento, valor_original, 
                          id_motivo, observacoes=""):
    """Registra um cancelamento no sistema"""
    try:
        valor_original = float(valor_original)
        
        sql = """
            INSERT INTO cancelamentos 
            (id_venda_original, id_usuario_vendedor, id_regional, id_supervisor_cancelamento,
             data_cancelamento, data_ocorrencia, valor_original, id_motivo_cancelamento, 
             observacoes, status)
            VALUES (%s, %s, %s, %s, NOW(), CURDATE(), %s, %s, %s, 'pendente')
        """
        
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (id_venda_original, id_usuario_vendedor, id_regional,
                                id_supervisor_cancelamento, valor_original, 
                                id_motivo, observacoes))
            
            cancel_id = cursor.lastrowid
            
            try:
                cursor.execute("UPDATE venda SET id_status = 4 WHERE id_venda = %s", 
                              (id_venda_original,))
            except Exception as e_update:
                print(f"⚠️ Aviso: venda não atualizada - {e_update}")
            
            return cancel_id
            
    except Exception as e:
        print(f"❌ Erro ao registrar cancelamento: {e}")
        import traceback
        traceback.print_exc()
        return None

def buscar_cancelamentos_por_regional(id_regional, mes, ano):
    """Busca cancelamentos de uma regional específica"""
    sql = """
        SELECT 
            c.id_cancelamento,
            c.data_ocorrencia,
            u.nome_usuario as vendedor,
            u.id_usuario as id_vendedor,
            c.valor_original,
            m.descricao as motivo,
            m.id_motivo,
            c.observacoes,
            c.status,
            v.codigo_cliente,
            v.id_venda,
            TIMESTAMPDIFF(MONTH, v.data_venda, c.data_ocorrencia) as meses_apos_venda
        FROM cancelamentos c
        JOIN users u ON c.id_usuario_vendedor = u.id_usuario
        LEFT JOIN motivos_cancelamento m ON c.id_motivo_cancelamento = m.id_motivo
        LEFT JOIN venda v ON c.id_venda_original = v.id_venda
        WHERE c.id_regional = %s 
          AND MONTH(c.data_ocorrencia) = %s 
          AND YEAR(c.data_ocorrencia) = %s
          AND c.ativo = 1
        ORDER BY c.data_ocorrencia DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (id_regional, mes, ano))
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar cancelamentos: {e}")
        return []

def buscar_todos_cancelamentos(mes, ano, id_regional=None):
    """Busca cancelamentos de todas as regionais (para admin)"""
    sql = """
        SELECT 
            c.id_cancelamento,
            c.data_ocorrencia,
            r.descricao as regional,
            u.nome_usuario as vendedor,
            c.valor_original,
            m.descricao as motivo,
            c.status,
            TIMESTAMPDIFF(MONTH, v.data_venda, c.data_ocorrencia) as meses_apos_venda
        FROM cancelamentos c
        JOIN users u ON c.id_usuario_vendedor = u.id_usuario
        JOIN regional r ON c.id_regional = r.id_regional
        LEFT JOIN motivos_cancelamento m ON c.id_motivo_cancelamento = m.id_motivo
        LEFT JOIN venda v ON c.id_venda_original = v.id_venda
        WHERE MONTH(c.data_ocorrencia) = %s 
          AND YEAR(c.data_ocorrencia) = %s
          AND c.ativo = 1
    """
    params = [mes, ano]
    
    if id_regional:
        sql += " AND c.id_regional = %s"
        params.append(id_regional)
    
    sql += " ORDER BY c.data_ocorrencia DESC"
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar todos cancelamentos: {e}")
        return []

def get_motivos_cancelamento():
    """Retorna lista de motivos de cancelamento ativos"""
    sql = "SELECT id_motivo, descricao, categoria FROM motivos_cancelamento WHERE ativo = 1 ORDER BY descricao"
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar motivos: {e}")
        return []

def calcular_impacto_cancelamentos_comissoes(id_regional, mes, ano):
    """Calcula o impacto dos cancelamentos nas comissões (para estorno)"""
    sql = """
        SELECT 
            c.id_usuario_vendedor,
            u.nome_usuario as vendedor,
            COUNT(*) as total_cancelamentos,
            SUM(c.valor_original) as valor_total_cancelado,
            CASE 
                WHEN TIMESTAMPDIFF(MONTH, v.data_venda, c.data_ocorrencia) <= 3 
                THEN 'ESTORNAR' 
                ELSE 'MANTER' 
            END as impacto_comissao,
            GROUP_CONCAT(DISTINCT v.id_venda) as vendas_afetadas
        FROM cancelamentos c
        JOIN users u ON c.id_usuario_vendedor = u.id_usuario
        JOIN venda v ON c.id_venda_original = v.id_venda
        WHERE c.id_regional = %s 
          AND MONTH(c.data_ocorrencia) = %s 
          AND YEAR(c.data_ocorrencia) = %s
          AND c.status IN ('aprovado', 'pendente')
          AND c.ativo = 1
        GROUP BY c.id_usuario_vendedor, 
                 CASE WHEN TIMESTAMPDIFF(MONTH, v.data_venda, c.data_ocorrencia) <= 3 
                      THEN 'ESTORNAR' ELSE 'MANTER' END
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (id_regional, mes, ano))
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao calcular impacto: {e}")
        return []

def aprovar_cancelamento(id_cancelamento, id_supervisor):
    """Aprova um cancelamento (após validação)"""
    sql = "UPDATE cancelamentos SET status = 'aprovado' WHERE id_cancelamento = %s"
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql, (id_cancelamento,))
            return True
    except Exception as e:
        print(f"Erro ao aprovar cancelamento: {e}")
        return False

def reverter_cancelamento(id_cancelamento, id_supervisor):
    """Reverte um cancelamento (caso seja indevido)"""
    sql_select = "SELECT id_venda_original FROM cancelamentos WHERE id_cancelamento = %s"
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(sql_select, (id_cancelamento,))
            cancel = cursor.fetchone()
            
            if cancel:
                cursor.execute("UPDATE venda SET id_status = 2 WHERE id_venda = %s", 
                             (cancel['id_venda_original'],))
                cursor.execute("UPDATE cancelamentos SET ativo = 0 WHERE id_cancelamento = %s", 
                             (id_cancelamento,))
                return True
            return False
    except Exception as e:
        print(f"Erro ao reverter cancelamento: {e}")
        return False

def buscar_vendas_para_cancelamento(id_regional, mes, ano):
    """Busca vendas aprovadas que ainda não foram canceladas"""
    sql = """
        SELECT v.*
        FROM venda v
        LEFT JOIN cancelamentos c ON v.id_venda = c.id_venda_original AND c.ativo = 1
        WHERE v.id_status = 2 
          AND v.ativo = 1
          AND v.id_regional = %s
          AND MONTH(v.data_venda) = %s
          AND YEAR(v.data_venda) = %s
          AND c.id_cancelamento IS NULL
        ORDER BY v.data_venda DESC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (id_regional, mes, ano))
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar vendas para cancelamento: {e}")
        return []

def calcular_receita_liquida_regional(id_regional, mes, ano):
    """Calcula a receita líquida da regional considerando cancelamentos com até 3 meses"""
    sql = """
        SELECT 
            COALESCE((
                SELECT SUM(valor_venda)
                FROM venda v
                JOIN users u ON v.id_usuario_vendedor = u.id_usuario
                WHERE u.id_regional = %s 
                  AND MONTH(v.data_venda) = %s 
                  AND YEAR(v.data_venda) = %s
                  AND v.id_status = 2
                  AND v.ativo = 1
            ), 0) as receita_bruta,
            
            COALESCE((
                SELECT SUM(c.valor_original)
                FROM cancelamentos c
                JOIN users u ON c.id_usuario_vendedor = u.id_usuario
                JOIN venda v ON c.id_venda_original = v.id_venda
                WHERE u.id_regional = %s 
                  AND MONTH(c.data_ocorrencia) = %s 
                  AND YEAR(c.data_ocorrencia) = %s
                  AND c.status IN ('pendente', 'aprovado')
                  AND c.ativo = 1
                  AND TIMESTAMPDIFF(MONTH, v.data_venda, c.data_ocorrencia) <= 3
            ), 0) as total_cancelamentos_estorno
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (id_regional, mes, ano, id_regional, mes, ano))
            result = cursor.fetchone()
            
            if result:
                receita_bruta = float(result['receita_bruta'])
                total_cancelamentos = float(result['total_cancelamentos_estorno'])
                receita_liquida = receita_bruta - total_cancelamentos
                
                return {
                    'receita_bruta': receita_bruta,
                    'total_cancelamentos': total_cancelamentos,
                    'receita_liquida': receita_liquida
                }
            return None
    except Exception as e:
        print(f"Erro ao calcular receita líquida: {e}")
        return None

def buscar_cargos():
    """Retorna todos os cargos ativos do sistema"""
    sql = "SELECT id_tipo_usuario, descricao FROM tipo_usuario WHERE ativo = 1 ORDER BY descricao"
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            return {c['id_tipo_usuario']: c['descricao'] for c in cursor.fetchall()}
    except Exception as e:
        print(f"Erro ao buscar cargos: {e}")
        return {}

def buscar_cargo_por_usuario(id_usuario):
    """Retorna o cargo de um usuário específico"""
    sql = """
        SELECT t.descricao 
        FROM users u
        LEFT JOIN tipo_usuario t ON u.id_tipo_usuario = t.id_tipo_usuario
        WHERE u.id_usuario = %s
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (id_usuario,))
            result = cursor.fetchone()
            return result['descricao'] if result else 'Desconhecido'
    except Exception as e:
        print(f"Erro ao buscar cargo do usuário: {e}")
        return 'Desconhecido'

# ===== FUNÇÃO COMPARTILHADA PARA CARREGAR LOGO =====
def carregar_logo_sistema():
    """Carrega a logo do sistema (mesma lógica do App.py)"""
    import os
    import base64
    from PIL import Image
    import io
    
    nomes_arquivo = [
        "MELL beacons.png",
        "logo.png",
        "assets/LOGO MELL.png",
        "assets/MELL beacons.png"
    ]
    
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

def carregar_logo_redimensionada(tamanho_maximo=200):
    """Carrega a logo redimensionada para um tamanho específico"""
    import os
    import base64
    from PIL import Image
    import io
    
    nomes_arquivo = [
        "MELL beacons.png",
        "logo.png",
        "assets/LOGO MELL.png",
        "assets/MELL beacons.png"
    ]
    
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
        
        if img.width > tamanho_maximo:
            ratio = tamanho_maximo / img.width
            new_size = (tamanho_maximo, int(img.height * ratio))
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
        
        return base64.b64encode(buffer.read()).decode()
        
    except Exception as e:
        print(f"Erro ao carregar logo redimensionada: {e}")
        return None

# ===== FUNÇÕES PARA ASSINATURAS DE CERTIFICADOS =====
def buscar_assinaturas_certificados():
    """Busca todas as assinaturas ativas para certificados"""
    sql = """
        SELECT id_assinatura, tipo, nome, cargo, imagem_assinatura, ordem
        FROM assinaturas_certificados
        WHERE ativo = 1
        ORDER BY ordem ASC
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar assinaturas: {e}")
        return []

def salvar_assinatura_certificado(tipo, nome, cargo, imagem_bytes=None):
    """Salva ou atualiza uma assinatura com imagem"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("SELECT id_assinatura FROM assinaturas_certificados WHERE tipo = %s", (tipo,))
            existe = cursor.fetchone()
            
            if existe:
                if imagem_bytes:
                    sql = """
                        UPDATE assinaturas_certificados 
                        SET nome = %s, cargo = %s, imagem_assinatura = %s 
                        WHERE tipo = %s
                    """
                    cursor.execute(sql, (nome, cargo, imagem_bytes, tipo))
                else:
                    sql = """
                        UPDATE assinaturas_certificados 
                        SET nome = %s, cargo = %s 
                        WHERE tipo = %s
                    """
                    cursor.execute(sql, (nome, cargo, tipo))
            else:
                if imagem_bytes:
                    sql = """
                        INSERT INTO assinaturas_certificados (tipo, nome, cargo, imagem_assinatura, ativo, ordem)
                        VALUES (%s, %s, %s, %s, 1, 
                            (SELECT COALESCE(MAX(ordem), 0) + 1 FROM assinaturas_certificados a2))
                    """
                    cursor.execute(sql, (tipo, nome, cargo, imagem_bytes))
                else:
                    sql = """
                        INSERT INTO assinaturas_certificados (tipo, nome, cargo, ativo, ordem)
                        VALUES (%s, %s, %s, 1, 
                            (SELECT COALESCE(MAX(ordem), 0) + 1 FROM assinaturas_certificados a2))
                    """
                    cursor.execute(sql, (tipo, nome, cargo))
            return True
    except Exception as e:
        print(f"Erro ao salvar assinatura: {e}")
        return False

def excluir_assinatura_certificado(id_assinatura):
    """Exclui (desativa) uma assinatura"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("UPDATE assinaturas_certificados SET ativo = 0 WHERE id_assinatura = %s", (id_assinatura,))
            return True
    except Exception as e:
        print(f"Erro ao excluir assinatura: {e}")
        return False

def buscar_selo_certificado():
    """Busca o selo/carimbo da empresa"""
    sql = """
        SELECT id_selo, nome, imagem
        FROM selo_certificado
        WHERE ativo = 1
        ORDER BY id_selo DESC LIMIT 1
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar selo: {e}")
        return None

def salvar_selo_certificado(nome, imagem_bytes):
    """Salva o selo da empresa"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("UPDATE selo_certificado SET ativo = 0 WHERE ativo = 1")
            sql = "INSERT INTO selo_certificado (nome, imagem, ativo) VALUES (%s, %s, 1)"
            cursor.execute(sql, (nome, imagem_bytes))
            return True
    except Exception as e:
        print(f"Erro ao salvar selo: {e}")
        return False

def registrar_pagamento_comissao(id_venda, id_usuario_vendedor, codigo_cliente, valor_venda, mes_referencia, ano_referencia):
    """Registra o pagamento da comissão de uma venda aprovada na tabela historico_comissoes_detalhes"""
    try:
        with get_db_cursor(commit=True) as cursor:
            # Verificar se a tabela existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historico_comissoes_detalhes (
                    id_detalhe INT AUTO_INCREMENT PRIMARY KEY,
                    id_historico INT,
                    id_venda INT NOT NULL,
                    id_servico VARCHAR(50) NOT NULL,
                    vendedor_nome VARCHAR(100) NOT NULL,
                    valor DECIMAL(10,2) NOT NULL,
                    mes_referencia INT NOT NULL,
                    ano_referencia INT NOT NULL,
                    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_venda_mes (id_venda, mes_referencia, ano_referencia),
                    INDEX idx_servico (id_servico),
                    INDEX idx_venda (id_venda),
                    INDEX idx_data (mes_referencia, ano_referencia)
                )
            """)
            
            # Verificar se a tabela principal existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historico_comissoes (
                    id_historico INT AUTO_INCREMENT PRIMARY KEY,
                    vendedor_nome VARCHAR(100) NOT NULL,
                    mes_referencia INT NOT NULL,
                    ano_referencia INT NOT NULL,
                    valor_pago DECIMAL(10,2) NOT NULL,
                    status_pagamento VARCHAR(20) DEFAULT 'PAGO',
                    data_fechamento DATETIME DEFAULT CURRENT_TIMESTAMP,
                    observacao TEXT,
                    INDEX idx_vendedor (vendedor_nome),
                    INDEX idx_data (mes_referencia, ano_referencia)
                )
            """)

            # Obter nome do vendedor
            cursor.execute("SELECT nome_usuario FROM users WHERE id_usuario = %s", (id_usuario_vendedor,))
            vendedor_info = cursor.fetchone()
            vendedor_nome = vendedor_info['nome_usuario'] if vendedor_info else 'Desconhecido'
            
            # Verificar se já existe um registro mestre para este vendedor no período
            cursor.execute("""
                SELECT id_historico, valor_pago 
                FROM historico_comissoes 
                WHERE vendedor_nome = %s AND mes_referencia = %s AND ano_referencia = %s
            """, (vendedor_nome, mes_referencia, ano_referencia))
            hist_mestre = cursor.fetchone()
            
            if hist_mestre:
                id_historico = hist_mestre['id_historico']
                # Atualizar valor total
                cursor.execute("""
                    UPDATE historico_comissoes 
                    SET valor_pago = valor_pago + %s, data_fechamento = NOW() 
                    WHERE id_historico = %s
                """, (valor_venda, id_historico))
            else:
                # Criar novo registro mestre
                cursor.execute("""
                    INSERT INTO historico_comissoes 
                    (vendedor_nome, mes_referencia, ano_referencia, valor_pago, status_pagamento, data_fechamento, observacao)
                    VALUES (%s, %s, %s, %s, 'PAGO', NOW(), %s)
                """, (
                    vendedor_nome,
                    mes_referencia,
                    ano_referencia,
                    valor_venda,
                    f"Pagamento gerado para venda {id_venda}"
                ))
                id_historico = cursor.lastrowid
            
            # Inserir detalhe
            cursor.execute("""
                INSERT INTO historico_comissoes_detalhes 
                (id_historico, id_venda, id_servico, vendedor_nome, valor, mes_referencia, ano_referencia, data_pagamento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE 
                    id_historico = VALUES(id_historico), 
                    valor = VALUES(valor), 
                    data_pagamento = NOW()
            """, (
                id_historico,
                id_venda,
                codigo_cliente,
                vendedor_nome,
                valor_venda,
                mes_referencia,
                ano_referencia
            ))
            
            print(f"✅ Pagamento de comissão registrado para venda ID: {id_venda}")
            return True
    except Exception as e:
        print(f"❌ Erro ao registrar pagamento de comissão para venda {id_venda}: {e}")
        import traceback
        traceback.print_exc()
        return False
def testar_insercao_pagamento():
    """Função de teste para verificar se a inserção funciona"""
    try:
        with get_db_cursor(commit=True) as cursor:
            # Criar tabelas se não existirem
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historico_comissoes (
                    id_historico INT AUTO_INCREMENT PRIMARY KEY,
                    vendedor_nome VARCHAR(100) NOT NULL,
                    mes_referencia INT NOT NULL,
                    ano_referencia INT NOT NULL,
                    valor_pago DECIMAL(10,2) NOT NULL,
                    status_pagamento VARCHAR(20) DEFAULT 'PAGO',
                    data_fechamento DATETIME DEFAULT CURRENT_TIMESTAMP,
                    observacao TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historico_comissoes_detalhes (
                    id_detalhe INT AUTO_INCREMENT PRIMARY KEY,
                    id_historico INT,
                    id_venda INT NOT NULL,
                    id_servico VARCHAR(50) NOT NULL,
                    vendedor_nome VARCHAR(100) NOT NULL,
                    valor DECIMAL(10,2) NOT NULL,
                    mes_referencia INT NOT NULL,
                    ano_referencia INT NOT NULL,
                    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_venda_mes (id_venda, mes_referencia, ano_referencia)
                )
            """)
            
            # Teste de inserção
            cursor.execute("""
                INSERT INTO historico_comissoes 
                (vendedor_nome, mes_referencia, ano_referencia, valor_pago, observacao)
                VALUES ('TESTE_AUDITOR', 3, 2026, 100.00, 'TESTE DE INSERÇÃO')
            """)
            id_hist = cursor.lastrowid
            print(f"✅ Teste inserido com ID: {id_hist}")
            
            cursor.execute("""
                INSERT INTO historico_comissoes_detalhes 
                (id_historico, id_venda, id_servico, vendedor_nome, valor, mes_referencia, ano_referencia)
                VALUES (%s, 9999, 'TESTE', 'TESTE_AUDITOR', 100.00, 3, 2026)
            """, (id_hist,))
            
            print("✅ Teste de inserção concluído com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False
    # Adicione esta função no final do arquivo queries.py

def buscar_vendas_aprovadas_completas(mes=None, ano=None, regional_id=None):
    """
    Busca todas as vendas aprovadas com informações completas
    Inclui vendas sem código de cliente
    """
    try:
        with get_db_cursor() as cursor:
            sql = """
                SELECT 
                    v.id_venda,
                    COALESCE(v.codigo_cliente, '') as codigo_cliente,
                    v.valor_venda,
                    u.nome_usuario as vendedor,
                    u.id_usuario as id_vendedor,
                    u.id_regional,
                    r.descricao as regional_nome,
                    DATE_FORMAT(v.data_venda, '%d/%m/%Y') as data_venda_br,
                    v.data_venda as data_venda_raw,
                    t.descricao as tipo_operacao,
                    v.id_tipo_operacao,
                    s.descricao as status_descricao,
                    v.id_status
                FROM venda v
                INNER JOIN users u ON v.id_usuario_vendedor = u.id_usuario
                INNER JOIN regional r ON u.id_regional = r.id_regional
                INNER JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
                INNER JOIN status s ON v.id_status = s.id_status
                WHERE v.id_status = 2 
                  AND v.ativo = 1
            """
            params = []
            
            if mes:
                sql += " AND MONTH(v.data_venda) = %s"
                params.append(mes)
            
            if ano:
                sql += " AND YEAR(v.data_venda) = %s"
                params.append(ano)
            
            if regional_id:
                sql += " AND u.id_regional = %s"
                params.append(regional_id)
            
            sql += " ORDER BY v.data_venda DESC"
            
            cursor.execute(sql, tuple(params) if params else None)
            resultados = cursor.fetchall()
            
            if resultados:
                df = pd.DataFrame(resultados)
                
                # Validar IDs (apenas numéricos com 4+ dígitos)
                df['id_valido'] = df['codigo_cliente'].apply(
                    lambda x: x.strip().isdigit() and len(x.strip()) >= 4 if x and x.strip() else False
                )
                
                # Adicionar status de validação
                df['status_validacao'] = df.apply(
                    lambda row: '⚠️ SEM ID' if not row['codigo_cliente'] or row['codigo_cliente'] == '' 
                    else ('✅ ID VÁLIDO' if row['id_valido'] else '⚠️ ID INVÁLIDO'),
                    axis=1
                )
                
                print(f"✅ Busca de vendas concluída: {len(df)} registros")
                print(f"   - Com ID válido: {df['id_valido'].sum()}")
                print(f"   - Sem ID: {len(df[df['codigo_cliente'] == ''])}")
                
                return df
            else:
                print("⚠️ Nenhuma venda encontrada")
                return pd.DataFrame()
                
    except Exception as e:
        print(f"❌ Erro ao buscar vendas: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def buscar_comissoes_pagas_historico(limite_meses=12):
    """
    Busca histórico de comissões pagas dos últimos meses
    """
    try:
        with get_db_cursor() as cursor:
            sql = """
                SELECT 
                    ca.id_comissao,
                    ca.vendedor_nome,
                    ca.mes_referencia,
                    ca.ano_referencia,
                    ca.total_vendas,
                    ca.meta,
                    ca.migracoes,
                    ca.comissao_total,
                    ca.status_pagamento,
                    ca.data_aprovacao,
                    ca.data_pagamento,
                    ca.id_auditor_aprovador,
                    a.nome_usuario as aprovador_nome,
                    r.descricao as regional
                FROM comissoes_aprovadas ca
                LEFT JOIN users a ON ca.id_auditor_aprovador = a.id_usuario
                LEFT JOIN users v ON ca.id_vendedor = v.id_usuario
                LEFT JOIN regional r ON v.id_regional = r.id_regional
                WHERE ca.status_pagamento = 'PAGO'
                ORDER BY ca.ano_referencia DESC, ca.mes_referencia DESC
                LIMIT %s
            """
            cursor.execute(sql, (limite_meses * 50,))
            resultados = cursor.fetchall()
            
            if resultados:
                df = pd.DataFrame(resultados)
                return df
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Erro ao buscar comissões pagas: {e}")
        return pd.DataFrame()


def buscar_metas_regionais_completas(ano=None):
    """
    Busca todas as metas regionais
    """
    try:
        with get_db_cursor() as cursor:
            sql = """
                SELECT 
                    m.id_meta,
                    m.id_regional,
                    r.descricao as regional_nome,
                    m.mes_referencia,
                    MONTH(m.mes_referencia) as mes,
                    YEAR(m.mes_referencia) as ano,
                    m.meta_vendas_qtd,
                    m.meta_migracao_qtd
                FROM metas_regionais m
                JOIN regional r ON m.id_regional = r.id_regional
                WHERE 1=1
            """
            params = []
            
            if ano:
                sql += " AND YEAR(m.mes_referencia) = %s"
                params.append(ano)
            
            sql += " ORDER BY m.ano_referencia DESC, m.mes_referencia DESC"
            
            cursor.execute(sql, tuple(params) if params else None)
            resultados = cursor.fetchall()
            
            if resultados:
                return pd.DataFrame(resultados)
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Erro ao buscar metas: {e}")
        return pd.DataFrame()


def buscar_dashboard_auditor_completo(mes=None, ano=None, regional_id=None):
    """
    Busca todos os dados necessários para o dashboard do auditor
    """
    try:
        # Buscar vendas
        df_vendas = buscar_vendas_aprovadas_completas(mes, ano, regional_id)
        
        # Buscar metas
        df_metas = buscar_metas_regionais_completas(ano)
        
        # Buscar comissões já aprovadas
        with get_db_cursor() as cursor:
            sql = """
                SELECT 
                    id_vendedor,
                    vendedor_nome,
                    mes_referencia,
                    ano_referencia,
                    total_vendas,
                    meta,
                    migracoes,
                    comissao_total,
                    status_pagamento,
                    data_aprovacao,
                    data_pagamento
                FROM comissoes_aprovadas
                WHERE 1=1
            """
            params = []
            
            if mes:
                sql += " AND mes_referencia = %s"
                params.append(mes)
            if ano:
                sql += " AND ano_referencia = %s"
                params.append(ano)
            
            sql += " ORDER BY comissao_total DESC"
            
            cursor.execute(sql, tuple(params) if params else None)
            comissoes = cursor.fetchall()
            df_comissoes = pd.DataFrame(comissoes) if comissoes else pd.DataFrame()
        
        # Buscar histórico de comissões pagas
        df_pagas = buscar_comissoes_pagas_historico()
        
        # Calcular totais por regional
        if not df_vendas.empty:
            df_resumo_regional = df_vendas.groupby(['id_regional', 'regional_nome']).agg({
                'id_venda': 'count',
                'valor_venda': 'sum',
                'vendedor': 'nunique'
            }).reset_index()
            df_resumo_regional.columns = ['id_regional', 'regional', 'total_vendas', 'faturamento', 'vendedores_ativos']
        else:
            df_resumo_regional = pd.DataFrame()
        
        return {
            'vendas': df_vendas,
            'metas': df_metas,
            'comissoes_aprovadas': df_comissoes,
            'comissoes_pagas': df_pagas,
            'resumo_regional': df_resumo_regional
        }
        
    except Exception as e:
        print(f"Erro ao buscar dashboard completo: {e}")
        import traceback
        traceback.print_exc()
        return None
# Adicione esta função no arquivo queries.py

def buscar_vendas_do_periodo(reg_sel, mes_num, ano_sel, regs):
    """
    Busca todas as vendas do período selecionado
    Função mantida para compatibilidade com admin.py
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SHOW COLUMNS FROM venda")
            colunas = [col['Field'] for col in cursor.fetchall()]
            
            campo_id = 'codigo_cliente' if 'codigo_cliente' in colunas else None
            
            if not campo_id:
                possiveis = ['id_servico', 'id_cliente', 'codigo_servico']
                for campo in possiveis:
                    if campo in colunas:
                        campo_id = campo
                        break
            
            if not campo_id:
                return pd.DataFrame()
            
            select_cols = [
                f"CAST(v.{campo_id} AS CHAR) as id_servico_raw",
                f"CAST(v.{campo_id} AS CHAR) as id_servico_limpo",
                "v.id_venda",
                "u.nome_usuario as vendedor_nome",
                "DATE_FORMAT(v.data_venda, '%d/%m/%Y') as data_venda_br",
                "v.data_venda",
                "COALESCE(v.valor_venda, 0) as valor_venda",
                "COALESCE(t.descricao, 'Venda Nova') as tipo_operacao"
            ]
            
            query = f"""
                SELECT 
                    {', '.join(select_cols)}
                FROM venda v
                LEFT JOIN users u ON v.id_usuario_vendedor = u.id_usuario
                LEFT JOIN tipo_operacao t ON v.id_tipo_operacao = t.id_tipo_operacao
                WHERE v.ativo = 1
            """
            params = []
            
            if reg_sel != "Geral" and reg_sel in regs:
                query += " AND u.id_regional = %s"
                params.append(regs[reg_sel])
            
            if mes_num and ano_sel:
                query += " AND MONTH(v.data_venda) = %s AND YEAR(v.data_venda) = %s"
                params.extend([mes_num, ano_sel])
            
            query += " ORDER BY v.data_venda DESC"
            
            cursor.execute(query, tuple(params) if params else None)
            resultados = cursor.fetchall()
            
            if resultados:
                df = pd.DataFrame(resultados)
                df['id_servico_limpo'] = df['id_servico_limpo'].astype(str)
                df['id_valido'] = df['id_servico_limpo'].apply(
                    lambda x: x.isdigit() and len(x) >= 4 if x and x != 'nan' and x != '' else False
                )
                return df
            else:
                return pd.DataFrame()
                
    except Exception as e:
        print(f"Erro ao buscar vendas: {e}")
        return pd.DataFrame()
# database/queries.py

def login_usuario(usuario, senha):
    """Realiza login do usuário - compatível com SQLite e MySQL"""
    from database.connection import get_db_cursor
    
    sql = """
    SELECT u.id_usuario, u.nome_usuario, u.id_regional, u.id_tipo_usuario, u.ativo,
           COALESCE(r.descricao, 'Geral') as regional_nome
    FROM users u
    LEFT JOIN regional r ON u.id_regional = r.id_regional
    WHERE u.nome_usuario = ? AND u.senha = ? AND u.ativo = 1
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (usuario, senha))
            user = cursor.fetchone()
            if user:
                # Converter para dicionário se for tupla (SQLite)
                if isinstance(user, tuple):
                    user = {
                        'id_usuario': user[0],
                        'nome_usuario': user[1],
                        'id_regional': user[2],
                        'id_tipo_usuario': user[3],
                        'ativo': user[4],
                        'regional_nome': user[5]
                    }
                # Mapear perfil
                perfis = {1: 'admin', 2: 'vendedor', 3: 'supervisor', 4: 'auditor', 26: 'suporte'}
                user['nivel_acesso'] = perfis.get(user['id_tipo_usuario'], 'vendedor')
                return user
    except Exception as e:
        print(f"Erro no login: {e}")
        return None
    return None
# database/queries.py - SOMENTE A FUNÇÃO LOGIN

def login_usuario(usuario, senha):
    """Realiza login do usuário - VERSÃO SIMPLIFICADA"""
    from database.connection import get_db_cursor
    
    print(f"🔍 Tentando login: usuário='{usuario}', senha='{senha}'")  # Debug
    
    sql = """
    SELECT id_usuario, nome_usuario, id_regional, id_tipo_usuario, ativo
    FROM users 
    WHERE nome_usuario = ? AND senha = ? AND ativo = 1
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(sql, (usuario, senha))
            resultado = cursor.fetchone()
            
            print(f"Resultado da consulta: {resultado}")  # Debug
            
            if resultado:
                # Converter para dicionário
                if isinstance(resultado, dict):
                    user = dict(resultado)
                else:
                    user = {
                        'id_usuario': resultado[0],
                        'nome_usuario': resultado[1],
                        'id_regional': resultado[2],
                        'id_tipo_usuario': resultado[3],
                        'ativo': resultado[4],
                        'regional_nome': 'Geral'
                    }
                
                # Mapear perfil
                perfis = {1: 'admin', 2: 'vendedor', 3: 'supervisor', 4: 'auditor', 26: 'suporte'}
                user['nivel_acesso'] = perfis.get(user['id_tipo_usuario'], 'vendedor')
                print(f"✅ Login OK: {user['nome_usuario']}")  # Debug
                return user
            else:
                print("❌ Nenhum usuário encontrado")  # Debug
                return None
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        import traceback
        traceback.print_exc()
        return None