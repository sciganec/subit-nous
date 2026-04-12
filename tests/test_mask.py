#!/usr/bin/env python3
"""Test MaskOperator."""

import sys
sys.path.insert(0, 'src')

from subit_nous.operators import MaskOperator

# Test text
text = "I think logically. The sunset is beautiful. We must act now."

print("Original text:")
print(text)
print()

# Use GREEK names (PATHOS, LOGOS, ETHOS, THYMOS)
mask = MaskOperator("MODE=PATHOS", "MODE=LOGOS")  # FORM → STATE
result = mask.apply_to_text(text)

print("After Mask (PATHOS → LOGOS):")
print(result)
print()

# Mask: change ME to WE
mask2 = MaskOperator("WHO=ME", "WHO=WE")
result2 = mask2.apply_to_text(text)

print("After Mask (ME → WE):")
print(result2)