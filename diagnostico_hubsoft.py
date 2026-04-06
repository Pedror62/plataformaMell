# diagnostico_hubsoft.py
import os
import requests
from dotenv import load_dotenv
from database.queries import get_db_cursor

load_dotenv()

def testar_hubsoft():
    print("="*60)
    print("TESTE DE DIAGNÓSTICO - HUBSOFT")
    print("="*60)
    
    token = os.getenv('HUBSOFT_TOKEN')
    url_base = os.getenv('HUBSOFT_URL', 'https://api.hubsoft.com.br/v1')
    
    print(f"\n📌 URL Base: {url_base}")
    print(f"📌 Token: {token[:10]}...{token[-5:] if token else 'NÃO ENCONTRADO'}")
    
    if not token:
        print("\n❌ ERRO: Token não encontrado no arquivo .env")
        print("   Verifique se o arquivo .env está na raiz do projeto")
        print("   e se contém a linha: HUBSOFT_TOKEN=seu_token_aqui")
        return
    
    # 1. Buscar IDs reais do banco
    print("\n" + "="*60)
    print("1. BUSCANDO IDs REAIS DO BANCO DE DADOS")
    print("="*60)
    
    with get_db_cursor() as cursor:
        # Verificar a coluna correta
        cursor.execute("SHOW COLUMNS FROM venda")
        colunas = [col['Field'] for col in cursor.fetchall()]
        
        print("\n📋 Colunas da tabela venda:")
        for col in colunas:
            print(f"   - {col}")
        
        # Possíveis colunas para ID do serviço
        possiveis = ['id_cliente_servico', 'codigo_cliente', 'cliente_id', 'id_servico', 'cliente', 'id_cliente']
        
        campo_id = None
        for campo in possiveis:
            if campo in colunas:
                campo_id = campo
                break
        
        if not campo_id:
            print("\n❌ Nenhuma coluna de ID encontrada!")
            return
        
        print(f"\n✅ Usando coluna: {campo_id}")
        
        # Buscar IDs reais
        cursor.execute(f"""
            SELECT DISTINCT {campo_id} as id_servico 
            FROM venda 
            WHERE {campo_id} IS NOT NULL 
            AND {campo_id} != '' 
            AND {campo_id} != '0'
            LIMIT 10
        """)
        ids_reais = cursor.fetchall()
        
        if ids_reais:
            print(f"\n📋 IDs reais encontrados no banco:")
            for row in ids_reais:
                print(f"   - {row['id_servico']}")
        else:
            print("\n⚠️ Nenhum ID encontrado no banco!")
            return
    
    # 2. Testar cada ID real
    print("\n" + "="*60)
    print("2. TESTANDO CADA ID NO HUBSOFT")
    print("="*60)
    
    headers = {'Authorization': f'Bearer {token}'}
    
    for row in ids_reais:
        id_servico = row['id_servico']
        try:
            id_int = int(id_servico)
            url = f"{url_base}/servicos/{id_int}"
            
            print(f"\n🔍 Testando ID: {id_int}")
            print(f"   URL: {url}")
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    dados = response.json()
                    print(f"   ✅ ENCONTRADO!")
                    print(f"   Nome: {dados.get('nome')}")
                    print(f"   Status: {dados.get('status')}")
                    print(f"   Data Habilitação: {dados.get('data_habilitacao')}")
                    print(f"\n   🎯 Este ID funciona! Use-o para os testes.")
                    return True
                    
                elif response.status_code == 401:
                    print(f"   ❌ Token inválido ou expirado")
                    return False
                elif response.status_code == 404:
                    print(f"   ❌ Serviço não encontrado")
                else:
                    print(f"   ❌ Erro: {response.text[:100]}")
                    
            except requests.exceptions.ConnectionError:
                print(f"   ❌ Erro de conexão com a API")
                print(f"   Verifique a URL: {url_base}")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                
        except ValueError:
            print(f"\n🔍 ID inválido: {id_servico} (não é numérico)")
    
    print("\n" + "="*60)
    print("3. SUGESTÕES")
    print("="*60)
    print("""
    ⚠️ Nenhum ID funcionou. Possíveis causas:
    
    1. Token inválido ou expirado - Verifique no .env
    2. URL da API incorreta - Confirme com o Hubsoft
    3. Os IDs do banco não existem no Hubsoft
    4. Conexão com a internet bloqueada
    
    🔧 Para corrigir:
    - Verifique o token no arquivo .env
    - Entre em contato com o suporte Hubsoft
    - Verifique se há um ID de teste válido
    """)
    
    return False

if __name__ == "__main__":
    testar_hubsoft()