# SUBIT‑NOUS Documentation

Welcome to the official documentation for **SUBIT‑NOUS** – a tool that transforms any folder into an interactive knowledge graph using 4 transversal modes and 256 archetypes.

## Table of Contents

- [Overview](#overview)
- [The SUBIT Framework](#the-subit-framework)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Reference](#cli-reference)
- [Outputs](#outputs)
- [API Server](#api-server)
- [Git Hooks](#git-hooks)
- [Extending](#extending)
- [License](#license)

## Overview

**SUBIT‑NOUS** reads text, PDF, and image files, converts each chunk into one of 256 archetypes (8‑bit numbers), and builds a directed graph of transitions. The result is an interactive 4D visualization, a Markdown report, and an Obsidian vault – all without any LLM API calls (optional for images).

The name combines:
- **SUBIT** – the 4‑dimensional framework (WHO × WHERE × WHEN × WHY)
- **NOUS** (νοῦς) – the ancient Greek concept of intellect that perceives archetypal patterns.

## The SUBIT Framework

Four dimensions, each with four categories:

| Dimension | Categories (bits) |
|-----------|------------------|
| **WHO**   | ME (10), WE (11), YOU (01), THEY (00) |
| **WHERE** | EAST (10), SOUTH (11), WEST (01), NORTH (00) |
| **WHEN**  | SPRING (10), SUMMER (11), AUTUMN (01), WINTER (00) |
| **WHY**   | LOGOS (10), ETHOS (11), PATHOS (01), THYMOS (00) |

Every combination of one category from each dimension gives **256 archetypes** (8 bits). Four of them are **transversal modes**:

| Mode   | Bits | WHO  | WHERE | WHEN   | WHY     | Role |
|--------|------|------|-------|--------|---------|------|
| MICRO  | 10   | ME   | EAST  | SPRING | LOGOS   | individual, initiation |
| MACRO  | 11   | WE   | SOUTH | SUMMER | ETHOS   | collective, synergy |
| MESO   | 01   | YOU  | WEST  | AUTUMN | PATHOS  | transition, dialogue |
| META   | 00   | THEY | NORTH | WINTER | THYMOS  | transcendent, foundation |

## Installation

```bash
pip install subit-nous
```

For optional PDF support, install `PyPDF2`; for image fallback, `Pillow`. For the API server, install `uvicorn` and `fastapi` (included as dependencies).

## Quick Start

```bash
# Analyze a folder
nous ./my-documents --output ./results

# Open the interactive graph
open ./results/graph.html

# Read the report
cat ./results/report.md
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `nous analyze <path>` | Build knowledge graph from folder |
| `nous serve` | Start REST API + WebSocket server |
| `nous hooks install` | Install Git post‑commit hook |
| `nous info` | Show the SUBIT framework table |
| `nous version` | Show version |

### Options for `analyze`

- `--output`, `-o` – output directory (default `./nous_output`)
- `--chunk-size`, `-c` – characters per chunk (default 1000)
- `--watch`, `-w` – watch for changes (not yet implemented)
- `--api` – start API server after analysis
- `--no-viz` – skip HTML visualization
- `--no-obsidian` – skip Obsidian export
- `--no-report` – skip Markdown report
- `--json` – export graph as JSON

## Outputs

After running `nous analyze`, you get:

- `graph.html` – interactive 3D plot (WHO × WHERE × WHEN, colored by WHY)
- `report.md` – statistics, top archetypes, god nodes, unexpected connections
- `obsidian/` – Obsidian vault with one markdown file per archetype
- `graph.json` (if `--json` used) – node‑link data

## API Server

Start the server:

```bash
nous serve --port 8000
```

Then use the endpoints (OpenAPI docs at `http://localhost:8000/docs`):

- `POST /analyze/text` – send JSON `{"text": "..."}` → returns archetype ID, name, coordinates
- `POST /analyze/file` – upload a file → returns archetype info
- `GET /graph/stats` – get node count, edge count, top archetypes
- `WS /ws/live` – WebSocket that broadcasts archetype analysis in real time

## Git Hooks

Automatically run `nous analyze` after each commit:

```bash
cd your-git-repo
nous hooks install
```

Now every `git commit` will regenerate the knowledge graph in `.nous_output/`.

## Extending

### Custom markers

Modify `MARKERS` in `core.py` to add your own keywords for each category.

### Using with your own data

The tool works best with mixed content: code, documentation, meeting notes, research papers, etc. The more varied the input, the richer the graph.

### Integrating with other tools

- Export JSON and import into Neo4j, Gephi, or any graph database.
- Use the Obsidian vault as a personal knowledge base.

## License

MIT