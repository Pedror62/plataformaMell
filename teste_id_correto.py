# teste_id_correto.py
from integracao_hubsoft import HubsoftIntegracao

print("="*60)
print("TESTE COM ID CORRETO DO HUBSOFT")
print("="*60)

hubsoft = HubsoftIntegracao()

# IDs que existem no Hubsoft (baseado no seu JSON)
ids_corretos = [253162, 233858]

for id_teste in ids_corretos:
    print(f"\n🔍 Buscando serviço ID: {id_teste}")
    print("-"*40)
    
    servico = hubsoft.buscar_servico_por_id(id_teste)
    
    if servico and servico.get('encontrado'):
        print(f"✅ ENCONTRADO!")
        print(f"   📋 Plano: {servico.get('plano_nome')}")
        print(f"   📅 Data Habilitação: {servico.get('data_habilitacao_br')}")
        print(f"   📊 Status: {servico.get('status')}")
        print(f"   👤 Vendedor: {servico.get('vendedor_nome')}")
        print(f"   💰 Valor: R$ {servico.get('valor')}")
    else:
        print(f"❌ NÃO ENCONTRADO")