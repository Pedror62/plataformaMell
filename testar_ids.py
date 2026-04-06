# testar_ids.py
from integracao_hubsoft import HubsoftIntegracao

hubsoft = HubsoftIntegracao()

# Lista de IDs para testar (baseados na sua tabela)
ids_teste = [
  229808
]

print("=" * 60)
print("🔍 TESTANDO MÚLTIPLOS IDs")
print("=" * 60)

for id_teste in ids_teste:
    print(f"\n📌 Testando ID: {id_teste}")
    print("-" * 40)
    
    servico = hubsoft.buscar_servico_por_id(id_teste)
    
    if servico:
        print(f"✅ ENCONTRADO!")
        print(f"   📅 Data: {servico.get('data_habilitacao')}")
        print(f"   📊 Status: {servico.get('status')}")
        print(f"   💰 Valor: R$ {servico.get('valor', 0)}")
    else:
        print(f"❌ Não encontrado")

print("\n" + "=" * 60)
input("\nPressione Enter para sair...")