import sys
sys.path.insert(0, 'src')

from subit_nous.operators import TransferOperator
from subit_nous.core import text_to_subit

# Test content and style
content = "We recommend this product."
style = "The sunset paints the sky in gold."

print(f"Content: {content}")
print(f"Style: {style}")
print()

# Create transfer operator from style
transfer = TransferOperator.from_style(style, alpha=0.7)
print(f"Target SUBIT: {transfer.target_subit:08b}")

# Apply transfer
result = transfer.apply_to_text(content)
print(f"\nResult: {result}")

# Verify SUBIT changed
original_subit = text_to_subit(content)
result_subit = text_to_subit(result)
print(f"Original SUBIT: {original_subit:08b}")
print(f"Result SUBIT: {result_subit:08b}")