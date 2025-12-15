"""
LLM Fallback Agent
Uses LLM to generate medicine recommendations based on symptoms.
Can provide answers from general medical knowledge when RAG data is insufficient.
"""
import json
import sys
import os
from typing import Dict, Any, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from . import BaseAgent
from .config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from llm_client import get_llm_client

class LLMFallbackAgent(BaseAgent):
    """Uses LLM to suggest formulas based on symptoms and general medical knowledge."""

    def __init__(self):
        super().__init__("LLMFallback")
        self.llm_client = get_llm_client()

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate formula recommendations using LLM.

        Input: {
            "symptoms": ["headache", "fever"],
            "rag_context": "..."  # Optional context from RAG
        }
        Output: {
            "formulas": [
                {"formula": "Paracetamol (500mg)", "confidence": 0.8, "source": "llm"},
                ...
            ]
        }
        """
        symptoms = input_data.get("symptoms", [])
        rag_context = input_data.get("rag_context", "")

        # Build prompt
        prompt = self._build_prompt(symptoms, rag_context)

        # Call LLM
        formulas = self._call_llm(prompt)

        return {
            "formulas": formulas,
            "prompt_used": prompt
        }

    def _build_prompt(self, symptoms: List[str], context: str) -> str:
        """Build LLM prompt for formula extraction."""
        symptoms_str = ", ".join(symptoms)

        prompt = f"""You are a helpful medical AI assistant with comprehensive knowledge of pharmacology and medicine.

A patient reports the following symptoms: {symptoms_str}

{f"Additional context that may help: {context}" if context else ""}

Please recommend appropriate over-the-counter medicines for these symptoms. You may use your general medical knowledge to provide helpful suggestions.

Guidelines:
1. Suggest 1-3 active ingredients commonly used for these symptoms
2. Include standard dosages when possible
3. Focus on safe, commonly available OTC medicines
4. Provide your best recommendations based on the symptoms

Return your response as a JSON array with this format:
[
  {{"formula": "Medicine Name (dosage)", "confidence": 0.9}},
  {{"formula": "Another Medicine (dosage)", "confidence": 0.8}}
]

JSON OUTPUT:"""

        return prompt

    def _call_llm(self, prompt: str) -> List[Dict[str, Any]]:
        """
        Call LLM and parse response.
        """
        try:
            response = self.llm_client.complete(
                prompt=prompt,
                model=LLM_MODEL,
                temperature=LLM_TEMPERATURE,
                max_tokens=LLM_MAX_TOKENS
            )
            
            if response:
                # Try to parse JSON from response
                try:
                    # Clean up response - find JSON array
                    response = response.strip()
                    start_idx = response.find('[')
                    end_idx = response.rfind(']') + 1
                    if start_idx != -1 and end_idx > start_idx:
                        json_str = response[start_idx:end_idx]
                        formulas = json.loads(json_str)
                        # Add source field
                        for f in formulas:
                            f['source'] = 'llm'
                        return formulas
                except json.JSONDecodeError:
                    pass
            
            return []
        except Exception as e:
            print(f"LLM Fallback Error: {e}")
            return []
