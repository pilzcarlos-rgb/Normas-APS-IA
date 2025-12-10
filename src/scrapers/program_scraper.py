"""
Layer 3: Specialized scraper for programs with their own regulatory ecosystem

Programs like Previne Brasil and the new APS co-financing (3.493/2024) have
extensive micro-legislation that requires dedicated collection strategies.
"""

from typing import List, Dict
import logging
from datetime import datetime
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class ProgramScraper(BaseScraper):
    """
    Scraper for program-specific normative documents.
    Implements Layer 3 of the collection strategy.
    """
    
    def __init__(self):
        super().__init__(base_url='https://bvsms.saude.gov.br')
        
        # Key programs with their establishing norms
        self.programs = {
            'previne_brasil': {
                'name': 'Previne Brasil',
                'establishing_norm': 'Portaria 2.979/2019',
                'url': 'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2019/prt2979_12_11_2019.html',
                'search_terms': ['Previne Brasil', 'capitação', 'desempenho', 'incentivo'],
                'start_year': 2019
            },
            'novo_cofinanciamento': {
                'name': 'Novo Cofinanciamento APS',
                'establishing_norm': 'Portaria 3.493/2024',
                'url': 'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2024/prt3493_06_11_2024.html',
                'search_terms': ['cofinanciamento', 'Portaria 3.493'],
                'start_year': 2024
            },
            'pmaq': {
                'name': 'PMAQ - Programa de Melhoria do Acesso e Qualidade',
                'establishing_norm': 'Portaria 1.654/2011',
                'url': None,
                'search_terms': ['PMAQ', 'qualidade', 'acesso'],
                'start_year': 2011,
                'end_year': 2019  # Program ended
            },
            'informatiza_aps': {
                'name': 'Informatiza APS',
                'establishing_norm': 'Portaria 2.983/2019',
                'url': None,
                'search_terms': ['Informatiza APS', 'e-SUS', 'SISAB'],
                'start_year': 2019
            }
        }
    
    def scrape_program(self, program_key: str) -> Dict:
        """
        Scrape all normative documents related to a specific program.
        
        Args:
            program_key: Key identifying the program
        
        Returns:
            Dictionary with program data and related norms
        """
        if program_key not in self.programs:
            raise ValueError(f"Unknown program: {program_key}")
        
        program = self.programs[program_key]
        logger.info(f"Scraping program: {program['name']}")
        
        result = {
            'program_key': program_key,
            'program_name': program['name'],
            'establishing_norm': program['establishing_norm'],
            'norms': []
        }
        
        # 1. Get the establishing norm
        if program['url']:
            establishing_data = self._fetch_establishing_norm(program)
            if establishing_data:
                result['norms'].append(establishing_data)
        
        # 2. Search for related norms by year and search terms
        start_year = program['start_year']
        end_year = program.get('end_year', datetime.now().year)
        
        for year in range(start_year, end_year + 1):
            for term in program['search_terms']:
                related_norms = self._search_related_norms(term, year)
                result['norms'].extend(related_norms)
        
        # 3. Look for technical notes and operational manuals
        technical_docs = self._search_technical_documents(program['name'])
        result['technical_documents'] = technical_docs
        
        logger.info(f"Found {len(result['norms'])} norms for {program['name']}")
        return result
    
    def _fetch_establishing_norm(self, program: Dict) -> Dict:
        """
        Fetch the main norm that establishes the program.
        
        Args:
            program: Program dictionary with URL
        
        Returns:
            Dictionary with norm data
        """
        logger.info(f"Fetching establishing norm: {program['establishing_norm']}")
        
        soup = self.get_page(program['url'])
        if not soup:
            return None
        
        # Extract data from the norm page
        data = {
            'tipo': 'Portaria GM/MS',
            'url_html': program['url'],
            'ementa': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else '',
            'texto_completo': soup.get_text(),
            'program': program['name'],
            'is_establishing_norm': True
        }
        
        return data
    
    def _search_related_norms(self, search_term: str, year: int) -> List[Dict]:
        """
        Search for norms related to a program by term and year.
        
        Args:
            search_term: Search term
            year: Year to search
        
        Returns:
            List of related norms
        """
        # This would integrate with BVSMS search
        # Simplified for template purposes
        logger.info(f"Searching for '{search_term}' in {year}")
        return []
    
    def _search_technical_documents(self, program_name: str) -> List[Dict]:
        """
        Search for technical notes and operational manuals.
        
        Args:
            program_name: Name of the program
        
        Returns:
            List of technical documents
        """
        logger.info(f"Searching technical documents for {program_name}")
        
        # Search patterns for technical documents
        technical_docs = []
        
        # Note: Would need to implement actual search logic
        # This is a template showing the intended functionality
        
        return technical_docs
    
    def scrape(self) -> List[Dict]:
        """
        Scrape all programs.
        
        Returns:
            List of program data with their normative ecosystems
        """
        results = []
        
        for program_key in self.programs.keys():
            try:
                program_data = self.scrape_program(program_key)
                results.append(program_data)
            except Exception as e:
                logger.error(f"Error scraping program {program_key}: {e}")
        
        return results


def main():
    """Example usage of program scraper."""
    scraper = ProgramScraper()
    
    # Scrape a specific program
    previne_data = scraper.scrape_program('previne_brasil')
    
    # Save results
    import json
    with open('data/processed/previne_brasil.json', 'w', encoding='utf-8') as f:
        json.dump(previne_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"Collected {len(previne_data['norms'])} norms for Previne Brasil")


if __name__ == '__main__':
    main()
