"""
Layer 2: Parser for consolidated norms (Portaria 6/2017, SAPS 1/2021)

This parser extracts cited norms from consolidation ordinances to ensure
completeness of the normative collection.
"""

import re
from typing import List, Dict, Set
import logging
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class ConsolidationParser(BaseScraper):
    """
    Parser for Consolidation Ordinances.
    Implements Layer 2 of the collection strategy.
    
    Key ordinances:
    - Portaria de Consolidação GM/MS nº 6/2017 (financing)
    - Portaria de Consolidação SAPS nº 1/2021 (APS)
    """
    
    def __init__(self):
        super().__init__(base_url='https://bvsms.saude.gov.br')
        
        self.key_consolidations = {
            'GM_6_2017': {
                'tipo': 'Portaria de Consolidação GM/MS',
                'numero': '6',
                'ano': 2017,
                'descricao': 'Consolidação de financiamento',
                'url': 'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2017/prc0006_03_10_2017.html'
            },
            'SAPS_1_2021': {
                'tipo': 'Portaria de Consolidação SAPS',
                'numero': '1',
                'ano': 2021,
                'descricao': 'Consolidação da APS',
                'url': 'https://bvsms.saude.gov.br/bvs/saudelegis/saps/2021/prt0001_14_01_2021.html'
            }
        }
    
    def parse_consolidation(self, consolidation_key: str) -> Dict:
        """
        Parse a specific consolidation ordinance.
        
        Args:
            consolidation_key: Key identifying the consolidation
        
        Returns:
            Dictionary with consolidation data and cited norms
        """
        if consolidation_key not in self.key_consolidations:
            raise ValueError(f"Unknown consolidation: {consolidation_key}")
        
        consolidation = self.key_consolidations[consolidation_key]
        logger.info(f"Parsing {consolidation['descricao']}")
        
        soup = self.get_page(consolidation['url'])
        if not soup:
            return {'error': 'Failed to fetch consolidation'}
        
        # Extract the main content
        content = soup.get_text()
        
        # Parse structure
        result = {
            'id': consolidation_key,
            'metadata': consolidation,
            'annexes': self._extract_annexes(soup),
            'cited_norms': self._extract_cited_norms(content),
            'programs': self._extract_programs(content),
            'articles': self._extract_articles(soup)
        }
        
        return result
    
    def _extract_annexes(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract annexes from consolidation document.
        
        Args:
            soup: BeautifulSoup object of the document
        
        Returns:
            List of annexes with their content
        """
        annexes = []
        
        # Look for annex markers in the document
        # Pattern: "ANEXO I", "ANEXO II", etc.
        content_text = soup.get_text()
        annex_pattern = r'ANEXO\s+([IVXLCDM]+|[0-9]+)'
        
        matches = re.finditer(annex_pattern, content_text)
        
        for match in matches:
            annex_num = match.group(1)
            annexes.append({
                'number': annex_num,
                'position': match.start(),
                'text': f"Anexo {annex_num} encontrado"
            })
        
        logger.info(f"Found {len(annexes)} annexes")
        return annexes
    
    def _extract_cited_norms(self, content: str) -> Set[str]:
        """
        Extract references to other normative documents.
        
        Args:
            content: Text content of the document
        
        Returns:
            Set of cited norm identifiers
        """
        cited_norms = set()
        
        # Patterns for different norm types
        patterns = [
            r'Portaria\s+(?:GM/MS\s+)?n[º°]\s*(\d+)',
            r'Lei\s+(?:Complementar\s+)?n[º°]\s*(\d+)',
            r'Decreto\s+n[º°]\s*(\d+)',
            r'Resolução\s+(?:CIT\s+)?n[º°]\s*(\d+)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                cited_norms.add(match.group(0))
        
        logger.info(f"Found {len(cited_norms)} cited norms")
        return cited_norms
    
    def _extract_programs(self, content: str) -> List[str]:
        """
        Extract program names mentioned in the consolidation.
        
        Args:
            content: Text content of the document
        
        Returns:
            List of program names
        """
        programs = []
        
        # Common program names in APS
        program_keywords = [
            'Previne Brasil',
            'PMAQ',
            'Saúde da Família',
            'Informatiza APS',
            'e-SUS',
            'SISAB',
            'Saúde Bucal',
            'Agentes Comunitários',
        ]
        
        for keyword in program_keywords:
            if keyword in content:
                programs.append(keyword)
        
        return programs
    
    def _extract_articles(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract individual articles from the document.
        
        Args:
            soup: BeautifulSoup object of the document
        
        Returns:
            List of articles with their content
        """
        articles = []
        
        # Look for article patterns: "Art. 1º", "Art. 2º", etc.
        article_pattern = r'Art\.\s*(\d+)[º°]?'
        content = soup.get_text()
        
        matches = list(re.finditer(article_pattern, content))
        
        for i, match in enumerate(matches):
            article_num = match.group(1)
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            
            article_text = content[start:end].strip()[:500]  # Limit length
            
            articles.append({
                'number': article_num,
                'text': article_text
            })
        
        logger.info(f"Found {len(articles)} articles")
        return articles
    
    def scrape(self) -> List[Dict]:
        """
        Parse all key consolidations.
        
        Returns:
            List of parsed consolidation data
        """
        results = []
        
        for key in self.key_consolidations.keys():
            try:
                result = self.parse_consolidation(key)
                results.append(result)
            except Exception as e:
                logger.error(f"Error parsing {key}: {e}")
        
        return results


def main():
    """Example usage of consolidation parser."""
    parser = ConsolidationParser()
    results = parser.scrape()
    
    # Save results
    import json
    with open('data/processed/consolidations.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"Parsed {len(results)} consolidation ordinances")


if __name__ == '__main__':
    main()
