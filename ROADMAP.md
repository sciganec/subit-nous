Ось **оновлений ROADMAP.md** для SUBIT‑NOUS, що відображає поточний стан v4.0.0 та плани на майбутнє.

```markdown
# 🧠 SUBIT‑NOUS Roadmap

## Current Version: v4.0.0 (2026-04-11)

### ✅ Completed

#### v4.0.0
- [x] Neural classifier (DistilBERT) for text → SUBIT prediction
- [x] `nous classify` command with confidence scores
- [x] `nous update` – incremental graph updates (SHA256 cache)
- [x] `nous export` – GraphML, Cypher, JSON, Obsidian, Wiki
- [x] `nous integrate` – Claude Code integration (CLAUDE.md)
- [x] SDK with `SubitClient` for Python developers
- [x] Web UI with dark theme and 6 tabs
- [x] Sources and confidence scores in graph JSON
- [x] Fixed Windows Unicode issues

#### v3.1.0
- [x] Single file analysis
- [x] Empty file handling
- [x] `nous version` command
- [x] Windows console compatibility

#### v3.0.0
- [x] Formal algebraic core (ℤ₂)⁸
- [x] XOR, distance, projection, replace, invert, flip, permute
- [x] Continuous SUBIT (soft vectors, cosine similarity, interpolation)
- [x] Hybrid search with SQLite
- [x] Agent system (4 modes)
- [x] Web UI (Streamlit)

---

## 🚀 Next Releases

### v4.1.0 – Intelligent Search & Context (1-2 weeks)

#### High Priority
- [ ] **Query Rewriting** – LLM expands natural language queries into SUBIT filters
  ```python
  # "decisive actions" → {"mode": "FORCE", "who": "THEY"}
  ```
- [ ] **Dynamic Agent Switching** – agents automatically change MODE based on context
- [ ] **Classifier Fine-tuning** – improve accuracy from 80-85% to 90%+ (more data, RoBERTa)

#### Medium Priority
- [ ] **`nous suggest`** – suggest optimal MODE/WHO for a given text
- [ ] **Confidence thresholds** – configurable minimum confidence for classifications

---

### v4.2.0 – Geometry & Visualization (2-3 weeks)

#### High Priority
- [ ] **Clustered Knowledge Domains** – group nodes by Hamming distance (semantic neighborhoods)
- [ ] **Vector Interpolation UI** – sliders in Web UI for smooth transitions between archetypes
- [ ] **Manifold Analysis** – 3D projection of Clifford torus for all 256 states

#### Medium Priority
- [ ] **Force-directed graph layout** – better visualization of large graphs
- [ ] **Community coloring** – automatic color assignment by Leiden clusters

---

### v4.5.0 – Ecosystem & Integrations (3-4 weeks)

#### High Priority
- [ ] **Browser Extension** – analyze any web page, show SUBIT profile
- [ ] **Cursor integration** – `.cursorrules` for Cursor IDE
- [ ] **Codex/Gemini integration** – AGENTS.md support

#### Medium Priority
- [ ] **Multi-modal SUBIT** – image analysis via CLIP or metadata
- [ ] **VS Code extension** – inline archetype visualization

#### Low Priority
- [ ] **Cloud Sync** – encrypted knowledge graph sharing (experimental)

---

### v5.0.0 – Scientific Maturity (1-2 months)

#### High Priority
- [ ] **Academic Publication** – NeurIPS/arXiv paper on SUBIT algebra
- [ ] **Benchmark suite** – standardized evaluation for archetype classification
- [ ] **Production-ready SDK** – stable API, full type hints, extensive tests

#### Medium Priority
- [ ] **Custom Axis Plugin System** – user-defined axes for specific domains
- [ ] **Open standard** – JSON schema for SUBIT interchange format

#### Low Priority
- [ ] **Cross-language SDKs** – JavaScript/TypeScript, Rust, Go

---

## 📊 Progress Summary

| Version | Focus | Status | Completion |
|---------|-------|--------|------------|
| v3.0.0 | Formal Algebra | ✅ Released | 100% |
| v3.1.0 | Windows Compatibility | ✅ Released | 100% |
| v4.0.0 | Neural Classifier + SDK | ✅ Released | 100% |
| v4.1.0 | Intelligent Search | 🟡 In Progress | 0% |
| v4.2.0 | Geometry & Visualization | ⏳ Planned | 0% |
| v4.5.0 | Ecosystem | ⏳ Planned | 0% |
| v5.0.0 | Scientific Maturity | 🔮 Future | 0% |

---

## 🎯 How to Contribute

1. Check the [issue tracker](https://github.com/sciganec/subit-nous/issues)
2. Pick a feature from the roadmap above
3. Submit a PR with tests and documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📅 Timeline (Estimated)

| Quarter | Focus |
|---------|-------|
| Q2 2026 | v4.1.0 (Intelligent Search) |
| Q3 2026 | v4.2.0 (Geometry & Visualization) |
| Q4 2026 | v4.5.0 (Ecosystem) |
| Q1 2027 | v5.0.0 (Scientific Maturity) |

---

**Legend:** ✅ Released | 🟡 In Progress | ⏳ Planned | 🔮 Future
