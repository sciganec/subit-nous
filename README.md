# 🧠 SUBIT‑NOUS v3.1.0

## Formal algebraic coordinate system for meaning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **NOUS** (νοῦς) – the intellect that perceives archetypes.  
> **SUBIT** – a 4‑dimensional algebraic space over (ℤ₂)⁸.

SUBIT‑NOUS turns any folder or file into a **computable knowledge graph** of 256 archetypes.  
No LLM required for the core – but you can **control LLM generation** locally via Ollama.

---

## ✨ What's New in v3.1.0

- **Single file analysis** – analyze individual files, not only folders
- **Empty file handling** – empty files now default to MICRO mode
- **Windows compatibility** – fixed Unicode/emoji issues in PowerShell
- **Performance optimizations** – faster processing for 100+ files
- **Bug fixes** – syntax errors in graph.py, encoding issues

---

## 🚀 One command. Any file or folder. Full knowledge graph.

```bash
pip install subit-nous
nous analyze ./my-folder --output ./knowledge
nous analyze my-file.txt --output ./knowledge
```

---

## 📐 The SUBIT v3.0 Framework

Four axes, each with 4 values (2 bits):

| Axis   | Values                           | Binary   |
|--------|----------------------------------|----------|
| WHO    | ME / WE / YOU / THEY             | 10/11/01/00 |
| WHERE  | EAST / SOUTH / WEST / NORTH      | 10/11/01/00 |
| WHEN   | SPRING / SUMMER / AUTUMN / WINTER | 10/11/01/00 |
| MODE   | STATE / VALUE / FORM / FORCE     | 10/11/01/00 |

**Interface layer:** `STATE→LOGOS`, `VALUE→ETHOS`, `FORM→PATHOS`, `FORCE→THYMOS`

### Algebraic Structure

- **Space**: (ℤ₂)⁸
- **Operation**: XOR (commutative, associative, identity 0)
- **Metric**: Hamming distance
- **Embedding**: ℝ⁸ via {-1,+1} mapping
- **Similarity**: cosine, Euclidean
- **Transformations**: axis flip, bit flip, axis permutation

See SUBIT_v3.md for the full formal specification.

---

## 📦 What You Get

| Feature | Description |
|---------|-------------|
| **Formal algebra** | XOR, distance, projection, replacement, flip, permute |
| **Continuous SUBIT** | Soft vectors in ℝ⁸, cosine similarity, interpolation, radar charts |
| **Local LLM control** | Rewrite text into STATE/VALUE/FORM/FORCE mode via Ollama (no API key) |
| **Interactive 3D graph** | Click, search, filter by community |
| **Markdown report** | God nodes, surprising connections, archetype profile with ASCII bars |
| **Obsidian vault** | Backlinked knowledge base |
| **REST API + WebSocket** | Real‑time analysis |
| **Git hooks** | Auto‑sync on every commit |
| **Hybrid search** | SQLite indexing + SUBIT filtering + cosine similarity |
| **Agent system** | Four AI agents (STATE, VALUE, FORM, FORCE) |
| **Web UI** | Streamlit-based graphical interface |

---

## 🔧 Installation

```bash
# Basic installation
pip install subit-nous

# With all extras (testing, local LLM)
pip install subit-nous[all]
```

**Requirements:** Python 3.9+, [Ollama](https://ollama.com) (optional, for agents)

---

## 🎮 Quick Start

### 1. Analyze a folder or file

```bash
nous analyze ./my-documents --output ./knowledge
nous analyze my-file.txt --output ./knowledge
```

### 2. Watch mode (auto-update on changes)

```bash
nous watch ./my-documents --output ./live_output
```

### 3. Start API server

```bash
nous serve --port 8000
```

### 4. Install Git hooks (auto-analysis after commit)

```bash
nous hooks install .
```

### 5. Continuous SUBIT – soft vectors

```bash
nous soft ./my-folder --output profile.json
nous soft --sim1 file1.txt --sim2 file2.txt
nous soft --interp1 file1.txt --interp2 file2.txt --alpha 0.3
nous soft --radar profile.json
```

### 6. Hybrid search

```bash
nous index ./my-documents
nous search "climate change" --mode STATE --who WE --top 10
```

### 7. Agent system (requires Ollama)

```bash
nous agent "Explain AI" --mode STATE
nous agent "The sunset is beautiful" --mode auto
nous pipeline "Solar energy" --modes STATE,FORM,FORCE
```

### 8. Web UI

```bash
nous ui --port 8501
```

Then open `http://localhost:8501` in your browser.

---

## 📊 Example Output

### Command
```bash
nous analyze demo --output demo_out
```

### Report (demo_out/report.md)
```markdown
## Transversal Mode Profile
MICRO ████████████████████ 55.0%  (6 occurrences)
MACRO ██████░░░░░░░░░░░░░░ 18.0%  (2 occurrences)
MESO  ██████░░░░░░░░░░░░░░ 18.0%  (2 occurrences)
META  ███░░░░░░░░░░░░░░░░░  9.0%  (1 occurrences)
```

### Interactive Graph
Open `demo_out/graph.html` in your browser – a 3D visualization with colored nodes.

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_core.py -v
```

---

## 📁 Project Structure

```
subit-nous/
├── src/subit_nous/
│   ├── core.py          # Core SUBIT algebra
│   ├── subit_algebra.py # Formal algebraic class
│   ├── graph.py         # Knowledge graph builder
│   ├── exports.py       # Report & Obsidian export
│   ├── search.py        # Hybrid search (SQLite)
│   ├── agent.py         # Agent system (Ollama)
│   ├── ui.py            # Streamlit web interface
│   ├── api.py           # FastAPI server
│   └── cli.py           # CLI commands
├── tests/               # Unit tests
├── docs/                # Documentation
├── examples/            # Usage examples
└── demo/                # Demo data
```

---

## 📄 License

MIT

---

## Key Updates for v3.1.0

| Section | Change |
|---------|--------|
| Header | Version updated to 3.1.0 |
| What's New | Added bullet points for v3.1.0 features |
| Installation | Added `[all]` extras option |
| Quick Start | Added single file analysis example |
| Hybrid Search | New section for search commands |
| Agent System | New section for agent commands |
| Web UI | New section for UI commands |
| Testing | Added pytest instructions |
| Project Structure | Updated with new modules (search, agent, ui) |
