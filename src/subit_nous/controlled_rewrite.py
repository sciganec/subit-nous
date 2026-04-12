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
    """
    import ollama
    
    # Value names for prompts
    value_names = {
        "WHO": {2: "ME (first person, I)", 3: "WE (collective, we)", 
                1: "YOU (second person, you)", 0: "THEY (third person, they)"},
        "MODE": {2: "LOGOS (logical, factual)", 3: "ETHOS (ethical, communal)",
                 1: "PATHOS (emotional, aesthetic)", 0: "THYMOS (willful, strategic)"},
    }
    
    target_name = value_names.get(axis, {}).get(target_value, str(target_value))
    
    prompts = {
        "WHO": f"Change the perspective to {target_name}. Change pronouns (I/we/you/they) accordingly. Keep the core meaning. Output only the rewritten text.",
        "MODE": f"Change the tone to {target_name}. Keep the facts and core meaning. Output only the rewritten text.",
    }
    
    prompt = prompts.get(axis, f"Change {axis} to {target_name}. Keep the meaning.")
    
    print(f"[DEBUG] rewrite_axis: axis={axis}, target={target_name}")
    
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            options={"temperature": 0.3}
        )
        result = response['message']['content']
        print(f"[DEBUG] rewrite_axis result: {result}")
        return result
    except Exception as e:
        print(f"[DEBUG] rewrite_axis error: {e}")
        return text  # fallback


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