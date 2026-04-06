# diagnostico_ids.py
from database.queries import get_db_cursor

print("="*60)
print("DIAGNÓSTICO - IDs NA TABELA VENDA")
print("="*60)

with get_db_cursor() as cursor:
    # Busca os IDs reais
    cursor.execute("""
        SELECT 
            id_venda,
            codigo_cliente_servico as id_original,
            codigo_cliente as codigo_cliente,
            data_venda
        FROM venda 
        WHERE codigo_cliente_servico IS NOT NULL 
        AND codigo_cliente_servico != ''
        ORDER BY id_venda DESC
        LIMIT 20
    """)
    
    resultados = cursor.fetchall()
    
    print("\n📋 IDs encontrados na tabela venda:")
    print("-"*70)
    
    ids_validos = 0
    ids_invalidos = 0
    
    for row in resultados:
        # Converte para string primeiro
        id_original = str(row['id_original']) if row['id_original'] is not None else ''
        # Limpa o ID
        id_limpo = id_original.replace('.', '').replace('-', '').replace('/', '').strip()
        
        # Verifica se é numérico
        if id_limpo and id_limpo.isdigit():
            ids_validos += 1
            status = "✅ VÁLIDO"
        else:
            ids_invalidos += 1
            status = "❌ INVÁLIDO"
        
        print(f"ID Venda: {row['id_venda']}")
        print(f"  Original: '{id_original}'")
        print(f"  Limpo: '{id_limpo}'")
        print(f"  Status: {status}")
        print(f"  Data: {row['data_venda']}")
        print("-"*70)
    
    print(f"\n📊 RESUMO:")
    print(f"   Total IDs: {len(resultados)}")
    print(f"   ✅ Válidos (numéricos): {ids_validos}")
    print(f"   ❌ Inválidos: {ids_invalidos}")
    
    if ids_validos == 0:
        print("\n⚠️ NENHUM ID VÁLIDO ENCONTRADO!")
        print("\n💡 Possíveis soluções:")
        print("   1. A coluna 'codigo_cliente_servico' pode estar vazia")
        print("   2. Os IDs podem ter formato diferente (ex: 10.101.010)")
        print("   3. Talvez a coluna correta seja 'codigo_cliente'")
        print("\n🔍 Verificando coluna 'codigo_cliente'...")
        
        cursor.execute("""
            SELECT 
                id_venda,
                codigo_cliente as id_original,
                data_venda
            FROM venda 
            WHERE codigo_cliente IS NOT NULL 
            AND codigo_cliente != ''
            AND codigo_cliente REGEXP '^[0-9]+$'
            LIMIT 10
        """)
        
        resultados2 = cursor.fetchall()
        
        if resultados2:
            print(f"\n✅ Encontrados {len(resultados2)} IDs numéricos na coluna 'codigo_cliente':")
            for row in resultados2:
                print(f"   ID Venda: {row['id_venda']} -> codigo_cliente: {row['id_original']}")
        else:
            print("\n❌ Nenhum ID numérico encontrado na coluna 'codigo_cliente'")