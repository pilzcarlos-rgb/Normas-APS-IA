"""APS Normative Graph System - Main Package"""

__version__ = '1.0.0'
__author__ = 'APS Normative Graph Project'
__description__ = 'Sistema de Grafo Normativo da Atenção Primária à Saúde'

from .models import init_database, Norm, Relationship, Article, Program
from .scrapers import BVSMSScraper, ConsolidationParser, ProgramScraper
from .utils import QualityChecker, NormativeGraph, build_graph_from_norms

__all__ = [
    # Models
    'init_database',
    'Norm',
    'Relationship',
    'Article',
    'Program',
    # Scrapers
    'BVSMSScraper',
    'ConsolidationParser',
    'ProgramScraper',
    # Utils
    'QualityChecker',
    'NormativeGraph',
    'build_graph_from_norms',
]
