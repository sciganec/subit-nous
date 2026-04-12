import sys
sys.path.insert(0, 'src')

from subit_nous.controlled_rewrite import rewrite_axis

text = "We recommend this product."
result = rewrite_axis(text, "WHO", 2)  # 2 = ME

print(f"Original: {text}")
print(f"Rewritten: {result}")