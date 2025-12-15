"""
Results Formatter Agent
Formats matched medicines for display and calculates savings.
"""
from typing import Dict, Any, List
from . import BaseAgent

class ResultsFormatterAgent(BaseAgent):
    """Formats final response for the frontend."""

    def __init__(self):
        super().__init__("ResultsFormatter")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format output.

        Input: {
            "matches": [...], # From MedicineMatcher
            "query_data": {...}, # From QueryProcessor
            "rag_data": {...} # From RAGRetriever
        }
        """
        matches = input_data.get("matches", [])
        formatted_medicines = []
        total_savings_potential = 0.0

        for match_group in matches:
            formula = match_group.get("formula")
            medicines = match_group.get("medicines", [])
            
            if not medicines:
                continue

            # Calculate price stats
            prices = []
            for m in medicines:
                try:
                    price_str = str(m.get("price", "0")).replace("Rs.", "").strip()
                    price = float(price_str) if price_str else 0.0
                    prices.append(price)
                except ValueError:
                    continue
            
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                # Calculate savings percentage if bought cheapest vs most expensive
                if max_price > 0:
                    savings_pct = ((max_price - min_price) / max_price) * 100
                else:
                    savings_pct = 0
            else:
                min_price = 0
                max_price = 0
                savings_pct = 0

            formatted_medicines.append({
                "formula": formula,
                "medicines": medicines, # Backend returns full list, frontend can slice
                "medicine_count": len(medicines),
                "price_range": {
                    "min": min_price,
                    "max": max_price
                },
                "savings_percentage": round(savings_pct, 1)
            })

            # Rough aggregation of savings (just taking the max found)
            if savings_pct > total_savings_potential:
                total_savings_potential = savings_pct

        return {
            "results": formatted_medicines,
            "summary": {
                "total_formulas": len(formatted_medicines),
                "max_savings_potential": f"{round(total_savings_potential, 1)}%",
                "original_query": input_data.get("query_data", {}).get("cleaned_query", "")
            }
        }
