from subit_nous.core import text_to_subit

with open("force.txt") as f:
    force_text = f.read()
with open("pathos.txt") as f:
    pathos_text = f.read()

print(f"force SUBIT: {text_to_subit(force_text):08b} ({text_to_subit(force_text)})")
print(f"pathos SUBIT: {text_to_subit(pathos_text):08b} ({text_to_subit(pathos_text)})")