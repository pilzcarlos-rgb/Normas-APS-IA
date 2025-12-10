#!/usr/bin/env python3
"""
Script to export data from the database in various formats.

Supports export to:
- JSON (single file or JSONL)
- CSV
- HTML report
"""

import sys
import json
import csv
from pathlib import Path
from datetime import datetime
import argparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import init_database, Norm, Relationship


def export_to_json(session, output_file, pretty=True):
    """Export all norms to JSON."""
    print(f"Exporting to JSON: {output_file}")
    
    norms = session.query(Norm).all()
    norms_data = [n.to_dict() for n in norms]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        if pretty:
            json.dump(norms_data, f, ensure_ascii=False, indent=2, default=str)
        else:
            json.dump(norms_data, f, ensure_ascii=False, default=str)
    
    print(f"✓ Exported {len(norms_data)} norms to {output_file}")


def export_to_jsonl(session, output_file):
    """Export all norms to JSONL (one JSON object per line)."""
    print(f"Exporting to JSONL: {output_file}")
    
    norms = session.query(Norm).all()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for norm in norms:
            f.write(json.dumps(norm.to_dict(), ensure_ascii=False, default=str) + '\n')
    
    print(f"✓ Exported {len(norms)} norms to {output_file}")


def export_to_csv(session, output_file):
    """Export norms to CSV."""
    print(f"Exporting to CSV: {output_file}")
    
    norms = session.query(Norm).all()
    
    if not norms:
        print("⚠ No norms to export")
        return
    
    # Define CSV columns
    fieldnames = [
        'id_norma', 'tipo', 'orgao', 'numero', 'ano', 
        'data_publicacao', 'ementa', 'tema_principal', 
        'status_vigencia', 'fonte', 'url_html'
    ]
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for norm in norms:
            norm_dict = norm.to_dict()
            row = {k: norm_dict.get(k, '') for k in fieldnames}
            writer.writerow(row)
    
    print(f"✓ Exported {len(norms)} norms to {output_file}")


def export_relationships(session, output_file):
    """Export relationships to JSON."""
    print(f"Exporting relationships: {output_file}")
    
    relationships = session.query(Relationship).all()
    rel_data = [r.to_dict() for r in relationships]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rel_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✓ Exported {len(rel_data)} relationships to {output_file}")


def generate_html_report(session, output_file):
    """Generate an HTML report of the database."""
    print(f"Generating HTML report: {output_file}")
    
    norms = session.query(Norm).all()
    
    # Count by theme
    themes = {}
    for norm in norms:
        theme = norm.tema_principal or 'uncategorized'
        themes[theme] = themes.get(theme, 0) + 1
    
    # Count by year
    years = {}
    for norm in norms:
        years[norm.ano] = years.get(norm.ano, 0) + 1
    
    # Count by status
    statuses = {}
    for norm in norms:
        statuses[norm.status_vigencia] = statuses.get(norm.status_vigencia, 0) + 1
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório - Normas APS</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        h1, h2 {{ color: #0066cc; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #0066cc; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .stat {{ display: inline-block; margin: 10px 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
        .stat-value {{ font-size: 2em; color: #0066cc; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Relatório de Normas APS</h1>
    <p>Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <h2>Estatísticas Gerais</h2>
    <div class="stat">
        <div>Total de Normas</div>
        <div class="stat-value">{len(norms)}</div>
    </div>
    <div class="stat">
        <div>Normas Vigentes</div>
        <div class="stat-value">{statuses.get('vigente', 0)}</div>
    </div>
    <div class="stat">
        <div>Normas Revogadas</div>
        <div class="stat-value">{statuses.get('revogada', 0)}</div>
    </div>
    
    <h2>Distribuição por Tema</h2>
    <table>
        <tr><th>Tema</th><th>Quantidade</th></tr>
        {''.join(f'<tr><td>{theme}</td><td>{count}</td></tr>' for theme, count in sorted(themes.items(), key=lambda x: -x[1]))}
    </table>
    
    <h2>Distribuição por Ano</h2>
    <table>
        <tr><th>Ano</th><th>Quantidade</th></tr>
        {''.join(f'<tr><td>{year}</td><td>{count}</td></tr>' for year, count in sorted(years.items(), reverse=True))}
    </table>
    
    <h2>Últimas Normas Adicionadas</h2>
    <table>
        <tr><th>ID</th><th>Tipo</th><th>Número</th><th>Ano</th><th>Tema</th><th>Status</th></tr>
        {''.join(f'<tr><td>{n.id_norma}</td><td>{n.tipo}</td><td>{n.numero}</td><td>{n.ano}</td><td>{n.tema_principal or "-"}</td><td>{n.status_vigencia}</td></tr>' for n in norms[:20])}
    </table>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ HTML report generated: {output_file}")


def main():
    """Main export function."""
    parser = argparse.ArgumentParser(description='Export APS normative data')
    parser.add_argument('format', choices=['json', 'jsonl', 'csv', 'html', 'relationships', 'all'],
                        help='Export format')
    parser.add_argument('-o', '--output', help='Output file (optional)')
    parser.add_argument('--db', default='data/normas_aps.db', help='Database path')
    
    args = parser.parse_args()
    
    # Initialize database
    engine, Session = init_database(args.db)
    session = Session()
    
    # Create output directory
    Path('data/exports').mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        if args.format == 'json' or args.format == 'all':
            output_file = args.output or f'data/exports/norms_{timestamp}.json'
            export_to_json(session, output_file)
        
        if args.format == 'jsonl' or args.format == 'all':
            output_file = args.output or f'data/exports/norms_{timestamp}.jsonl'
            export_to_jsonl(session, output_file)
        
        if args.format == 'csv' or args.format == 'all':
            output_file = args.output or f'data/exports/norms_{timestamp}.csv'
            export_to_csv(session, output_file)
        
        if args.format == 'html' or args.format == 'all':
            output_file = args.output or f'data/exports/report_{timestamp}.html'
            generate_html_report(session, output_file)
        
        if args.format == 'relationships' or args.format == 'all':
            output_file = args.output or f'data/exports/relationships_{timestamp}.json'
            export_relationships(session, output_file)
        
        print("\n✓ Export complete!")
        
    finally:
        session.close()


if __name__ == '__main__':
    main()
