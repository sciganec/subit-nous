
## 📊 SUBIT-NOUS Knowledge Graph

This project has a knowledge graph that captures archetypal patterns across the codebase.

### How to use it

1. **Before answering architecture or design questions**, read `nous_output\report.md` for:
   - God nodes (most connected archetypes)
   - Community structure
   - Unexpected connections

2. **For specific queries**, use these commands:
   ```bash
   nous search "your query" --mode STATE --top 5
   nous query "start concept" "target concept"
   ```

3. **The graph is ~1500x more token-efficient** than reading raw files.

### Available modes

| Mode | Style | When to use |
|------|-------|-------------|
| STATE | logical, factual | technical questions, analysis |
| VALUE | ethical, communal | impact assessment, team decisions |
| FORM | aesthetic, emotional | creative tasks, user experience |
| FORCE | willful, strategic | planning, execution, negotiations |

Always prefer the knowledge graph over grepping through raw files.
