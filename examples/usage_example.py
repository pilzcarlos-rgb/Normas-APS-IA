"""
Example script demonstrating the usage of the APS Normative Graph System.

This script shows how to:
1. Initialize the database
2. Create sample norms
3. Establish relationships
4. Perform quality checks
5. Analyze the normative graph
6. Export data
"""

from datetime import datetime
import json

# Note: This example assumes dependencies are installed
# Run: pip install -r requirements.txt

def create_sample_database():
    """Create a sample database with example norms."""
    from src.models import init_database, Norm, Relationship, Program
    
    print("="*60)
    print("Initializing Database")
    print("="*60)
    
    # Initialize database
    engine, Session = init_database('data/example_normas.db')
    session = Session()
    
    print("✓ Database initialized\n")
    
    # Create sample norms
    print("Creating sample norms...")
    
    # LC 141/2012 - Estruturante
    lc_141 = Norm(
        id_norma='LC_141_2012',
        tipo='Lei Complementar',
        orgao='Presidência',
        numero='141',
        ano=2012,
        data_publicacao=datetime(2012, 1, 13),
        ementa='Regulamenta o § 3º do art. 198 da Constituição Federal para dispor sobre os valores mínimos a serem aplicados anualmente pela União, Estados, Distrito Federal e Municípios em ações e serviços públicos de saúde',
        tema_principal='financiamento',
        status_vigencia='vigente',
        fonte='planalto',
        url_html='http://www.planalto.gov.br/ccivil_03/leis/lcp/lcp141.htm'
    )
    
    # Decreto 7.508/2011
    decreto_7508 = Norm(
        id_norma='DECRETO_7508_2011',
        tipo='Decreto',
        orgao='Presidência',
        numero='7508',
        ano=2011,
        data_publicacao=datetime(2011, 6, 28),
        ementa='Regulamenta a Lei nº 8.080, de 19 de setembro de 1990, para dispor sobre a organização do Sistema Único de Saúde - SUS, o planejamento da saúde, a assistência à saúde e a articulação interfederativa',
        tema_principal='organizacao_aps',
        status_vigencia='vigente',
        fonte='planalto',
        url_html='http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/decreto/d7508.htm'
    )
    
    # Portaria 2.979/2019 - Previne Brasil
    portaria_2979 = Norm(
        id_norma='PORTARIA_2979_2019',
        tipo='Portaria GM/MS',
        orgao='GM/MS',
        numero='2979',
        ano=2019,
        data_publicacao=datetime(2019, 11, 12),
        ementa='Institui o Programa Previne Brasil, que estabelece novo modelo de financiamento de custeio da Atenção Primária à Saúde no âmbito do Sistema Único de Saúde',
        tema_principal='financiamento',
        temas_secundarios=['organizacao_aps', 'sistemas_informacao'],
        status_vigencia='vigente',
        efeitos_financeiros_partir_de=datetime(2020, 1, 1),
        fonte='bvsms',
        url_html='https://bvsms.saude.gov.br/bvs/saudelegis/gm/2019/prt2979_12_11_2019.html'
    )
    
    # Portaria 3.493/2024 - Novo Cofinanciamento
    portaria_3493 = Norm(
        id_norma='PORTARIA_3493_2024',
        tipo='Portaria GM/MS',
        orgao='GM/MS',
        numero='3493',
        ano=2024,
        data_publicacao=datetime(2024, 11, 6),
        ementa='Institui incentivo financeiro federal de implantação, custeio e desempenho para Atenção Primária à Saúde e Estratégia de Saúde da Família',
        tema_principal='financiamento',
        status_vigencia='vigente',
        efeitos_financeiros_partir_de=datetime(2025, 1, 1),
        fonte='bvsms',
        url_html='https://bvsms.saude.gov.br/bvs/saudelegis/gm/2024/prt3493_06_11_2024.html'
    )
    
    # Portaria de Consolidação SAPS 1/2021
    consolidacao_saps = Norm(
        id_norma='PORTARIA_CONSOLIDACAO_SAPS_1_2021',
        tipo='Portaria de Consolidação SAPS',
        orgao='SAPS',
        numero='1',
        ano=2021,
        data_publicacao=datetime(2021, 1, 14),
        ementa='Consolida as normas sobre as ações e os serviços públicos de saúde do Sistema Único de Saúde, sobre Atenção Primária à Saúde',
        tema_principal='organizacao_aps',
        status_vigencia='vigente',
        fonte='consolidacao',
        url_html='https://bvsms.saude.gov.br/bvs/saudelegis/saps/2021/prt0001_14_01_2021.html'
    )
    
    # Add all norms to session
    session.add_all([lc_141, decreto_7508, portaria_2979, portaria_3493, consolidacao_saps])
    session.commit()
    
    print(f"✓ Created {session.query(Norm).count()} norms\n")
    
    # Create relationships
    print("Creating relationships...")
    
    # Portaria 3.493 altera Portaria 2.979
    rel1 = Relationship(
        source_norm_id=portaria_3493.id,
        target_norm_id=portaria_2979.id,
        relationship_type='altera',
        description='Novo modelo de cofinanciamento altera regras do Previne Brasil'
    )
    
    # Decreto 7.508 regulamenta LC 141
    rel2 = Relationship(
        source_norm_id=decreto_7508.id,
        target_norm_id=lc_141.id,
        relationship_type='regulamenta',
        description='Decreto regulamenta aspectos da lei complementar'
    )
    
    # Consolidação consolida várias normas
    rel3 = Relationship(
        source_norm_id=consolidacao_saps.id,
        target_norm_id=portaria_2979.id,
        relationship_type='consolida',
        description='Consolidação incorpora normas da APS'
    )
    
    session.add_all([rel1, rel2, rel3])
    session.commit()
    
    print(f"✓ Created {session.query(Relationship).count()} relationships\n")
    
    # Create a program
    print("Creating program...")
    
    previne_brasil = Program(
        name='Previne Brasil',
        description='Novo modelo de financiamento da Atenção Primária à Saúde',
        establishing_norm_id=portaria_2979.id,
        is_active=True,
        start_date=datetime(2020, 1, 1)
    )
    
    session.add(previne_brasil)
    session.commit()
    
    print(f"✓ Created program: {previne_brasil.name}\n")
    
    session.close()
    return 'data/example_normas.db'


def perform_quality_checks():
    """Perform quality assurance checks."""
    from src.models import init_database, Norm
    from src.utils import QualityChecker
    
    print("="*60)
    print("Quality Checks")
    print("="*60)
    
    engine, Session = init_database('data/example_normas.db')
    session = Session()
    
    # Get all norms as dictionaries
    norms = session.query(Norm).all()
    norms_dict = [n.to_dict() for n in norms]
    
    # Run quality checks
    checker = QualityChecker(norms_dict)
    report = checker.run_all_checks()
    
    print(f"\nQuality Score: {report['quality_score']:.2f}%")
    print(f"Total Norms: {report['total_norms']}")
    
    print("\nChecks:")
    for check_name, check_result in report['checks'].items():
        status = "✓" if check_result['pass'] else "✗"
        print(f"  {status} {check_name}")
    
    if report['warnings']:
        print(f"\nWarnings ({len(report['warnings'])}):")
        for warning in report['warnings']:
            print(f"  ⚠ {warning}")
    
    if report['errors']:
        print(f"\nErrors ({len(report['errors'])}):")
        for error in report['errors']:
            print(f"  ✗ {error}")
    
    print()
    session.close()


def analyze_graph():
    """Analyze the normative graph."""
    from src.models import init_database, Norm
    from src.utils import build_graph_from_norms
    
    print("="*60)
    print("Graph Analysis")
    print("="*60)
    
    engine, Session = init_database('data/example_normas.db')
    session = Session()
    
    # Get all norms
    norms = session.query(Norm).all()
    norms_dict = [n.to_dict() for n in norms]
    
    # Build graph
    graph = build_graph_from_norms(norms_dict)
    
    print(f"\nGraph Statistics:")
    print(f"  Total nodes: {len(graph.nodes)}")
    print(f"  Total edges: {sum(len(edges) for edges in graph.edges.values())}")
    
    # Active and revoked norms
    active = graph.find_active_norms()
    revoked = graph.find_revoked_norms()
    
    print(f"\nNorm Status:")
    print(f"  Active: {len(active)}")
    print(f"  Revoked: {len(revoked)}")
    
    # Theme clusters
    clusters = graph.get_theme_clusters()
    print(f"\nTheme Distribution:")
    for theme, norm_ids in clusters.items():
        print(f"  {theme}: {len(norm_ids)} norms")
    
    # Financial timeline
    financial_norms = graph.get_financial_timeline()
    if financial_norms:
        print(f"\nNorms with Financial Effects: {len(financial_norms)}")
        for norm in financial_norms[:3]:  # Show first 3
            date = norm.get('efeitos_financeiros_partir_de', 'N/A')
            print(f"  - {norm.get('id_norma')}: {date}")
    
    print()
    session.close()
    
    return graph


def export_data(graph):
    """Export data to JSON files."""
    from src.models import init_database, Norm
    
    print("="*60)
    print("Exporting Data")
    print("="*60)
    
    engine, Session = init_database('data/example_normas.db')
    session = Session()
    
    # Export all norms
    norms = session.query(Norm).all()
    norms_dict = [n.to_dict() for n in norms]
    
    with open('data/example_norms_export.json', 'w', encoding='utf-8') as f:
        json.dump(norms_dict, f, ensure_ascii=False, indent=2, default=str)
    print("✓ Exported norms to data/example_norms_export.json")
    
    # Export graph data
    graph_data = graph.export_graph_data()
    with open('data/example_graph_export.json', 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2, default=str)
    print("✓ Exported graph to data/example_graph_export.json")
    
    print()
    session.close()


def main():
    """Run the complete example."""
    print("\n" + "="*60)
    print("APS Normative Graph System - Example Usage")
    print("="*60 + "\n")
    
    try:
        # Step 1: Create sample database
        db_path = create_sample_database()
        
        # Step 2: Perform quality checks
        perform_quality_checks()
        
        # Step 3: Analyze graph
        graph = analyze_graph()
        
        # Step 4: Export data
        export_data(graph)
        
        print("="*60)
        print("Example completed successfully!")
        print("="*60)
        print("\nNext steps:")
        print("1. View the exported data in data/example_*.json")
        print("2. Explore the database: sqlite3 data/example_normas.db")
        print("3. Start the web portal: python -m src.portal.app")
        print("4. Run the full pipeline: python main.py")
        print()
        
    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease install dependencies first:")
        print("  pip install -r requirements.txt")
        print()
        return 1
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
