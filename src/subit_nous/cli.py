#!/usr/bin/env python3
"""SUBIT-NOUS CLI: analyze, watch, serve, hooks, export"""

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from typing import Optional

from .graph import build_graph, visualize_4d
from .exports import export_report, export_obsidian
from .llm_control_ollama import apply_control

app = typer.Typer(help="🧠 SUBIT-NOUS: Knowledge from chaos (MICRO/MACRO/MESO/META)")
console = Console()

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
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
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
@app.command()
def soft(
    path: str = typer.Argument(..., help="Folder to analyze"),
    output: str = typer.Option("./soft_output", "--output", "-o", help="Output JSON file"),
    chunk_size: int = typer.Option(1000, "--chunk-size", "-c", help="Text chunk size"),
):
    """Compute soft archetype vectors for all files and show average profile."""
    import json
    import numpy as np
    from pathlib import Path
    from .core import text_to_soft, soft_to_hard, subit_to_name

    all_soft = []
    files = list(Path(path).rglob("*"))
    text_extensions = {'.txt', '.md', '.py', '.json', '.yaml', '.yml', '.rst', '.csv'}
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
    # Вивести профіль
    console.print("\n[bold cyan]Continuous SUBIT Profile (average soft vector)[/bold cyan]")
    console.print("Bits (b7..b0):")
    for i, val in enumerate(avg_soft):
        bar_len = int(abs(val) * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        sign = "+" if val >= 0 else "-"
        console.print(f"  bit{i}: {sign} {bar} {val:5.2f}")

    # Перетворити в жорсткий архетип
    hard = soft_to_hard(avg_soft)
    console.print(f"\n[bold]Closest hard archetype:[/bold] {subit_to_name(hard)} (ID {hard})")

    # Зберегти soft-вектори у JSON
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
    console.print(f"\n[green]✅ Soft vectors saved to {out_path}[/green]")
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

@app.command()
def serve(
    port: int = typer.Option(8000, "--port", "-p", help="Port for API server"),
):
    """Start REST API + WebSocket server."""
    import uvicorn
    from subit_nous.api import app as api_app
    console.print(f"[bold blue]🚀 Starting SUBIT‑NOUS API on http://0.0.0.0:{port}[/]")
    uvicorn.run(api_app, host="0.0.0.0", port=port)

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

@app.command()
def export(
    graph_file: str = typer.Argument(..., help="Path to JSON graph file (from /graph/export)"),
    format: str = typer.Option("obsidian", "--format", "-f", help="obsidian, json, cypher"),
    output: str = typer.Option("./export", "--output", "-o", help="Output directory or file"),
):
    """Export graph to different formats (experimental)."""
    import json
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

@app.command()
def control(
    text: str = typer.Argument(..., help="Input text to transform"),
    mode: str = typer.Argument(..., help="Target mode: STATE, VALUE, FORM, FORCE"),
    model: str = typer.Option("gpt-3.5-turbo", "--model", "-m", help="OpenAI model"),
):
    """Transform text to match a given SUBIT mode using LLM."""
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
        console.print("Make sure OPENAI_API_KEY is set in your environment.")

def main():
    app()

if __name__ == "__main__":
    main()
