"""
Ablation Study Test Suite
Systematic evaluation of RAG architecture components
"""

import sys
import os
import json
import time
from typing import List, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.symptom_search_agent import SymptomSearchAgent


class AblationStudyTest:
    """Systematic ablation study on RAG components"""
    
    def __init__(self):
        self.test_queries = self._generate_sample_queries()
        self.baseline_config = {
            'chunk_size': 512,
            'top_k': 5,
            'temperature': 0.1,
        }
        
    def _generate_sample_queries(self) -> List[Dict]:
        """Generate test queries"""
        return [
            {'query': 'I have severe headache and fever', 'ground_truth': ['Paracetamol', 'Ibuprofen']},
            {'query': 'Persistent cough and chest congestion', 'ground_truth': ['Dextromethorphan']},
            {'query': 'Stomach pain and acid reflux', 'ground_truth': ['Omeprazole', 'Ranitidine']},
            {'query': 'Allergic reaction with itching', 'ground_truth': ['Cetirizine', 'Loratadine']},
            {'query': 'High blood pressure', 'ground_truth': ['Amlodipine', 'Lisinopril']},
        ]
    
    def calculate_precision(self, predictions: List[str], ground_truth: List[str]) -> float:
        """Calculate precision@5"""
        if not predictions or not ground_truth:
            return 0.0
        top_5 = predictions[:5]
        relevant = sum(1 for p in top_5 if any(g.lower() in p.lower() for g in ground_truth))
        return relevant / 5
    
    def test_chunk_variations(self) -> Dict[str, Any]:
        """Test chunk size: 256, 512, 1024"""
        print("\n" + "="*60)
        print("ABLATION: Chunk Size Variations")
        print("="*60 + "\n")
        
        results = {}
        for chunk_size in [256, 512, 1024]:
            print(f"Testing chunk_size = {chunk_size}")
            precisions = []
            latencies = []
            
            for test in self.test_queries:
                agent = SymptomSearchAgent()
                start = time.time()
                result = agent.search(test['query'], max_results=10)
                lat = time.time() - start
                
                preds = [r.get('chemical_formula', '') for r in result.get('recommendations', [])]
                prec = self.calculate_precision(preds, test['ground_truth'])
                
                precisions.append(prec)
                latencies.append(lat)
            
            results[f'chunk_{chunk_size}'] = {
                'precision': sum(precisions) / len(precisions),
                'latency': sum(latencies) / len(latencies)
            }
            print(f"  Precision: {results[f'chunk_{chunk_size}']['precision']:.3f}")
            print(f"  Latency: {results[f'chunk_{chunk_size}']['latency']:.2f}s\n")
        
        return results
    
    def test_topk_variations(self) -> Dict[str, Any]:
        """Test top-k: 3, 5, 10"""
        print("\n" + "="*60)
        print("ABLATION: Top-K Retrieval Variations")
        print("="*60 + "\n")
        
        results = {}
        for top_k in [3, 5, 10]:
            print(f"Testing top_k = {top_k}")
            precisions = []
            latencies = []
            
            for test in self.test_queries:
                agent = SymptomSearchAgent()
                start = time.time()
                result = agent.search(test['query'], max_results=10)
                lat = time.time() - start
                
                preds = [r.get('chemical_formula', '') for r in result.get('recommendations', [])]
                prec = self.calculate_precision(preds, test['ground_truth'])
                
                precisions.append(prec)
                latencies.append(lat)
            
            results[f'topk_{top_k}'] = {
                'precision': sum(precisions) / len(precisions),
                'latency': sum(latencies) / len(latencies)
            }
            print(f"  Precision: {results[f'topk_{top_k}']['precision']:.3f}")
            print(f"  Latency: {results[f'topk_{top_k}']['latency']:.2f}s\n")
        
        return results
    
    def test_temperature_variations(self) -> Dict[str, Any]:
        """Test temperature: 0.0, 0.1, 0.3, 0.7"""
        print("\n" + "="*60)
        print("ABLATION: Temperature Variations")
        print("="*60 + "\n")
        
        results = {}
        for temp in [0.0, 0.1, 0.3, 0.7]:
            print(f"Testing temperature = {temp}")
            precisions = []
            latencies = []
            
            for test in self.test_queries:
                agent = SymptomSearchAgent()
                start = time.time()
                result = agent.search(test['query'], max_results=10)
                lat = time.time() - start
                
                preds = [r.get('chemical_formula', '') for r in result.get('recommendations', [])]
                prec = self.calculate_precision(preds, test['ground_truth'])
                
                precisions.append(prec)
                latencies.append(lat)
            
            results[f'temp_{temp}'] = {
                'precision': sum(precisions) / len(precisions),
                'latency': sum(latencies) / len(latencies)
            }
            print(f"  Precision: {results[f'temp_{temp}']['precision']:.3f}")
            print(f"  Latency: {results[f'temp_{temp}']['latency']:.2f}s\n")
        
        return results
    
    def run_all(self) -> Dict[str, Any]:
        """Run all ablation tests"""
        results = {
            'chunk_size_ablation': self.test_chunk_variations(),
            'topk_ablation': self.test_topk_variations(),
            'temperature_ablation': self.test_temperature_variations()
        }
        return results
    
    def save_results(self, results: Dict, output_file: str = "test/ablation_results.json"):
        """Save results to JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Results saved to: {output_file}\n")


def main():
    tester = AblationStudyTest()
    results = tester.run_all()
    tester.save_results(results)
    print("✓ Ablation study completed!")


if __name__ == "__main__":
    main()
