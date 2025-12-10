"""
Quality Assurance module for the APS Normative Graph System.

This module implements validation rules to ensure completeness and consistency
of the normative collection.
"""

import logging
from typing import Dict, List, Set
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class QualityChecker:
    """
    Quality assurance checker for normative data completeness.
    
    Validates:
    1. Temporal coverage (2010-2025)
    2. Source coverage (Planalto, BVSMS, Consolidations)
    3. Theme coverage (Organization, Financing, Information Systems, Workforce)
    4. Graph consistency
    """
    
    def __init__(self, norms: List[Dict]):
        """
        Initialize the quality checker.
        
        Args:
            norms: List of norm dictionaries to validate
        """
        self.norms = norms
        self.report = {
            'total_norms': len(norms),
            'checks': {},
            'warnings': [],
            'errors': []
        }
    
    def run_all_checks(self) -> Dict:
        """
        Run all quality checks.
        
        Returns:
            Comprehensive quality report
        """
        logger.info("Running quality checks...")
        
        self.check_temporal_coverage()
        self.check_source_coverage()
        self.check_theme_coverage()
        self.check_graph_consistency()
        self.check_key_norms_presence()
        
        # Calculate overall quality score
        self.report['quality_score'] = self._calculate_quality_score()
        
        logger.info(f"Quality score: {self.report['quality_score']:.2f}%")
        return self.report
    
    def check_temporal_coverage(self) -> bool:
        """
        Verify that all years from 2010-2025 are covered.
        
        Returns:
            True if coverage is adequate
        """
        years_with_data = set()
        year_counts = defaultdict(int)
        
        for norm in self.norms:
            year = norm.get('ano')
            if year:
                years_with_data.add(year)
                year_counts[year] += 1
        
        expected_years = set(range(2010, 2026))
        missing_years = expected_years - years_with_data
        
        self.report['checks']['temporal_coverage'] = {
            'pass': len(missing_years) == 0,
            'years_covered': sorted(list(years_with_data)),
            'missing_years': sorted(list(missing_years)),
            'year_counts': dict(year_counts)
        }
        
        if missing_years:
            self.report['warnings'].append(
                f"Missing data for years: {sorted(missing_years)}"
            )
        
        return len(missing_years) == 0
    
    def check_source_coverage(self) -> bool:
        """
        Verify that all key sources are represented.
        
        Returns:
            True if all sources are present
        """
        sources = defaultdict(int)
        
        for norm in self.norms:
            source = norm.get('fonte', 'unknown')
            sources[source] += 1
        
        required_sources = {'planalto', 'bvsms', 'consolidacao'}
        present_sources = set(sources.keys())
        missing_sources = required_sources - present_sources
        
        self.report['checks']['source_coverage'] = {
            'pass': len(missing_sources) == 0,
            'sources': dict(sources),
            'missing_sources': list(missing_sources)
        }
        
        if missing_sources:
            self.report['warnings'].append(
                f"Missing data from sources: {missing_sources}"
            )
        
        return len(missing_sources) == 0
    
    def check_theme_coverage(self) -> bool:
        """
        Verify that all key themes are covered.
        
        Returns:
            True if all themes are adequately covered
        """
        themes = defaultdict(int)
        
        for norm in self.norms:
            theme = norm.get('tema_principal')
            if theme:
                themes[theme] += 1
        
        required_themes = {
            'organizacao_aps',
            'financiamento',
            'sistemas_informacao',
            'forca_trabalho'
        }
        
        present_themes = set(themes.keys())
        missing_themes = required_themes - present_themes
        
        self.report['checks']['theme_coverage'] = {
            'pass': len(missing_themes) == 0,
            'themes': dict(themes),
            'missing_themes': list(missing_themes)
        }
        
        if missing_themes:
            self.report['warnings'].append(
                f"Insufficient coverage for themes: {missing_themes}"
            )
        
        return len(missing_themes) == 0
    
    def check_graph_consistency(self) -> bool:
        """
        Verify that the normative graph is consistent.
        
        Checks:
        - If norm A revokes B, B should exist and be marked as revoked
        - All referenced norms should exist in the database
        
        Returns:
            True if graph is consistent
        """
        norm_ids = {norm.get('id_norma') for norm in self.norms}
        inconsistencies = []
        
        for norm in self.norms:
            # Check relationships
            for rel_type in ['altera', 'revoga', 'regulamenta']:
                related = norm.get(rel_type, [])
                if isinstance(related, list):
                    for related_id in related:
                        if related_id not in norm_ids:
                            inconsistencies.append({
                                'source': norm.get('id_norma'),
                                'type': rel_type,
                                'target': related_id,
                                'issue': 'Referenced norm not found'
                            })
        
        self.report['checks']['graph_consistency'] = {
            'pass': len(inconsistencies) == 0,
            'inconsistencies': inconsistencies,
            'total_checked': len(self.norms)
        }
        
        if inconsistencies:
            self.report['errors'].append(
                f"Found {len(inconsistencies)} graph inconsistencies"
            )
        
        return len(inconsistencies) == 0
    
    def check_key_norms_presence(self) -> bool:
        """
        Verify that key structural norms are present.
        
        Returns:
            True if all key norms are present
        """
        key_norms = [
            ('LC_141_2012', 'Lei Complementar 141/2012'),
            ('DECRETO_7508_2011', 'Decreto 7.508/2011'),
            ('PORTARIA_CONSOLIDACAO_6_2017', 'Portaria de Consolidação 6/2017'),
            ('PORTARIA_CONSOLIDACAO_SAPS_1_2021', 'Portaria de Consolidação SAPS 1/2021'),
            ('PORTARIA_2979_2019', 'Portaria 2.979/2019 - Previne Brasil'),
            ('PORTARIA_3493_2024', 'Portaria 3.493/2024 - Novo cofinanciamento'),
        ]
        
        norm_ids = {norm.get('id_norma') for norm in self.norms}
        missing_key_norms = []
        
        for norm_id, description in key_norms:
            if norm_id not in norm_ids:
                missing_key_norms.append(description)
        
        self.report['checks']['key_norms_presence'] = {
            'pass': len(missing_key_norms) == 0,
            'missing': missing_key_norms,
            'total_key_norms': len(key_norms)
        }
        
        if missing_key_norms:
            self.report['errors'].append(
                f"Missing key norms: {', '.join(missing_key_norms)}"
            )
        
        return len(missing_key_norms) == 0
    
    def _calculate_quality_score(self) -> float:
        """
        Calculate overall quality score based on checks.
        
        Returns:
            Quality score as percentage (0-100)
        """
        checks = self.report['checks']
        passed = sum(1 for check in checks.values() if check.get('pass', False))
        total = len(checks)
        
        if total == 0:
            return 0.0
        
        return (passed / total) * 100


def main():
    """Example usage of quality checker."""
    # Example with mock data
    mock_norms = [
        {
            'id_norma': 'PORTARIA_2979_2019',
            'ano': 2019,
            'fonte': 'bvsms',
            'tema_principal': 'financiamento'
        },
        {
            'id_norma': 'LC_141_2012',
            'ano': 2012,
            'fonte': 'planalto',
            'tema_principal': 'financiamento'
        }
    ]
    
    checker = QualityChecker(mock_norms)
    report = checker.run_all_checks()
    
    import json
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
