"""Evolution operator for dynamic path traversal."""

from dataclasses import dataclass
from typing import List, Optional, Callable

from .base import SubitOperator
from ..core import text_to_subit
from ..controlled_rewrite import controlled_rewrite, semantic_delta


def hamming_path(a: int, b: int) -> List[int]:
    """Generate path by flipping one bit at a time."""
    path = [a]
    current = a
    diff = a ^ b
    
    for i in range(8):
        if diff & (1 << i):
            current ^= (1 << i)
            path.append(current)
    
    return path


@dataclass
class EvolutionOperator(SubitOperator):
    """
    Dynamic operator that animates path between archetypes.
    
    Examples:
        # Evolve from STATE to FORM
        evolve = EvolutionOperator(from_subit=170, to_subit=85, steps=5)
        results = evolve.apply_to_text_animated(text)
        
        # With custom step callback
        def on_step(step, subit, text):
            print(f"Step {step}: {subit:08b}")
        evolve = EvolutionOperator(..., on_step=on_step)
    """
    
    from_subit: int
    to_subit: int
    steps: int = 5
    on_step: Optional[Callable[[int, int, str], None]] = None
    
    def apply(self, subit: int) -> int:
        """Return the target subit (final state)."""
        return self.to_subit
    
    def apply_to_text(self, text: str) -> str:
        """Apply full evolution and return final text."""
        path = hamming_path(self.from_subit, self.to_subit)
        
        # If steps > len(path), interpolate
        if self.steps > len(path):
            # For now, just use path
            pass
        
        current_text = text
        for i, target_subit in enumerate(path[1:], 1):
            current_text = controlled_rewrite(current_text, target_subit)
            if self.on_step:
                self.on_step(i, target_subit, current_text)
        
        return current_text
    
    def evolve(self, text: str) -> List[dict]:
        """Return all intermediate states."""
        path = hamming_path(self.from_subit, self.to_subit)
        results = []
        
        current_text = text
        results.append({"step": 0, "subit": self.from_subit, "text": current_text})
        
        for i, target_subit in enumerate(path[1:], 1):
            current_text = controlled_rewrite(current_text, target_subit)
            results.append({"step": i, "subit": target_subit, "text": current_text})
        
        return results
    
    def __repr__(self) -> str:
        return f"Evolution({self.from_subit:08b} → {self.to_subit:08b}, steps={self.steps})"