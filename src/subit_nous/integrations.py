"""Integrations with AI coding assistants (Claude Code, Cursor, Gemini CLI, etc.)."""

from pathlib import Path


def generate_claude_md(output_dir: str = "./nous_output") -> str:
    report_path = Path(output_dir) / "report.md"
    return f"""
## 📊 SUBIT-NOUS Knowledge Graph

This project has a knowledge graph that captures archetypal patterns across the codebase.

### How to use it

1. **Before answering architecture or design questions**, read `{report_path}` for:
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
"""


def generate_cursor_rule(output_dir: str = "./nous_output") -> str:
    return f"""---
description: SUBIT-NOUS Knowledge Graph - use before searching files
alwaysApply: true
---

# SUBIT-NOUS Knowledge Graph

Before answering questions about this codebase:

1. Read `{output_dir}/report.md` to understand:
   - God nodes (most connected archetypes)
   - Community structure
   - Unexpected connections

2. For specific questions, use:
   ```bash
   nous search "your query" --mode STATE --top 5
   nous query "start" "target"
   ```

The knowledge graph is ~1500x more token-efficient than reading raw files.
"""


def generate_gemini_md(output_dir: str = "./nous_output") -> str:
    report_path = Path(output_dir) / "report.md"
    return f"""
## SUBIT-NOUS Knowledge Graph

Before answering questions, read `{report_path}` to understand the archetype structure.

Use `nous search "query" --mode STATE` for specific questions.

The graph is 1500x more token-efficient than reading raw files.
"""


def install_claude_integration(output_dir: str = "./nous_output") -> None:
    claude_md = Path("CLAUDE.md")
    content = generate_claude_md(output_dir)
    
    if claude_md.exists():
        existing = claude_md.read_text(encoding='utf-8')
        if "SUBIT-NOUS Knowledge Graph" not in existing:
            with open(claude_md, 'a', encoding='utf-8') as f:
                f.write(f"\n{content}")
            print("[OK] Added SUBIT-NOUS section to existing CLAUDE.md")
        else:
            print("[OK] CLAUDE.md already contains SUBIT-NOUS instructions")
    else:
        claude_md.write_text(content, encoding='utf-8')
        print("[OK] Created CLAUDE.md with SUBIT-NOUS instructions")


def install_cursor_integration(output_dir: str = "./nous_output") -> None:
    rules_dir = Path(".cursor/rules")
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    rule_file = rules_dir / "subit-nous.mdc"
    content = generate_cursor_rule(output_dir)
    rule_file.write_text(content, encoding='utf-8')
    print(f"[OK] Installed Cursor rule to {rule_file}")


def install_gemini_integration(output_dir: str = "./nous_output") -> None:
    gemini_md = Path("GEMINI.md")
    content = generate_gemini_md(output_dir)
    
    if gemini_md.exists():
        existing = gemini_md.read_text(encoding='utf-8')
        if "SUBIT-NOUS Knowledge Graph" not in existing:
            with open(gemini_md, 'a', encoding='utf-8') as f:
                f.write(f"\n{content}")
            print("[OK] Added SUBIT-NOUS section to existing GEMINI.md")
        else:
            print("[OK] GEMINI.md already contains SUBIT-NOUS instructions")
    else:
        gemini_md.write_text(content, encoding='utf-8')
        print("[OK] Created GEMINI.md with SUBIT-NOUS instructions")


def install_all_integrations(output_dir: str = "./nous_output") -> None:
    print("Installing all integrations...")
    install_claude_integration(output_dir)
    install_cursor_integration(output_dir)
    install_gemini_integration(output_dir)
    print("[OK] All integrations installed!")


def uninstall_claude_integration() -> None:
    claude_md = Path("CLAUDE.md")
    if claude_md.exists():
        content = claude_md.read_text(encoding='utf-8')
        if "SUBIT-NOUS Knowledge Graph" in content:
            lines = content.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if '## 📊 SUBIT-NOUS Knowledge Graph' in line:
                    skip = True
                if skip and line.startswith('## '):
                    skip = False
                if not skip and 'SUBIT-NOUS Knowledge Graph' not in line:
                    new_lines.append(line)
            claude_md.write_text('\n'.join(new_lines), encoding='utf-8')
            print("[OK] Removed SUBIT-NOUS section from CLAUDE.md")
        else:
            print("[OK] No SUBIT-NOUS section found in CLAUDE.md")


def uninstall_cursor_integration() -> None:
    rule_file = Path(".cursor/rules/subit-nous.mdc")
    if rule_file.exists():
        rule_file.unlink()
        print(f"[OK] Removed {rule_file}")
    else:
        print("[OK] No Cursor rule found")


def uninstall_gemini_integration() -> None:
    gemini_md = Path("GEMINI.md")
    if gemini_md.exists():
        content = gemini_md.read_text(encoding='utf-8')
        if "SUBIT-NOUS Knowledge Graph" in content:
            lines = content.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if '## SUBIT-NOUS Knowledge Graph' in line:
                    skip = True
                if skip and line.startswith('## '):
                    skip = False
                if not skip:
                    new_lines.append(line)
            gemini_md.write_text('\n'.join(new_lines), encoding='utf-8')
            print("[OK] Removed SUBIT-NOUS section from GEMINI.md")
        else:
            print("[OK] No SUBIT-NOUS section found in GEMINI.md")