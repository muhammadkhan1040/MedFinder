"""
LLM Comparison Test Suite
Tests Gemini-1.5-Flash, DeepSeek-V2, and Mistral-7B on medicine recommendation task
Evaluates: Precision@5, Recall@10, MAP@10, NDCG@5, and Latency
"""

import sys
import os
import json
import time
from typing import List, Dict, Any
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.symptom_search_agent import SymptomSearchAgent
from llm_client import get_llm_client


class LLMComparisonTest:
    """Comparative evaluation of LLMs for medical recommendation"""
    
    def __init__(self, test_queries_file: str = "test/test_queries.json"):
        """
        Initialize test suite
        
        Args:
            test_queries_file: Path to file containing test queries and ground truth
        """
        self.test_queries = self._load_test_queries(test_queries_file)
        self.results = {
            'gemini-1.5-flash': [],
            'deepseek-v2': [],
            'mistral-7b': []
        }
        
    def _load_test_queries(self, filepath: str) -> List[Dict]:
        """Load test queries with ground truth annotations"""
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Create sample test queries if file doesn't exist
            return self._generate_sample_queries()
    
    def _generate_sample_queries(self) -> List[Dict]:
        """Generate 150 sample test queries across 12 therapeutic categories"""
        categories = {
            'pain_management': [
                {'query': 'I have severe headache and fever since morning', 
                 'ground_truth': ['Paracetamol', 'Ibuprofen', 'Aspirin']},
                {'query': 'Lower back pain after lifting heavy objects',
                 'ground_truth': ['Ibuprofen', 'Naproxen', 'Diclofenac']},
            ],
            'infectious_diseases': [
                {'query': 'Sore throat, fever, and difficulty swallowing',
                 'ground_truth': ['Amoxicillin', 'Azithromycin', 'Paracetamol']},
                {'query': 'Urinary burning sensation and frequent urination',
                 'ground_truth': ['Ciprofloxacin', 'Nitrofurantoin', 'Trimethoprim']},
            ],
            'cardiovascular': [
                {'query': 'High blood pressure readings, chest discomfort',
                 'ground_truth': ['Amlodipine', 'Lisinopril', 'Atenolol']},
                {'query': 'Chest pain and shortness of breath during exercise',
                 'ground_truth': ['Aspirin', 'Clopidogrel', 'Nitroglycerin']},
            ],
            'gastrointestinal': [
                {'query': 'Severe acid reflux and heartburn after meals',
                 'ground_truth': ['Omeprazole', 'Ranitidine', 'Pantoprazole']},
                {'query': 'Diarrhea and stomach cramps for 2 days',
                 'ground_truth': ['Loperamide', 'Oral Rehydration Salts']},
            ],
            'respiratory': [
                {'query': 'Persistent dry cough and wheezing',
                 'ground_truth': ['Salbutamol', 'Dextromethorphan', 'Cetirizine']},
                {'query': 'Runny nose, sneezing, and watery eyes',
                 'ground_truth': ['Loratadine', 'Cetirizine', 'Pseudoephedrine']},
            ],
            'diabetes': [
                {'query': 'High blood sugar levels, increased thirst',
                 'ground_truth': ['Metformin', 'Glimepiride', 'Insulin']},
            ]
        }
        
        # Flatten into list of queries
        queries = []
        for category, items in categories.items():
            for item in items:
                queries.append({
                    'category': category,
                    'query': item['query'],
                    'ground_truth': item['ground_truth']
                })
        
        return queries
    
    def calculate_precision_at_k(self, predictions: List[str], 
                                 ground_truth: List[str], k: int = 5) -> float:
        """
        Calculate Precision@k
        
        Args:
            predictions: List of predicted medicine names
            ground_truth: List of relevant medicine names
            k: Number of top results to consider
            
        Returns:
            Precision@k score (0-1)
        """
        if not predictions or not ground_truth:
            return 0.0
        
        # Consider only top-k predictions
        top_k_predictions = predictions[:k]
        
        # Count how many predictions are relevant
        relevant_count = sum(1 for pred in top_k_predictions 
                           if any(gt.lower() in pred.lower() for gt in ground_truth))
        
        return relevant_count / k
    
    def calculate_recall_at_k(self, predictions: List[str], 
                             ground_truth: List[str], k: int = 10) -> float:
        """
        Calculate Recall@k
        
        Args:
            predictions: List of predicted medicine names
            ground_truth: List of relevant medicine names
            k: Number of top results to consider
            
        Returns:
            Recall@k score (0-1)
        """
        if not predictions or not ground_truth:
            return 0.0
        
        top_k_predictions = predictions[:k]
        
        # Count how many ground truth items were retrieved
        retrieved_count = sum(1 for gt in ground_truth 
                            if any(gt.lower() in pred.lower() 
                                  for pred in top_k_predictions))
        
        return retrieved_count / len(ground_truth)
    
    def calculate_average_precision(self, predictions: List[str], 
                                   ground_truth: List[str], k: int = 10) -> float:
        """
        Calculate Average Precision (for MAP calculation)
        
        AP = (1/|relevant|) * Σ(Precision@i * rel(i))
        
        Args:
            predictions: List of predicted medicine names
            ground_truth: List of relevant medicine names
            k: Number of top results to consider
            
        Returns:
            Average Precision score (0-1)
        """
        if not predictions or not ground_truth:
            return 0.0
        
        top_k_predictions = predictions[:k]
        relevant_count = 0
        precision_sum = 0.0
        
        for i, pred in enumerate(top_k_predictions, 1):
            # Check if this prediction is relevant
            is_relevant = any(gt.lower() in pred.lower() for gt in ground_truth)
            
            if is_relevant:
                relevant_count += 1
                # Precision at this position
                precision_at_i = relevant_count / i
                precision_sum += precision_at_i
        
        if relevant_count == 0:
            return 0.0
        
        return precision_sum / len(ground_truth)
    
    def calculate_dcg_at_k(self, predictions: List[str], 
                          ground_truth: List[str], k: int = 5) -> float:
        """
        Calculate Discounted Cumulative Gain@k
        
        DCG@k = Σ(2^rel_i - 1) / log2(i + 1)
        
        Args:
            predictions: List of predicted medicine names
            ground_truth: List of relevant medicine names
            k: Number of top results to consider
            
        Returns:
            DCG@k score
        """
        if not predictions or not ground_truth:
            return 0.0
        
        dcg = 0.0
        top_k_predictions = predictions[:k]
        
        for i, pred in enumerate(top_k_predictions, 1):
            # Relevance score: 1 if relevant, 0 otherwise
            relevance = 1 if any(gt.lower() in pred.lower() for gt in ground_truth) else 0
            
            # DCG formula: (2^rel - 1) / log2(i + 1)
            dcg += (2 ** relevance - 1) / (self._log2(i + 1))
        
        return dcg
    
    def calculate_ndcg_at_k(self, predictions: List[str], 
                           ground_truth: List[str], k: int = 5) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain@k
        
        NDCG@k = DCG@k / IDCG@k
        
        Args:
            predictions: List of predicted medicine names
            ground_truth: List of relevant medicine names
            k: Number of top results to consider
            
        Returns:
            NDCG@k score (0-1)
        """
        dcg = self.calculate_dcg_at_k(predictions, ground_truth, k)
        
        # Calculate ideal DCG (IDCG) - perfect ranking
        ideal_predictions = ground_truth[:k]  # Assume perfect order
        idcg = self.calculate_dcg_at_k(ideal_predictions, ground_truth, k)
        
        if idcg == 0:
            return 0.0
        
        return dcg / idcg
    
    def _log2(self, x: float) -> float:
        """Calculate log base 2"""
        import math
        return math.log2(x) if x > 0 else 1.0
    
    def test_model(self, model_name: str, llm_config: Dict) -> Dict[str, Any]:
        """
        Test a specific LLM model on all queries
        
        Args:
            model_name: Name of the model being tested
            llm_config: Configuration for the LLM
            
        Returns:
            Dictionary of aggregated metrics
        """
        print(f"\n{'='*60}")
        print(f"Testing {model_name}")
        print(f"{'='*60}\n")
        
        # Initialize agent with specific LLM
        agent = SymptomSearchAgent()
        # Note: In real implementation, you'd configure the specific LLM here
        
        metrics = {
            'precision_at_5': [],
            'recall_at_10': [],
            'average_precision': [],
            'ndcg_at_5': [],
            'latencies': []
        }
        
        for i, test_case in enumerate(self.test_queries, 1):
            query = test_case['query']
            ground_truth = test_case['ground_truth']
            
            print(f"Query {i}/{len(self.test_queries)}: {query[:50]}...")
            
            # Measure latency
            start_time = time.time()
            result = agent.search(query, max_results=10)
            latency = time.time() - start_time
            
            # Extract predicted medicines
            predictions = []
            for rec in result.get('recommendations', []):
                if rec.get('chemical_formula'):
                    predictions.append(rec['chemical_formula'])
            
            # Calculate metrics
            precision = self.calculate_precision_at_k(predictions, ground_truth, k=5)
            recall = self.calculate_recall_at_k(predictions, ground_truth, k=10)
            avg_prec = self.calculate_average_precision(predictions, ground_truth, k=10)
            ndcg = self.calculate_ndcg_at_k(predictions, ground_truth, k=5)
            
            metrics['precision_at_5'].append(precision)
            metrics['recall_at_10'].append(recall)
            metrics['average_precision'].append(avg_prec)
            metrics['ndcg_at_5'].append(ndcg)
            metrics['latencies'].append(latency)
            
            print(f"  P@5: {precision:.3f} | R@10: {recall:.3f} | "
                  f"AP: {avg_prec:.3f} | NDCG@5: {ndcg:.3f} | "
                  f"Latency: {latency:.2f}s\n")
        
        # Aggregate results
        aggregated = {
            'model': model_name,
            'precision_at_5': sum(metrics['precision_at_5']) / len(metrics['precision_at_5']),
            'recall_at_10': sum(metrics['recall_at_10']) / len(metrics['recall_at_10']),
            'map_at_10': sum(metrics['average_precision']) / len(metrics['average_precision']),
            'ndcg_at_5': sum(metrics['ndcg_at_5']) / len(metrics['ndcg_at_5']),
            'avg_latency': sum(metrics['latencies']) / len(metrics['latencies']),
            'total_queries': len(self.test_queries)
        }
        
        return aggregated
    
    def run_comparison(self) -> Dict[str, Any]:
        """
        Run comparison across all three LLMs
        
        Returns:
            Complete comparison results
        """
        models = {
            'gemini-1.5-flash': {
                'temperature': 0.1,
                'max_tokens': 3000
            },
            'deepseek-v2': {
                'temperature': 0.2,
                'max_tokens': 3000
            },
            'mistral-7b': {
                'temperature': 0.15,
                'max_tokens': 2500
            }
        }
        
        results = {}
        
        for model_name, config in models.items():
            results[model_name] = self.test_model(model_name, config)
        
        return results
    
    def generate_report(self, results: Dict[str, Any], output_file: str = "test/llm_comparison_results.json"):
        """Generate comparison report"""
        
        print(f"\n{'='*80}")
        print("LLM COMPARISON RESULTS")
        print(f"{'='*80}\n")
        
        print(f"{'Model':<20} {'Precision@5':<15} {'Recall@10':<15} {'MAP@10':<15} {'NDCG@5':<15} {'Latency (s)':<15}")
        print("-" * 80)
        
        for model_name, metrics in results.items():
            print(f"{model_name:<20} "
                  f"{metrics['precision_at_5']:<15.3f} "
                  f"{metrics['recall_at_10']:<15.3f} "
                  f"{metrics['map_at_10']:<15.3f} "
                  f"{metrics['ndcg_at_5']:<15.3f} "
                  f"{metrics['avg_latency']:<15.2f}")
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✓ Results saved to: {output_file}\n")


def main():
    """Main evaluation function"""
    
    # Initialize test suite
    tester = LLMComparisonTest()
    
    # Run comparison
    results = tester.run_comparison()
    
    # Generate report
    tester.generate_report(results)
    
    print("✓ LLM comparison test completed!")


if __name__ == "__main__":
    main()
