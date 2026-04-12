"""Mask operator for local semantic editing."""

from typing import Optional, List
from dataclasses import dataclass

from .base import SubitOperator
from ..dsl import parse, Evaluator
from ..core import text_to_subit, subit_to_name
from ..controlled_rewrite import rewrite_axis, semantic_delta


@dataclass
class MaskOperator(SubitOperator):
    """
    Local operator that applies transformation only to sentences matching a condition.
    
    Examples:
        # Make all emotional sentences more logical
        mask = MaskOperator("MODE=FORM", "MODE=STATE")
        result = mask.apply_to_text(text)
        
        # Change perspective of first-person sentences
        mask = MaskOperator("WHO=ME", "WHO=WE")
        result = mask.apply_to_text(text)
    """
    
    condition: str
    transformation: str
    max_changes: int = 3
    
    def apply(self, subit: int) -> int:
        """Apply transformation at algebraic level (direct)."""
        # Parse transformation
        if self.transformation.startswith("MODE="):
            mode_name = self.transformation[5:]
            mode_map = {"STATE": 0b10, "VALUE": 0b11, "FORM": 0b01, "FORCE": 0b00,
                       "LOGOS": 0b10, "ETHOS": 0b11, "PATHOS": 0b01, "THYMOS": 0b00}
            mode_bits = mode_map.get(mode_name.upper(), 0b10)
            # Replace MODE bits (bits 0-1)
            return (subit & 0b11111100) | mode_bits
        
        elif self.transformation.startswith("WHO="):
            who_name = self.transformation[4:]
            who_map = {"ME": 0b10, "WE": 0b11, "YOU": 0b01, "THEY": 0b00}
            who_bits = who_map.get(who_name.upper(), 0b10)
            # Replace WHO bits (bits 6-7)
            return (subit & 0b00111111) | (who_bits << 6)
        
        else:
            raise ValueError(f"Unknown transformation: {self.transformation}")
    
    def apply_to_text(self, text: str) -> str:
        """Apply mask to text (local transformation)."""
        # Parse condition
        query = parse(f"text WHERE {self.condition}")
        
        # Split into sentences
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        results = []
        
        for sent in sentences:
            if not sent.strip():
                continue
            
            # Check if sentence matches condition
            subit = text_to_subit(sent)
            evaluator = Evaluator()
            if evaluator._evaluate_condition(query.condition, subit):
                # Apply transformation to this sentence
                target_subit = self.apply(subit)
                
                # Use controlled rewrite
                delta = semantic_delta(subit, target_subit)
                new_sent = sent
                for axis in delta:
                    target_val = (target_subit >> {"WHO":6, "WHERE":4, "WHEN":2, "MODE":0}[axis]) & 0b11
                    new_sent = rewrite_axis(new_sent, axis, target_val)
                results.append(new_sent)
            else:
                results.append(sent)
        
        return " ".join(results)
    
    def __repr__(self) -> str:
        return f"Mask(condition='{self.condition}', transformation='{self.transformation}')"
    

# Додайте маппінг для англійських назв
ENGLISH_TO_GREEK = {
    "STATE": "LOGOS",
    "VALUE": "ETHOS", 
    "FORM": "PATHOS",
    "FORCE": "THYMOS",
}