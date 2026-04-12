#!/usr/bin/env python3
"""Direct test of DSL without CLI."""

import sys
sys.path.insert(0, 'src')

from subit_nous.dsl import parse, Evaluator

# Create test file
with open("doc.txt", "w") as f:
    f.write("I think logically. The sunset is beautiful. We must act now.")

# Use GREEK names (these work)
queries = [
    "text WHERE MODE=LOGOS",   # STATE
    "text WHERE MODE=ETHOS",   # VALUE
    "text WHERE MODE=PATHOS",  # FORM
    "text WHERE MODE=THYMOS",  # FORCE
]

for query_str in queries:
    print(f"\n--- Query: {query_str} ---")
    try:
        parsed = parse(query_str)
        parsed.source = "doc.txt"
        evaluator = Evaluator()
        results = evaluator.evaluate(parsed)
        print(f"Found {len(results)} matches:")
        for r in results:
            print(f"  {r['text'][:50]} → {r['archetype']}")
    except Exception as e:
        print(f"Error: {e}")

print("\n✅ Done")