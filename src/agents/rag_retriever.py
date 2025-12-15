"""
RAG Retriever Agent
Searches medical pharmacology books using FAISS index.
"""
import sys
import os
from typing import Dict, Any, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from traditional_rag.retriever import TraditionalRetriever
from . import BaseAgent
from .config import RAG_TOP_K, RAG_SCORE_THRESHOLD

class RAGRetrieverAgent(BaseAgent):
    """Retrieves relevant medical information from indexed books."""

    def __init__(self):
        super().__init__("RAGRetriever")
        try:
            self.retriever = TraditionalRetriever()
        except Exception as e:
            print(f"Warning: Could not load RAG retriever: {e}")
            self.retriever = None

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve relevant medical book excerpts.

        Input: {"cleaned_query": "headache fever"}
        Output: {
            "chunks": [
                {"text": "...", "score": 0.85, "metadata": {...}},
                ...
            ],
            "is_sufficient": True,
            "best_score": 0.85
        }
        """
        if not self.retriever:
            return {
                "chunks": [],
                "is_sufficient": False,
                "best_score": 0.0,
                "error": "RAG retriever not available"
            }

        query = input_data.get("cleaned_query", "")
        top_k = input_data.get("top_k", RAG_TOP_K)

        # Retrieve chunks
        results = self.retriever.retrieve(query, top_k=top_k)

        # Filter by score threshold
        filtered_results = [
            r for r in results
            if r['score'] >= RAG_SCORE_THRESHOLD
        ]

        # Determine if results are sufficient
        is_sufficient = len(filtered_results) > 0 and filtered_results[0]['score'] >= 0.7
        best_score = filtered_results[0]['score'] if filtered_results else 0.0

        return {
            "chunks": filtered_results,
            "is_sufficient": is_sufficient,
            "best_score": best_score,
            "total_retrieved": len(results)
        }
