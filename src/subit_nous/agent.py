"""SUBIT Agent System: four agents for different modes"""

import ollama
from typing import List, Dict, Optional
from .core import text_to_subit, get_mode, MODE_NAMES

# System prompts для кожного модусу
AGENT_PROMPTS = {
    "STATE": """You are a STATE agent – logical, factual, structured, analytical.
Your task: Analyze the input text objectively. Focus on facts, data, and logical structure.
Respond with clear, concise analysis. Avoid emotional language or value judgments.
Use bullet points or numbered lists when appropriate.""",

    "VALUE": """You are a VALUE agent – ethical, trustworthy, communal, harmonious.
Your task: Evaluate the input text from an ethical perspective. Consider community impact, moral implications, and shared values.
Respond with emphasis on fairness, responsibility, and collective well-being.""",

    "FORM": """You are a FORM agent – aesthetic, emotional, artistic, beautiful.
Your task: Transform the input text with attention to beauty, emotion, and artistic expression.
Use vivid language, metaphors, and sensory details. Focus on the emotional resonance and aesthetic quality.""",

    "FORCE": """You are a FORCE agent – willful, powerful, controlling, ambitious.
Your task: Analyze the input text for power dynamics, control structures, and strategic opportunities.
Respond with focus on influence, action, and achieving goals. Be direct and decisive.""",
}

# Мапінг назв модусів до бітів
MODE_TO_BITS = {"STATE": 2, "VALUE": 3, "FORM": 1, "FORCE": 0}
BITS_TO_MODE = {2: "STATE", 3: "VALUE", 1: "FORM", 0: "FORCE"}

def run_agent(
    text: str,
    mode: str,
    model: str = "llama3.2:3b",
    instructions: Optional[str] = None,
) -> str:
    """
    Запускає агента для заданого модусу.
    """
    mode = mode.upper()
    if mode not in AGENT_PROMPTS:
        raise ValueError(f"Unknown mode: {mode}. Use STATE, VALUE, FORM, FORCE")
    
    system = instructions or AGENT_PROMPTS[mode]
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text}
        ],
        options={"temperature": 0.7}
    )
    return response['message']['content']

def classify_and_run(
    text: str,
    model: str = "llama3.2:3b",
) -> Dict[str, str]:
    """
    Визначає поточний MODE тексту, потім запускає відповідного агента.
    """
    subit = text_to_subit(text)
    mode_bits = subit & 0b11
    mode = BITS_TO_MODE.get(mode_bits, "STATE")
    response = run_agent(text, mode, model)
    return {
        "original_mode": mode,
        "original_archetype": get_mode(subit) or str(subit),
        "agent_response": response,
    }

def run_pipeline(
    text: str,
    modes: List[str],
    model: str = "llama3.2:3b",
) -> List[Dict[str, str]]:
    """
    Послідовний пайплайн агентів.
    Кожен агент отримує результат попереднього.
    """
    results = []
    current_text = text
    for mode in modes:
        response = run_agent(current_text, mode, model)
        results.append({
            "mode": mode,
            "input": current_text[:100] + "..." if len(current_text) > 100 else current_text,
            "output": response,
        })
        current_text = response  # наступний агент отримує результат попереднього
    return results