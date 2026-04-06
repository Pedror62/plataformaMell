# integracao_hubsoft.py
import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class HubsoftIntegracao:
    def __init__(self):
        self.token = os.getenv('HUBSOFT_TOKEN')
        if not self.token:
            raise ValueError("HUBSOFT_TOKEN não configurado")
        # URL base correta (sem barra extra)
        base_url = os.getenv('HUBSOFT_URL', 'https://api.microtell.hubsoft.com.br')
        self.base_url = base_url.rstrip('/')
        
        # Configuração de timeout
        self.timeout = 30
        self.max_retries = 2
    
    def _fazer_requisicao(self, url, retry=0):
        """Faz requisição com retry automático"""
        try:
            print(f"🌐 URL: {url}")
            response = requests.get(
                url,
                headers={'Authorization': f'Bearer {self.token}'},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"Serviço não encontrado: {url}")
                return None
            elif response.status_code == 429:
                if retry < self.max_retries:
                    time.sleep(2 ** retry)
                    return self._fazer_requisicao(url, retry + 1)
                return None
            else:
                print(f"Erro {response.status_code}: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return None
    
    def _processar_servico(self, dados):
        """Processa os dados do serviço para formato padronizado"""
        if not dados:
            return None
        
        # Extrai vendedor
        vendedor = dados.get('vendedor', {})
        if isinstance(vendedor, dict):
            nome_vendedor = vendedor.get('nome', '-')
        else:
            nome_vendedor = str(vendedor) if vendedor else '-'
        
        # Extrai data de habilitação
        data_hab = dados.get('data_habilitacao')
        data_hab_raw = data_hab
        if data_hab:
            try:
                if isinstance(data_hab, str):
                    data_obj = None
                    for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y']:
                        try:
                            data_obj = datetime.strptime(data_hab, fmt)
                            break
                        except:
                            continue
                    
                    if data_obj:
                        data_hab_br = data_obj.strftime('%d/%m/%Y %H:%M')
                    else:
                        data_hab_br = data_hab
                else:
                    data_hab_br = str(data_hab)
            except:
                data_hab_br = str(data_hab)
        else:
            data_hab_br = '-'
            data_hab_raw = ''
        
        # Determina status
        status = dados.get('status', '')
        status_prefixo = dados.get('status_prefixo', '')
        
        if not status_prefixo and status:
            if 'habilitado' in status.lower() or 'ativo' in status.lower():
                status_prefixo = 'servico_habilitado'
            elif 'pendente' in status.lower():
                status_prefixo = 'servico_pendente'
            elif 'cancelado' in status.lower():
                status_prefixo = 'servico_cancelado'
        
        instalado = (status_prefixo == 'servico_habilitado')
        
        tipo = "Venda"
        if dados.get('id_cliente_servico_antigo'):
            tipo = "Migração"
        
        return {
            'encontrado': True,
            'id': dados.get('id_cliente_servico'),
            'nome': dados.get('nome', '-'),
            'plano_nome': dados.get('nome', '-'),
            'valor': float(dados.get('valor', 0)),
            'status': status,
            'status_prefixo': status_prefixo,
            'data_habilitacao': data_hab_raw,
            'data_habilitacao_br': data_hab_br,
            'data_habilitacao_raw': data_hab_raw,
            'vendedor': {'nome': nome_vendedor},
            'vendedor_nome': nome_vendedor,
            'tipo': tipo,
            'instalado': instalado,
            'id_cliente_servico_antigo': dados.get('id_cliente_servico_antigo')
        }
    
    def buscar_servico_por_id(self, id_servico):
        """Busca serviço no Hubsoft pelo ID usando o endpoint correto"""
        print(f"🔍 Consultando Hubsoft para ID {id_servico}...")
        
        # Endpoint correto baseado no Postman
        # {{url}}/api/v1/integracao/cliente?busca=id_cliente_servico&termo_busca=229808
        url = f"{self.base_url}/api/v1/integracao/cliente?busca=id_cliente_servico&termo_busca={id_servico}"
        dados = self._fazer_requisicao(url)
        
        if dados and dados.get('status') == 'success':
            clientes = dados.get('clientes', [])
            if clientes:
                servicos = clientes[0].get('servicos', [])
                # Procura o serviço específico pelo ID
                for servico in servicos:
                    if str(servico.get('id_cliente_servico')) == str(id_servico):
                        return self._processar_servico(servico)
                # Se não encontrou, pega o primeiro
                if servicos:
                    return self._processar_servico(servicos[0])
        
        return {
            'encontrado': False,
            'instalado': False,
            'tipo': 'Venda',
            'valor': 0,
            'plano_nome': '-',
            'data_habilitacao_br': '-',
            'data_habilitacao_raw': '',
            'vendedor_nome': '-'
        }
    
    def buscar_servicos_em_lote(self, ids_servicos):
        """Busca múltiplos serviços"""
        resultados = {}
        for id_servico in ids_servicos:
            servico = self.buscar_servico_por_id(id_servico)
            if servico:
                resultados[str(id_servico)] = servico
        return resultados


def buscar_data_habilitacao(id_servico):
    """Função auxiliar para buscar data de habilitação"""
    try:
        hubsoft = HubsoftIntegracao()
        servico = hubsoft.buscar_servico_por_id(id_servico)
        if servico and servico.get('encontrado'):
            return servico.get('data_habilitacao_br', '-')
        return '-'
    except Exception as e:
        print(f"Erro ao buscar data: {e}")
        return '-'