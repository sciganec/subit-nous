"""SUBIT classifier using fine-tuned DistilBERT."""

from pathlib import Path
import json
from typing import Dict, Any, Optional

try:
    import torch
    from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


class SubitClassifier:
    def __init__(self, model_path: str = "./subit_model"):
        self.model_path = Path(model_path)
        self.model = None
        self.tokenizer = None
        
        if not TRANSFORMERS_AVAILABLE:
            print("Warning: transformers not installed")
            return
        
        if self.model_path.exists():
            self.tokenizer = DistilBertTokenizer.from_pretrained(str(self.model_path))
            self.model = DistilBertForSequenceClassification.from_pretrained(str(self.model_path))
            self.model.eval()
    
    def classify(self, text: str, return_probs: bool = False) -> Dict[str, Any]:
        """Classify text and return SUBIT bits."""
        from .core import subit_to_name
        
        if self.model is None:
            # Fallback to marker-based
            from .core import text_to_subit
            subit = text_to_subit(text)
            return {
                "subit": subit,
                "bits": f"{subit:08b}",
                "archetype": subit_to_name(subit),
                "mode": None,
                "who": None,
                "where": None,
                "when": None,
            }
        
        # Real classification (simplified)
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            outputs = self.model(**inputs)
            subit = torch.argmax(outputs.logits, dim=1).item()
        
        return {
            "subit": subit,
            "bits": f"{subit:08b}",
            "archetype": subit_to_name(subit),
            "mode": None,
            "who": None,
            "where": None,
            "when": None,
        }


def classify_text(text: str) -> int:
    """Convenience function."""
    classifier = SubitClassifier()
    return classifier.classify(text)["subit"]