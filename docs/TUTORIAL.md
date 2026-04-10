# SUBIT-NOUS Tutorial: From Chaos to Knowledge Graph

This tutorial walks you through every feature of **SUBIT-NOUS** – the CLI tool that transforms any folder into an interactive knowledge graph using 4 transversal modes: **MICRO · MACRO · MESO · META**.

## Table of Contents

1. [Installation](#1-installation)
2. [First Run: Analyze a Folder](#2-first-run-analyze-a-folder)
3. [Understanding the Output](#3-understanding-the-output)
   - Interactive Graph
   - Markdown Report
   - Obsidian Vault
4. [Watch Mode: Auto‑update on Changes](#4-watch-mode-auto‑update-on-changes)
5. [Git Hooks: Auto‑analysis on Commit](#5-git-hooks-auto‑analysis-on-commit)
6. [API Server: Real‑time Analysis](#6-api-server-real‑time-analysis)
   - REST API
   - WebSocket Live Feed
7. [Exporting the Graph](#7-exporting-the-graph)
8. [Advanced: Custom Markers & Configuration](#8-advanced-custom-markers--configuration)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Installation

```bash
pip install subit-nous
```

Verify installation:

```bash
nous --help
```

You should see a list of commands: `analyze`, `watch`, `serve`, `hooks`, `export`.

---

## 2. First Run: Analyze a Folder

Create a test folder with four small text files:

```bash
mkdir test_raw
echo "I think logically about the east in spring" > test_raw/micro.txt
echo "We trust our community in the south during summer" > test_raw/macro.txt
echo "You feel the beauty of autumn in the west" > test_raw/meso.txt
echo "They exert power in the north during winter" > test_raw/meta.txt
```

Now run the analysis:

```bash
nous analyze test_raw --output my_output
```

**Expected output:**

```
🧠 NOUS analyzing test_raw ...
📊 Graph built: 4 archetypes, 3 transitions
✅ Visualization: my_output/graph.html
✅ Report saved to my_output/report.md
✅ Obsidian vault exported to my_output/obsidian
```

That’s it! You’ve built a knowledge graph from 4 text files.

---

## 3. Understanding the Output

### 3.1 Interactive Graph (`my_output/graph.html`)

Open this file in any browser. You will see a 3D scatter plot where:

- **X axis** = WHO (ME, WE, YOU, THEY)
- **Y axis** = WHERE (EAST, SOUTH, WEST, NORTH)
- **Z axis** = WHEN (SPRING, SUMMER, AUTUMN, WINTER)
- **Color** = WHY (LOGOS=blue, ETHOS=green, PATHOS=yellow, THYMOS=purple)

Hover over a node to see its exact archetype name and frequency. Edges represent transitions between files (in alphabetical order).

### 3.2 Markdown Report (`my_output/report.md`)

This file contains:

- **Top archetypes** (which modes appear most often)
- **God nodes** (archetypes with most connections)
- **Unexpected connections** (edges between archetypes with large Hamming distance)
- **Archetype profile** (percentage of MICRO/MACRO/MESO/META)
- **Suggested questions** for further analysis

Example snippet:

```markdown
## Archetype profile
- MICRO ████████████████░░░░ 42%
- MACRO ████████████████░░░░ 42%
- MESO  ██░░░░░░░░░░░░░░░░░░  8%
- META  ██░░░░░░░░░░░░░░░░░░  8%
```

### 3.3 Obsidian Vault (`my_output/obsidian/`)

Open this folder as an Obsidian vault. You will find:

- `index.md` – navigation hub
- A note for each archetype that appears (e.g., `MICRO mode.md`, `LOGOS_ME_EAST_SPRING.md`)
- Each note contains backlinks to related archetypes, making it easy to explore the knowledge graph inside Obsidian.

---

## 4. Watch Mode: Auto‑update on Changes

If you are actively editing files, use watch mode to rebuild the graph automatically whenever a file changes.

```bash
nous watch test_raw --output watch_output
```

Now modify one of the files (e.g., `test_raw/micro.txt`) and save. The tool will immediately re‑analyze and update `watch_output/graph.html`.

---

## 5. Git Hooks: Auto‑analysis on Commit

Integrate SUBIT‑NOUS into your Git workflow. After every commit, the knowledge graph will be updated automatically.

### Install hooks in your repository:

```bash
cd /path/to/your/git/repo
nous hooks install .
```

Now whenever you run `git commit`, a post‑commit hook will execute `nous analyze .` and refresh the graph. You can store the output in a `nous_output/` folder (add it to `.gitignore` if you don’t want to commit it).

### Uninstall hooks:

```bash
nous hooks uninstall
```

---

## 6. API Server: Real‑time Analysis

Start the REST API + WebSocket server:

```bash
nous serve --port 8000
```

Keep this terminal running.

### 6.1 REST API

#### Health check

```bash
curl http://localhost:8000/health
```

#### Analyze text

```bash
curl -X POST http://localhost:8000/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text": "We build together in the south during summer"}'
```

Response:

```json
{
  "subit_id": 255,
  "archetype_name": "MACRO mode",
  "coordinates": {"WHO": 3, "WHERE": 3, "WHEN": 3, "WHY": 3},
  "timestamp": "2025-04-09T10:30:00Z"
}
```

#### Get graph statistics

```bash
curl http://localhost:8000/graph/stats
```

### 6.2 WebSocket Live Feed

You can connect any WebSocket client to `ws://localhost:8000/ws/live`. Every message you send will be analysed and broadcast to all connected clients.

Example using `websocat` (install separately) or a simple HTML page:

```html
<script>
  const ws = new WebSocket("ws://localhost:8000/ws/live");
  ws.onmessage = (e) => console.log(JSON.parse(e.data));
  ws.send("I think the truth is in the east");
</script>
```

---

## 7. Exporting the Graph

You can export the graph in different formats for use in other tools.

### JSON (Node‑Link Data)

```bash
curl http://localhost:8000/graph/export?format=json > graph.json
```

### Cypher (for Neo4j)

```bash
curl http://localhost:8000/graph/export?format=cypher > graph.cypher
```

Then import into Neo4j:

```bash
cat graph.cypher | cypher-shell -u neo4j -p password
```

---

## 8. Advanced: Custom Markers & Configuration

The built‑in markers work well for English technical text. You can extend them by editing `src/subit_nous/core.py` (if installed from source) or by providing a custom config file (planned for future releases).

Example: adding a new marker for “team” to strengthen the WE (MACRO) category.

In `MARKERS['WHO'][0b11]`, add `'team'`.

After modification, rebuild the package or re‑run the CLI.

---

## 9. Troubleshooting

| Problem | Solution |
|---------|----------|
| `nous: command not found` | Re‑install with `pip install --upgrade subit-nous` or check that your Python `bin` folder is in PATH. |
| `UnicodeDecodeError` on `.txt` files | Ensure files are saved as UTF‑8 without BOM. Use `Out-File -Encoding ascii` on Windows. |
| Only 1 archetype in graph | Your folder may contain non‑text files. Use `--ext` to filter extensions, or delete binary files. |
| Graph has no edges | If you have only one file, there are no transitions. Add at least two files. |
| API server fails to start | Port 8000 may be busy. Change port with `--port 8080`. |

---

## What’s Next?

- Try `nous analyze` on a real project folder (source code + documentation).
- Use watch mode while writing a blog post – see how your archetype profile changes.
- Build a personal knowledge graph of your notes and explore it in Obsidian.
- Integrate the API into a Slack bot or a dashboard.

For more details, check the [README](README.md) and the [SUBIT framework explanation](docs/subit_framework.md).

**Happy knowledge mining! 🧠**
