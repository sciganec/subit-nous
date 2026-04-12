#!/usr/bin/env python3
"""Test SUBIT-NOUS SDK."""

from subit_nous import SubitClient

def main():
    print("=" * 60)
    print("SUBIT-NOUS SDK Test")
    print("=" * 60)
    
    client = SubitClient()
    
    # 1. Analyze
    print("\n1. Text Analysis:")
    texts = [
        "I think logically about the east in spring",
        "We trust our community",
        "The beautiful sunset over the ocean"
    ]
    for text in texts:
        r = client.analyze(text)
        print(f"   {text[:40]:40} -> {r.archetype} ({r.subit})")
    
    # 2. Classify
    print("\n2. Classification:")
    r = client.classify("We trust our community")
    print(f"   We trust our community -> {r.archetype} (confidence: {r.confidence or 'N/A'})")
    
    # 3. Algebra
    print("\n3. SUBIT Algebra:")
    s1 = client.to_subit("I think logically")
    s2 = client.to_subit("We trust our community")
    print(f"   Distance: {client.distance(s1, s2)} bits differ")
    print(f"   XOR: {client.xor(s1, s2).to_human()}")
    
    # 4. Search (if index exists)
    print("\n4. Search:")
    try:
        results = client.search("logic", top_k=2)
        print(f"   Found {len(results)} results")
        for r in results:
            print(f"      {r.path[:50]}... (score: {r.score:.3f})")
    except Exception as e:
        print(f"   Search not available: {e}")
    
    # 5. Generate (if Ollama available)
    print("\n5. Generation:")
    try:
        response = client.generate("Explain AI", mode="STATE")
        print(f"   STATE: {response[:80]}...")
    except Exception as e:
        print(f"   Generation not available: {e}")
    
    print("\n" + "=" * 60)
    print("✅ SDK test complete!")

if __name__ == "__main__":
    main()