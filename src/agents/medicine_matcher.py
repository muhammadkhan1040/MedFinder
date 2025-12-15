"""
Medicine Matcher Agent
Matches extracted formulas to medicines in the database.
"""
import sys
import os
from typing import Dict, Any, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.search_engine import search_by_composition
from src.agents import BaseAgent

class MedicineMatcherAgent(BaseAgent):
    """Matches extracted formulas to medicines."""

    def __init__(self):
        super().__init__("MedicineMatcher")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Match formulas to medicines.

        Input: {
            "formulas": [
                {"formula": "Paracetamol (500mg)", "confidence": 0.9}
            ]
        }
        Output: {
            "matches": [
                {
                    "formula": "Paracetamol (500mg)",
                    "medicines": [...], # List of medicine dicts
                    "count": 15
                }
            ],
            "total_matches": 15
        }
        """
        formulas = input_data.get("formulas", [])
        matches = []
        total_count = 0

        for item in formulas:
            formula_str = item.get("formula", "")
            if not formula_str:
                continue

            # search_by_composition handles normalization and matching
            # We try search without exact match first to capture variations
            # unless the logic requires strictness. Let's start with flexible.
            medicines = search_by_composition(formula_str, exact_match=False, max_results=50)

            if medicines:
                matches.append({
                    "formula": formula_str,
                    "medicines": medicines,
                    "count": len(medicines),
                    "confidence": item.get("confidence", 0.0)
                })
                total_count += len(medicines)

        return {
            "matches": matches,
            "total_matches": total_count
        }
