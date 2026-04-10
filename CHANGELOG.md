# Changelog

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