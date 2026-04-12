#!/usr/bin/env python3
"""SUBIT-NOUS CLI: analyze, watch, serve, hooks, export, soft, control, query"""

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from typing import Optional, List
import json
import numpy as np
import networkx as nx

from .graph import build_graph, visualize_4d
from .exports import export_report, export_obsidian
from .core import text_to_soft, soft_to_hard, subit_to_name, cosine_similarity, interpolate_soft, text_to_subit
from .agent import run_agent, classify_and_run
from .search import search, index_folder
from .subit_algebra import Subit
from .query import find_path, find_all_paths, get_node_info, find_common_connections, format_path_result_with_metadata

# Version
__version__ = "4.0.0"

app = typer.Typer(help="🧠 SUBIT-NOUS: Knowledge from chaos (MICRO/MACRO/MESO/META)")
console = Console()


@app.command()
def version():
    """Show version."""
    console.print(f"SUBIT-NOUS version {__version__}")


@app.command()
def apply(
    text: str = typer.Argument(..., help="Input text to transform"),
    mode: str = typer.Option("auto", "--mode", "-m", help="STATE, VALUE, FORM, FORCE, or auto"),
    who: str = typer.Option("auto", "--who", "-w", help="ME, WE, YOU, THEY, or auto"),
    model: str = typer.Option("llama3.2:3b", "--model", help="Ollama model name"),
):
    """Apply SUBIT control to transform text into target semantic style."""
    from .control import apply_subit
    from .core import text_to_subit
    from .subit_algebra import Subit

    # Mode mapping
    mode_map = {"STATE": 2, "VALUE": 3, "FORM": 1, "FORCE": 0}
    who_map = {"ME": 2, "WE": 3, "YOU": 1, "THEY": 0}

    # Handle different combinations
    if mode == "auto" and who == "auto":
        # Auto-detect from text
        bits = text_to_subit(text)
        target = Subit(bits)
        detected_mode = {2: "STATE", 3: "VALUE", 1: "FORM", 0: "FORCE"}.get(target.project("MODE"), "STATE")
        detected_who = {2: "ME", 3: "WE", 1: "YOU", 0: "THEY"}.get(target.project("WHO"), "ME")
        console.print(f"[dim]Auto-detected: mode={detected_mode}, who={detected_who}[/dim]")
    elif mode != "auto" and who == "auto":
        # Only mode specified, use default WHO (ME)
        mode_bits = mode_map.get(mode.upper(), 2)
        target = Subit.from_coords(who=2, where=2, when=2, mode=mode_bits)
        console.print(f"[dim]Using mode={mode}, who=ME (default)[/dim]")
    elif who != "auto" and mode == "auto":
        # Only who specified, use default MODE (STATE)
        who_bits = who_map.get(who.upper(), 2)
        target = Subit.from_coords(who=who_bits, where=2, when=2, mode=2)
        console.print(f"[dim]Using who={who}, mode=STATE (default)[/dim]")
    else:
        # Both specified
        mode_bits = mode_map.get(mode.upper(), 2)
        who_bits = who_map.get(who.upper(), 2)
        target = Subit.from_coords(who=who_bits, where=2, when=2, mode=mode_bits)

    console.print(f"[bold blue]🎮 Applying SUBIT control...[/]")
    console.print(f"[dim]Target: {target.to_human()} (bits={target.bits:08b})[/dim]")

    result = apply_subit(text, target, model)
    console.print("\n[bold green]Result:[/]")
    console.print(result)


@app.command()
def index(
    path: str = typer.Argument(..., help="Folder to index"),
    chunk_size: int = typer.Option(1000, "--chunk-size", "-c", help="Text chunk size"),
):
    """Index a folder for fast search."""
    from .search import index_folder
    console.print(f"[bold blue]Indexing[/] {path} ...")
    count = index_folder(path, chunk_size)
    console.print(f"[green]Indexed {count} documents.[/green]")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    mode: Optional[str] = typer.Option(None, "--mode", help="STATE, VALUE, FORM, FORCE"),
    who: Optional[str] = typer.Option(None, "--who", help="ME, WE, YOU, THEY"),
    where: Optional[str] = typer.Option(None, "--where", help="EAST, SOUTH, WEST, NORTH"),
    when: Optional[str] = typer.Option(None, "--when", help="SPRING, SUMMER, AUTUMN, WINTER"),
    top_k: int = typer.Option(10, "--top", "-k", help="Number of results"),
    alpha: float = typer.Option(0.5, "--alpha", help="Weight for semantic similarity (0..1)"),
):
    """Hybrid search: SUBIT filter + cosine similarity."""
    from .search import search as search_func
    results = search_func(query, mode=mode, who=who, where=where, when=when, top_k=top_k, alpha=alpha)
    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return
    console.print(f"\n[bold cyan]Top {len(results)} results:[/bold cyan]\n")
    for i, r in enumerate(results, 1):
        mode_name = {2:"STATE",3:"VALUE",1:"FORM",0:"FORCE"}.get(r["mode"], "?")
        who_name = {2:"ME",3:"WE",1:"YOU",0:"THEY"}.get(r["who"], "?")
        console.print(f"{i}. [bold]{r['path']}[/bold]")
        console.print(f"   Score: {r['score']:.3f} (sim={r['similarity']:.3f}) | {mode_name} / {who_name}")


@app.command()
def analyze(
    path: str = typer.Argument(..., help="Folder to analyze"),
    output: str = typer.Option("./nous_output", "--output", "-o", help="Output directory"),
    chunk_size: int = typer.Option(1000, "--chunk-size", "-c", help="Text chunk size in characters"),
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch mode (auto-update on changes)"),
    api: bool = typer.Option(False, "--api", help="Start API server after analysis"),
):
    """Build knowledge graph from any folder."""
    console.print(f"[bold blue]NOUS[/] analyzing {path} ...")
    console.print("Building graph...")
    graph = build_graph(path, chunk_size=chunk_size)
    console.print(f"[bold]Graph built:[/] {len(graph.nodes)} archetypes, {graph.number_of_edges()} transitions")
    out_path = Path(output)
    out_path.mkdir(parents=True, exist_ok=True)
    visualize_4d(graph, str(out_path / "graph.html"))
    export_report(graph, str(out_path / "report.md"))
    export_obsidian(graph, str(out_path / "obsidian"))
    console.print(f"[green]Done![/] Open {out_path / 'graph.html'}")
    if watch:
        console.print("[yellow]Watch mode not yet implemented in CLI, use `nous watch` separately.[/]")
    if api:
        console.print("[yellow]Starting API server...[/]")
        serve(port=8000)


@app.command()
def watch(
    path: str = typer.Argument(..., help="Folder to watch"),
    output: str = typer.Option("./nous_output", "--output", "-o", help="Output directory"),
    chunk_size: int = typer.Option(1000, "--chunk-size", "-c", help="Text chunk size"),
    debounce_docs: int = typer.Option(2000, "--debounce", help="Debounce delay for docs in milliseconds"),
):
    """Watch folder for changes and smartly update the knowledge graph."""
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import time

    # Класифікація файлів за типом
    CODE_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.java', '.c', '.cpp', '.h'}
    DOC_EXTENSIONS = {'.md', '.txt', '.rst', '.pdf', '.docx'}

    class SmartHandler(FileSystemEventHandler):
        def __init__(self):
            self.last_triggered = 0
            self.pending_update = False

        def on_modified(self, event):
            if event.is_directory:
                return

            file_ext = Path(event.src_path).suffix.lower()
            
            # Якщо це кодовий файл - оновлюємо миттєво
            if file_ext in CODE_EXTENSIONS:
                console.print(f"[dim]Code change detected: {Path(event.src_path).name}[/dim]")
                self._update_graph()
            
            # Якщо це документ - використовуємо затримку (debounce)
            elif file_ext in DOC_EXTENSIONS:
                current_time = time.time() * 1000  # milliseconds
                if current_time - self.last_triggered > debounce_docs:
                    console.print(f"[dim]Doc change detected: {Path(event.src_path).name}. Waiting {debounce_docs/1000}s for stable state...[/dim]")
                
                self.last_triggered = current_time
                if not self.pending_update:
                    self.pending_update = True
                    # Запускаємо таймер для відкладеного оновлення
                    import threading
                    timer = threading.Timer(debounce_docs / 1000.0, self._delayed_update)
                    timer.daemon = True
                    timer.start()

        def _delayed_update(self):
            self.pending_update = False
            self._update_graph()

        def _update_graph(self):
            graph = build_graph(path, chunk_size=chunk_size)
            out_path = Path(output)
            out_path.mkdir(parents=True, exist_ok=True)
            visualize_4d(graph, str(out_path / "graph.html"))
            export_report(graph, str(out_path / "report.md"))
            export_obsidian(graph, str(out_path / "obsidian"))
            console.print("[green]✅ Graph updated.[/green]")

    console.print(f"[bold blue]👀 Smart watching[/] {path} (press Ctrl+C to stop)")
    console.print("[dim]Code files update instantly. Docs wait for changes to settle.[/dim]")
    event_handler = SmartHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@app.command()
def serve(
    port: int = typer.Option(8000, "--port", "-p", help="Port for API server"),
):
    """Start REST API + WebSocket server."""
    import uvicorn
    from subit_nous.api import app as api_app
    console.print(f"[bold blue]Starting SUBIT-NOUS API on http://0.0.0.0:{port}[/]")
    uvicorn.run(api_app, host="0.0.0.0", port=port)


@app.command()
def hooks(
    action: str = typer.Argument("install", help="install or uninstall"),
    repo_path: str = typer.Option(".", "--repo", "-r", help="Git repository path"),
):
    """Install or uninstall Git hooks for auto-analysis on commit."""
    hooks_dir = Path(repo_path) / ".git" / "hooks"
    if action == "install":
        hooks_dir.mkdir(parents=True, exist_ok=True)
        post_commit = hooks_dir / "post-commit"
        post_commit.write_text(f"""#!/bin/sh
nous analyze {repo_path} --output {repo_path}/nous_output
""")
        post_commit.chmod(0o755)
        console.print(f"[green]Git post-commit hook installed in {hooks_dir}[/]")
    elif action == "uninstall":
        hook = hooks_dir / "post-commit"
        if hook.exists():
            hook.unlink()
            console.print(f"[yellow]Removed post-commit hook[/]")
        else:
            console.print("[yellow]No post-commit hook found.[/]")
    else:
        console.print(f"[red]Unknown action: {action}. Use 'install' or 'uninstall'.[/]")


@app.command()
def export(
    graph_file: str = typer.Argument(..., help="Path to JSON graph file (from /graph/export)"),
    format: str = typer.Option("obsidian", "--format", "-f", help="obsidian, json, cypher"),
    output: str = typer.Option("./export", "--output", "-o", help="Output directory or file"),
):
    """Export graph to different formats (experimental)."""
    import networkx as nx
    with open(graph_file, 'r') as f:
        data = json.load(f)
    G = nx.node_link_graph(data)
    if format == "obsidian":
        export_obsidian(G, output)
    elif format == "json":
        with open(output, 'w') as f:
            json.dump(data, f, indent=2)
        console.print(f"JSON exported to {output}")
    elif format == "cypher":
        cypher_lines = []
        for node in G.nodes:
            name = G.nodes[node].get('name', str(node))
            cypher_lines.append(f"CREATE (a:{name.replace(' ', '_')} {{id: {node}}})")
        for u, v in G.edges:
            cypher_lines.append(f"MATCH (a {{id: {u}}}), (b {{id: {v}}}) CREATE (a)-[:TRANSITIONS]->(b)")
        Path(output).write_text("\n".join(cypher_lines))
        console.print(f"Cypher exported to {output}")
    else:
        console.print(f"[red]Unknown format: {format}[/]")


@app.command()
def soft(
    path: Optional[str] = typer.Argument(None, help="Folder to analyze (for average profile)"),
    output: str = typer.Option("./soft_output.json", "--output", "-o", help="Output JSON file"),
    chunk_size: int = typer.Option(1000, "--chunk-size", "-c", help="Text chunk size"),
    sim1: Optional[str] = typer.Option(None, "--sim1", help="First file for cosine similarity"),
    sim2: Optional[str] = typer.Option(None, "--sim2", help="Second file for cosine similarity"),
    interp1: Optional[str] = typer.Option(None, "--interp1", help="First file for interpolation"),
    interp2: Optional[str] = typer.Option(None, "--interp2", help="Second file for interpolation"),
    alpha: float = typer.Option(0.5, "--alpha", help="Interpolation weight (0..1)"),
    radar: Optional[str] = typer.Option(None, "--radar", help="Generate radar chart from a soft JSON file"),
):
    """Compute soft archetype vectors, similarity, interpolation, radar chart."""
    # Radar chart from existing JSON
    if radar:
        with open(radar, 'r') as f:
            data = json.load(f)
        avg_soft = np.array(data.get("average_soft", data.get("soft_vector", [])))
        if len(avg_soft) == 0:
            console.print("[red]No soft vector found in JSON.[/red]")
            return
        out_html = output.replace(".json", "_radar.html") if output.endswith(".json") else output + "_radar.html"
        soft_to_radar_chart(avg_soft, out_html)
        console.print(f"[green]Radar chart saved to {out_html}[/green]")
        return

    # Cosine similarity between two files
    if sim1 and sim2:
        def read_text(p):
            with open(p, 'r', encoding='utf-8') as f:
                return f.read()
        soft1 = text_to_soft(read_text(sim1), chunk_size)
        soft2 = text_to_soft(read_text(sim2), chunk_size)
        sim = cosine_similarity(soft1, soft2)
        console.print(f"[bold]Cosine similarity[/] between {sim1} and {sim2}: {sim:.4f}")
        return

    # Interpolation between two files
    if interp1 and interp2:
        def read_text(p):
            with open(p, 'r', encoding='utf-8') as f:
                return f.read()
        soft1 = text_to_soft(read_text(interp1), chunk_size)
        soft2 = text_to_soft(read_text(interp2), chunk_size)
        interp = interpolate_soft(soft1, soft2, alpha)
        console.print(f"[bold]Interpolated soft vector (alpha={alpha}):[/]")
        for i, val in enumerate(interp):
            console.print(f"  bit{i}: {val:5.2f}")
        out_path = Path(output)
        with open(out_path, 'w') as f:
            json.dump({"interpolated_soft": interp.tolist(), "alpha": alpha, "file1": interp1, "file2": interp2}, f, indent=2)
        console.print(f"[green]Saved to {out_path}[/green]")
        return

    # Default: compute average soft vector for a folder
    if path is None:
        console.print("[red]Please provide a folder path or use --sim1/--sim2 or --interp1/--interp2 or --radar.[/red]")
        raise typer.Exit(1)

    # Analyze folder
    all_soft = []
    text_extensions = {'.txt', '.md', '.py', '.json', '.yaml', '.yml', '.rst', '.csv', '.html', '.css', '.js'}
    files = list(Path(path).rglob("*"))
    for f in files:
        if f.is_file() and f.suffix.lower() in text_extensions:
            try:
                text = f.read_text(encoding='utf-8', errors='ignore')
                if text.strip():
                    soft_vec = text_to_soft(text, chunk_size)
                    all_soft.append(soft_vec)
            except Exception as e:
                console.print(f"[red]Error reading {f}: {e}[/red]")

    if not all_soft:
        console.print("[red]No text files found.[/red]")
        return

    avg_soft = np.mean(all_soft, axis=0)
    console.print("\n[bold cyan]Continuous SUBIT Profile (average soft vector)[/bold cyan]")
    console.print("Bits (b7..b0):")
    for i, val in enumerate(avg_soft):
        bar_len = int(abs(val) * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        sign = "+" if val >= 0 else "-"
        console.print(f"  bit{i}: {sign} {bar} {val:5.2f}")

    hard = soft_to_hard(avg_soft)
    console.print(f"\n[bold]Closest hard archetype:[/bold] {subit_to_name(hard)} (ID {hard})")

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "average_soft": avg_soft.tolist(),
        "closest_archetype": hard,
        "closest_archetype_name": subit_to_name(hard),
        "num_chunks": len(all_soft),
        "all_soft_vectors": [v.tolist() for v in all_soft]
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    console.print(f"\n[green]Soft vectors saved to {out_path}[/green]")


@app.command()
def control(
    text: str = typer.Argument(..., help="Input text to transform"),
    mode: str = typer.Argument(..., help="Target mode: STATE, VALUE, FORM, FORCE"),
    model: str = typer.Option("llama3.2:3b", "--model", "-m", help="Ollama model name"),
):
    """Transform text to match a given SUBIT mode using a local Ollama model."""
    from .llm_control_ollama import apply_control
    mode_map = {"STATE": 2, "VALUE": 3, "FORM": 1, "FORCE": 0}
    target = mode_map.get(mode.upper())
    if target is None:
        console.print(f"[red]Invalid mode: {mode}. Use STATE, VALUE, FORM, FORCE.[/red]")
        raise typer.Exit(1)
    try:
        console.print(f"[bold blue]Controlling text to mode {mode.upper()}...[/]")
        result = apply_control(text, target, model=model)
        console.print("\n[bold green]Result:[/]")
        console.print(result)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("Make sure Ollama server is running and the model is downloaded.")


@app.command()
def agent(
    text: str = typer.Argument(..., help="Input text to process"),
    mode: str = typer.Option("auto", "--mode", "-m", help="STATE, VALUE, FORM, FORCE, or auto"),
    model: str = typer.Option("llama3.2:3b", "--model", help="Ollama model name"),
    instructions: Optional[str] = typer.Option(None, "--instructions", "-i", help="Custom system prompt"),
):
    """Run an agent for a given mode (or auto-detect)."""
    from .agent import run_agent, classify_and_run
    
    if mode.upper() == "AUTO":
        console.print("[bold blue]Auto-detecting mode...[/]")
        result = classify_and_run(text, model)
        console.print(f"[dim]Detected mode: {result['original_mode']} (archetype: {result['original_archetype']})[/dim]")
        console.print("\n[bold green]Agent response:[/]")
        console.print(result['agent_response'])
    else:
        console.print(f"[bold blue]Running {mode.upper()} agent...[/]")
        response = run_agent(text, mode.upper(), model, instructions)
        console.print("\n[bold green]Response:[/]")
        console.print(response)


@app.command()
def pipeline(
    text: str = typer.Argument(..., help="Input text"),
    modes: str = typer.Option(..., "--modes", "-m", help="Comma-separated modes: STATE,VALUE,FORM,FORCE"),
    model: str = typer.Option("llama3.2:3b", "--model", help="Ollama model name"),
):
    """Run a multi-agent pipeline (sequential processing)."""
    from .agent import run_pipeline
    
    mode_list = [m.strip().upper() for m in modes.split(",")]
    console.print(f"[bold blue]Running pipeline: {' -> '.join(mode_list)}[/]")
    
    results = run_pipeline(text, mode_list, model)
    
    for i, r in enumerate(results, 1):
        console.print(f"\n[bold cyan]Step {i}: {r['mode']}[/]")
        console.print(f"[dim]Input: {r['input']}[/dim]")
        console.print(f"[green]Output: {r['output'][:200]}...[/green]" if len(r['output']) > 200 else f"[green]Output: {r['output']}[/green]")


@app.command()
def ui(
    port: int = typer.Option(8501, "--port", "-p", help="Port for web UI"),
):
    """Launch Streamlit web UI."""
    import subprocess
    import sys
    from pathlib import Path
    
    ui_file = Path(__file__).parent / "ui.py"
    if not ui_file.exists():
        console.print("[red]UI file not found. Please reinstall the package.[/red]")
        raise typer.Exit(1)
    
    console.print(f"[bold blue]Starting SUBIT-NOUS UI at http://localhost:{port}[/]")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(ui_file), "--server.port", str(port)])


@app.command()
def classify(
    text: str = typer.Argument(..., help="Text to classify"),
    probs: bool = typer.Option(False, "--probs", "-p", help="Show probabilities"),
):
    """Classify text using neural classifier (if available)."""
    from .classifier import SubitClassifier
    
    classifier = SubitClassifier()
    result = classifier.classify(text, return_probs=probs)
    
    console.print(f"\n[bold]Text:[/] {text}")
    console.print(f"[bold]SUBIT:[/] {result['subit']} ({result['bits']})")
    console.print(f"[bold]Archetype:[/] {result['archetype']}")
    
    if result.get('mode'):
        console.print(f"[bold]Mode:[/] {result['mode']}")
        console.print(f"[bold]Who:[/] {result['who']}")


@app.command()
def clusters(
    input: str = typer.Argument(..., help="Path to graph.json file"),
    max_distance: int = typer.Option(2, "--max-dist", "-d", help="Max Hamming distance for clustering"),
    output: str = typer.Option("./clusters.json", "--output", "-o", help="Output JSON file"),
):
    """Group archetypes into semantic clusters based on Hamming distance."""
    import json
    import networkx as nx
    from .graph import get_semantic_clusters
    from .core import subit_to_name
    
    # Load graph
    with open(input, 'r') as f:
        data = json.load(f)
    G = nx.node_link_graph(data)
    
    # Get clusters
    clusters = get_semantic_clusters(G, max_distance)
    
    # Prepare output
    result = {
        "max_distance": max_distance,
        "total_clusters": len(clusters),
        "total_nodes": len(G.nodes),
        "clusters": {}
    }
    
    for cluster_id, nodes_list in clusters.items():
        result["clusters"][cluster_id] = {
            "size": len(nodes_list),
            "archetypes": [
                {"id": node, "name": subit_to_name(node)}
                for node in nodes_list
            ]
        }
    
    # Save to file
    with open(output, 'w') as f:
        json.dump(result, f, indent=2)
    
    console.print(f"[bold blue]📊 Found {len(clusters)} semantic clusters[/]")
    console.print(f"[green]✅ Saved to {output}[/]")

@app.command()
def torus(
    input: str = typer.Argument(..., help="Path to graph.json file"),
    output: str = typer.Option("./torus.html", "--output", "-o", help="Output HTML file"),
):
    """Generate Clifford torus 3D visualization of all archetypes."""
    import json
    import networkx as nx
    from .graph import visualize_clifford_torus
    
    # Load graph
    with open(input, 'r') as f:
        data = json.load(f)
    G = nx.node_link_graph(data)
    
    console.print(f"[bold blue]🌀 Generating Clifford torus from {len(G.nodes)} archetypes...[/]")
    visualize_clifford_torus(G, output)
    console.print(f"[green]✅ Torus saved to {output}[/]")


@app.command()
def umap(
    input: str = typer.Argument(..., help="Path to graph.json file"),
    output: str = typer.Option("./umap.html", "--output", "-o", help="Output HTML file"),
):
    """Generate UMAP 3D projection of archetypes (preserves semantic topology)."""
    import json
    import networkx as nx
    from .graph import visualize_umap
    
    with open(input, 'r') as f:
        data = json.load(f)
    G = nx.node_link_graph(data)
    
    console.print(f"[bold blue]🗺️ Generating UMAP projection from {len(G.nodes)} archetypes...[/]")
    visualize_umap(G, output)
    console.print(f"[green]✅ UMAP saved to {output}[/]")

# Додайте цю функцію до вашого `cli.py`
@app.command()
def query(
    start: str = typer.Argument(..., help="Start archetype (ID, name, or text)"),
    target: str = typer.Argument(..., help="Target archetype (ID, name, or text)"),
    graph_path: str = typer.Option("./nous_output/graph.json", "--graph", "-g", help="Path to graph.json file"),
    all_paths: bool = typer.Option(False, "--all", "-a", help="Find all paths (not just shortest)"),
    max_depth: int = typer.Option(3, "--depth", "-d", help="Maximum depth for path finding"),
    common: bool = typer.Option(False, "--common", "-c", help="Find common connections instead of path"),
):
    
    # Load the graph
    if not Path(graph_path).exists():
        console.print(f"[red]Error: Graph file {graph_path} not found. Run 'nous analyze' first.[/red]")
        raise typer.Exit(1)
    
    with open(graph_path, 'r') as f:
        data = json.load(f)
    G = nx.node_link_graph(data)
    
    # Resolve start and target nodes
    def resolve_node(input_str: str) -> Optional[int]:
        if input_str.isdigit():
            node_id = int(input_str)
            if node_id in G.nodes:
                return node_id
        else:
            # Try to find by name
            for node in G.nodes:
                if subit_to_name(node).lower() == input_str.lower():
                    return node
            # Try as text
            node_id = text_to_subit(input_str)
            if node_id in G.nodes:
                return node_id
        return None
    
    start_node = resolve_node(start)
    target_node = resolve_node(target)
    
    if start_node is None:
        console.print(f"[red]Error: Could not resolve start '{start}' to an archetype in the graph.[/red]")
        raise typer.Exit(1)
    
    if target_node is None:
        console.print(f"[red]Error: Could not resolve target '{target}' to an archetype in the graph.[/red]")
        raise typer.Exit(1)
    
    console.print(f"[bold blue]🔍 Querying graph:[/] {subit_to_name(start_node)} → {subit_to_name(target_node)}")
    
    if common:
        common_nodes = find_common_connections(G, start_node, target_node)
        if common_nodes:
            console.print(f"\n[bold green]Common connections found:[/]")
            for node in common_nodes:
                console.print(f"  • {subit_to_name(node)} (ID: {node})")
        else:
            console.print("[yellow]No common connections found.[/yellow]")
        return
    
    if all_paths:
        paths = find_all_paths(G, start_node, target_node, max_depth)
        if paths:
            console.print(f"\n[bold green]Found {len(paths)} path(s) (max depth: {max_depth}):[/]\n")
            for i, path in enumerate(paths, 1):
                console.print(f"Path {i}:")
                console.print(format_path_result_with_metadata(G, path))
                console.print("")
        else:
            console.print(f"[yellow]No paths found between these archetypes within depth {max_depth}.[/yellow]")
    else:
        path = find_path(G, start_node, target_node)
        if path:
            console.print(f"\n[bold green]Shortest path found:[/]\n")
            console.print(format_path_result_with_metadata(G, path))
            console.print(f"\n[dim]Path length: {len(path)-1} steps[/dim]")
        else:
            console.print("[yellow]No path found between these archetypes.[/yellow]")

@app.command()
def wiki(
    input: str = typer.Argument(..., help="Path to graph.json file or folder with graph.json"),
    output: str = typer.Option("./wiki", "--output", "-o", help="Output directory for wiki"),
):
    """Generate Wikipedia-style markdown wiki from knowledge graph."""
    import json
    import networkx as nx
    from .wiki import generate_wiki
    
    # Find graph.json
    input_path = Path(input)
    if input_path.is_dir():
        graph_path = input_path / "graph.json"
    else:
        graph_path = input_path
    
    if not graph_path.exists():
        console.print(f"[red]Error: {graph_path} not found[/red]")
        raise typer.Exit(1)
    
    with open(graph_path, 'r') as f:
        data = json.load(f)
    G = nx.node_link_graph(data)
    
    console.print(f"[bold blue]📚 Generating wiki from graph with {len(G.nodes)} nodes...[/]")
    generate_wiki(G, output)
    console.print(f"[green]✅ Wiki exported to {output}[/]")
    console.print(f"[dim]Open {output}/index.md to start browsing[/dim]")


@app.command()
def integrate(
    platform: str = typer.Argument(..., help="Platform: claude, cursor, gemini, all, uninstall"),
    output: str = typer.Option("./nous_output", "--output", "-o", help="Output directory with graph"),
):
    """Integrate with AI coding assistants (Claude Code, Cursor, Gemini CLI)."""
    from .integrations import (
        install_claude_integration,
        install_cursor_integration,
        install_gemini_integration,
        install_all_integrations,
        uninstall_claude_integration,
        uninstall_cursor_integration,
        uninstall_gemini_integration,
    )
    
    if platform == "claude":
        install_claude_integration(output)
        console.print("[green]✅ Claude Code integration installed![/]")
    
    elif platform == "cursor":
        install_cursor_integration(output)
        console.print("[green]✅ Cursor integration installed![/]")
    
    elif platform == "gemini":
        install_gemini_integration(output)
        console.print("[green]✅ Gemini CLI integration installed![/]")
    
    elif platform == "all":
        install_all_integrations(output)
        console.print("[green]✅ All integrations installed![/]")
    
    elif platform == "uninstall":
        console.print("[yellow]Uninstalling integrations...[/]")
        uninstall_claude_integration()
        uninstall_cursor_integration()
        uninstall_gemini_integration()
        console.print("[green]✅ All integrations uninstalled![/]")
    
    else:
        console.print(f"[red]Unknown platform: {platform}[/]")
        console.print("[dim]Supported: claude, cursor, gemini, all, uninstall[/dim]")
        raise typer.Exit(1)


def main():
    app()


if __name__ == "__main__":
    main()