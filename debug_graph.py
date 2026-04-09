from pathlib import Path
from subit_nous.core import text_to_subit

test_dir = Path("test_raw")
files = list(test_dir.rglob("*"))
print(f"Знайдено файлів: {len(files)}")
for f in files:
    if f.is_file():
        text = f.read_text(encoding='utf-8')
        subit = text_to_subit(text)
        print(f"{f.name}: {subit} ({subit:08b})")