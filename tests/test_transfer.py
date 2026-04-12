#!/usr/bin/env python3
"""Test TransferOperator."""

import sys
sys.path.insert(0, 'src')

from subit_nous.operators import TransferOperator

# Test text
text = "We must act now. This is critical."

print("Original text:")
print(text)
print()

# Transfer to MICRO mode (individual, logical)
transfer = TransferOperator(target_subit=170)
result = transfer.apply_to_text(text)

print("After Transfer (→ MICRO):")
print(result)