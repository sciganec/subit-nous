"""Evaluator for SUBIT Query Language."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import networkx as nx

from .ast import Query, QueryType, Condition, Eq, And, Or, Not, Distance
from ..core import text_to_subit, subit_to_name


class Evaluator:
    """Evaluate SUBIT queries against different data sources."""
    
    def __init__(self, ref_subit: Optional[int] = None):
        self.ref_subit = ref_subit
    
    def evaluate(self, query: Query) -> List[Dict[str, Any]]:
        """Execute query and return results."""
        if query.query_type == QueryType.TEXT:
            return self._evaluate_text(query)
        elif query.query_type == QueryType.GRAPH:
            return self._evaluate_graph(query)
        elif query.query_type == QueryType.FILES:
            return self._evaluate_files(query)
        else:
            raise ValueError(f"Unknown query type: {query.query_type}")
    
    def _evaluate_condition(self, condition: Condition, subit: int) -> bool:
        """Evaluate condition against a single SUBIT value."""
        if isinstance(condition, Eq):
            return condition.evaluate(subit)
        elif isinstance(condition, And):
            return self._evaluate_condition(condition.left, subit) and \
                   self._evaluate_condition(condition.right, subit)
        elif isinstance(condition, Or):
            return self._evaluate_condition(condition.left, subit) or \
                   self._evaluate_condition(condition.right, subit)
        elif isinstance(condition, Not):
            return not self._evaluate_condition(condition.condition, subit)
        elif isinstance(condition, Distance):
            if self.ref_subit is None:
                raise ValueError("Distance requires reference SUBIT")
            return condition.evaluate_with_ref(subit, self.ref_subit)
        return True
    
    def _evaluate_text(self, query: Query) -> List[Dict[str, Any]]:
        """Evaluate query against a text file."""
        source_path = Path(query.source)
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {query.source}")
        
        text = source_path.read_text(encoding='utf-8', errors='ignore')
        sentences = self._split_sentences(text)
        
        results = []
        for sent in sentences:
            subit = text_to_subit(sent)
            if query.condition is None or self._evaluate_condition(query.condition, subit):
                results.append({
                    "text": sent,
                    "subit": subit,
                    "bits": f"{subit:08b}",
                    "archetype": subit_to_name(subit)
                })
        
        return results
    
    def _evaluate_graph(self, query: Query) -> List[Dict[str, Any]]:
        """Evaluate query against a graph.json file."""
        source_path = Path(query.source)
        if not source_path.exists():
            raise FileNotFoundError(f"Graph file not found: {query.source}")
        
        with open(source_path, 'r') as f:
            data = json.load(f)
        G = nx.node_link_graph(data)
        
        results = []
        for node in G.nodes:
            if query.condition is None or self._evaluate_condition(query.condition, node):
                results.append({
                    "node_id": node,
                    "bits": f"{node:08b}",
                    "archetype": subit_to_name(node),
                    "degree": G.degree(node),
                    "count": G.nodes[node].get('count', 0)
                })
        
        return results
    
    def _evaluate_files(self, query: Query) -> List[Dict[str, Any]]:
        """Evaluate query against a folder of files."""
        source_path = Path(query.source)
        if not source_path.exists() or not source_path.is_dir():
            raise FileNotFoundError(f"Folder not found: {query.source}")
        
        results = []
        for file_path in source_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in {'.txt', '.md', '.py'}:
                try:
                    text = file_path.read_text(encoding='utf-8', errors='ignore')
                    subit = text_to_subit(text[:1000])
                    if query.condition is None or self._evaluate_condition(query.condition, subit):
                        results.append({
                            "file": str(file_path),
                            "subit": subit,
                            "bits": f"{subit:08b}",
                            "archetype": subit_to_name(subit)
                        })
                except Exception:
                    continue
        
        return results
    
    def _split_sentences(self, text: str) -> List[str]:
        """Simple sentence splitting."""
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]