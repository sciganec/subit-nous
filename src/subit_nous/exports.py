"""Export knowledge graph to Obsidian vault, Markdown report, and JSON."""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from collections import Counter

import networkx as nx

from .core import subit_to_name, archetype_color, get_mode


def export_obsidian(graph: nx.Graph, output_dir: str = "nous_obsidian") -> None:
    """
    Export graph as an Obsidian vault.

    - Creates an index.md with navigation by transversal modes.
    - Creates one markdown file per archetype (by ID), with backlinks.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Index file
    index = out_path / "index.md"
    with open(index, "w", encoding="utf-8") as f:
        f.write("# SUBIT‑NOUS Knowledge Vault\n\n")
        f.write("## Transversal Modes\n\n")
        for mode, mode_name in [("MICRO", "MICRO"), ("MACRO", "MACRO"), ("MESO", "MESO"), ("META", "META")]:
            f.write(f"### {mode_name}\n")
            # Find archetypes that are exactly the corner (or belong to that mode's corner)
            # In Obsidian we simply list the special corners and all others grouped by WHY perhaps.
        f.write("\n### All Archetypes\n\n")
        f.write("| ID | Name | Count | Color |\n")
        f.write("|----|------|-------|-------|\n")
        for node, data in sorted(graph.nodes(data=True), key=lambda x: x[0]):
            name = data.get("name", subit_to_name(node))
            count = data.get("count", 0)
            color = archetype_color(node)
            f.write(f"| {node} | {name} | {count} | {color} |\n")
        f.write("\n## Navigation\n\n")
        for node in graph.nodes():
            f.write(f"- [[{node}.md]]\n")

    # Individual archetype pages
    for node, data in graph.nodes(data=True):
        page = out_path / f"{node}.md"
        name = data.get("name", subit_to_name(node))
        count = data.get("count", 0)
        color = archetype_color(node)

        with open(page, "w", encoding="utf-8") as f:
            f.write(f"# {name}\n\n")
            f.write(f"- **ID**: {node}\n")
            f.write(f"- **Count**: {count}\n")
            f.write(f"- **Color**: {color}\n")
            mode = get_mode(node)
            if mode:
                f.write(f"- **Transversal Mode**: {mode}\n")
            f.write("\n## Connected Archetypes\n\n")
            neighbors = list(graph.neighbors(node))
            if neighbors:
                for nb in neighbors:
                    nb_name = graph.nodes[nb].get("name", subit_to_name(nb))
                    weight = graph.get_edge_data(node, nb, {}).get("weight", 1)
                    f.write(f"- [[{nb}.md]] (weight {weight})\n")
            else:
                f.write("*No connections*\n")

    print(f"✅ Obsidian vault exported to {out_path}")


def export_report(graph: nx.Graph, output_file: str = "nous_report.md") -> None:
    """Generate a markdown report with statistics, top archetypes, and insights."""
    if len(graph.nodes()) == 0:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# SUBIT‑NOUS Report\n\nNo archetypes found.\n")
        return

    # Counts
    total_nodes = graph.number_of_nodes()
    total_edges = graph.number_of_edges()
    total_counts = sum(data.get("count", 0) for _, data in graph.nodes(data=True))

    # Top archetypes by count
    sorted_nodes = sorted(graph.nodes(data=True), key=lambda x: x[1].get("count", 0), reverse=True)
    top10 = [(node, data.get("count", 0), data.get("name", subit_to_name(node))) for node, data in sorted_nodes[:10]]

    # Mode distribution (for corner archetypes)
    mode_counts = Counter()
    for node in graph.nodes():
        mode = get_mode(node)
        if mode:
            mode_counts[mode] += graph.nodes[node].get("count", 0)

    # God nodes (high degree)
    degrees = dict(graph.degree())
    god_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# SUBIT‑NOUS Analytical Report\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Total archetypes found**: {total_nodes}/256\n")
        f.write(f"- **Total transitions**: {total_edges}\n")
        f.write(f"- **Total content chunks processed**: {total_counts}\n\n")

        f.write("## Top 10 Archetypes by Frequency\n\n")
        for i, (node, cnt, name) in enumerate(top10, 1):
            f.write(f"{i}. **{name}** (ID {node}) — {cnt} occurrences\n")
        f.write("\n")

        if mode_counts:
            f.write("## Transversal Mode Distribution\n\n")
            for mode in ["MICRO", "MACRO", "MESO", "META"]:
                cnt = mode_counts.get(mode, 0)
                f.write(f"- **{mode}**: {cnt} occurrences\n")
            f.write("\n")

        f.write("## God Nodes (Highest Connectivity)\n\n")
        for node, deg in god_nodes:
            name = graph.nodes[node].get("name", subit_to_name(node))
            f.write(f"- **{name}** — {deg} connections\n")
        f.write("\n")

        f.write("## Unexpected Connections\n\n")
        # Find edges between distant archetypes (Hamming distance > 3)
        unexpected = []
        for u, v, data in graph.edges(data=True):
            hamming = bin(u ^ v).count("1")
            if hamming >= 6:  # very different
                weight = data.get("weight", 1)
                unexpected.append((u, v, hamming, weight))
        unexpected = sorted(unexpected, key=lambda x: x[3], reverse=True)[:10]
        if unexpected:
            for u, v, hamming, w in unexpected:
                u_name = graph.nodes[u].get("name", subit_to_name(u))
                v_name = graph.nodes[v].get("name", subit_to_name(v))
                f.write(f"- **{u_name}** → **{v_name}** (Hamming distance {hamming}, weight {w})\n")
        else:
            f.write("*No strongly unexpected connections found.*\n\n")

        f.write("## Suggested Questions\n\n")
        f.write("1. Which transversal mode dominates your corpus?\n")
        f.write("2. Are there missing archetypes that should appear?\n")
        f.write("3. What explains the most frequent transitions?\n")
        f.write("4. How does the archetype distribution change over time (if using versioned data)?\n")

    print(f"✅ Report saved to {output_file}")


def export_json(graph: nx.Graph, output_file: str = "nous_graph.json") -> None:
    """Export graph as JSON (node‑link data)."""
    data = nx.node_link_data(graph)
    # Convert to serializable format (weights, etc., are already numbers)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ JSON graph exported to {output_file}")