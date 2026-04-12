# 🧠 SUBIT‑NOUS v5.0

## Operating System for Meaning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> **SUBIT = discrete cognitive addressing for AI systems**

SUBIT‑NOUS transforms any text into an **8-bit address** in a space of 256 archetypes. It is the world's first operating system for meaning.

---

## 📐 Algebra of Meaning

```
SUBIT = (ℤ₂)⁸ = WHO × WHERE × WHEN × MODE
```

| Axis | Values | Bits |
|------|--------|------|
| **WHO** | ME / WE / YOU / THEY | 10/11/01/00 |
| **WHERE** | EAST / SOUTH / WEST / NORTH | 10/11/01/00 |
| **WHEN** | SPRING / SUMMER / AUTUMN / WINTER | 10/11/01/00 |
| **MODE** | LOGOS / ETHOS / PATHOS / THYMOS | 10/11/01/00 |

**Four cardinal archetypes:**
- `MICRO` (10,10,10,10) = 170 – individual, logical
- `MACRO` (11,11,11,11) = 255 – collective, ethical
- `MESO` (01,01,01,01) = 85 – dialogical, aesthetic
- `META` (00,00,00,00) = 0 – systemic, willful

---

## 🚀 New in v5.0: Three Operators

### 🎭 Mask – Local Editing

Changes only sentences that match a condition.

```bash
# Change all FORCE sentences to LOGOS
nous mask input.txt --condition "MODE=THYMOS" --transform "MODE=LOGOS"

# Change perspective from ME to WE
nous mask input.txt --condition "WHO=ME" --transform "WHO=WE"
```

### 🎨 Transfer – Global Style Transfer

Moves entire text to a target point in SUBIT space.

```bash
# Move text to MICRO archetype
nous transfer content.txt --target 170 --output logical.txt

# Transfer style from poem to report
nous transfer report.txt --style poem.txt --output poetic_report.txt
```

### 🧬 Evolution – Path Animation

Smoothly changes text step by step, showing trajectory through space.

```bash
# Evolve from FORCE to LOGOS in 5 steps
nous evolve input.txt --from FORCE --to LOGOS --steps 5 --output evolution/
```

---

## 📊 Other Commands

### Classification & Analysis

```bash
# Neural text classification (87.8% accuracy)
nous classify "I think logically about the east"

# Find paths in the graph
nous query "MICRO mode" "MACRO mode"

# Hybrid search
nous search "climate change" --mode STATE --who WE --top 5
```

### DSL – Query Language for Meaning

```bash
# Find all sentences in logical style
nous query text "WHERE MODE=LOGOS" --source doc.txt

# Find graph nodes with ME perspective
nous query graph "WHERE WHO=ME" --source graph.json
```

### Agents & Generation

```bash
# Style-specific generation
nous agent "Explain solar energy" --mode LOGOS

# Agent pipeline
nous pipeline "Solar energy" --modes LOGOS,PATHOS,THYMOS
```

### Visualization

```bash
# Web UI (10 tabs)
nous ui --port 8501

# 3D graph, UMAP, Torus, clusters
nous umap graph.json --output umap.html
nous torus graph.json --output torus.html
nous clusters graph.json --max-dist 2
```

---

## 🔧 Installation

```bash
pip install subit-nous
```

Or from GitHub:

```bash
pip install git+https://github.com/sciganec/subit-nous.git
```

---

## 🎥 Video Demo Script (2-3 minutes)

### Scene 1: Mask (Local Editing) – 45 seconds

**Preparation:**
```bash
echo "We must act now. The sunset is beautiful. I think logically." > test.txt
```

**Demo:**
1. Show input text
2. Run `nous mask test.txt --condition "WHO=WE" --transform "WHO=ME" --output masked.txt`
3. Show result: `"I must act now. The sunset is beautiful. I think logically."`
4. Explain: only the first sentence changed (where WE was)

### Scene 2: Transfer (Style Transfer) – 45 seconds

**Preparation:**
```bash
echo "The product is good. We recommend it." > content.txt
echo "The sunset paints the sky in gold." > style.txt
```

**Demo:**
1. Show content and style
2. Run `nous transfer content.txt --style style.txt --output transferred.txt`
3. Show result: `"The product radiates quality. We wholeheartedly endorse its brilliance."`
4. Explain: meaning preserved, style transformed

### Scene 3: Evolution (Animation) – 45 seconds

**Preparation:**
```bash
echo "We must win." > start.txt
```

**Demo:**
1. Run `nous evolve start.txt --from FORCE --to LOGOS --steps 3 --output evolution/`
2. Show three steps:
   - Step 0: `"We must win."` (FORCE)
   - Step 1: `"We need to win."` (mixed)
   - Step 2: `"We can achieve victory."` (LOGOS)
3. Explain: smooth transition from will to logic

### Final Frame (15 seconds)

Show logo and call to action:
```
🧠 SUBIT‑NOUS
Operating System for Meaning
pip install subit-nous
github.com/sciganec/subit-nous
```

---

## 🔗 Links

- **GitHub:** https://github.com/sciganec/subit-nous
---

**SUBIT‑NOUS – discrete cognitive addressing for AI systems.** 🧠🚀