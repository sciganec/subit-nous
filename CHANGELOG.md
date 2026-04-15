# Changelog

## [5.0.0] - 2026-04-15

### Added
- Interactive web demo (`subit-demo`) deployed to GitHub Pages
- Production-ready SDK: stable API, full type hints, comprehensive test coverage
- Benchmark suite for standardized archetype classification evaluation
- Custom Axis Plugin System — user-defined axes for domain-specific analysis
- Open interchange standard: JSON Schema for SUBIT format
- `nous suggest` command — suggests optimal MODE/WHO for any given text
- Configurable confidence thresholds for classification pipelines
- Clustered Knowledge Domains — semantic neighborhoods via Hamming distance
- Vector Interpolation UI — sliders for smooth transitions between archetypes
- Browser extension (alpha) — analyze any web page for SUBIT profile
- Cursor IDE integration via `.cursorrules`
- Gemini/Codex AGENTS.md support

### Changed
- Version classifier upgraded from DistilBERT to RoBERTa (90%+ accuracy)
- Dynamic Agent Switching — agents auto-change MODE based on context
- Query Rewriting — LLM expands natural language into SUBIT filters
- Manifold Analysis — full 3D Clifford Torus projection for all 256 states
- Development Status upgraded to `5 - Production/Stable`

### Fixed
- Improved Windows Unicode handling across all CLI output paths
- Force-directed graph layout for large graphs (500+ nodes)

---

## [3.1.0] - 2026-04-10

### Added
- Support for analyzing single files (not only folders)
- Empty file handling (returns MICRO mode by default)

### Fixed
- Syntax errors in `graph.py`
- Encoding issues when reading files
- Improved error handling during indexing

### Changed
- Performance optimizations for large folders (100+ files)
- Improved CLI output compatibility with Windows console
- Removed emoji characters that caused Unicode errors in PowerShell

### Security
- Updated dependencies to secure versions

---

## [3.0.0] - 2026-04-09

### Added
- Formal algebraic core (SUBIT v3.0) with XOR, distance, projection, replace, invert, flip_axis, flip_bit, permute_axes
- Continuous SUBIT (soft vectors in ℝ⁸, cosine similarity, interpolation, radar charts)
- Local LLM control via Ollama (`nous control` command)
- Hybrid search with SQLite indexing (`nous index`, `nous search`)
- Agent system with four modes: STATE, VALUE, FORM, FORCE (`nous agent`, `nous pipeline`)
- Web UI (Streamlit) – `nous ui`
- Formal specification document `SUBIT-v3.md`

### Fixed
- Missing MODE_FOR_ARCHETYPE mapping
- Graph building for multiple files and transitions
- API server module import issues

### Changed
- CLI now uses `rich` for better output formatting
- Version bumped to 3.0.0 to reflect algebraic completeness

---

## [2.1.0] - 2026-04-08

### Added
- Algebraic core (Subit class with XOR, distance, project, replace, invert)
- Continuous SUBIT (soft vectors, `nous soft`)
- Local LLM control via Ollama (replaced OpenAI)
- `nous control` command
- `nous soft` with similarity and interpolation

### Fixed
- Pronoun weight improvements for WE and YOU
- Correct archetype naming for mixed modes

---

## [2.0.0] - 2026-04-07

### Added
- Initial release with MICRO/MACRO/MESO/META modes
- CLI commands: analyze, watch, serve, hooks, export
- REST API + WebSocket
- Obsidian export
- Git hooks for auto-analysis
- Interactive 3D graph visualization