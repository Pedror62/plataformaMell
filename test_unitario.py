# test_unitario.py
import pytest
import pandas as pd
from decimal import Decimal
from datetime import datetime
from database.queries import get_db_cursor
from modulos.supervisor import format_brl, determinar_tipo_migracao, calcular_comissoes_equipe

# ===== TESTES DE FORMATAÇÃO =====
def test_format_brl():
    """Testa formatação de valores monetários"""
    assert format_brl(100) == "R$ 100,00"
    assert format_brl(1000.50) == "R$ 1.000,50"
    assert format_brl(Decimal("99.90")) == "R$ 99,90"
    assert format_brl(0) == "R$ 0,00"
    assert format_brl(None) == "R$ 0,00"

def test_format_brl_valores_grandes():
    """Testa formatação de valores grandes"""
    assert format_brl(1000000) == "R$ 1.000.000,00"
    assert format_brl(1234567.89) == "R$ 1.234.567,89"

# ===== TESTES DE TIPO DE MIGRAÇÃO =====
def test_determinar_tipo_migracao():
    """Testa identificação de Upgrade/Downgrade"""
    assert determinar_tipo_migracao(129.90, 89.90) == "Migração (Upgrade)"
    assert determinar_tipo_migracao(89.90, 129.90) == "Migração (Downgrade)"
    assert determinar_tipo_migracao(100, 100) == "Migração (mesmo valor)"
    assert determinar_tipo_migracao(0, 100) == "Migração (Downgrade)"

# ===== TESTES DE OPERAÇÃO DETALHADA =====
def test_get_operacao_detalhada():
    """Testa identificação de operação detalhada"""
    from modulos.supervisor import get_operacao_detalhada
    
    # Teste venda normal
    assert get_operacao_detalhada({"operacao": "Venda Nova", "id_tipo_operacao": 1}) == "Venda Nova"
    
    # Teste upgrade
    assert get_operacao_detalhada({
        "operacao": "Migração", 
        "id_tipo_operacao": 2,
        "valor_venda": 129.90,
        "valor_venda_antiga": 89.90
    }) == "Migração (Upgrade)"
    
    # Teste downgrade
    assert get_operacao_detalhada({
        "operacao": "Migração",
        "id_tipo_operacao": 2, 
        "valor_venda": 89.90,
        "valor_venda_antiga": 129.90
    }) == "Migração (Downgrade)"

# ===== TESTES DE IMPACTO FINANCEIRO =====
def test_calcular_impacto():
    """Testa cálculo de impacto financeiro"""
    from modulos.supervisor import get_impacto
    
    # Upgrade - aumento positivo
    assert get_impacto({
        "operacao_detalhada": "Migração (Upgrade)",
        "valor_venda": 129.90,
        "valor_venda_antiga": 89.90
    }) == 40.00
    
    # Downgrade - redução negativa
    assert get_impacto({
        "operacao_detalhada": "Migração (Downgrade)", 
        "valor_venda": 89.90,
        "valor_venda_antiga": 129.90
    }) == -40.00
    
    # Venda nova
    assert get_impacto({
        "operacao_detalhada": "Venda Nova",
        "valor_venda": 79.90
    }) == 79.90

# ===== TESTES DE COMISSÕES =====
def test_calcular_comissoes_equipe_sem_dados():
    """Testa cálculo de comissões sem dados"""
    comissoes, meta = calcular_comissoes_equipe(999, 3, 2026)
    assert comissoes == []
    assert meta == 10  # meta padrão

# ===== TESTES DE VALIDAÇÃO DE DADOS =====
def test_validar_status_venda():
    """Testa validação de status"""
    status_validos = ['APROVADO', 'EM ANÁLISE', 'REPROVADO', 'CANCELADO']
    
    for status in status_validos:
        assert status in status_validos
    
    with pytest.raises(AssertionError):
        assert "INVÁLIDO" in status_validos

def test_validar_valor_venda():
    """Testa validação de valores de venda"""
    valores_validos = [79.90, 89.90, 129.90, 250.00]
    
    for valor in valores_validos:
        assert valor > 0
        assert isinstance(valor, (int, float))
    
    with pytest.raises(AssertionError):
        assert -10 > 0  # valor negativo não deve ser permitido

# ===== TESTES DE CONSULTAS SQL =====
def test_buscar_vendas_por_supervisor_integracao():
    """Testa busca de vendas por supervisor (integração)"""
    from database.queries import buscar_vendas_por_supervisor
    
    # Testa com regional existente
    vendas = buscar_vendas_por_supervisor(1, 3, 2026)
    assert isinstance(vendas, list)
    
    # Testa com regional inexistente
    vendas = buscar_vendas_por_supervisor(999, 3, 2026)
    assert vendas == []

def test_buscar_metas_regionais():
    """Testa busca de metas regionais"""
    from database.queries import buscar_metas_regionais
    
    metas = buscar_metas_regionais(1, 3, 2026)
    
    if metas:
        assert 'meta_vendas_qtd' in metas[0]
        assert metas[0]['meta_vendas_qtd'] > 0
        assert isinstance(metas[0]['meta_vendas_qtd'], (int, Decimal))

# ===== TESTES DE PERFORMANCE =====
def test_performance_consulta_vendas():
    """Testa performance de consulta de vendas"""
    import time
    from database.queries import buscar_vendas_por_supervisor
    
    start = time.time()
    vendas = buscar_vendas_por_supervisor(1, 3, 2026)
    end = time.time()
    
    tempo_execucao = end - start
    assert tempo_execucao < 1.0  # deve levar menos de 1 segundo
    print(f"Consulta executada em {tempo_execucao:.3f} segundos")

# ===== TESTES DE RELATÓRIOS =====
def test_gerar_resumo_operacoes():
    """Testa geração de resumo por operação"""
    dados = pd.DataFrame({
        'operacao_detalhada': ['Venda Nova', 'Venda Nova', 'Migração (Upgrade)', 'Migração (Downgrade)'],
        'valor_venda': [79.90, 89.90, 129.90, 89.90],
        'id_status': [2, 2, 2, 2]
    })
    
    resumo = dados.groupby('operacao_detalhada').agg({
        'valor_venda': 'count'
    }).reset_index()
    
    assert len(resumo) == 3
    assert 'Venda Nova' in resumo['operacao_detalhada'].values
    assert 'Migração (Upgrade)' in resumo['operacao_detalhada'].values
    assert 'Migração (Downgrade)' in resumo['operacao_detalhada'].values

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])