# test_conexao_simples.py
import requests
import socket

print("="*60)
print("TESTE DE CONEXÃO COM HUBSOFT")
print("="*60)

# Teste 1: DNS
print("\n1. TESTANDO DNS...")
try:
    ip = socket.gethostbyname("api.hubsoft.com.br")
    print(f"✅ DNS OK - IP: {ip}")
except Exception as e:
    print(f"❌ Erro de DNS: {e}")

# Teste 2: Conexão simples (sem token)
print("\n2. TESTANDO CONEXÃO HTTP...")
try:
    response = requests.get("https://api.hubsoft.com.br", timeout=10)
    print(f"✅ Conexão OK - Status: {response.status_code}")
    print(f"   Response: {response.text[:200]}")
except requests.exceptions.ConnectionError as e:
    print(f"❌ Erro de conexão: {e}")
    print("\n   Possíveis causas:")
    print("   - URL incorreta")
    print("   - Firewall bloqueando")
    print("   - Proxy configurado")
    print("   - API offline")
except Exception as e:
    print(f"❌ Outro erro: {e}")

# Teste 3: Com token (se disponível)
print("\n3. TESTANDO COM TOKEN...")
try:
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv('HUBSOFT_TOKEN')
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get("https://api.hubsoft.com.br/v1/servicos/1", 
                                headers=headers, timeout=10)
        print(f"✅ Requisição com token - Status: {response.status_code}")
        if response.status_code == 200:
            print("   Token parece válido!")
        elif response.status_code == 401:
            print("   Token inválido ou expirado")
        elif response.status_code == 404:
            print("   Serviço não encontrado (mas API respondeu)")
    else:
        print("⚠️ Token não encontrado no .env")
except Exception as e:
    print(f"❌ Erro: {e}")