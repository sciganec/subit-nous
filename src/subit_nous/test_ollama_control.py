# test_ollama_control.py
import sys
from subit_nous.llm_control_ollama import apply_control

# Тестові тексти для різних режимів
test_text = "I think the server needs to be restarted because of a memory leak."
target_modes = ["STATE", "VALUE", "FORM", "FORCE"]

for mode in target_modes:
    print(f"\n--- Applying control to mode: {mode} ---")
    try:
        # target_mode має бути числом: 2 для STATE, 3 для VALUE, 1 для FORM, 0 для FORCE
        result = apply_control(test_text, MODE_VALUES[mode], model="llama3.2:3b")
        print(result)
    except Exception as e:
        print(f"Error during processing: {e}")
        print("Make sure the Ollama server is running and the 'llama3.2:3b' model is downloaded.")
        sys.exit(1)