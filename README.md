# 🧠 SUBIT‑NOUS v4.0.0

## Formal algebraic coordinate system for meaning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Classifier Accuracy](https://img.shields.io/badge/accuracy-87.8%25-brightgreen)]()

> **NOUS** (νοῦς) – the intellect that perceives archetypes.  
> **SUBIT** – a 4‑dimensional algebraic space over (ℤ₂)⁸.

SUBIT‑NOUS turns any folder or file into a **computable knowledge graph** of 256 archetypes.  
No LLM required for the core – but you can **control LLM generation** locally via Ollama.

**Neural classifier now available with 87.8% accuracy!** 🎯

---

## ✨ What's New in v4.0.0

- **Neural Classifier** – fine-tuned DistilBERT (87.8% accuracy) for text → SUBIT prediction
- **`nous classify`** – CLI command with confidence scores and probability distribution
- **`nous query`** – find paths and connections between archetypes in the graph
- **`nous wiki`** – generate Wikipedia-style markdown documentation
- **`nous integrate`** – integrate with Claude Code, Cursor, and Gemini CLI
- **Smart `--watch`** – instant updates for code, debounced for docs
- **UMAP projection** – visualize semantic topology in 3D
- **Vector Interpolation UI** – smooth transitions between archetypes
- **Semantic clusters** – group archetypes by Hamming distance
- **Clifford Torus** – 3D visualization of all 256 states

---

## 🚀 One command. Any file or folder. Full knowledge graph.

```bash
pip install subit-nous
nous analyze ./my-folder --output ./knowledge
nous analyze my-file.txt --output ./knowledge
```

---

## 🧠 Classify text with neural AI (87.8% accuracy)

```bash
nous classify "I think logically about the east in spring"
# Output: MICRO mode (170) | STATE | ME | EAST | SPRING

nous classify "We trust our community" --probs
# Output with confidence scores and top predictions
```

---

## 📐 The SUBIT v4.0 Framework

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

See [SUBIT-v3.md](SUBIT_v3.md) for the full formal specification.

---

## 📦 What You Get

| Feature | Description |
|---------|-------------|
| **Neural Classifier** | Fine-tuned DistilBERT – **87.8% accuracy** |
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
| **Web UI** | Streamlit-based graphical interface with 10 tabs |
| **UMAP projection** | 3D semantic topology visualization |
| **Vector Interpolation** | Smooth transitions between archetypes |
| **Wiki export** | Wikipedia-style markdown documentation |

---

## 🔧 Installation

```bash
# Basic installation
pip install subit-nous

# With all extras (testing, local LLM, ML)
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

### 2. Classify text (neural, 87.8% accuracy)

```bash
nous classify "I think logically about the east"
nous classify "We trust our community" --probs
```

### 3. Query the knowledge graph

```bash
nous query "MICRO mode" "MACRO mode"
# Output shows the path: MICRO → ETHOS_WE_EAST_SPRING → MACRO
```

### 4. Watch mode (smart updates)

```bash
nous watch ./my-documents --output ./live_output
# Code files update instantly, docs wait for changes to settle
```

### 5. Generate wiki documentation

```bash
nous wiki nous_output/graph.json --output ./wiki
# Creates Wikipedia-style markdown files
```

### 6. Integrate with AI assistants

```bash
nous integrate all --output nous_output
# Creates CLAUDE.md, .cursor/rules, GEMINI.md
```

### 7. Start API server

```bash
nous serve --port 8000
```

### 8. Web UI

```bash
nous ui --port 8501
```

Then open `http://localhost:8501` in your browser.

---

## 📊 Example Output

### Classification
```bash
$ nous classify "I think logically about the east"
📝 Text: I think logically about the east
🎯 SUBIT: 170 (10101010)
🏺 Archetype: MICRO mode
🎭 Mode: STATE
👤 Who: ME
🧭 Where: EAST
⏰ When: SPRING
```

### Query
```bash
$ nous query "MICRO mode" "MACRO mode"
🔍 Querying graph: MICRO mode → MACRO mode

Shortest path found:

1. MICRO mode (ID: 170)
   └─[ EXTRACTED (confidence: 1.0) weight: 1 ]
2. ETHOS_WE_EAST_SPRING (ID: 235)
   └─[ EXTRACTED (confidence: 1.0) weight: 1 ]
3. MACRO mode (ID: 255)

Path length: 2 steps
```

### Report (nous_output/report.md)
```markdown
## Transversal Mode Profile
MICRO ████████████████████ 55.0%  (6 occurrences)
MACRO ██████░░░░░░░░░░░░░░ 18.0%  (2 occurrences)
MESO  ██████░░░░░░░░░░░░░░ 18.0%  (2 occurrences)
META  ███░░░░░░░░░░░░░░░░░  9.0%  (1 occurrences)
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Test classifier accuracy
pytest tests/test_classifier.py -v
```

---

## 📁 Project Structure

```
subit-nous/
├── src/subit_nous/
│   ├── core.py          # Core SUBIT algebra
│   ├── subit_algebra.py # Formal algebraic class
│   ├── classifier.py    # Neural classifier (DistilBERT)
│   ├── graph.py         # Knowledge graph builder
│   ├── exports.py       # Report & Obsidian export
│   ├── search.py        # Hybrid search (SQLite)
│   ├── agent.py         # Agent system (Ollama)
│   ├── query.py         # Graph query (paths, connections)
│   ├── wiki.py          # Wikipedia-style export
│   ├── integrations.py  # AI assistant integrations
│   ├── ui.py            # Streamlit web interface (10 tabs)
│   ├── api.py           # FastAPI server
│   └── cli.py           # CLI commands
├── tests/               # Unit tests
├── docs/                # Documentation
├── examples/            # Usage examples
├── scripts/             # Training scripts
└── demo/                # Demo data
```

---

## 📚 Documentation

- [API Reference](docs/api.md) – REST API documentation
- [Classifier Guide](docs/classifier.md) – Neural classifier training and usage
- [Formal Specification](SUBIT_v3.md) – Complete SUBIT algebra specification
- [CHANGELOG](CHANGELOG.md) – Version history

---

## 📄 License

MIT