#!/usr/bin/env python3
"""Test controlled rewrite."""

import sys
sys.path.insert(0, 'src')

from subit_nous.controlled_rewrite import semantic_delta, controlled_rewrite
from subit_nous.core import text_to_subit

# Test text
text = "We must act now."
current = text_to_subit(text)
target = 0b10101010  # MICRO mode

print(f"Text: {text}")
print(f"Current SUBIT: {current:08b}")
print(f"Target SUBIT: {target:08b}")
print(f"Delta axes: {semantic_delta(current, target)}")
print()

result = controlled_rewrite(text, target)
result_subit = text_to_subit(result)

print(f"Rewritten: {result}")
print(f"Result SUBIT: {result_subit:08b}")
print(f"Target achieved: {result_subit == target}")
print()

# Check if "I" is recognized as ME
test_me = text_to_subit("I think")
print(f"'I think' SUBIT: {test_me:08b} (expected 10101010?)")