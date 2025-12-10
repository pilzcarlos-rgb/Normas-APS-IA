"""
Layer 1 Scraper: Broad temporal sweep of BVSMS (2010-2025)

This scraper performs a comprehensive search across years and key terms
to ensure no relevant normative documents are missed.
"""

from typing import List, Dict, Optional
import logging
from datetime import datetime
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class BVSMSScraper(BaseScraper):
    """
    Scraper for Biblioteca Virtual em Saúde MS (BVSMS).
    Implements Layer 1 of the collection strategy.
    """
    
    def __init__(self):
        super().__init__(base_url='https://bvsms.saude.gov.br/bvs/saudelegis')
        
        # Key search terms for APS
        self.search_terms = [
            "Atenção Básica",
            "Atenção Primária",
            "ESF",
            "eAP",
            "eSB",
            "ACS",
            "ACE",
            "SISAB",
            "e-SUS",
            "Informatiza APS",
            "PMAQ",
            "Previne Brasil",
            "financiamento",
            "capitação",
            "desempenho",
            "equidade",
            "vínculo"
        ]
    
    def scrape_by_year(self, year: int, search_term: str) -> List[Dict]:
        """
        Scrape BVSMS for a specific year and search term.
        
        Args:
            year: Year to search
            search_term: Search term to use
        
        Returns:
            List of found normative documents
        """
        results = []
        
        logger.info(f"Searching BVSMS for '{search_term}' in {year}")
        
        # Note: This is a template. The actual BVSMS API/interface would need
        # to be studied and implemented based on their actual structure.
        # This demonstrates the intended functionality.
        
        # Construct search URL
        search_url = f"{self.base_url}/search"
        params = {
            'q': search_term,
            'year': year,
            'type': 'portaria'
        }
        
        # Example structure - would need to be adapted to actual BVSMS
        soup = self.get_page(search_url, params)
        if not soup:
            return results
        
        # Parse results (structure depends on actual BVSMS layout)
        # This is a template showing what data should be captured
        for result_item in soup.find_all('div', class_='result-item'):
            try:
                norm_data = self._extract_norm_data(result_item)
                if norm_data:
                    results.append(norm_data)
            except Exception as e:
                logger.error(f"Error parsing result: {e}")
        
        return results
    
    def _extract_norm_data(self, element) -> Optional[Dict]:
        """
        Extract normative document data from HTML element.
        
        Args:
            element: BeautifulSoup element containing norm data
        
        Returns:
            Dictionary with norm data or None
        """
        # Template for data extraction
        # Actual implementation would depend on BVSMS structure
        try:
            data = {
                'fonte': 'bvsms',
                'tipo': element.find('span', class_='tipo').text.strip(),
                'numero': element.find('span', class_='numero').text.strip(),
                'orgao': element.find('span', class_='orgao').text.strip(),
                'data_publicacao': element.find('span', class_='data').text.strip(),
                'ementa': element.find('div', class_='ementa').text.strip(),
                'url_html': element.find('a', class_='link-html')['href'],
                'url_pdf': element.find('a', class_='link-pdf')['href'] if element.find('a', class_='link-pdf') else None,
                'collected_at': datetime.now().isoformat()
            }
            return data
        except Exception as e:
            logger.error(f"Error extracting norm data: {e}")
            return None
    
    def scrape(self, start_year: int = 2010, end_year: int = 2025) -> List[Dict]:
        """
        Execute comprehensive scraping across all years and search terms.
        
        Args:
            start_year: Starting year for search
            end_year: Ending year for search
        
        Returns:
            List of all found normative documents
        """
        all_results = []
        
        for year in range(start_year, end_year + 1):
            for term in self.search_terms:
                results = self.scrape_by_year(year, term)
                all_results.extend(results)
                logger.info(f"Found {len(results)} results for '{term}' in {year}")
        
        # Remove duplicates based on URL or unique identifier
        unique_results = self._deduplicate_results(all_results)
        logger.info(f"Total unique results: {len(unique_results)}")
        
        return unique_results
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """
        Remove duplicate entries from results.
        
        Args:
            results: List of norm dictionaries
        
        Returns:
            Deduplicated list
        """
        seen_urls = set()
        unique = []
        
        for result in results:
            url = result.get('url_html')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique.append(result)
        
        return unique


def main():
    """Example usage of BVSMS scraper."""
    scraper = BVSMSScraper()
    
    # Test with a single year first
    results = scraper.scrape(start_year=2024, end_year=2024)
    
    # Save results
    scraper.save_to_jsonl(results, 'data/processed/bvsms_2024.jsonl')
    
    print(f"Collected {len(results)} normative documents from BVSMS")


if __name__ == '__main__':
    main()
