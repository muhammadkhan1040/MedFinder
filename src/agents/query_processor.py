"""
Query Processor Agent
Cleans and validates user symptom queries.
"""
import re
from typing import Dict, Any, List
from . import BaseAgent

class QueryProcessorAgent(BaseAgent):
    """Processes and validates user symptom queries."""

    def __init__(self):
        super().__init__("QueryProcessor")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user query.

        Input: {"query": "I have a headache and fever"}
        Output: {
            "cleaned_query": "headache fever",
            "symptoms": ["headache", "fever"],
            "is_valid": True,
            "confidence": 0.95
        }
        """
        query = input_data.get("query", "")

        # 1. Clean query
        cleaned = self._clean_query(query)

        # 2. Extract symptoms
        symptoms = self._extract_symptoms(cleaned)

        # 3. Validate medical relevance
        is_valid, confidence = self._validate_medical(symptoms)

        return {
            "cleaned_query": cleaned,
            "symptoms": symptoms,
            "is_valid": is_valid,
            "confidence": confidence
        }

    def _clean_query(self, query: str) -> str:
        """Remove special characters, standardize text."""
        # Lowercase
        query = query.lower()
        # Remove punctuation except spaces
        query = re.sub(r'[^\w\s]', '', query)
        # Remove common filler words
        filler_words = ["i", "have", "a", "an", "the", "my", "me", "am", "is"]
        words = query.split()
        words = [w for w in words if w not in filler_words]
        return " ".join(words)

    def _extract_symptoms(self, query: str) -> List[str]:
        """Extract symptom keywords."""
        # Simple extraction: split by common separators
        symptoms = []
        separators = ["and", "with", ","]

        parts = [query]
        for sep in separators:
            new_parts = []
            for part in parts:
                new_parts.extend(part.split(sep))
            parts = new_parts

        symptoms = [p.strip() for p in parts if p.strip()]
        return symptoms

    def _validate_medical(self, symptoms: List[str]) -> tuple:
        """
        Validate if query is medical-related.

        Returns: (is_valid, confidence_score)
        """
        # Simple keyword-based validation
        # In production, you could use a medical NER model
        medical_keywords = [
            "pain", "ache", "fever", "cough", "cold", "nausea", "vomit",
            "diarrhea", "headache", "stomach", "chest", "throat", "dizzy",
            "infection", "allergy", "rash", "itch", "sore", "swelling",
            "pressure", "diabetes", "high", "low", "blood"
        ]

        if not symptoms:
            return False, 0.0

        # Check if any symptom contains medical keywords
        matches = 0
        for symptom in symptoms:
            for keyword in medical_keywords:
                if keyword in symptom:
                    matches += 1
                    break

        confidence = min(matches / len(symptoms), 1.0)
        is_valid = confidence > 0.3

        return is_valid, confidence
