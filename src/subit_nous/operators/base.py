"""Base classes for SUBIT operators."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from ..subit_algebra import Subit
from ..core import text_to_subit, subit_to_name


class SubitOperator(ABC):
    """Base class for all SUBIT operators."""
    
    @abstractmethod
    def apply(self, subit: int) -> int:
        """Apply operator to SUBIT value (algebraic level)."""
        pass
    
    @abstractmethod
    def apply_to_text(self, text: str) -> str:
        """Apply operator to text (semantic level)."""
        pass
    
    def __call__(self, input: any) -> any:
        """Make operator callable."""
        if isinstance(input, str):
            return self.apply_to_text(input)
        elif isinstance(input, int):
            return self.apply(input)
        else:
            raise TypeError(f"Unsupported input type: {type(input)}")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


@dataclass
class OperatorPipeline:
    """Pipeline of operators applied sequentially."""
    
    operators: List[SubitOperator]
    
    def apply(self, subit: int) -> int:
        result = subit
        for op in self.operators:
            result = op.apply(result)
        return result
    
    def apply_to_text(self, text: str) -> str:
        result = text
        for op in self.operators:
            result = op.apply_to_text(result)
        return result
    
    def __call__(self, input: any) -> any:
        if isinstance(input, str):
            return self.apply_to_text(input)
        elif isinstance(input, int):
            return self.apply(input)
        else:
            raise TypeError(f"Unsupported input type: {type(input)}")
    
    def __repr__(self) -> str:
        return f"Pipeline({self.operators})"
    
    def __rshift__(self, other: SubitOperator) -> 'OperatorPipeline':
        """Allow operator composition with >>."""
        if isinstance(self, OperatorPipeline):
            return OperatorPipeline(self.operators + [other])
        return OperatorPipeline([self, other])