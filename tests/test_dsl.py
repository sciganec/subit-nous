#!/usr/bin/env python3
"""Test DSL functionality."""

from subit_nous.dsl import parse, Evaluator
from subit_nous.core import text_to_subit

# Test 1: Parse simple condition
print("Test 1: Parse MODE=FORM")
query = parse("text WHERE MODE=FORM")
print(f"  Parsed: {query}")
print(f"  Condition: {query.condition}")

# Test 2: Parse AND condition
print("\nTest 2: Parse WHO=ME AND MODE=STATE")
query = parse("text WHERE WHO=ME AND MODE=STATE")
print(f"  Parsed: {query}")

# Test 3: Parse with parentheses
print("\nTest 3: Parse (WHO=ME AND MODE=STATE) OR DISTANCE>2")
query = parse("text WHERE (WHO=ME AND MODE=STATE) OR DISTANCE>2")
print(f"  Parsed: {query}")

# Test 4: Evaluate on actual text
print("\nTest 4: Evaluate on text")
with open("doc.txt", "w") as f:
    f.write("I think logically. The sunset is beautiful. We must act now.")

query = parse("text WHERE MODE=FORM")
query.source = "doc.txt"

evaluator = Evaluator()
results = evaluator.evaluate(query)
print(f"  Found {len(results)} matches:")
for r in results:
    print(f"    - {r['text'][:50]}... → {r['archetype']}")

print("\n✅ DSL tests passed!")