"""Demonstrate SUBIT control generation – one prompt, four different outputs."""

from subit_nous.control import apply_subit
from subit_nous.subit_algebra import Subit

prompt = "Write a short statement about renewable energy."

modes = [
    ("STATE", 2, "logical, factual"),
    ("VALUE", 3, "ethical, communal"),
    ("FORM", 1, "aesthetic, emotional"),
    ("FORCE", 0, "willful, strategic"),
]

print(f"Original prompt: {prompt}\n")
print("=" * 60)

for mode_name, mode_bits, description in modes:
    # Create Subit state with default WHO=ME (2), WHERE=EAST (2), WHEN=SPRING (2)
    target = Subit.from_coords(who=2, where=2, when=2, mode=mode_bits)

    print(f"\n--- {mode_name} mode ({description}) ---")
    print(f"Target: {target.to_human()}")

    # Uncomment to actually run (requires Ollama)
    # result = apply_subit(prompt, target)
    # print(f"Result: {result}")

print("\n" + "=" * 60)
print("To actually run, uncomment the apply_subit calls and ensure Ollama is running.")