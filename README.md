# 🧠 SUBIT‑NOUS v3.0

## Formal algebraic coordinate system for meaning

> **NOUS** (νοῦς) – the intellect that perceives archetypes.  
> **SUBIT** – a 4‑dimensional algebraic space over (ℤ₂)⁸.

SUBIT‑NOUS turns any folder into a **computable knowledge graph** of 256 archetypes.  
No LLM required for the core – but you can **control LLM generation** locally via Ollama.

---

## 🔗 One command. Any folder. Full knowledge graph.

```bash
pip install subit-nous
nous analyze ./raw --output ./knowledge
```

---

## ✨ What you get

- **Formal algebra** – XOR, distance, projection, replacement, axis flip, bit flip, axis permutation
- **Continuous SUBIT** – soft vectors in ℝ⁸, cosine similarity, interpolation, radar charts
- **Local LLM control** – rewrite any text into **STATE / VALUE / FORM / FORCE** mode using Ollama (no API key)
- **Interactive 3D graph** – click, search, filter by community
- **Markdown report** – god nodes, surprising connections, archetype profile with ASCII bars
- **Obsidian vault** – backlinked knowledge base
- **REST API + WebSocket** – real‑time analysis
- **Git hooks** – auto‑sync on every commit

---

## 📐 The SUBIT v3.0 framework

Four axes, each with 4 values (2 bits):

| Axis   | Values                           | Binary   |
|--------|----------------------------------|----------|
| WHO    | ME / WE / YOU / THEY             | 10/11/01/00 |
| WHERE  | EAST / SOUTH / WEST / NORTH      | 10/11/01/00 |
| WHEN   | SPRING / SUMMER / AUTUMN / WINTER | 10/11/01/00 |
| MODE   | STATE / VALUE / FORM / FORCE     | 10/11/01/00 |

Interface layer:  
`STATE → LOGOS`, `VALUE → ETHOS`, `FORM → PATHOS`, `FORCE → THYMOS`.

### Algebraic structure

- **Space**: (ℤ₂)⁸  
- **Operation**: XOR (commutative, associative, identity 0)  
- **Metric**: Hamming distance  
- **Embedding**: ℝ⁸ via {-1,+1} mapping  
- **Similarity**: cosine, Euclidean  
- **Transformations**: axis flip, bit flip, axis permutation  

---

## 🚀 Quick start

### 1. Analyse a folder

```bash
nous analyse ./my-documents
```

### 2. Watch mode (auto‑update on changes)

```bash
nous watch ./my-documents --output ./live_output
```

### 3. Start API server

```bash
nous serve --port 8000
```

### 4. Install Git hooks (auto‑analysis after commit)

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

### 6. Local LLM control (requires [Ollama](https://ollama.com))

```bash
nous control "I think logically about the east" STATE --model llama3.2:3b
```

---

## 📦 Installation

```bash
pip install subit-nous
```

For development with all extras (testing, linting, local LLM):

```bash
pip install subit-nous[all]
```

---

## 🧪 Example

```bash
git clone https://github.com/sciganec/subit-nous.git
cd subit-nous
pip install -e .
nous analyse demo --output demo_out
open demo_out/graph.html
```

---

## 📄 License

MIT