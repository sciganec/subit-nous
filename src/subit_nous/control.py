"""SUBIT control generation – apply semantic coordinates to LLM prompts."""

from typing import Optional
from .subit_algebra import Subit
from .core import text_to_subit

# Mode-specific system prompts for control
MODE_PROMPTS = {
    "STATE": "You are in STATE mode. Respond logically, factually, and structurally. Use data and clear reasoning.",
    "VALUE": "You are in VALUE mode. Respond ethically, with emphasis on trust, community, and shared values.",
    "FORM": "You are in FORM mode. Respond aesthetically, emotionally, with beauty and artistic expression.",
    "FORCE": "You are in FORCE mode. Respond decisively, with willpower, ambition, and strategic thinking.",
}

WHO_PROMPTS = {
    "ME": "Write from first-person perspective. Use 'I', 'me', 'my'.",
    "WE": "Write from collective perspective. Use 'we', 'us', 'our'.",
    "YOU": "Write addressing the reader. Use 'you', 'your'.",
    "THEY": "Write from third-person perspective. Use 'they', 'them', 'their'.",
}

# Mapping from axis values to names
MODE_NAMES = {2: "STATE", 3: "VALUE", 1: "FORM", 0: "FORCE"}
WHO_NAMES = {2: "ME", 3: "WE", 1: "YOU", 0: "THEY"}


def apply_subit(
    prompt: str,
    target: Subit,
    model: str = "llama3.2:3b",
    instructions: Optional[str] = None,
) -> str:
    """
    Apply SUBIT semantic coordinates to control LLM generation.

    Args:
        prompt: Input text to transform
        target: Target Subit state (contains WHO and MODE)
        model: Ollama model name
        instructions: Optional custom system prompt

    Returns:
        Generated text following the target semantic coordinates
    """
    mode_value = target.project("MODE")
    who_value = target.project("WHO")

    mode_name = MODE_NAMES.get(mode_value, "STATE")
    who_name = WHO_NAMES.get(who_value, "ME")

    # Build system prompt
    if instructions:
        system = instructions
    else:
        system = (
            f"{MODE_PROMPTS[mode_name]}\n"
            f"{WHO_PROMPTS[who_name]}\n\n"
            f"Rewrite the following text according to these guidelines."
        )

    # Reuse existing agent system
    from .agent import run_agent
    return run_agent(prompt, mode_name, model, instructions=system)


def apply_subit_from_text(
    prompt: str,
    target_text: str,
    model: str = "llama3.2:3b",
    chunk_size: int = 1000,
) -> str:
    """
    Apply SUBIT from a target example text.

    The target text is first converted to a Subit state,
    then used to control generation.

    Args:
        prompt: Input text to transform
        target_text: Example text with desired semantic style
        model: Ollama model name
        chunk_size: Text chunk size for encoding

    Returns:
        Generated text following the target semantic style
    """
    target = Subit.from_text(target_text, chunk_size)
    return apply_subit(prompt, target, model)