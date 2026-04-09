# 🧠 SUBIT-NOUS

**Transform any folder into a knowledge graph using 4 transversal modes: MICRO · MACRO · MESO · META**

> **NOUS** (νοῦς) — the intellect that perceives archetypes.  
> **SUBIT** — a 4D framework (WHO × WHERE × WHEN × WHY).

## One command. Any folder. Full knowledge graph.

```bash
pip install subit-nous
nous ./raw --output ./knowledge
```

## The SUBIT framework

Four dimensions, each with four categories, form **256 archetypes** (8 bits).  
Four **transversal modes** cut across all dimensions:

| Mode   | Bits | WHO  | WHERE | WHEN   | WHY     |
|--------|------|------|-------|--------|---------|
| **MICRO** | 10 | ME   | EAST  | SPRING | LOGOS   |
| **MACRO** | 11 | WE   | SOUTH | SUMMER | ETHOS   |
| **MESO**  | 01 | YOU  | WEST  | AUTUMN | PATHOS  |
| **META**  | 00 | THEY | NORTH | WINTER | THYMOS  |

Every text, PDF, or image is reduced to one of these 256 archetypes – **no LLM required**.

## Quick start

```bash
# Analyze a folder
nous ./my-documents

# Watch mode (auto‑update on changes)
nous watch ./my-documents

# Start API server on port 8000
nous serve --port 8000

# Install Git hooks for auto‑analysis
nous hooks install .
```

## Output

After running `nous ./raw`, you’ll find in `./nous_output`:

- `graph.html` – interactive 3D/4D visualization
- `report.md` – analytical report (top archetypes, unexpected connections)
- `obsidian/` – an Obsidian vault with backlinked archetype pages
- `metadata.json` – raw graph data

## Why “NOUS”?

In Greek philosophy, **NOUS** is the divine intellect that brings order from chaos and recognises eternal patterns. **SUBIT‑NOUS** brings this ancient wisdom to modern knowledge management.

## Structure 

```
subit-nous/
├── .github/workflows/publish.yml
├── src/subit_nous/
│   ├── __init__.py
│   ├── core.py
│   ├── graph.py
│   ├── io.py
│   ├── exports.py
│   └── cli.py
├── tests/
│   ├── test_core.py
│   └── fixtures/sample.txt
├── examples/basic.py
├── docs/README.md
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── LICENSE
├── README.md
└── Makefile
```

## License

MIT