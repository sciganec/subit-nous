# test_simple.py
from subit_nous.controlled_rewrite import controlled_rewrite
from subit_nous.core import text_to_subit

# Text without FORCE marker
text = "We think."
current = text_to_subit(text)
target = 0b10101010  # MICRO

print(f"Text: {text}")
print(f"Current: {current:08b}")
print(f"Target: {target:08b}")

result = controlled_rewrite(text, target)
result_subit = text_to_subit(result)

print(f"Rewritten: {result}")
print(f"Result SUBIT: {result_subit:08b}")
print(f"Success: {result_subit == target}")