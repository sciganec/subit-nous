"""Demonstrate SUBIT core SDK functionality."""

from subit_nous.subit_algebra import Subit

# Create states from text
micro = Subit.from_text("I think logically about the east in spring")
macro = Subit.from_text("We trust our community in the south during summer")

print(f"MICRO: {micro} (bits={micro.bits:08b})")
print(f"MACRO: {macro} (bits={macro.bits:08b})")

# Operations - використовуємо оператор ^ (який викликає __xor__)
xor_result = micro ^ macro
print(f"XOR: {xor_result} (bits={xor_result.bits:08b})")

# Або явно через метод, якщо додати
# Якщо хочете мати метод .xor(), додайте його в клас Subit

distance = micro.distance(macro)
print(f"Hamming distance: {distance}")

# Projections
print(f"MICRO MODE: {micro.project('MODE')} (STATE=2)")
print(f"MACRO WHO: {macro.project('WHO')} (WE=3)")

# Flip axis
flipped = micro.flip_axis("WHO")
print(f"MICRO flipped WHO: {flipped} (bits={flipped.bits:08b})")

# Invert
inverted = micro.invert()
print(f"MICRO inverted: {inverted}")