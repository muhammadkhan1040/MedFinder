"""
Agent Orchestrator
Coordinates the execution of all agents in the symptom search pipeline.
"""
from typing import Dict, Any
from . import BaseAgent
from .query_processor import QueryProcessorAgent
from .rag_retriever import RAGRetrieverAgent
from .formula_extractor import FormulaExtractorAgent
from .llm_fallback import LLMFallbackAgent
from .medicine_matcher import MedicineMatcherAgent
from .results_formatter import ResultsFormatterAgent
from .config import ENABLE_LLM_FALLBACK

class AgentOrchestrator(BaseAgent):
    """Main coordinator for the agent system."""

    def __init__(self):
        super().__init__("Orchestrator")
        # Initialize all agents
        self.query_processor = QueryProcessorAgent()
        self.rag_retriever = RAGRetrieverAgent()
        self.formula_extractor = FormulaExtractorAgent()
        self.llm_fallback = LLMFallbackAgent()
        self.medicine_matcher = MedicineMatcherAgent()
        self.results_formatter = ResultsFormatterAgent()

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the full pipeline.

        Input: {"query": "headache and fever"}
        """
        results_log = {}

        # 1. Query Processing
        q_result = self.query_processor.execute(input_data)
        results_log["query_processor"] = q_result
        if q_result["status"] == "error":
            return {"error": "Query processing failed", "details": q_result}

        # 2. RAG Retrieval
        rag_input = q_result["output"]
        r_result = self.rag_retriever.execute(rag_input)
        results_log["rag_retriever"] = r_result
        
        # 3. Formula Extraction
        f_input = {
            "chunks": r_result["output"].get("chunks", []),
            "symptoms": rag_input.get("symptoms", [])
        }
        f_result = self.formula_extractor.execute(f_input)
        results_log["formula_extractor"] = f_result

        formulas = f_result["output"].get("formulas", [])
        
        # 4. LLM Fallback (if needed)
        if not formulas and ENABLE_LLM_FALLBACK:
            llm_input = {
                "symptoms": rag_input.get("symptoms", []),
                "rag_context": "\n".join([c["text"] for c in f_input["chunks"]])
            }
            l_result = self.llm_fallback.execute(llm_input)
            results_log["llm_fallback"] = l_result
            formulas = l_result["output"].get("formulas", [])

        # 5. Medicine Matching
        m_input = {"formulas": formulas}
        m_result = self.medicine_matcher.execute(m_input)
        results_log["medicine_matcher"] = m_result

        # 6. Results Formatting
        fmt_input = {
            "matches": m_result["output"].get("matches", []),
            "query_data": rag_input,
            "rag_data": r_result["output"]
        }
        fmt_result = self.results_formatter.execute(fmt_input)
        results_log["results_formatter"] = fmt_result

        # Final Response
        return {
            "result": fmt_result["output"],
            "execution_log": results_log,
            "status": "success"
        }
