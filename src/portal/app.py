"""
Flask web application for the APS Normative Graph Portal.

Provides navigation by:
- Theme
- Year
- Validity status
- Official links
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)


def load_norms_data():
    """Load norms data from database or JSON file."""
    # This would connect to the actual database
    # For now, return mock structure
    return {
        'norms': [],
        'themes': [],
        'years': list(range(2010, 2026)),
        'stats': {
            'total_norms': 0,
            'active_norms': 0,
            'revoked_norms': 0
        }
    }


@app.route('/')
def index():
    """Main page with overview and navigation."""
    data = load_norms_data()
    return render_template('index.html', **data)


@app.route('/api/norms')
def api_norms():
    """
    API endpoint to get norms with filters.
    
    Query parameters:
    - theme: filter by theme
    - year: filter by year
    - status: filter by status (vigente, revogada, alterada_parcial)
    - search: search term
    """
    theme = request.args.get('theme')
    year = request.args.get('year', type=int)
    status = request.args.get('status', 'vigente')
    search = request.args.get('search', '')
    
    # This would query the actual database
    data = load_norms_data()
    
    # Apply filters
    filtered_norms = data['norms']
    
    if theme:
        filtered_norms = [n for n in filtered_norms if n.get('tema_principal') == theme]
    
    if year:
        filtered_norms = [n for n in filtered_norms if n.get('ano') == year]
    
    if status:
        filtered_norms = [n for n in filtered_norms if n.get('status_vigencia') == status]
    
    if search:
        search_lower = search.lower()
        filtered_norms = [
            n for n in filtered_norms
            if search_lower in n.get('ementa', '').lower()
            or search_lower in str(n.get('numero', '')).lower()
        ]
    
    return jsonify({
        'norms': filtered_norms,
        'total': len(filtered_norms)
    })


@app.route('/norm/<norm_id>')
def norm_detail(norm_id):
    """Display detailed information about a specific norm."""
    # This would query the database for the specific norm
    norm = {
        'id_norma': norm_id,
        'tipo': 'Portaria',
        'numero': '0000',
        'ano': 2024,
        'ementa': 'Detalhes da norma',
        'relationships': {
            'altera': [],
            'revoga': [],
            'alterada_por': []
        }
    }
    return render_template('norm_detail.html', norm=norm)


@app.route('/theme/<theme_name>')
def theme_view(theme_name):
    """View all norms for a specific theme."""
    data = load_norms_data()
    norms = [n for n in data['norms'] if n.get('tema_principal') == theme_name]
    return render_template('theme_view.html', theme=theme_name, norms=norms)


@app.route('/year/<int:year>')
def year_view(year):
    """View all norms for a specific year."""
    data = load_norms_data()
    norms = [n for n in data['norms'] if n.get('ano') == year]
    return render_template('year_view.html', year=year, norms=norms)


@app.route('/graph')
def graph_view():
    """Interactive graph visualization."""
    # This would load graph data from the analysis module
    graph_data = {
        'nodes': [],
        'edges': []
    }
    return render_template('graph.html', graph_data=graph_data)


@app.route('/search')
def search():
    """Search page."""
    return render_template('search.html')


@app.route('/about')
def about():
    """About page with methodology."""
    return render_template('about.html')


@app.route('/api/stats')
def api_stats():
    """Get statistics about the normative collection."""
    data = load_norms_data()
    return jsonify(data['stats'])


@app.route('/api/graph')
def api_graph():
    """Get graph data for visualization."""
    # This would use the graph_analysis module
    graph_data = {
        'nodes': [],
        'edges': [],
        'stats': {}
    }
    return jsonify(graph_data)


def run_portal(host='0.0.0.0', port=5000, debug=False):
    """
    Run the web portal.
    
    Args:
        host: Host address
        port: Port number
        debug: Debug mode
    """
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_portal(debug=True)
