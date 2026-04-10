#!/usr/bin/env python3
"""SUBIT-NOUS CLI: analyze, watch, serve, hooks, export, soft, control"""

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from typing import Optional, List
import json
import numpy as np

from .graph import build_graph, visualize_4d
from .exports import export_report, export_obsidian
from .core import text_to_soft, soft_to_hard, subit_to_name, cosine_similarity, interpolate_soft, soft_to_radar_chart

app = typer.Typer(help="🧠 SUBIT-NOUS: Knowledge from chaos (MICRO/MACRO/MESO/META)")
console = Console()

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
    
    console.print(f"[bold blue]🌐 Starting SUBIT‑NOUS UI at http://localhost:{port}[/]")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(ui_file), "--server.port", str(port)])
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
        console.print("[bold blue]🤖 Auto-detecting mode...[/]")
        result = classify_and_run(text, model)
        console.print(f"[dim]Detected mode: {result['original_mode']} (archetype: {result['original_archetype']})[/dim]")
        console.print("\n[bold green]Agent response:[/]")
        console.print(result['agent_response'])
    else:
        console.print(f"[bold blue]🤖 Running {mode.upper()} agent...[/]")
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
    console.print(f"[bold blue]🔗 Running pipeline: {' → '.join(mode_list)}[/]")
    
    results = run_pipeline(text, mode_list, model)
    
    for i, r in enumerate(results, 1):
        console.print(f"\n[bold cyan]Step {i}: {r['mode']}[/]")
        console.print(f"[dim]Input: {r['input']}[/dim]")
        console.print(f"[green]Output: {r['output'][:200]}...[/green]" if len(r['output']) > 200 else f"[green]Output: {r['output']}[/green]")
@app.command()
def index(
    path: str = typer.Argument(..., help="Folder to index"),
    chunk_size: int = typer.Option(1000, "--chunk-size", "-c", help="Text chunk size"),
):
    """Index a folder for fast search."""
    from .search import index_folder
    console.print(f"[bold blue]📇 Indexing[/] {path} ...")
    count = index_folder(path, chunk_size)
    console.print(f"[green]✅ Indexed {count} documents.[/green]")

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
# ----------------------------------------------------------------------
# analyze
# ----------------------------------------------------------------------
@app.command()
def analyze(
    path: str = typer.Argument(..., help="Folder to analyze"),
    output: str = typer.Option("./nous_output", "--output", "-o", help="Output directory"),
    chunk_size: int = typer.Option(1000, "--chunk-size", "-c", help="Text chunk size in characters"),
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch mode (auto-update on changes)"),
    api: bool = typer.Option(False, "--api", help="Start API server after analysis"),
):
    """Build knowledge graph from any folder."""
    console.print(f"[bold blue]🧠 NOUS[/] analyzing {path} ...")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Building graph...", total=None)
        graph = build_graph(path, chunk_size=chunk_size)
        progress.update(task, completed=True)
    console.print(f"[bold]📊 Graph built:[/] {len(graph.nodes)} archetypes, {graph.number_of_edges()} transitions")
    out_path = Path(output)
    out_path.mkdir(parents=True, exist_ok=True)
    visualize_4d(graph, str(out_path / "graph.html"))
    export_report(graph, str(out_path / "report.md"))
    export_obsidian(graph, str(out_path / "obsidian"))
    console.print(f"[green]✅ Done![/] Open {out_path / 'graph.html'}")
    if watch:
        console.print("[yellow]👀 Watch mode not yet implemented in CLI, use `nous watch` separately.[/]")
    if api:
        console.print("[yellow]🚀 Starting API server...[/]")
        serve(port=8000)

# ----------------------------------------------------------------------
# watch
# ----------------------------------------------------------------------
@app.command()
def watch(
    path: str = typer.Argument(..., help="Folder to watch"),
    output: str = typer.Option("./nous_output", "--output", "-o", help="Output directory"),
    chunk_size: int = typer.Option(1000, "--chunk-size", "-c", help="Text chunk size"),
):
    """Watch folder for changes and auto‑update the knowledge graph."""
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import time
    class Handler(FileSystemEventHandler):
        def on_modified(self, event):
            if not event.is_directory:
                console.print(f"[dim]Change detected: {event.src_path}[/dim]")
                graph = build_graph(path, chunk_size=chunk_size)
                out_path = Path(output)
                out_path.mkdir(parents=True, exist_ok=True)
                visualize_4d(graph, str(out_path / "graph.html"))
                export_report(graph, str(out_path / "report.md"))
                export_obsidian(graph, str(out_path / "obsidian"))
                console.print("[green]✅ Graph updated.[/green]")
    console.print(f"[bold blue]👀 Watching[/] {path} (press Ctrl+C to stop)")
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# ----------------------------------------------------------------------
# serve
# ----------------------------------------------------------------------
@app.command()
def serve(
    port: int = typer.Option(8000, "--port", "-p", help="Port for API server"),
):
    """Start REST API + WebSocket server."""
    import uvicorn
    from subit_nous.api import app as api_app
    console.print(f"[bold blue]🚀 Starting SUBIT‑NOUS API on http://0.0.0.0:{port}[/]")
    uvicorn.run(api_app, host="0.0.0.0", port=port)

# ----------------------------------------------------------------------
# hooks
# ----------------------------------------------------------------------
@app.command()
def hooks(
    action: str = typer.Argument("install", help="install or uninstall"),
    repo_path: str = typer.Option(".", "--repo", "-r", help="Git repository path"),
):
    """Install or uninstall Git hooks for auto‑analysis on commit."""
    hooks_dir = Path(repo_path) / ".git" / "hooks"
    if action == "install":
        hooks_dir.mkdir(parents=True, exist_ok=True)
        post_commit = hooks_dir / "post-commit"
        post_commit.write_text(f"""#!/bin/sh
nous analyze {repo_path} --output {repo_path}/nous_output
""")
        post_commit.chmod(0o755)
        console.print(f"[green]✅ Git post-commit hook installed in {hooks_dir}[/]")
    elif action == "uninstall":
        hook = hooks_dir / "post-commit"
        if hook.exists():
            hook.unlink()
            console.print(f"[yellow]🗑️ Removed post-commit hook[/]")
        else:
            console.print("[yellow]No post-commit hook found.[/]")
    else:
        console.print(f"[red]Unknown action: {action}. Use 'install' or 'uninstall'.[/]")

# ----------------------------------------------------------------------
# export
# ----------------------------------------------------------------------
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
        console.print(f"✅ JSON exported to {output}")
    elif format == "cypher":
        cypher_lines = []
        for node in G.nodes:
            name = G.nodes[node].get('name', str(node))
            cypher_lines.append(f"CREATE (a:{name.replace(' ', '_')} {{id: {node}}})")
        for u, v in G.edges:
            cypher_lines.append(f"MATCH (a {{id: {u}}}), (b {{id: {v}}}) CREATE (a)-[:TRANSITIONS]->(b)")
        Path(output).write_text("\n".join(cypher_lines))
        console.print(f"✅ Cypher exported to {output}")
    else:
        console.print(f"[red]Unknown format: {format}[/]")

# ----------------------------------------------------------------------
# soft (розширена версія)
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# control (Ollama)
# ----------------------------------------------------------------------
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
        console.print(f"[bold blue]🎮 Controlling text to mode {mode.upper()}...[/]")
        result = apply_control(text, target, model=model)
        console.print("\n[bold green]Result:[/]")
        console.print(result)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("Make sure Ollama server is running and the model is downloaded.")

# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main():
    app()

if __name__ == "__main__":
    main()