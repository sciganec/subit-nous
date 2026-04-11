"""Export functions: Markdown report, Obsidian vault, JSON, Cypher"""

from pathlib import Path
from collections import Counter
from typing import Dict, Any
import networkx as nx
from .core import subit_to_name, archetype_color, MODE_FOR_ARCHETYPE

def export_report(graph: nx.Graph, output_path: str = "report.md") -> None:
    """Generate a markdown report with ASCII profile of transversal modes."""
    if not graph.nodes:
        print("[WARN] No nodes to report.")
        return

    nodes = list(graph.nodes)
    total_chunks = sum(graph.nodes[n].get('count', 0) for n in nodes)

    # Count frequencies
    freq = {n: graph.nodes[n].get('count', 0) for n in nodes}
    top_archetypes = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]

    # Count transversal modes (pure MICRO/MACRO/MESO/META)
    mode_counts = {mode: 0 for mode in ["MICRO", "MACRO", "MESO", "META"]}
    for node, cnt in freq.items():
        mode = MODE_FOR_ARCHETYPE.get(node)
        if mode:
            mode_counts[mode] += cnt

    total_mode_occurrences = sum(mode_counts.values())

    # Calculate percentages for ASCII bars
    bar_length = 20
    mode_bars = {}
    for mode, cnt in mode_counts.items():
        percent = (cnt / total_mode_occurrences * 100) if total_mode_occurrences else 0
        filled = int(bar_length * percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        mode_bars[mode] = (bar, percent)

    # Build report content
    lines = []
    lines.append("# SUBIT‑NOUS Analytical Report\n")
    lines.append("## Summary\n")
    lines.append(f"- **Total archetypes found**: {len(nodes)}/256")
    lines.append(f"- **Total transitions**: {graph.number_of_edges()}")
    lines.append(f"- **Total content chunks processed**: {total_chunks}\n")

    lines.append("## Top 10 Archetypes by Frequency\n")
    for i, (node, cnt) in enumerate(top_archetypes, 1):
        name = subit_to_name(node)
        lines.append(f"{i}. **{name}** (ID {node}) — {cnt} occurrence{'s' if cnt != 1 else ''}")

    lines.append("\n## Transversal Mode Profile\n")
    for mode in ["MICRO", "MACRO", "MESO", "META"]:
        bar, percent = mode_bars[mode]
        lines.append(f"{mode:5} {bar} {percent:5.1f}%  ({mode_counts[mode]} occurrences)")

    # God nodes (highest degree)
    lines.append("\n## God Nodes (Highest Connectivity)\n")
    degrees = sorted(graph.degree, key=lambda x: x[1], reverse=True)[:5]
    for node, deg in degrees:
        name = subit_to_name(node)
        lines.append(f"- **{name}** — {deg} connections")

    # Unexpected connections (Hamming distance >= 4)
    lines.append("\n## Unexpected Connections\n")
    unexpected = []
    for u, v, data in graph.edges(data=True):
        hamming = bin(u ^ v).count('1')
        if hamming >= 4:
            unexpected.append((u, v, hamming, data.get('weight', 1)))
    if unexpected:
        for u, v, hamming, w in unexpected[:10]:
            lines.append(f"- **{subit_to_name(u)}** ↔ **{subit_to_name(v)}** (Hamming distance {hamming}, weight {w})")
    else:
        lines.append("*No strongly unexpected connections found.*")

    lines.append("\n## Suggested Questions\n")
    lines.append("1. Which transversal mode dominates your corpus?")
    lines.append("2. Are there missing archetypes that should appear?")
    lines.append("3. What explains the most frequent transitions?")
    lines.append("4. How does the archetype distribution change over time (if using versioned data)?")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"[OK] Report saved to {output_path}")

def export_obsidian(graph: nx.Graph, output_dir: str = "obsidian") -> None:
    """Export graph as Obsidian vault with one note per archetype."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Index file
    index = out / "index.md"
    with open(index, 'w', encoding='utf-8') as f:
        f.write("# SUBIT‑NOUS Knowledge Graph\n\n")
        f.write("## Archetypes found\n\n")
        for node in graph.nodes:
            name = subit_to_name(node)
            f.write(f"- [[{name}]]\n")

    # Individual archetype notes
    for node in graph.nodes:
        name = subit_to_name(node)
        note_path = out / f"{name}.md"
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(f"# {name}\n\n")
            f.write(f"**ID**: {node}\n\n")
            f.write(f"**Frequency**: {graph.nodes[node].get('count', 0)}\n\n")
            f.write("## Connected archetypes\n\n")
            for neighbor in graph.neighbors(node):
                nb_name = subit_to_name(neighbor)
                weight = graph[node][neighbor].get('weight', 1)
                f.write(f"- [[{nb_name}]] (weight {weight})\n")

    print(f"[OK] Obsidian vault exported to {output_dir}")