"""
Tests for utility functions.
"""

import pytest
from datetime import datetime
from src.utils import QualityChecker, NormativeGraph, build_graph_from_norms


def test_quality_checker_temporal_coverage():
    """Test temporal coverage validation."""
    norms = [
        {'id_norma': 'N1', 'ano': 2015, 'fonte': 'bvsms', 'tema_principal': 'financiamento'},
        {'id_norma': 'N2', 'ano': 2020, 'fonte': 'bvsms', 'tema_principal': 'financiamento'},
        {'id_norma': 'N3', 'ano': 2024, 'fonte': 'planalto', 'tema_principal': 'organizacao_aps'},
    ]
    
    checker = QualityChecker(norms)
    result = checker.check_temporal_coverage()
    
    assert 'temporal_coverage' in checker.report['checks']
    assert 2015 in checker.report['checks']['temporal_coverage']['years_covered']
    assert 2020 in checker.report['checks']['temporal_coverage']['years_covered']


def test_quality_checker_source_coverage():
    """Test source coverage validation."""
    norms = [
        {'id_norma': 'N1', 'ano': 2020, 'fonte': 'bvsms', 'tema_principal': 'financiamento'},
        {'id_norma': 'N2', 'ano': 2020, 'fonte': 'planalto', 'tema_principal': 'financiamento'},
        {'id_norma': 'N3', 'ano': 2020, 'fonte': 'consolidacao', 'tema_principal': 'organizacao_aps'},
    ]
    
    checker = QualityChecker(norms)
    result = checker.check_source_coverage()
    
    assert result is True  # All required sources present
    assert 'bvsms' in checker.report['checks']['source_coverage']['sources']
    assert 'planalto' in checker.report['checks']['source_coverage']['sources']


def test_quality_checker_theme_coverage():
    """Test theme coverage validation."""
    norms = [
        {'id_norma': 'N1', 'ano': 2020, 'fonte': 'bvsms', 'tema_principal': 'organizacao_aps'},
        {'id_norma': 'N2', 'ano': 2020, 'fonte': 'bvsms', 'tema_principal': 'financiamento'},
        {'id_norma': 'N3', 'ano': 2020, 'fonte': 'bvsms', 'tema_principal': 'sistemas_informacao'},
        {'id_norma': 'N4', 'ano': 2020, 'fonte': 'bvsms', 'tema_principal': 'forca_trabalho'},
    ]
    
    checker = QualityChecker(norms)
    result = checker.check_theme_coverage()
    
    assert result is True  # All required themes present


def test_normative_graph_add_norm():
    """Test adding norms to graph."""
    graph = NormativeGraph()
    
    norm = {
        'id_norma': 'NORM_A',
        'tipo': 'Portaria',
        'numero': '123',
        'ano': 2024
    }
    
    graph.add_norm(norm)
    
    assert 'NORM_A' in graph.nodes
    assert graph.nodes['NORM_A']['tipo'] == 'Portaria'


def test_normative_graph_add_relationship():
    """Test adding relationships between norms."""
    graph = NormativeGraph()
    
    norm_a = {'id_norma': 'NORM_A', 'tipo': 'Lei', 'numero': '1', 'ano': 2020}
    norm_b = {'id_norma': 'NORM_B', 'tipo': 'Decreto', 'numero': '2', 'ano': 2021}
    
    graph.add_norm(norm_a)
    graph.add_norm(norm_b)
    graph.add_relationship('NORM_B', 'NORM_A', 'regulamenta')
    
    affected = graph.get_affected_norms('NORM_B')
    assert ('NORM_A', 'regulamenta') in affected


def test_normative_graph_find_revoked():
    """Test finding revoked norms."""
    graph = NormativeGraph()
    
    norm_a = {'id_norma': 'NORM_A', 'tipo': 'Lei', 'numero': '1', 'ano': 2020}
    norm_b = {'id_norma': 'NORM_B', 'tipo': 'Lei', 'numero': '2', 'ano': 2021}
    
    graph.add_norm(norm_a)
    graph.add_norm(norm_b)
    graph.add_relationship('NORM_B', 'NORM_A', 'revoga')
    
    revoked = graph.find_revoked_norms()
    assert 'NORM_A' in revoked


def test_normative_graph_export():
    """Test exporting graph data."""
    graph = NormativeGraph()
    
    norm = {
        'id_norma': 'NORM_EXPORT',
        'tipo': 'Portaria',
        'numero': '999',
        'ano': 2024,
        'tema_principal': 'financiamento',
        'status_vigencia': 'vigente'
    }
    
    graph.add_norm(norm)
    
    export_data = graph.export_graph_data()
    
    assert 'nodes' in export_data
    assert 'edges' in export_data
    assert 'stats' in export_data
    assert len(export_data['nodes']) == 1


def test_build_graph_from_norms():
    """Test building graph from list of norms."""
    norms = [
        {
            'id_norma': 'NORM_1',
            'tipo': 'Lei',
            'numero': '1',
            'ano': 2020,
            'altera': []
        },
        {
            'id_norma': 'NORM_2',
            'tipo': 'Decreto',
            'numero': '2',
            'ano': 2021,
            'altera': ['NORM_1']
        }
    ]
    
    graph = build_graph_from_norms(norms)
    
    assert len(graph.nodes) == 2
    assert 'NORM_1' in graph.nodes
    assert 'NORM_2' in graph.nodes


def test_normative_graph_theme_clusters():
    """Test clustering norms by theme."""
    graph = NormativeGraph()
    
    norms = [
        {'id_norma': 'N1', 'tema_principal': 'financiamento'},
        {'id_norma': 'N2', 'tema_principal': 'financiamento'},
        {'id_norma': 'N3', 'tema_principal': 'organizacao_aps'},
    ]
    
    for norm in norms:
        graph.add_norm(norm)
    
    clusters = graph.get_theme_clusters()
    
    assert len(clusters['financiamento']) == 2
    assert len(clusters['organizacao_aps']) == 1
