"""SUBIT Control Generation – зміна тексту через LLM відповідно до алгебри"""

import os
from typing import Optional
from openai import OpenAI

from .subit_algebra import Subit
from .core import text_to_subit_object

# Мапінг назв модусів до бітових значень (MODE axis)
MODE_VALUES = {
    "STATE": 0b10,   # LOGOS
    "VALUE": 0b11,   # ETHOS
    "FORM": 0b01,    # PATHOS
    "FORCE": 0b00,   # THYMOS
}

MODE_NAMES = {v: k for k, v in MODE_VALUES.items()}

def _get_openai_client() -> Optional[OpenAI]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


def apply_control(
    text: str,
    target_mode: int,
    model: str = "gpt-3.5-turbo",
    instructions: Optional[str] = None,
) -> str:
    """
    Змінює текст, щоб він відповідав заданому MODE (0..3).
    target_mode: 0=FORCE, 1=FORM, 2=STATE, 3=VALUE.
    """
    mode_name = MODE_NAMES[target_mode]
    system = (
        instructions
        or f"You are a style editor. Rewrite the following text to emphasize the mode '{mode_name}'. "
        f"Meaning of '{mode_name}':\n"
        f"- STATE: logical, factual, structured, analytical\n"
        f"- VALUE: ethical, trustworthy, communal, harmonious\n"
        f"- FORM: aesthetic, emotional, artistic, beautiful\n"
        f"- FORCE: willful, powerful, controlling, ambitious\n"
        f"Keep the core meaning but adjust tone, vocabulary, and examples accordingly."
    )
    client = _get_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


def classify_and_control(text: str, desired_mode_name: str) -> str:
    """
    Визначає поточний MODE тексту, потім змінює до desired_mode_name.
    desired_mode_name: 'STATE', 'VALUE', 'FORM', 'FORCE'.
    """
    desired_mode = MODE_VALUES[desired_mode_name.upper()]
    s = text_to_subit_object(text)
    current_mode = s.project("MODE")
    if current_mode == desired_mode:
        return text  # вже відповідає
    return apply_control(text, desired_mode)