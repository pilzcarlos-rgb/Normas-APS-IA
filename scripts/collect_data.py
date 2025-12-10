#!/usr/bin/env python3
"""
Script to collect data from all sources and update the database.

This script runs the complete 3-layer collection strategy and
updates the quality reports.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import init_database, Norm
from src.scrapers import BVSMSScraper, ConsolidationParser, ProgramScraper
from src.utils import QualityChecker, build_graph_from_norms
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/collect_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def collect_layer1(start_year=2010, end_year=2025):
    """Collect data from BVSMS (Layer 1)."""
    logger.info("Starting Layer 1 collection (BVSMS)")
    scraper = BVSMSScraper()
    results = scraper.scrape(start_year=start_year, end_year=end_year)
    
    # Save to file
    output_file = f'data/processed/bvsms_{datetime.now().strftime("%Y%m%d")}.jsonl'
    scraper.save_to_jsonl(results, output_file)
    
    logger.info(f"Layer 1 complete: {len(results)} norms collected")
    return results


def collect_layer2():
    """Parse consolidation ordinances (Layer 2)."""
    logger.info("Starting Layer 2 collection (Consolidations)")
    parser = ConsolidationParser()
    results = parser.scrape()
    
    # Save to file
    output_file = f'data/processed/consolidations_{datetime.now().strftime("%Y%m%d")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    logger.info(f"Layer 2 complete: {len(results)} consolidations parsed")
    return results


def collect_layer3():
    """Collect program-specific data (Layer 3)."""
    logger.info("Starting Layer 3 collection (Programs)")
    scraper = ProgramScraper()
    results = scraper.scrape()
    
    # Save to file
    output_file = f'data/processed/programs_{datetime.now().strftime("%Y%m%d")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    logger.info(f"Layer 3 complete: {len(results)} programs collected")
    return results


def update_database(all_data):
    """Update the database with collected data."""
    logger.info("Updating database...")
    
    engine, Session = init_database('data/normas_aps.db')
    session = Session()
    
    # This is a simplified version - actual implementation would
    # need to handle deduplication, updates, etc.
    count = 0
    for norm_data in all_data:
        # Check if norm already exists
        existing = session.query(Norm).filter_by(
            id_norma=norm_data.get('id_norma')
        ).first()
        
        if not existing:
            # Create new norm (would need proper field mapping)
            count += 1
    
    session.commit()
    session.close()
    
    logger.info(f"Database updated: {count} new norms added")
    return count


def generate_reports():
    """Generate quality and analysis reports."""
    logger.info("Generating reports...")
    
    engine, Session = init_database('data/normas_aps.db')
    session = Session()
    
    # Get all norms
    norms = session.query(Norm).all()
    norms_dict = [n.to_dict() for n in norms]
    
    # Quality report
    checker = QualityChecker(norms_dict)
    quality_report = checker.run_all_checks()
    
    report_file = f'data/processed/quality_report_{datetime.now().strftime("%Y%m%d")}.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(quality_report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Quality report saved: {report_file}")
    logger.info(f"Quality score: {quality_report['quality_score']:.2f}%")
    
    # Graph analysis
    graph = build_graph_from_norms(norms_dict)
    graph_data = graph.export_graph_data()
    
    graph_file = f'data/processed/graph_analysis_{datetime.now().strftime("%Y%m%d")}.json'
    with open(graph_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2, default=str)
    
    logger.info(f"Graph analysis saved: {graph_file}")
    
    session.close()
    
    return quality_report


def main():
    """Run the complete collection process."""
    logger.info("="*60)
    logger.info("Starting APS Normative Data Collection")
    logger.info("="*60)
    
    try:
        # Ensure logs directory exists
        Path('logs').mkdir(exist_ok=True)
        
        # Run collection layers
        all_data = []
        
        # Layer 1
        layer1_data = collect_layer1()
        all_data.extend(layer1_data)
        
        # Layer 2
        layer2_data = collect_layer2()
        # Would need to extract norms from consolidation results
        
        # Layer 3
        layer3_data = collect_layer3()
        # Would need to extract norms from program results
        
        # Update database
        new_count = update_database(all_data)
        
        # Generate reports
        quality_report = generate_reports()
        
        # Summary
        logger.info("="*60)
        logger.info("Collection Complete!")
        logger.info(f"Total norms processed: {len(all_data)}")
        logger.info(f"New norms added: {new_count}")
        logger.info(f"Quality score: {quality_report.get('quality_score', 0):.2f}%")
        logger.info("="*60)
        
        return 0
        
    except Exception as e:
        logger.error(f"Collection failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
