# teste_rapido.py
from integracao_hubsoft import HubsoftIntegracao

print("=" * 50)
print("🔍 TESTE RÁPIDO DA INTEGRAÇÃO")
print("=" * 50)

try:
    # Tenta inicializar
    hubsoft = HubsoftIntegracao()
    print("✅ 1. Classe inicializada com sucesso!")
    
    # Testa com ID conhecido que funcionou
    id_teste = 229808
    print(f"\n 2. Buscando serviço ID: {id_teste}")
    
    servico = hubsoft.buscar_servico_por_id(id_teste)
    
    if servico:
        print("    Serviço ENCONTRADO!")
        print(f"    Data Habilitação: {servico.get('data_habilitacao')}")
        print(f"    Status: {servico.get('status')}")
        print(f"    Valor: R$ {servico.get('valor', 0)}")
    else:
        print("    Serviço NÃO encontrado")
        
except Exception as e:
    print(f" ERRO: {e}")

print("\n" + "=" * 50)