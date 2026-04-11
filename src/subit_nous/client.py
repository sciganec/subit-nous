"""SUBIT-NOUS Python SDK – programmatic interface for all features."""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union
from pathlib import Path

from .core import text_to_subit, subit_to_name, get_mode
from .subit_algebra import Subit
from .search import search as search_func
from .agent import run_agent, classify_and_run


@dataclass
class AnalysisResult:
    """Result from text analysis."""
    subit: int
    bits: str
    archetype: str
    mode: Optional[str]
    who: str
    where: str
    when: str
    
    def __repr__(self) -> str:
        return f"AnalysisResult(archetype='{self.archetype}', mode='{self.mode}', subit={self.subit})"


@dataclass
class ClassificationResult(AnalysisResult):
    """Result from neural classification."""
    confidence: Optional[float] = None
    top_predictions: Optional[List[tuple]] = None


@dataclass
class SearchResult:
    """Result from hybrid search."""
    path: str
    score: float
    similarity: float
    mode: str
    who: str
    
    def __repr__(self) -> str:
        return f"SearchResult(path='{self.path}', score={self.score:.3f})"


class SubitClient:
    """Main SDK client for SUBIT-NOUS."""
    
    def __init__(self, use_classifier: bool = True, model_path: str = "./subit_model"):
        self.use_classifier = use_classifier
        self._classifier = None
        
        if use_classifier:
            try:
                from .classifier import SubitClassifier
                self._classifier = SubitClassifier(model_path)
                self.use_classifier = True
            except (FileNotFoundError, ImportError):
                self.use_classifier = False
    
    def analyze(self, text: str) -> AnalysisResult:
        """Analyze text using marker-based SUBIT classification."""
        subit = text_to_subit(text)
        who_names = ["THEY", "YOU", "ME", "WE"]
        where_names = ["NORTH", "WEST", "EAST", "SOUTH"]
        when_names = ["WINTER", "AUTUMN", "SPRING", "SUMMER"]
        
        return AnalysisResult(
            subit=subit,
            bits=f"{subit:08b}",
            archetype=subit_to_name(subit),
            mode=get_mode(subit),
            who=who_names[(subit >> 6) & 0b11],
            where=where_names[(subit >> 4) & 0b11],
            when=when_names[(subit >> 2) & 0b11],
        )
    
    def classify(self, text: str, return_probs: bool = False) -> ClassificationResult:
        """Classify text using neural classifier (if available)."""
        if self._classifier:
            result = self._classifier.classify(text, return_probs)
            return ClassificationResult(
                subit=result['subit'],
                bits=result['bits'],
                archetype=result['archetype'],
                mode=result['mode'],
                who=result['who'],
                where=result['where'],
                when=result['when'],
                confidence=result.get('top_classes', [[None, None]])[0][1] if return_probs else None,
                top_predictions=result.get('top_classes') if return_probs else None,
            )
        else:
            result = self.analyze(text)
            return ClassificationResult(
                subit=result.subit,
                bits=result.bits,
                archetype=result.archetype,
                mode=result.mode,
                who=result.who,
                where=result.where,
                when=result.when,
            )
    
    def search(self, query: str, mode: str = None, who: str = None, top_k: int = 10, alpha: float = 0.5) -> List[SearchResult]:
        """Hybrid search across indexed documents."""
        results = search_func(query, mode=mode, who=who, top_k=top_k, alpha=alpha)
        mode_names = {0: "FORCE", 1: "FORM", 2: "STATE", 3: "VALUE"}
        who_names = {0: "THEY", 1: "YOU", 2: "ME", 3: "WE"}
        
        return [
            SearchResult(
                path=r['path'],
                score=r['score'],
                similarity=r['similarity'],
                mode=mode_names.get(r['mode'], "?"),
                who=who_names.get(r['who'], "?"),
            )
            for r in results
        ]
    
    def generate(self, prompt: str, mode: str = "auto", who: str = "auto", model: str = "llama3.2:3b") -> str:
        """Generate or transform text using SUBIT-controlled agents."""
        if mode == "auto" and who == "auto":
            result = classify_and_run(prompt, model)
            return result['agent_response']
        elif mode != "auto" and who == "auto":
            return run_agent(prompt, mode, model)
        else:
            mode_map = {"STATE": 2, "VALUE": 3, "FORM": 1, "FORCE": 0}
            who_map = {"ME": 2, "WE": 3, "YOU": 1, "THEY": 0}
            target = Subit.from_coords(
                who=who_map.get(who, 2),
                where=2,
                when=2,
                mode=mode_map.get(mode, 2),
            )
            from .control import apply_subit
            return apply_subit(prompt, target, model)
    
    def to_subit(self, text: str) -> Subit:
        """Convert text to Subit object."""
        return Subit.from_text(text)
    
    def from_subit(self, subit: Union[Subit, int]) -> Dict[str, Any]:
        """Convert Subit object or int to dict representation."""
        if isinstance(subit, int):
            subit = Subit(subit)
        
        who_names = {2: "ME", 3: "WE", 1: "YOU", 0: "THEY"}
        where_names = {2: "EAST", 3: "SOUTH", 1: "WEST", 0: "NORTH"}
        when_names = {2: "SPRING", 3: "SUMMER", 1: "AUTUMN", 0: "WINTER"}
        mode_names = {2: "STATE", 3: "VALUE", 1: "FORM", 0: "FORCE"}
        
        return {
            "subit": subit.bits,
            "bits": f"{subit.bits:08b}",
            "archetype": subit.to_human(),
            "who": who_names.get(subit.project("WHO"), "?"),
            "where": where_names.get(subit.project("WHERE"), "?"),
            "when": when_names.get(subit.project("WHEN"), "?"),
            "mode": mode_names.get(subit.project("MODE"), "?"),
        }
    
    def xor(self, a: Union[str, Subit, int], b: Union[str, Subit, int]) -> Subit:
        """XOR two SUBIT states."""
        if isinstance(a, str):
            a = self.to_subit(a)
        elif isinstance(a, int):
            a = Subit(a)
        if isinstance(b, str):
            b = self.to_subit(b)
        elif isinstance(b, int):
            b = Subit(b)
        return a.xor(b)
    
    def distance(self, a: Union[str, Subit, int], b: Union[str, Subit, int]) -> int:
        """Hamming distance between two SUBIT states."""
        if isinstance(a, str):
            a = self.to_subit(a)
        elif isinstance(a, int):
            a = Subit(a)
        if isinstance(b, str):
            b = self.to_subit(b)
        elif isinstance(b, int):
            b = Subit(b)
        return a.distance(b)