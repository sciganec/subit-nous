"""Transfer operator for global style transfer."""

from dataclasses import dataclass
from typing import Optional

from .base import SubitOperator
from ..core import text_to_subit

@dataclass
class TransferOperator(SubitOperator):
    """
    Global operator that moves text to target semantic coordinates.
    
    Examples:
        # Transfer to a specific archetype
        transfer = TransferOperator(target_subit=170)
        result = transfer.apply_to_text(text)
        
        # Transfer style from another text
        transfer = TransferOperator.from_style(style_text, alpha=0.7)
        result = transfer.apply_to_text(content_text)
    """
    
    target_subit: int
    alpha: float = 0.7
    preserve_facts: bool = True
    
    @classmethod
    def from_style(cls, style_text: str, alpha: float = 0.7) -> 'TransferOperator':
        """Create operator from example style text."""
        target_subit = text_to_subit(style_text)
        return cls(target_subit=target_subit, alpha=alpha)
    
    def apply(self, subit: int) -> int:
        """Blend current SUBIT with target."""
        import random
        result = 0
        for axis, shift in [("WHO", 6), ("WHERE", 4), ("WHEN", 2), ("MODE", 0)]:
            a_val = (subit >> shift) & 0b11
            b_val = (self.target_subit >> shift) & 0b11
            if random.random() < self.alpha:
                result |= (b_val << shift)
            else:
                result |= (a_val << shift)
        return result
    
    def apply_to_text(self, text: str) -> str:
        """Transfer text to target style."""
        from ..controlled_rewrite import controlled_rewrite, semantic_delta
    
        current_subit = text_to_subit(text)
        target_subit = self.apply(current_subit)
    
        print(f"[DEBUG] Transfer: current={current_subit:08b}, target={target_subit:08b}")
        print(f"[DEBUG] Delta axes: {semantic_delta(current_subit, target_subit)}")
    
        # Check if we need to change anything
        delta = semantic_delta(current_subit, target_subit)
        if not delta:
            print("[DEBUG] No changes needed")
            return text
    
        # Use controlled rewrite
        result = controlled_rewrite(text, target_subit)
        print(f"[DEBUG] Transfer result: {result}")
        return result
    
    def __repr__(self) -> str:
        return f"Transfer(target={self.target_subit:08b}, alpha={self.alpha})"