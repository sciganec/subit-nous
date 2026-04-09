"""Command‑line interface for SUBIT‑NOUS."""

import sys
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .core import __version__
from .graph import build_graph, visualize_4d
from .exports import export_report, export_obsidian, export_json
from .io import file_to_subit

app = typer.Typer(
    name="nous",
    help="🧠 SUBIT‑NOUS: Transform chaos into structured knowledge using 4 transversal modes (MICRO·MACRO·MESO·META).",
    add_completion=False,
)
console = Console()


@app.command()
def analyze(
    path: str = typer.Argument(..., help="Folder to analyze"),
    output: str = typer.Option("./nous_output", "--output", "-o", help="Output directory"),
    chunk_size: int = typer.Option(1000, "--chunk-size", "-c", help="Text chunk size in characters"),
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch for changes and auto‑update"),
    api: bool = typer.Option(False, "--api", help="Start API server after analysis"),
    no_viz: bool = typer.Option(False, "--no-viz", help="Skip HTML visualization"),
    no_obsidian: bool = typer.Option(False, "--no-obsidian", help="Skip Obsidian export"),
    no_report: bool = typer.Option(False, "--no-report", help="Skip markdown report"),
    json: bool = typer.Option(False, "--json", help="Export graph as JSON"),
):
    """Build knowledge graph from a folder."""
    console.print(f"[bold blue]🧠 NOUS[/] analyzing [green]{path}[/] ...")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Building graph...", total=None)
        graph = build_graph(path, chunk_size=chunk_size)
        progress.update(task, completed=True)

    console.print(f"[bold]📊 Graph built:[/] {len(graph.nodes())} archetypes, {graph.number_of_edges()} transitions")

    out_dir = Path(output)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not no_viz:
        html_path = out_dir / "graph.html"
        visualize_4d(graph, str(html_path))
        console.print(f"[green]✅ Visualization:[/] {html_path}")

    if not no_report:
        report_path = out_dir / "report.md"
        export_report(graph, str(report_path))
        console.print(f"[green]✅ Report:[/] {report_path}")

    if not no_obsidian:
        obsidian_dir = out_dir / "obsidian"
        export_obsidian(graph, str(obsidian_dir))
        console.print(f"[green]✅ Obsidian vault:[/] {obsidian_dir}")

    if json:
        json_path = out_dir / "graph.json"
        export_json(graph, str(json_path))
        console.print(f"[green]✅ JSON export:[/] {json_path}")

    if watch:
        console.print("[yellow]👀 Watch mode not yet implemented in this version.[/]")
        # Future: use watchdog

    if api:
        console.print("[yellow]🚀 Starting API server...[/]")
        serve_cmd = [sys.executable, "-m", "uvicorn", "subit_nous.api:app", "--host", "0.0.0.0", "--port", "8000"]
        try:
            subprocess.run(serve_cmd)
        except KeyboardInterrupt:
            console.print("[dim]API stopped.[/]")


@app.command()
def serve(
    port: int = typer.Option(8000, "--port", "-p", help="Port to listen on"),
    host: str = typer.Option("0.0.0.0", "--host", help="Host address"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto‑reload (development)"),
):
    """Start REST API + WebSocket server."""
    console.print(f"[bold blue]🚀 Starting SUBIT‑NOUS API on http://{host}:{port}[/]")
    try:
        import uvicorn
    except ImportError:
        console.print("[red]Error: uvicorn not installed. Run `pip install uvicorn`.[/]")
        raise typer.Exit(1)
    uvicorn.run("subit_nous.api:app", host=host, port=port, reload=reload)


@app.command()
def hooks(
    action: str = typer.Argument("install", help="install or uninstall"),
    repo_path: str = typer.Option(".", "--repo", help="Path to git repository"),
):
    """Install or uninstall Git hooks for auto‑analysis."""
    git_dir = Path(repo_path) / ".git"
    if not git_dir.exists():
        console.print(f"[red]Error: {repo_path} is not a git repository.[/]")
        raise typer.Exit(1)

    hooks_dir = git_dir / "hooks"
    if action == "install":
        post_commit = hooks_dir / "post-commit"
        post_commit.write_text("#!/bin/sh\nnous analyze . --output .nous_output\n")
        post_commit.chmod(0o755)
        console.print("[green]✅ Installed post‑commit hook: runs `nous analyze .` after each commit.[/]")
    elif action == "uninstall":
        for hook in ["post-commit", "post-checkout"]:
            hook_path = hooks_dir / hook
            if hook_path.exists():
                hook_path.unlink()
        console.print("[green]✅ Uninstalled SUBIT‑NOUS hooks.[/]")
    else:
        console.print(f"[red]Unknown action: {action}. Use 'install' or 'uninstall'.[/]")
        raise typer.Exit(1)


@app.command()
def version():
    """Show version and exit."""
    console.print(f"SUBIT‑NOUS version [bold]{__version__}[/]")


@app.command()
def info():
    """Display information about the SUBIT framework."""
    table = Table(title="SUBIT‑NOUS Framework")
    table.add_column("Mode", style="cyan")
    table.add_column("Bits", style="green")
    table.add_column("WHO", style="yellow")
    table.add_column("WHERE", style="yellow")
    table.add_column("WHEN", style="yellow")
    table.add_column("WHY", style="yellow")
    table.add_row("MICRO", "10", "ME", "EAST", "SPRING", "LOGOS")
    table.add_row("MACRO", "11", "WE", "SOUTH", "SUMMER", "ETHOS")
    table.add_row("MESO",  "01", "YOU", "WEST",  "AUTUMN", "PATHOS")
    table.add_row("META",  "00", "THEY","NORTH", "WINTER", "THYMOS")
    console.print(table)
    console.print("\n[dim]Every text, image, or PDF → one of 256 archetypes (8 bits).[/]")


def main():
    """Entry point for console script."""
    if len(sys.argv) == 1:
        console.print("[bold]SUBIT‑NOUS[/] – knowledge from chaos.")
        console.print("Try: [green]nous info[/] or [green]nous analyze ./folder[/]")
        sys.exit(0)
    app()


if __name__ == "__main__":
    main()