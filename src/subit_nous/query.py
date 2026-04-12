"""Query the SUBIT knowledge graph for paths, connections, and explanations."""

import networkx as nx
from typing import List, Dict, Any, Optional, Tuple
from .core import subit_to_name

def find_path(graph: nx.Graph, start_node: int, target_node: int) -> Optional[List[int]]:
    """
    Find the shortest path between two archetypes in the graph.
    Returns a list of node IDs or None if no path exists.
    """
    try:
        path = nx.shortest_path(graph, source=start_node, target=target_node)
        return path
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None

def find_all_paths(graph: nx.Graph, start_node: int, target_node: int, max_depth: int = 3) -> List[List[int]]:
    """
    Find all simple paths between two archetypes up to a maximum depth.
    """
    try:
        paths = list(nx.all_simple_paths(graph, source=start_node, target=target_node, cutoff=max_depth))
        return paths
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return []

def get_node_info(graph: nx.Graph, node_id: int) -> Dict[str, Any]:
    """Get all information about a specific archetype node."""
    if node_id not in graph.nodes:
        return {"error": f"Node {node_id} not found in graph"}
    
    neighbors = []
    for neighbor in graph.neighbors(node_id):
        edge_data = graph.get_edge_data(node_id, neighbor)
        neighbors.append({
            "id": neighbor,
            "name": subit_to_name(neighbor),
            "weight": edge_data.get('weight', 1) if edge_data else 1,
            "type": edge_data.get('type', 'EXTRACTED') if edge_data else 'EXTRACTED'
        })
    
    return {
        "id": node_id,
        "name": subit_to_name(node_id),
        "bits": f"{node_id:08b}",
        "count": graph.nodes[node_id].get('count', 0),
        "neighbors": sorted(neighbors, key=lambda x: x['weight'], reverse=True)[:10],
        "degree": len(neighbors)
    }

def find_common_connections(graph: nx.Graph, node1: int, node2: int) -> List[int]:
    """Find archetypes that are connected to both given nodes."""
    try:
        neighbors1 = set(graph.neighbors(node1))
        neighbors2 = set(graph.neighbors(node2))
        common = neighbors1.intersection(neighbors2)
        return list(common)
    except nx.NodeNotFound:
        return []

def format_path_result(path: List[int]) -> str:
    """Format a path of node IDs into a human-readable string."""
    if not path:
        return "No path found."
    
    result = []
    for i, node in enumerate(path):
        result.append(f"{i+1}. {subit_to_name(node)} (ID: {node})")
        if i < len(path) - 1:
            result.append("   ↓")
    return "\n".join(result)

# Додайте цю функцію до `query.py`
def get_edge_info(graph: nx.Graph, u: int, v: int) -> Dict[str, Any]:
    """Get metadata for the edge between two nodes."""
    edge_data = graph.get_edge_data(u, v)
    if edge_data:
        return {
            "weight": edge_data.get('weight', 1),
            "type": edge_data.get('type', 'UNKNOWN'),
            "confidence": edge_data.get('confidence', 0.0)
        }
    return None

# Оновіть функцію format_path_result, щоб включити цю інформацію
def format_path_result_with_metadata(graph: nx.Graph, path: List[int]) -> str:
    """Format a path with edge metadata."""
    if not path:
        return "No path found."
    
    result = []
    for i, node in enumerate(path):
        result.append(f"{i+1}. {subit_to_name(node)} (ID: {node})")
        if i < len(path) - 1:
            edge_info = get_edge_info(graph, node, path[i+1])
            if edge_info:
                result.append(f"   └─[ {edge_info['type']} (confidence: {edge_info['confidence']}) weight:{edge_info['weight']} ]")
            else:
                result.append("   └─[ connection ]")
    return "\n".join(result)

def format_path_result_with_metadata(graph: nx.Graph, path: List[int]) -> str:
    """Format a path with edge metadata (type, confidence, weight)."""
    if not path:
        return "No path found."
    
    result = []
    for i, node in enumerate(path):
        result.append(f"{i+1}. {subit_to_name(node)} (ID: {node})")
        if i < len(path) - 1:
            edge_data = graph.get_edge_data(node, path[i+1])
            if edge_data:
                edge_type = edge_data.get('type', 'UNKNOWN')
                confidence = edge_data.get('confidence', 0.0)
                weight = edge_data.get('weight', 1)
                result.append(f"   └─[ {edge_type} (confidence: {confidence}) weight: {weight} ]")
            else:
                result.append("   └─[ connection ]")
    return "\n".join(result)

def explain_node(graph: nx.Graph, node_id: int, text: str = None) -> Dict[str, Any]:
    """
    Explain why a text or node was classified as a specific archetype.
    Returns reasoning with contributing markers and confidence.
    """
    from .core import text_to_subit, subit_to_name, MARKERS, _detect_dimension
    
    if text:
        # Analyze text directly
        subit = text_to_subit(text)
        name = subit_to_name(subit)
        
        # Get marker contributions for each dimension
        contributions = {}
        for dim in ['WHO', 'WHERE', 'WHEN', 'WHY']:
            bits = _detect_dimension(text.lower(), MARKERS[dim], dim)
            # Find which markers matched
            matched = []
            for marker_bits, words in MARKERS[dim].items():
                if marker_bits == bits:
                    for w in words:
                        if w in text.lower():
                            matched.append(w)
            contributions[dim] = {
                "bits": bits,
                "matched_markers": matched[:5]  # Top 5 matches
            }
        
        return {
            "node_id": subit,
            "archetype": name,
            "bits": f"{subit:08b}",
            "confidence": 1.0,
            "contributions": contributions,
            "is_from_graph": False
        }
    else:
        # Analyze node from graph
        if node_id not in graph.nodes:
            return {"error": f"Node {node_id} not found in graph"}
        
        name = subit_to_name(node_id)
        return {
            "node_id": node_id,
            "archetype": name,
            "bits": f"{node_id:08b}",
            "frequency": graph.nodes[node_id].get('count', 0),
            "neighbors": list(graph.neighbors(node_id))[:10],
            "is_from_graph": True
        }