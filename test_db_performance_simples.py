# test_db_performance_simples.py
import time
import pandas as pd
from database.queries import get_db_cursor
from datetime import datetime

def format_tempo(segundos):
    """Formata tempo em milissegundos"""
    return f"{segundos * 1000:.2f} ms"

def testar_consulta(nome, sql, params=None, repeticoes=10):
    """Testa performance de uma consulta SQL"""
    tempos = []
    
    print(f"\n📊 Testando: {nome}")
    print("-" * 50)
    
    for i in range(repeticoes):
        try:
            start = time.time()
            with get_db_cursor() as cursor:
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                resultado = cursor.fetchall()
            end = time.time()
            
            tempo = end - start
            tempos.append(tempo)
            
            if i == 0:
                print(f"   Registros retornados: {len(resultado)}")
                
        except Exception as e:
            print(f"   ❌ Erro na execução {i+1}: {e}")
            tempos.append(None)
    
    # Remove None e calcula estatísticas
    tempos_validos = [t for t in tempos if t is not None]
    
    if tempos_validos:
        media = sum(tempos_validos) / len(tempos_validos)
        minimo = min(tempos_validos)
        maximo = max(tempos_validos)
        
        print(f"   ✅ Mínimo: {format_tempo(minimo)}")
        print(f"   ✅ Médio: {format_tempo(media)}")
        print(f"   ✅ Máximo: {format_tempo(maximo)}")
        
        return {
            'nome': nome,
            'media': media,
            'minimo': minimo,
            'maximo': maximo,
            'registros': len(resultado) if i == 0 else 0
        }
    else:
        print(f"   ❌ Todas as execuções falharam")
        return None

def testar_consultas_complexas():
    """Testa consultas complexas do sistema"""
    print("\n" + "="*60)
    print("🚀 TESTE DE PERFORMANCE DO BANCO DE DADOS")
    print("="*60)
    
    resultados = []
    
    # 1. Consulta de vendas do vendedor
    sql_vendas_vendedor = """
        SELECT v.*, tu.descricao as tipo_operacao
        FROM venda v
        LEFT JOIN tipo_operacao tu ON v.id_tipo_operacao = tu.id_tipo_operacao
        WHERE v.id_usuario_vendedor = %s 
            AND MONTH(v.data_venda) = %s 
            AND YEAR(v.data_venda) = %s
        LIMIT 1000
    """
    res = testar_consulta(
        "1. Vendas do Vendedor",
        sql_vendas_vendedor,
        (1, 3, 2026)
    )
    if res: resultados.append(res)
    
    # 2. Consulta de vendas do supervisor
    sql_vendas_supervisor = """
        SELECT v.*, u.nome_usuario as vendedor, tu.descricao as tipo_operacao
        FROM venda v
        INNER JOIN users u ON v.id_usuario_vendedor = u.id_usuario
        LEFT JOIN tipo_operacao tu ON v.id_tipo_operacao = tu.id_tipo_operacao
        WHERE u.id_regional = %s 
            AND MONTH(v.data_venda) = %s 
            AND YEAR(v.data_venda) = %s
        ORDER BY v.data_venda DESC
        LIMIT 1000
    """
    res = testar_consulta(
        "2. Vendas do Supervisor",
        sql_vendas_supervisor,
        (1, 3, 2026)
    )
    if res: resultados.append(res)
    
    # 3. Metas regionais
    sql_metas = """
        SELECT * FROM metas_regionais 
        WHERE id_regional = %s 
            AND mes = %s 
            AND ano = %s
    """
    res = testar_consulta(
        "3. Metas Regionais",
        sql_metas,
        (1, 3, 2026)
    )
    if res: resultados.append(res)
    
    # 4. Cancelamentos
    sql_cancelamentos = """
        SELECT c.*, u.nome_usuario as vendedor, m.descricao as motivo
        FROM cancelamentos c
        INNER JOIN users u ON c.id_usuario_vendedor = u.id_usuario
        LEFT JOIN motivos_cancelamento m ON c.id_motivo = m.id_motivo
        WHERE c.id_regional = %s 
            AND MONTH(c.data_ocorrencia) = %s 
            AND YEAR(c.data_ocorrencia) = %s
        ORDER BY c.data_ocorrencia DESC
        LIMIT 1000
    """
    res = testar_consulta(
        "4. Cancelamentos",
        sql_cancelamentos,
        (1, 3, 2026)
    )
    if res: resultados.append(res)
    
    # 5. Ranking de vendedores
    sql_ranking = """
        SELECT 
            u.id_usuario,
            u.nome_usuario,
            COUNT(v.id_venda) as total_vendas,
            SUM(v.valor_venda) as total_valor,
            RANK() OVER (ORDER BY COUNT(v.id_venda) DESC) as ranking
        FROM users u
        LEFT JOIN venda v ON u.id_usuario = v.id_usuario_vendedor 
            AND v.id_status = 2 
            AND MONTH(v.data_venda) = %s 
            AND YEAR(v.data_venda) = %s
        WHERE u.id_regional = %s 
            AND u.id_tipo_usuario = 2
        GROUP BY u.id_usuario, u.nome_usuario
        HAVING total_vendas > 0
        ORDER BY ranking
        LIMIT 10
    """
    res = testar_consulta(
        "5. Ranking Vendedores",
        sql_ranking,
        (3, 2026, 1)
    )
    if res: resultados.append(res)
    
    # 6. Resumo mensal
    sql_resumo = """
        SELECT 
            v.id_status,
            COUNT(*) as quantidade,
            SUM(v.valor_venda) as total_valor
        FROM venda v
        WHERE MONTH(v.data_venda) = %s 
            AND YEAR(v.data_venda) = %s
        GROUP BY v.id_status
    """
    res = testar_consulta(
        "6. Resumo Mensal",
        sql_resumo,
        (3, 2026)
    )
    if res: resultados.append(res)
    
    return resultados

def testar_consultas_com_joins():
    """Testa consultas com múltiplos JOINs"""
    print("\n" + "="*60)
    print("🔗 TESTE DE CONSULTAS COM JOINS")
    print("="*60)
    
    resultados = []
    
    # Dashboard completo
    sql_dashboard = """
        SELECT 
            COUNT(DISTINCT v.id_venda) as total_vendas,
            COUNT(DISTINCT u.id_usuario) as total_vendedores,
            SUM(CASE WHEN v.id_status = 2 THEN v.valor_venda ELSE 0 END) as faturamento,
            SUM(CASE WHEN v.id_status = 1 THEN 1 ELSE 0 END) as pendentes,
            SUM(CASE WHEN v.id_status = 3 THEN 1 ELSE 0 END) as reprovadas,
            (SELECT COUNT(*) FROM cancelamentos c 
             WHERE MONTH(c.data_ocorrencia) = 3 AND YEAR(c.data_ocorrencia) = 2026) as cancelamentos
        FROM venda v
        LEFT JOIN users u ON v.id_usuario_vendedor = u.id_usuario
        WHERE MONTH(v.data_venda) = 3 AND YEAR(v.data_venda) = 2026
    """
    res = testar_consulta(
        "7. Dashboard Completo",
        sql_dashboard,
        repeticoes=5
    )
    if res: resultados.append(res)
    
    return resultados

def testar_indices():
    """Verifica se os índices recomendados existem"""
    print("\n" + "="*60)
    print("🔍 VERIFICANDO ÍNDICES RECOMENDADOS")
    print("="*60)
    
    try:
        with get_db_cursor() as cursor:
            # Verifica índices na tabela venda
            cursor.execute("SHOW INDEX FROM venda")
            indices_venda = cursor.fetchall()
            
            if indices_venda:
                print("\n📋 Índices existentes na tabela venda:")
                for idx in indices_venda:
                    print(f"   • {idx['Key_name']} - {idx['Column_name']}")
            else:
                print("\n📋 Nenhum índice encontrado na tabela venda")
            
            # Índices recomendados
            recomendados = {
                'idx_venda_data': "CREATE INDEX idx_venda_data ON venda(data_venda)",
                'idx_venda_vendedor': "CREATE INDEX idx_venda_vendedor ON venda(id_usuario_vendedor)",
                'idx_venda_status': "CREATE INDEX idx_venda_status ON venda(id_status)"
            }
            
            indices_existentes = [idx['Key_name'] for idx in indices_venda] if indices_venda else []
            
            print("\n💡 ÍNDICES RECOMENDADOS:")
            for nome, sql in recomendados.items():
                if nome not in indices_existentes:
                    print(f"   ⚠️ {nome} - NÃO ENCONTRADO")
                    print(f"      Sugestão: {sql}")
                else:
                    print(f"   ✅ {nome} - JÁ EXISTE")
                    
    except Exception as e:
        print(f"❌ Erro ao verificar índices: {e}")

def gerar_relatorio(resultados):
    """Gera relatório de performance"""
    
    if not resultados:
        print("\n❌ Nenhum resultado para gerar relatório")
        return
    
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE PERFORMANCE")
    print("="*60)
    
    # Classifica resultados
    rapidas = []
    lentas = []
    muito_lentas = []
    
    for r in resultados:
        tempo_ms = r['media'] * 1000
        if tempo_ms < 500:
            rapidas.append(r)
        elif tempo_ms < 1000:
            lentas.append(r)
        else:
            muito_lentas.append(r)
    
    print(f"\n✅ Consultas Rápidas (<500ms): {len(rapidas)}")
    for r in rapidas:
        print(f"   • {r['nome']}: {r['media']*1000:.2f}ms")
    
    if lentas:
        print(f"\n⚠️ Consultas Lentas (500-1000ms): {len(lentas)}")
        for r in lentas:
            print(f"   • {r['nome']}: {r['media']*1000:.2f}ms")
    
    if muito_lentas:
        print(f"\n❌ Consultas Muito Lentas (>1000ms): {len(muito_lentas)}")
        for r in muito_lentas:
            print(f"   • {r['nome']}: {r['media']*1000:.2f}ms")
    
    # Resumo
    print("\n" + "-"*60)
    media_geral = sum(r['media'] for r in resultados) / len(resultados) * 1000
    print(f"📊 Tempo médio geral: {media_geral:.2f}ms")
    
    if media_geral < 500:
        print("🏆 PERFORMANCE EXCELENTE! Todas as consultas estão otimizadas.")
    elif media_geral < 1000:
        print("👍 PERFORMANCE BOA! Considere otimizar as consultas mais lentas.")
    else:
        print("⚠️ PERFORMANCE PREOCUPANTE! Necessário otimizar as consultas.")
    
    # Sugestões
    if muito_lentas:
        print("\n💡 SUGESTÕES DE MELHORIA:")
        for r in muito_lentas:
            print(f"\n   • {r['nome']} - {r['media']*1000:.0f}ms")
            print(f"     → Adicionar índices nas colunas de filtro")
            print(f"     → Revisar JOINs e subconsultas")
            print(f"     → Limitar quantidade de registros")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 INICIANDO TESTES DE PERFORMANCE DO BANCO")
    print("="*60)
    
    # Testa consultas simples
    resultados_simples = testar_consultas_complexas()
    
    # Testa consultas com joins
    resultados_joins = testar_consultas_com_joins()
    
    # Todos os resultados
    todos_resultados = resultados_simples + resultados_joins
    
    # Gera relatório
    gerar_relatorio(todos_resultados)
    
    # Verifica índices
    testar_indices()
    
    print("\n" + "="*60)
    print("✅ TESTES CONCLUÍDOS!")
    print("="*60)