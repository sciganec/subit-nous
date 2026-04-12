"""Controlled rewrite engine for semantic editing."""

from typing import List, Tuple, Dict, Any, Optional
from .core import text_to_subit, subit_to_name


def semantic_delta(a: int, b: int) -> List[str]:
    """
    Return list of axes that differ between two SUBIT values.
    
    Examples:
        >>> semantic_delta(0b10101010, 0b11111111)
        ['WHO', 'WHERE', 'WHEN', 'MODE']
        
        >>> semantic_delta(0b10101010, 0b10101011)
        ['MODE']
    """
    axes = []
    for axis, shift in [("WHO", 6), ("WHERE", 4), ("WHEN", 2), ("MODE", 0)]:
        a_val = (a >> shift) & 0b11
        b_val = (b >> shift) & 0b11
        if a_val != b_val:
            axes.append(axis)
    return axes


def rewrite_axis(text: str, axis: str, target_value: int, model: str = "llama3.2:3b") -> str:
    """
    Rewrite text to change only one axis.
    
    Args:
        text: Input text
        axis: Axis to change (WHO, WHERE, WHEN, MODE)
        target_value: Target value (0-3)
        model: Ollama model name
    
    Returns:
        Rewritten text
    """
    # Value names for prompts
    value_names = {
        "WHO": {2: "ME (first person, I)", 3: "WE (collective, us)", 
                1: "YOU (second person, you)", 0: "THEY (third person, them)"},
        "WHERE": {2: "EAST (future, progress)", 3: "SOUTH (growth, action)",
                  1: "WEST (past, reflection)", 0: "NORTH (center, stability)"},
        "WHEN": {2: "SPRING (beginning, birth)", 3: "SUMMER (peak, growth)",
                 1: "AUTUMN (decline, reflection)", 0: "WINTER (end, stillness)"},
        "MODE": {2: "LOGOS/STATE (logical, factual)", 3: "ETHOS/VALUE (ethical, communal)",
                 1: "PATHOS/FORM (emotional, aesthetic)", 0: "THYMOS/FORCE (willful, strategic)"},
    }
    
    target_name = value_names.get(axis, {}).get(target_value, str(target_value))
    
    # Build prompt
    prompts = {
        "WHO": f"Change the perspective to {target_name}. Use appropriate pronouns. Keep the meaning and facts.",
        "WHERE": f"Change the spatial/directional aspect to {target_name}. Keep the core message.",
        "WHEN": f"Change the temporal aspect to {target_name}. Keep the core message.",
        "MODE": f"Change the tone/style to {target_name}. Keep the facts and core meaning.",
    }
    
    prompt = prompts.get(axis, f"Change {axis} to {target_name}. Keep the meaning.")
    
    # Use Ollama for rewrite
    import ollama
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": f"You are a precise text editor. {prompt} Output only the rewritten text, nothing else."},
            {"role": "user", "content": text}
        ],
        options={"temperature": 0.3}
    )
    
    return response['message']['content']


def controlled_rewrite(text: str, target_subit: int, max_changes: int = 3, model: str = "llama3.2:3b") -> str:
    """
    Rewrite text to target SUBIT with controlled changes.
    
    Args:
        text: Input text
        target_subit: Target SUBIT value
        max_changes: Maximum number of axis changes per step
        model: Ollama model name
    
    Returns:
        Rewritten text
    """
    current = text
    current_subit = text_to_subit(current)
    
    # Get axes that need to change
    axes = semantic_delta(current_subit, target_subit)
    
    if len(axes) == 0:
        return text
    
    # Limit changes per step
    if len(axes) > max_changes:
        # Change first max_changes axes
        axes = axes[:max_changes]
    
    for axis in axes:
        shift = {"WHO":6, "WHERE":4, "WHEN":2, "MODE":0}[axis]
        target_val = (target_subit >> shift) & 0b11
        current = rewrite_axis(current, axis, target_val, model)
    
    return current


def stepwise_rewrite(text: str, path: List[int], model: str = "llama3.2:3b") -> List[str]:
    """
    Rewrite text through a path of intermediate SUBIT values.
    Returns list of texts at each step.
    """
    results = [text]
    current = text
    
    for target_subit in path[1:]:
        current = controlled_rewrite(current, target_subit, model=model)
        results.append(current)
    
    return results