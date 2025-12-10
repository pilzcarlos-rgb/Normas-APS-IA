"""
Main script to run the complete data collection pipeline.

This script coordinates all three layers of data collection and 
quality assurance checks.
"""

import logging
import sys
import json
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.models import init_database
from src.scrapers import BVSMSScraper, ConsolidationParser, ProgramScraper
from src.utils import QualityChecker, build_graph_from_norms

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def ensure_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        'data',
        'data/processed',
        'data/schemas'
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    logger.info("Directories ensured")


def initialize_database():
    """Initialize the database with all tables."""
    logger.info("Initializing database...")
    engine, Session = init_database('data/normas_aps.db')
    logger.info("Database initialized successfully")
    return engine, Session


def run_layer1_collection(start_year=2010, end_year=2025):
    """
    Run Layer 1: Broad temporal sweep of BVSMS.
    
    Args:
        start_year: Starting year for collection
        end_year: Ending year for collection
    
    Returns:
        List of collected norms
    """
    logger.info(f"Starting Layer 1 collection: {start_year}-{end_year}")
    
    scraper = BVSMSScraper()
    results = scraper.scrape(start_year=start_year, end_year=end_year)
    
    # Save results
    output_file = f'data/processed/bvsms_{start_year}_{end_year}.jsonl'
    scraper.save_to_jsonl(results, output_file)
    
    logger.info(f"Layer 1 complete: {len(results)} norms collected")
    return results


def run_layer2_collection():
    """
    Run Layer 2: Parse consolidation ordinances.
    
    Returns:
        List of parsed consolidations
    """
    logger.info("Starting Layer 2 collection: Consolidations")
    
    parser = ConsolidationParser()
    results = parser.scrape()
    
    # Save results
    output_file = 'data/processed/consolidations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    logger.info(f"Layer 2 complete: {len(results)} consolidations parsed")
    return results


def run_layer3_collection():
    """
    Run Layer 3: Specialized program collection.
    
    Returns:
        List of program data
    """
    logger.info("Starting Layer 3 collection: Programs")
    
    scraper = ProgramScraper()
    results = scraper.scrape()
    
    # Save results
    output_file = 'data/processed/programs.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    logger.info(f"Layer 3 complete: {len(results)} programs collected")
    return results


def run_quality_checks(all_norms):
    """
    Run quality assurance checks on collected data.
    
    Args:
        all_norms: List of all collected norms
    
    Returns:
        Quality report dictionary
    """
    logger.info("Running quality checks...")
    
    checker = QualityChecker(all_norms)
    report = checker.run_all_checks()
    
    # Save report
    output_file = 'data/processed/quality_report.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Quality score: {report['quality_score']:.2f}%")
    
    # Log warnings and errors
    for warning in report['warnings']:
        logger.warning(warning)
    
    for error in report['errors']:
        logger.error(error)
    
    return report


def build_and_analyze_graph(all_norms):
    """
    Build the normative graph and perform analyses.
    
    Args:
        all_norms: List of all collected norms
    
    Returns:
        Graph analysis results
    """
    logger.info("Building normative graph...")
    
    graph = build_graph_from_norms(all_norms)
    
    # Perform analyses
    analysis = {
        'graph_data': graph.export_graph_data(),
        'active_norms': graph.find_active_norms(),
        'revoked_norms': graph.find_revoked_norms(),
        'consolidation_chains': graph.find_consolidation_chains(),
        'financial_timeline': [n for n in graph.get_financial_timeline()],
        'theme_clusters': graph.get_theme_clusters()
    }
    
    # Save analysis
    output_file = 'data/processed/graph_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2, default=str)
    
    logger.info(f"Graph analysis complete: {len(analysis['active_norms'])} active norms")
    return analysis


def main():
    """Main execution function."""
    start_time = datetime.now()
    logger.info("="*60)
    logger.info("Starting APS Normative Graph Collection Pipeline")
    logger.info("="*60)
    
    try:
        # Step 1: Setup
        ensure_directories()
        initialize_database()
        
        # Step 2: Data Collection (3 Layers)
        all_norms = []
        
        # Layer 1: BVSMS broad sweep
        layer1_results = run_layer1_collection(start_year=2010, end_year=2025)
        all_norms.extend(layer1_results)
        
        # Layer 2: Consolidations
        layer2_results = run_layer2_collection()
        # Extract norms from consolidation results
        # (would need actual extraction logic here)
        
        # Layer 3: Programs
        layer3_results = run_layer3_collection()
        # Extract norms from program results
        # (would need actual extraction logic here)
        
        # Step 3: Quality Assurance
        quality_report = run_quality_checks(all_norms)
        
        # Step 4: Graph Analysis
        graph_analysis = build_and_analyze_graph(all_norms)
        
        # Step 5: Summary
        duration = datetime.now() - start_time
        logger.info("="*60)
        logger.info("Pipeline Complete!")
        logger.info(f"Duration: {duration}")
        logger.info(f"Total norms collected: {len(all_norms)}")
        logger.info(f"Quality score: {quality_report['quality_score']:.2f}%")
        logger.info(f"Active norms: {len(graph_analysis['active_norms'])}")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
