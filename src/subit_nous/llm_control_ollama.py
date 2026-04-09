import ollama
from .core import MODE_VALUES, MODE_NAMES

def apply_control(text: str, target_mode: int, model: str = "llama3.2:3b") -> str:
    mode_name = MODE_NAMES[target_mode]
    system = (
        f"You are a text rewriting assistant. Your task is to rewrite the user's sentence below "
        f"so that it strongly exhibits the '{mode_name}' mode. "
        f"Do NOT explain what '{mode_name}' means. Do NOT add extra commentary. "
        f"Just output the rewritten version of the original sentence.\n\n"
        f"Meaning of '{mode_name}':\n"
        f"- STATE: logical, factual, structured, analytical\n"
        f"- VALUE: ethical, trustworthy, communal\n"
        f"- FORM: aesthetic, emotional, artistic\n"
        f"- FORCE: willful, powerful, controlling\n\n"
        f"Original sentence: {text}\n"
        f"Rewritten sentence (only the rewritten version, no extra text):"
    )
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": system}],
        options={"temperature": 0.7}
    )
    return response['message']['content'].strip()