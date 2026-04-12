"""Generate Wikipedia-style markdown wiki from knowledge graph."""

from pathlib import Path
import networkx as nx
from typing import List, Dict, Any
from .core import subit_to_name, archetype_color, MODE_FOR_ARCHETYPE

def generate_wiki(graph: nx.Graph, output_dir: str = "wiki") -> None:
    """
    Generate a Wikipedia-style markdown wiki from the knowledge graph.
    
    Structure:
    - index.md (main navigation)
    - nodes/ (one file per archetype)
    - communities/ (one file per community)
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    
    nodes_dir = out / "nodes"
    communities_dir = out / "communities"
    nodes_dir.mkdir(exist_ok=True)
    communities_dir.mkdir(exist_ok=True)
    
    # 1. Generate main index.md
    _generate_index(graph, out)
    
    # 2. Generate individual archetype pages
    _generate_archetype_pages(graph, nodes_dir)
    
    # 3. Generate community pages
    _generate_community_pages(graph, communities_dir)
    
    print(f"[OK] Wiki generated at {output_dir}")
    print(f"   - index.md (main navigation)")
    print(f"   - nodes/ ({len(graph.nodes)} archetype pages)")
    print(f"   - communities/ (community pages)")

def _generate_index(graph: nx.Graph, output_dir: Path) -> None:
    """Generate the main index.md file."""
    index_path = output_dir / "index.md"
    
    # Count modes
    mode_counts = {"MICRO": 0, "MACRO": 0, "MESO": 0, "META": 0, "OTHER": 0}
    for node in graph.nodes:
        mode = MODE_FOR_ARCHETYPE.get(node)
        if mode:
            mode_counts[mode] += 1
        else:
            mode_counts["OTHER"] += 1
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# SUBIT-NOUS Knowledge Graph\n\n")
        f.write("## Overview\n\n")
        f.write(f"- **Total archetypes:** {len(graph.nodes)}/256\n")
        f.write(f"- **Total transitions:** {graph.number_of_edges()}\n\n")
        
        f.write("## Mode Distribution\n\n")
        f.write("| Mode | Count |\n")
        f.write("|------|-------|\n")
        for mode, count in mode_counts.items():
            f.write(f"| {mode} | {count} |\n")
        
        f.write("\n## Navigation\n\n")
        f.write("- [Browse all archetypes](nodes/index.md)\n")
        f.write("- [Browse communities](communities/index.md)\n")
        
        # Top 10 archetypes by frequency
        f.write("\n## Most Frequent Archetypes\n\n")
        freq = [(node, graph.nodes[node].get('count', 0)) for node in graph.nodes]
        freq.sort(key=lambda x: x[1], reverse=True)
        for node, count in freq[:10]:
            name = subit_to_name(node)
            f.write(f"- [{name}](nodes/{_sanitize_filename(name)}.md) (count: {count})\n")

def _generate_archetype_pages(graph: nx.Graph, nodes_dir: Path) -> None:
    """Generate individual pages for each archetype."""
    # Create index for nodes
    nodes_index = nodes_dir / "index.md"
    with open(nodes_index, 'w', encoding='utf-8') as f:
        f.write("# All Archetypes\n\n")
        f.write("| ID | Archetype | Mode | Frequency |\n")
        f.write("|----|-----------|------|-----------|\n")
        for node in sorted(graph.nodes):
            name = subit_to_name(node)
            mode = MODE_FOR_ARCHETYPE.get(node, "mixed")
            count = graph.nodes[node].get('count', 0)
            f.write(f"| {node} | [{name}]({_sanitize_filename(name)}.md) | {mode} | {count} |\n")
    
    # Create individual pages
    for node in graph.nodes:
        name = subit_to_name(node)
        node_path = nodes_dir / f"{_sanitize_filename(name)}.md"
        
        with open(node_path, 'w', encoding='utf-8') as f:
            f.write(f"# {name}\n\n")
            f.write(f"**ID:** {node}\n\n")
            f.write(f"**Binary:** `{node:08b}`\n\n")
            f.write(f"**Frequency:** {graph.nodes[node].get('count', 0)}\n\n")
            
            # Coordinates
            who_idx = (node >> 6) & 0b11
            where_idx = (node >> 4) & 0b11
            when_idx = (node >> 2) & 0b11
            mode_idx = node & 0b11
            
            who_names = ["THEY", "YOU", "ME", "WE"]
            where_names = ["NORTH", "WEST", "EAST", "SOUTH"]
            when_names = ["WINTER", "AUTUMN", "SPRING", "SUMMER"]
            mode_names = ["FORCE", "FORM", "STATE", "VALUE"]
            
            f.write("## Coordinates\n\n")
            f.write(f"- **WHO:** {who_names[who_idx]}\n")
            f.write(f"- **WHERE:** {where_names[where_idx]}\n")
            f.write(f"- **WHEN:** {when_names[when_idx]}\n")
            f.write(f"- **MODE:** {mode_names[mode_idx]}\n\n")
            
            # Connected archetypes
            neighbors = list(graph.neighbors(node))
            if neighbors:
                f.write("## Connected Archetypes\n\n")
                f.write("| Neighbor | Weight | Type | Confidence |\n")
                f.write("|----------|--------|------|------------|\n")
                for nb in sorted(neighbors):
                    nb_name = subit_to_name(nb)
                    edge_data = graph.get_edge_data(node, nb, default={})
                    weight = edge_data.get('weight', 1)
                    edge_type = edge_data.get('type', 'EXTRACTED')
                    confidence = edge_data.get('confidence', 1.0)
                    f.write(f"| [{nb_name}]({_sanitize_filename(nb_name)}.md) | {weight} | {edge_type} | {confidence} |\n")

def _generate_community_pages(graph: nx.Graph, communities_dir: Path) -> None:
    """Generate pages for graph communities (connected components)."""
    # Find connected components
    components = list(nx.connected_components(graph.to_undirected()))
    
    communities_index = communities_dir / "index.md"
    with open(communities_index, 'w', encoding='utf-8') as f:
        f.write("# Communities\n\n")
        f.write(f"Found **{len(components)}** communities in the knowledge graph.\n\n")
        
        for i, comp in enumerate(components):
            f.write(f"## Community {i+1}\n\n")
            f.write(f"**Size:** {len(comp)} archetypes\n\n")
            f.write("**Archetypes:**\n")
            for node in sorted(comp):
                name = subit_to_name(node)
                f.write(f"- [{name}](../nodes/{_sanitize_filename(name)}.md)\n")
            f.write("\n")

def _sanitize_filename(name: str) -> str:
    """Remove characters that are problematic in filenames."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name