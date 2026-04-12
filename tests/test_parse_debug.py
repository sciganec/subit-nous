from subit_nous.dsl import parse

# Test direct parsing
test_queries = [
    "text WHERE MODE=PATHOS",
    "text WHERE MODE=LOGOS",
    "text WHERE WHO=ME",
]

for q in test_queries:
    print(f"\nParsing: '{q}'")
    try:
        result = parse(q)
        print(f"  ✅ Success: {result}")
    except Exception as e:
        print(f"  ❌ Error: {e}")