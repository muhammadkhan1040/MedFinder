"""
Formula Extractor Agent
Extracts chemical formulas from medical text using regex and LLM.
"""
import re
from typing import Dict, Any, List
from . import BaseAgent
from .config import FORMULA_REGEX_PATTERNS, CONFIDENCE_THRESHOLD

class FormulaExtractorAgent(BaseAgent):
    """Extracts chemical formulas from text."""

    def __init__(self):
        super().__init__("FormulaExtractor")
        

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract formulas from RAG chunks.

        Input: {
            "chunks": [...],
            "symptoms": ["headache", "fever"]
        }
        Output: {
            "formulas": [
                {"formula": "Paracetamol (500mg)", "confidence": 0.9, "source": "regex"},
                ...
            ],
            "method": "regex"  # or "llm"
        }
        """
        chunks = input_data.get("chunks", [])
        symptoms = input_data.get("symptoms", [])

        # Combine all chunk texts
        combined_text = "\n".join([chunk['text'] for chunk in chunks])

        # 1. Try regex extraction first (fast)
        formulas = self._extract_with_regex(combined_text)

        if formulas and formulas[0]['confidence'] >= CONFIDENCE_THRESHOLD:
            return {
                "formulas": formulas,
                "method": "regex"
            }

        # 2. Fall back to LLM extraction (slower but more accurate)
        formulas = self._extract_with_llm(combined_text, symptoms)

        return {
            "formulas": formulas,
            "method": "llm"
        }

    def _extract_with_regex(self, text: str) -> List[Dict[str, Any]]:
        """Extract formulas using regex patterns."""
        formulas = []
        seen = set()  # Avoid duplicates

        for pattern in FORMULA_REGEX_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # Format: (ingredient, dosage)
                    formula = f"{match[0].title()} ({match[1]})"
                else:
                    formula = match

                if formula not in seen:
                    formulas.append({
                        "formula": formula,
                        "confidence": 0.8,  # Regex is fairly confident
                        "source": "regex"
                    })
                    seen.add(formula)

        return formulas

    def _extract_with_llm(self, text: str, symptoms: List[str]) -> List[Dict[str, Any]]:
        """
        Extract formulas using LLM.

        This is a fallback when regex doesn't find clear patterns.
        """
        # For now, return empty list
        # You'll implement this when integrating with your LLM

        # TODO: Implement LLM extraction
        # Example prompt:
        """
        You are a medical AI. Given this medical text and symptoms,
        extract the active ingredient and dosage for appropriate treatment.

        TEXT: {text}
        SYMPTOMS: {symptoms}

        Return JSON array of formulas:
        [{"formula": "Paracetamol (500mg)", "confidence": 0.9}]
        """

        return []
