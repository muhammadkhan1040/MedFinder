"""
Base Agent class for the agentic system.
All agents inherit from this class.
"""
import time
from typing import Dict, Any
from datetime import datetime

class BaseAgent:
    """Base class for all agents."""

    def __init__(self, name: str):
        self.name = name
        self.execution_log = []

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic. Override this in subclasses.

        Args:
            input_data: Input data for the agent

        Returns:
            Dict with:
            - status: "success" or "error"
            - output: Agent output data
            - execution_time: Time taken in seconds
            - timestamp: Execution timestamp
        """
        start_time = time.time()

        try:
            # Call the process method (implemented by subclasses)
            output = self.process(input_data)
            status = "success"
        except Exception as e:
            output = {"error": str(e)}
            status = "error"

        execution_time = time.time() - start_time

        result = {
            "agent": self.name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "input": input_data,
            "output": output,
            "execution_time": f"{execution_time:.2f}s"
        }

        self.execution_log.append(result)
        return result

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data. Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement process()")


# Import and export agents
try:
    from .symptom_search_agent import SymptomSearchAgent
    __all__ = ['BaseAgent', 'SymptomSearchAgent']
except ImportError as e:
    print(f"Warning: Could not import SymptomSearchAgent: {e}")
    __all__ = ['BaseAgent']
