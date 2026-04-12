#!/usr/bin/env python3
"""Complete demo of SUBIT-NOUS v5.0 operators."""

import subprocess
import sys
from pathlib import Path

def check_ollama():
    """Check if Ollama is running."""
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    return result.returncode == 0

def run_demo():
    print("=" * 60)
    print("🧠 SUBIT-NOUS v5.0 Demo")
    print("Three Operators: Mask · Transfer · Evolution")
    print("=" * 60)
    
    # Check Ollama
    ollama_ok = check_ollama()
    if not ollama_ok:
        print("\n⚠️ Ollama not running. Transfer operator will use fallback mode.")
        print("   For full experience, run: ollama serve\n")
    
    # Prepare test files
    Path("test.txt").write_text("We must act now. The sunset is beautiful. I think logically.")
    Path("content.txt").write_text("The product is good. We recommend it.")
    Path("style.txt").write_text("The sunset paints the sky in gold.")
    Path("start.txt").write_text("We must win.")
    
    # Demo 1: Mask
    print("\n" + "=" * 60)
    print("🎭 Demo 1: Mask (Local Editing)")
    print("=" * 60)
    print(f"\nInput: {Path('test.txt').read_text().strip()}")
    print("\nCommand: nous mask test.txt --condition 'WHO=WE' --transform 'WHO=ME'")
    
    result = subprocess.run(
        ["nous", "mask", "test.txt", "--condition", "WHO=WE", "--transform", "WHO=ME", "--output", "masked.txt"],
        capture_output=True, text=True
    )
    
    if Path("masked.txt").exists():
        print(f"\nOutput: {Path('masked.txt').read_text().strip()}")
    else:
        print(f"Error: {result.stderr}")
    
    # Demo 2: Transfer
    print("\n" + "=" * 60)
    print("🎨 Demo 2: Transfer (Style Transfer)")
    print("=" * 60)
    print(f"\nContent: {Path('content.txt').read_text().strip()}")
    print(f"Style: {Path('style.txt').read_text().strip()}")
    print("\nCommand: nous transfer content.txt --style style.txt")
    
    result = subprocess.run(
        ["nous", "transfer", "content.txt", "--style", "style.txt", "--output", "transferred.txt"],
        capture_output=True, text=True
    )
    
    if Path("transferred.txt").exists():
        transferred = Path("transferred.txt").read_text().strip()
        print(f"\nResult: {transferred}")
        if transferred == "The product is good. We recommend it.":
            print("\n⚠️ Transfer used fallback mode (Ollama not running)")
            print("   Start Ollama for full style transfer effect")
    else:
        print(f"Error: {result.stderr}")
    
    # Demo 3: Evolution
    print("\n" + "=" * 60)
    print("🧬 Demo 3: Evolution (Path Animation)")
    print("=" * 60)
    print(f"\nInput: {Path('start.txt').read_text().strip()}")
    print("\nCommand: nous evolve start.txt --from FORCE --to LOGOS --steps 3")
    
    result = subprocess.run(
        ["nous", "evolve", "start.txt", "--from", "FORCE", "--to", "LOGOS", "--steps", "3", "--output", "evolution"],
        capture_output=True, text=True
    )
    
    evolution_dir = Path("evolution")
    if evolution_dir.exists():
        print("\nEvolution steps:")
        for step_file in sorted(evolution_dir.glob("step_*.txt")):
            content = step_file.read_text().strip()
            print(f"  {step_file.name}: {content}")
    else:
        print(f"Error: {result.stderr}")
    
    # Cleanup
    print("\n" + "=" * 60)
    print("✅ Demo complete!")
    print("=" * 60)
    print("\nCleanup:")
    for f in ["test.txt", "content.txt", "style.txt", "start.txt", "masked.txt", "transferred.txt"]:
        if Path(f).exists():
            Path(f).unlink()
            print(f"  Removed {f}")
    if Path("evolution").exists():
        import shutil
        shutil.rmtree("evolution")
        print("  Removed evolution/")
    
    print("\n🧠 SUBIT-NOUS: Operating System for Meaning")
    print("pip install subit-nous | github.com/sciganec/subit-nous")
    
    if not ollama_ok:
        print("\n💡 Tip: Run 'ollama serve' and 'ollama pull llama3.2:3b' for full experience")

if __name__ == "__main__":
    run_demo()