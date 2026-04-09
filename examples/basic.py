"""Basic example: analyze a folder and display archetype distribution."""

import sys
from pathlib import Path

# Add parent directory to path if running as script
sys.path.insert(0, str(Path(__file__).parent.parent))

from subit_nous import build_graph, visualize_4d, export_report, export_obsidian
from subit_nous.core import subit_to_name, get_mode


def main():
    # Example: analyze the `sample_data` folder (create it if needed)
    data_dir = Path(__file__).parent / "sample_data"
    if not data_dir.exists():
        data_dir.mkdir()
        # Create a couple of example files
        (data_dir / "micro.txt").write_text(
            "I think the truth is in the east, like a spring morning. Logic and reason guide me."
        )
        (data_dir / "macro.txt").write_text(
            "We build our community in the south during summer. Our ethics and trust are strong."
        )
        (data_dir / "meso.txt").write_text(
            "You look to the west in autumn and feel the beauty of change. Art and emotion matter."
        )
        (data_dir / "meta.txt").write_text(
            "They control the north during winter with strong will and power. Their spirit prevails."
        )
        print(f"Created sample files in {data_dir}")

    print("Building knowledge graph...")
    graph = build_graph(str(data_dir))

    print(f"Graph has {len(graph.nodes())} archetypes and {graph.number_of_edges()} transitions.\n")

    # Show top 5 archetypes by frequency
    sorted_nodes = sorted(graph.nodes(data=True), key=lambda x: x[1].get("count", 0), reverse=True)
    print("Top 5 archetypes:")
    for i, (node, data) in enumerate(sorted_nodes[:5], 1):
        name = data.get("name", subit_to_name(node))
        count = data.get("count", 0)
        mode = get_mode(node)
        mode_str = f" ({mode} mode)" if mode else ""
        print(f"  {i}. {name}{mode_str} – {count} occurrences")

    # Export visualizations
    out_dir = Path("./basic_output")
    out_dir.mkdir(exist_ok=True)

    visualize_4d(graph, str(out_dir / "graph.html"))
    export_report(graph, str(out_dir / "report.md"))
    export_obsidian(graph, str(out_dir / "obsidian"))

    print(f"\nOutput saved to {out_dir}/")
    print("Open graph.html in your browser to explore the 4D knowledge graph.")


if __name__ == "__main__":
    main()