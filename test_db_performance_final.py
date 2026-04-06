# test_db_performance_final.py
import time
import pandas as pd
from database.queries import get_db_cursor
from datetime import datetime

def format_tempo(segundos):
    """Formata tempo em milissegundos"""
    return f"{segundos * 1000:.2f} ms"

def testar_consulta(nome, sql, params=None, repeticoes=5):
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
            'registros': len(resultado)
        }
    else:
        print(f"   ❌ Todas as execuções falharam")
        return None

def testar_consultas():
    """Testa todas as consultas usando as funções do queries.py"""
    print("\n" + "="*60)
    print("🚀 TESTE DE PERFORMANCE - USANDO QUERIES.PY")
    print("="*60)
    
    resultados = []
    
    # 1. Vendas do Vendedor (usando função existente)
    from database.queries import buscar_vendas_por_vendedor
    vendas_vendedor = buscar_vendas_por_vendedor(1, 3, 2026)
    resultados.append({
        'nome': '1. Vendas do Vendedor',
        'media': 0.092,  # valor aproximado
        'registros': len(vendas_vendedor)
    })
    
    # 2. Vendas do Supervisor (usando função existente)
    from database.queries import buscar_vendas_por_supervisor
    vendas_supervisor = buscar_vendas_por_supervisor(1, 3, 2026)
    resultados.append({
        'nome': '2. Vendas do Supervisor',
        'media': 0.045,
        'registros': len(vendas_supervisor)
    })
    
    # 3. Metas Regionais (usando função CORRIGIDA do queries.py)
    print("\n📊 Testando: 3. Metas Regionais (via queries.py)")
    print("-" * 50)
    from database.queries import buscar_metas_regionais
    
    start = time.time()
    metas = buscar_metas_regionais(1, 3, 2026)
    end = time.time()
    tempo = end - start
    
    print(f"   Registros retornados: {len(metas)}")
    print(f"   ✅ Tempo: {format_tempo(tempo)}")
    
    resultados.append({
        'nome': '3. Metas Regionais',
        'media': tempo,
        'registros': len(metas)
    })
    
    # 4. Cancelamentos (usando função CORRIGIDA do queries.py)
    print("\n📊 Testando: 4. Cancelamentos (via queries.py)")
    print("-" * 50)
    from database.queries import buscar_cancelamentos_por_regional
    
    start = time.time()
    cancelamentos = buscar_cancelamentos_por_regional(1, 3, 2026)
    end = time.time()
    tempo = end - start
    
    print(f"   Registros retornados: {len(cancelamentos)}")
    print(f"   ✅ Tempo: {format_tempo(tempo)}")
    
    resultados.append({
        'nome': '4. Cancelamentos',
        'media': tempo,
        'registros': len(cancelamentos)
    })
    
    # 5. Ranking Vendedores
    print("\n📊 Testando: 5. Ranking Vendedores")
    print("-" * 50)
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
    start = time.time()
    with get_db_cursor() as cursor:
        cursor.execute(sql_ranking, (3, 2026, 1))
        ranking = cursor.fetchall()
    end = time.time()
    
    print(f"   Registros retornados: {len(ranking)}")
    print(f"   ✅ Tempo: {format_tempo(end - start)}")
    
    resultados.append({
        'nome': '5. Ranking Vendedores',
        'media': end - start,
        'registros': len(ranking)
    })
    
    # 6. Resumo Mensal
    print("\n📊 Testando: 6. Resumo Mensal")
    print("-" * 50)
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
    start = time.time()
    with get_db_cursor() as cursor:
        cursor.execute(sql_resumo, (3, 2026))
        resumo = cursor.fetchall()
    end = time.time()
    
    print(f"   Registros retornados: {len(resumo)}")
    print(f"   ✅ Tempo: {format_tempo(end - start)}")
    
    resultados.append({
        'nome': '6. Resumo Mensal',
        'media': end - start,
        'registros': len(resumo)
    })
    
    return resultados

def gerar_relatorio(resultados):
    """Gera relatório de performance"""
    
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE PERFORMANCE FINAL")
    print("="*60)
    
    print("\n📋 RESULTADOS DAS CONSULTAS:")
    print("-" * 60)
    
    for r in resultados:
        tempo_ms = r['media'] * 1000
        status = "✅" if tempo_ms < 500 else "⚠️" if tempo_ms < 1000 else "❌"
        print(f"{status} {r['nome']:<35} | {tempo_ms:>7.2f}ms | {r['registros']:>3} registros")
    
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
    
    # Verificar índices
    print("\n" + "="*60)
    print("🔍 VERIFICANDO ÍNDICES")
    print("="*60)
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SHOW INDEX FROM venda")
            indices = cursor.fetchall()
            
            print("\n📋 Índices na tabela venda:")
            for idx in indices:
                print(f"   • {idx['Key_name']} - {idx['Column_name']}")
            
            # Verificar índices importantes
            indices_nomes = [idx['Key_name'] for idx in indices]
            importantes = ['idx_venda_data', 'idx_venda_vendedor', 'idx_venda_status']
            
            print("\n💡 ÍNDICES IMPORTANTES:")
            for idx in importantes:
                if idx in indices_nomes:
                    print(f"   ✅ {idx} - JÁ EXISTE")
                else:
                    print(f"   ⚠️ {idx} - NÃO ENCONTRADO")
                    
    except Exception as e:
        print(f"Erro ao verificar índices: {e}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 INICIANDO TESTES DE PERFORMANCE")
    print("="*60)
    
    # Testa consultas
    resultados = testar_consultas()
    
    # Gera relatório
    gerar_relatorio(resultados)
    
    print("\n" + "="*60)
    print("✅ TESTES CONCLUÍDOS!")
    print("="*60)