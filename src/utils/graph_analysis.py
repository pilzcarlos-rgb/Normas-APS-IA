"""
Graph analysis utilities for the APS Normative Graph System.

Provides tools to analyze relationships between normative documents
and visualize the regulatory structure.
"""

import logging
from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class NormativeGraph:
    """
    Graph representation of normative relationships.
    
    Nodes: normative documents
    Edges: relationships (institui, altera, revoga, regulamenta, consolida)
    """
    
    def __init__(self):
        """Initialize the graph structure."""
        self.nodes = {}  # id -> norm data
        self.edges = defaultdict(list)  # source_id -> [(target_id, relationship_type)]
        self.reverse_edges = defaultdict(list)  # for backward traversal
    
    def add_norm(self, norm: Dict):
        """
        Add a normative document as a node.
        
        Args:
            norm: Dictionary with norm data
        """
        norm_id = norm.get('id_norma')
        if norm_id:
            self.nodes[norm_id] = norm
    
    def add_relationship(self, source_id: str, target_id: str, rel_type: str):
        """
        Add a relationship between two norms.
        
        Args:
            source_id: Source norm ID
            target_id: Target norm ID
            rel_type: Type of relationship
        """
        self.edges[source_id].append((target_id, rel_type))
        self.reverse_edges[target_id].append((source_id, rel_type))
    
    def get_affected_norms(self, norm_id: str) -> List[Tuple[str, str]]:
        """
        Get all norms affected by a given norm.
        
        Args:
            norm_id: ID of the norm
        
        Returns:
            List of (target_id, relationship_type) tuples
        """
        return self.edges.get(norm_id, [])
    
    def get_affecting_norms(self, norm_id: str) -> List[Tuple[str, str]]:
        """
        Get all norms that affect a given norm.
        
        Args:
            norm_id: ID of the norm
        
        Returns:
            List of (source_id, relationship_type) tuples
        """
        return self.reverse_edges.get(norm_id, [])
    
    def get_norm_lineage(self, norm_id: str) -> Dict:
        """
        Get the full lineage of a norm (what it changes and what changes it).
        
        Args:
            norm_id: ID of the norm
        
        Returns:
            Dictionary with affects/affected_by relationships
        """
        return {
            'norm': self.nodes.get(norm_id),
            'affects': self.get_affected_norms(norm_id),
            'affected_by': self.get_affecting_norms(norm_id)
        }
    
    def find_revoked_norms(self) -> List[str]:
        """
        Find all norms that have been revoked.
        
        Returns:
            List of revoked norm IDs
        """
        revoked = []
        
        for norm_id in self.nodes:
            affecting = self.get_affecting_norms(norm_id)
            for source_id, rel_type in affecting:
                if rel_type == 'revoga':
                    revoked.append(norm_id)
                    break
        
        return revoked
    
    def find_active_norms(self) -> List[str]:
        """
        Find all currently active norms.
        
        Returns:
            List of active norm IDs
        """
        revoked = set(self.find_revoked_norms())
        active = [
            norm_id for norm_id in self.nodes
            if norm_id not in revoked
        ]
        return active
    
    def find_consolidation_chains(self) -> Dict[str, List[str]]:
        """
        Find consolidation chains (which norms consolidate others).
        
        Returns:
            Dictionary mapping consolidation IDs to lists of consolidated norms
        """
        chains = defaultdict(list)
        
        for source_id, targets in self.edges.items():
            for target_id, rel_type in targets:
                if rel_type == 'consolida':
                    chains[source_id].append(target_id)
        
        return dict(chains)
    
    def get_financial_timeline(self) -> List[Dict]:
        """
        Get a timeline of norms with financial effects.
        
        Returns:
            List of norms sorted by financial effect date
        """
        financial_norms = []
        
        for norm_id, norm in self.nodes.items():
            if norm.get('efeitos_financeiros_partir_de'):
                financial_norms.append(norm)
        
        # Sort by financial effect date
        financial_norms.sort(
            key=lambda n: n.get('efeitos_financeiros_partir_de', '')
        )
        
        return financial_norms
    
    def get_theme_clusters(self) -> Dict[str, List[str]]:
        """
        Cluster norms by theme.
        
        Returns:
            Dictionary mapping themes to lists of norm IDs
        """
        clusters = defaultdict(list)
        
        for norm_id, norm in self.nodes.items():
            theme = norm.get('tema_principal', 'uncategorized')
            clusters[theme].append(norm_id)
        
        return dict(clusters)
    
    def export_graph_data(self) -> Dict:
        """
        Export graph data for visualization.
        
        Returns:
            Dictionary with nodes and edges for graph visualization
        """
        nodes_list = []
        edges_list = []
        
        # Prepare nodes
        for norm_id, norm in self.nodes.items():
            nodes_list.append({
                'id': norm_id,
                'label': f"{norm.get('tipo', '')} {norm.get('numero', '')}/{norm.get('ano', '')}",
                'type': norm.get('tipo'),
                'theme': norm.get('tema_principal'),
                'status': norm.get('status_vigencia'),
                'year': norm.get('ano')
            })
        
        # Prepare edges
        for source_id, targets in self.edges.items():
            for target_id, rel_type in targets:
                edges_list.append({
                    'source': source_id,
                    'target': target_id,
                    'type': rel_type
                })
        
        return {
            'nodes': nodes_list,
            'edges': edges_list,
            'stats': {
                'total_nodes': len(nodes_list),
                'total_edges': len(edges_list),
                'themes': list(self.get_theme_clusters().keys())
            }
        }
    
    def find_shortest_path(self, start_id: str, end_id: str) -> List[str]:
        """
        Find shortest path between two norms in the graph.
        
        Args:
            start_id: Starting norm ID
            end_id: Target norm ID
        
        Returns:
            List of norm IDs forming the path, or empty list if no path
        """
        if start_id not in self.nodes or end_id not in self.nodes:
            return []
        
        queue = deque([(start_id, [start_id])])
        visited = {start_id}
        
        while queue:
            current, path = queue.popleft()
            
            if current == end_id:
                return path
            
            # Check outgoing edges
            for target_id, _ in self.edges.get(current, []):
                if target_id not in visited:
                    visited.add(target_id)
                    queue.append((target_id, path + [target_id]))
        
        return []


def build_graph_from_norms(norms: List[Dict]) -> NormativeGraph:
    """
    Build a graph from a list of norms.
    
    Args:
        norms: List of norm dictionaries
    
    Returns:
        NormativeGraph object
    """
    graph = NormativeGraph()
    
    # Add all norms as nodes
    for norm in norms:
        graph.add_norm(norm)
    
    # Add relationships
    for norm in norms:
        source_id = norm.get('id_norma')
        
        # Process different relationship types
        for rel_type in ['altera', 'revoga', 'regulamenta', 'consolida']:
            targets = norm.get(rel_type, [])
            if isinstance(targets, list):
                for target_id in targets:
                    graph.add_relationship(source_id, target_id, rel_type)
    
    return graph


def main():
    """Example usage of graph analysis."""
    # Example with mock data
    mock_norms = [
        {
            'id_norma': 'PORTARIA_2979_2019',
            'tipo': 'Portaria',
            'numero': '2979',
            'ano': 2019,
            'tema_principal': 'financiamento',
            'status_vigencia': 'vigente'
        },
        {
            'id_norma': 'PORTARIA_3493_2024',
            'tipo': 'Portaria',
            'numero': '3493',
            'ano': 2024,
            'tema_principal': 'financiamento',
            'status_vigencia': 'vigente',
            'altera': ['PORTARIA_2979_2019']
        }
    ]
    
    graph = build_graph_from_norms(mock_norms)
    graph_data = graph.export_graph_data()
    
    import json
    print(json.dumps(graph_data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
