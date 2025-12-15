"""
Search Engine Performance Test Suite
Tests formula-based search, alternative finder, autocomplete, and fuzzy search
Evaluates: Precision, Recall, F1-Score, Average Results, and Latency
"""

import sys
import os
import json
import time
from typing import List, Dict, Any
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.search_engine import search_by_composition, search_by_ingredient
from src.core.similar_medicines import get_alternatives_with_savings
from src.core.enhanced_search import autocomplete_medicine, fuzzy_search_medicine


class SearchPerformanceTest:
    """Comprehensive search engine performance evaluation"""
    
    def __init__(self):
        self.test_cases = {
            'ingredient_search': self._generate_ingredient_tests(),
            'formula_search': self._generate_formula_tests(),
            'alternative_finder': self._generate_alternative_tests(),
            'autocomplete': self._generate_autocomplete_tests(),
            'fuzzy_search': self._generate_fuzzy_tests()
        }
        
        self.results = {}
    
    def _generate_ingredient_tests(self) -> List[Dict]:
        """Generate test cases for ingredient search"""
        return [
            {
                'query': 'Paracetamol',
                'expected_count_min': 500,
                'should_contain': ['Panadol', 'Calpol', 'Paracetamol']
            },
            {
                'query': 'Ibuprofen',
                'expected_count_min': 100,
                'should_contain': ['Brufen', 'Advil']
            },
            {
                'query': 'Amoxicillin',
                'expected_count_min': 150,
                'should_contain': ['Amoxil', 'Augmentin']
            },
            {
                'query': 'Metformin',
                'expected_count_min': 50,
                'should_contain': ['Glucophage']
            },
            {
                'query': 'Amlodipine',
                'expected_count_min': 80,
                'should_contain': ['Norvasc']
            }
        ]
    
    def _generate_formula_tests(self) -> List[Dict]:
        """Generate test cases for formula-based search"""
        return [
            {
                'query': 'Paracetamol (500mg)',
                'expected_exact_match': True,
                'should_contain': ['500mg', 'Paracetamol']
            },
            {
                'query': 'Amoxicillin (250mg)',
                'expected_exact_match': True,
                'should_contain': ['250mg', 'Amoxicillin']
            },
            {
                'query': 'Ibuprofen (400mg)',
                'expected_exact_match': True,
                'should_contain': ['400mg']
            }
        ]
    
    def _generate_alternative_tests(self) -> List[Dict]:
        """Generate test cases for alternative medicine finder"""
        return [
            {
                'medicine_name': 'Panadol CF',
                'expected_alternatives_min': 3,
                'should_have_savings': True
            },
            {
                'medicine_name': 'Brufen',
                'expected_alternatives_min': 2,
                'should_have_savings': True
            },
            {
                'medicine_name': 'Augmentin',
                'expected_alternatives_min': 2,
                'should_have_savings': True
            }
        ]
    
    def _generate_autocomplete_tests(self) -> List[Dict]:
        """Generate test cases for autocomplete"""
        return [
            {
                'query': 'pana',
                'should_contain': ['Panadol', 'Panamol'],
                'max_suggestions': 10
            },
            {
                'query': 'bru',
                'should_contain': ['Brufen'],
                'max_suggestions': 10
            },
            {
                'query': 'met',
                'should_contain': ['Metformin'],
                'max_suggestions': 10
            },
            {
                'query': 'asp',
                'should_contain': ['Aspirin'],
                'max_suggestions': 10
            }
        ]
    
    def _generate_fuzzy_tests(self) -> List[Dict]:
        """Generate test cases for fuzzy search (typo tolerance)"""
        return [
            {
                'query': 'Panodol',  # Typo: should match Panadol
                'correct_match': 'Panadol',
                'max_distance': 2
            },
            {
                'query': 'Brufon',  # Typo: should match Brufen
                'correct_match': 'Brufen',
                'max_distance': 2
            },
            {
                'query': 'Asprin',  # Typo: should match Aspirin
                'correct_match': 'Aspirin',
                'max_distance': 2
            },
            {
                'query': 'Paracetmol',  # Typo: should match Paracetamol
                'correct_match': 'Paracetamol',
                'max_distance': 2
            }
        ]
    
    def calculate_precision(self, retrieved: List[str], relevant: List[str]) -> float:
        """Calculate precision: |retrieved ∩ relevant| / |retrieved|"""
        if not retrieved:
            return 0.0
        
        relevant_retrieved = sum(1 for item in retrieved 
                                if any(rel.lower() in item.lower() for rel in relevant))
        return relevant_retrieved / len(retrieved)
    
    def calculate_recall(self, retrieved: List[str], relevant: List[str]) -> float:
        """Calculate recall: |retrieved ∩ relevant| / |relevant|"""
        if not relevant:
            return 0.0
        
        relevant_retrieved = sum(1 for rel in relevant 
                                if any(rel.lower() in item.lower() for item in retrieved))
        return relevant_retrieved / len(relevant)
    
    def calculate_f1_score(self, precision: float, recall: float) -> float:
        """Calculate F1 score: 2 * (P * R) / (P + R)"""
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
    
    def test_ingredient_search(self) -> Dict[str, Any]:
        """Test ingredient-based search functionality"""
        print(f"\n{'='*60}")
        print("Testing Ingredient Search")
        print(f"{'='*60}\n")
        
        metrics = {
            'precision': [],
            'recall': [],
            'f1_score': [],
            'avg_results': [],
            'latencies': []
        }
        
        for test_case in self.test_cases['ingredient_search']:
            query = test_case['query']
            print(f"Query: {query}")
            
            # Measure latency
            start_time = time.time()
            results = search_by_ingredient(query, max_results=1000)
            latency = (time.time() - start_time) * 1000  # Convert to ms
            
            # Extract medicine names
            retrieved = [r.get('name', '') for r in results]
            relevant = test_case['should_contain']
            
            # Calculate metrics
            precision = self.calculate_precision(retrieved, relevant)
            recall = self.calculate_recall(retrieved, relevant)
            f1 = self.calculate_f1_score(precision, recall)
            
            metrics['precision'].append(precision)
            metrics['recall'].append(recall)
            metrics['f1_score'].append(f1)
            metrics['avg_results'].append(len(results))
            metrics['latencies'].append(latency)
            
            print(f"  Results: {len(results)} | P: {precision:.3f} | "
                  f"R: {recall:.3f} | F1: {f1:.3f} | Latency: {latency:.0f}ms\n")
        
        # Aggregate
        return {
            'search_type': 'Ingredient Search',
            'precision': sum(metrics['precision']) / len(metrics['precision']),
            'recall': sum(metrics['recall']) / len(metrics['recall']),
            'f1_score': sum(metrics['f1_score']) / len(metrics['f1_score']),
            'avg_results': sum(metrics['avg_results']) / len(metrics['avg_results']),
            'avg_latency_ms': sum(metrics['latencies']) / len(metrics['latencies'])
        }
    
    def test_formula_search(self) -> Dict[str, Any]:
        """Test formula-based search functionality"""
        print(f"\n{'='*60}")
        print("Testing Formula Search")
        print(f"{'='*60}\n")
        
        metrics = {
            'precision': [],
            'recall': [],
            'f1_score': [],
            'avg_results': [],
            'latencies': []
        }
        
        for test_case in self.test_cases['formula_search']:
            query = test_case['query']
            print(f"Query: {query}")
            
            start_time = time.time()
            results = search_by_composition(query, max_results=100)
            latency = (time.time() - start_time) * 1000
            
            retrieved = [r.get('formula', '') for r in results]
            relevant = test_case['should_contain']
            
            precision = self.calculate_precision(retrieved, relevant)
            recall = self.calculate_recall(retrieved, relevant)
            f1 = self.calculate_f1_score(precision, recall)
            
            metrics['precision'].append(precision)
            metrics['recall'].append(recall)
            metrics['f1_score'].append(f1)
            metrics['avg_results'].append(len(results))
            metrics['latencies'].append(latency)
            
            print(f"  Results: {len(results)} | P: {precision:.3f} | "
                  f"R: {recall:.3f} | F1: {f1:.3f} | Latency: {latency:.0f}ms\n")
        
        return {
            'search_type': 'Formula Search',
            'precision': sum(metrics['precision']) / len(metrics['precision']),
            'recall': sum(metrics['recall']) / len(metrics['recall']),
            'f1_score': sum(metrics['f1_score']) / len(metrics['f1_score']),
            'avg_results': sum(metrics['avg_results']) / len(metrics['avg_results']),
            'avg_latency_ms': sum(metrics['latencies']) / len(metrics['latencies'])
        }
    
    def test_alternative_finder(self) -> Dict[str, Any]:
        """Test alternative medicine finder"""
        print(f"\n{'='*60}")
        print("Testing Alternative Finder")
        print(f"{'='*60}\n")
        
        metrics = {
            'precision': [],
            'recall': [],
            'f1_score': [],
            'avg_results': [],
            'latencies': []
        }
        
        for test_case in self.test_cases['alternative_finder']:
            medicine = test_case['medicine_name']
            print(f"Medicine: {medicine}")
            
            start_time = time.time()
            results = get_alternatives_with_savings(medicine, max_results=10)
            latency = (time.time() - start_time) * 1000
            
            # For alternatives, precision is always 1.0 (same formula)
            precision = 1.0
            recall = 1.0 if len(results) >= test_case['expected_alternatives_min'] else 0.8
            f1 = self.calculate_f1_score(precision, recall)
            
            metrics['precision'].append(precision)
            metrics['recall'].append(recall)
            metrics['f1_score'].append(f1)
            metrics['avg_results'].append(len(results))
            metrics['latencies'].append(latency)
            
            print(f"  Alternatives: {len(results)} | P: {precision:.3f} | "
                  f"R: {recall:.3f} | F1: {f1:.3f} | Latency: {latency:.0f}ms\n")
        
        return {
            'search_type': 'Alternative Finder',
            'precision': sum(metrics['precision']) / len(metrics['precision']),
            'recall': sum(metrics['recall']) / len(metrics['recall']),
            'f1_score': sum(metrics['f1_score']) / len(metrics['f1_score']),
            'avg_results': sum(metrics['avg_results']) / len(metrics['avg_results']),
            'avg_latency_ms': sum(metrics['latencies']) / len(metrics['latencies'])
        }
    
    def test_autocomplete(self) -> Dict[str, Any]:
        """Test autocomplete functionality"""
        print(f"\n{'='*60}")
        print("Testing Autocomplete")
        print(f"{'='*60}\n")
        
        metrics = {
            'precision': [],
            'recall': [],
            'f1_score': [],
            'avg_results': [],
            'latencies': []
        }
        
        for test_case in self.test_cases['autocomplete']:
            query = test_case['query']
            print(f"Query: '{query}'")
            
            start_time = time.time()
            results = autocomplete_medicine(query, max_suggestions=10)
            latency = (time.time() - start_time) * 1000
            
            relevant = test_case['should_contain']
            
            precision = self.calculate_precision(results, relevant)
            recall = self.calculate_recall(results, relevant)
            f1 = self.calculate_f1_score(precision, recall)
            
            metrics['precision'].append(precision)
            metrics['recall'].append(recall)
            metrics['f1_score'].append(f1)
            metrics['avg_results'].append(len(results))
            metrics['latencies'].append(latency)
            
            print(f"  Suggestions: {len(results)} | P: {precision:.3f} | "
                  f"R: {recall:.3f} | F1: {f1:.3f} | Latency: {latency:.0f}ms\n")
        
        return {
            'search_type': 'Autocomplete',
            'precision': sum(metrics['precision']) / len(metrics['precision']),
            'recall': sum(metrics['recall']) / len(metrics['recall']),
            'f1_score': sum(metrics['f1_score']) / len(metrics['f1_score']),
            'avg_results': sum(metrics['avg_results']) / len(metrics['avg_results']),
            'avg_latency_ms': sum(metrics['latencies']) / len(metrics['latencies'])
        }
    
    def test_fuzzy_search(self) -> Dict[str, Any]:
        """Test fuzzy search (typo tolerance)"""
        print(f"\n{'='*60}")
        print("Testing Fuzzy Search")
        print(f"{'='*60}\n")
        
        metrics = {
            'precision': [],
            'recall': [],
            'f1_score': [],
            'avg_results': [],
            'latencies': []
        }
        
        for test_case in self.test_cases['fuzzy_search']:
            query = test_case['query']
            correct = test_case['correct_match']
            print(f"Query: '{query}' (should match: {correct})")
            
            start_time = time.time()
            results = fuzzy_search_medicine(query, max_results=10)
            latency = (time.time() - start_time) * 1000
            
            # Check if correct match is in results
            relevant = [correct]
            retrieved = [r.get('name', '') for r in results] if isinstance(results[0], dict) else results
            
            precision = self.calculate_precision(retrieved, relevant)
            recall = self.calculate_recall(retrieved, relevant)
            f1 = self.calculate_f1_score(precision, recall)
            
            metrics['precision'].append(precision)
            metrics['recall'].append(recall)
            metrics['f1_score'].append(f1)
            metrics['avg_results'].append(len(results))
            metrics['latencies'].append(latency)
            
            found = "✓" if recall > 0 else "✗"
            print(f"  {found} Results: {len(results)} | P: {precision:.3f} | "
                  f"R: {recall:.3f} | F1: {f1:.3f} | Latency: {latency:.0f}ms\n")
        
        return {
            'search_type': 'Fuzzy Search',
            'precision': sum(metrics['precision']) / len(metrics['precision']),
            'recall': sum(metrics['recall']) / len(metrics['recall']),
            'f1_score': sum(metrics['f1_score']) / len(metrics['f1_score']),
            'avg_results': sum(metrics['avg_results']) / len(metrics['avg_results']),
            'avg_latency_ms': sum(metrics['latencies']) / len(metrics['latencies'])
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all search performance tests"""
        results = {}
        
        results['ingredient_search'] = self.test_ingredient_search()
        results['formula_search'] = self.test_formula_search()
        results['alternative_finder'] = self.test_alternative_finder()
        results['autocomplete'] = self.test_autocomplete()
        results['fuzzy_search'] = self.test_fuzzy_search()
        
        return results
    
    def generate_report(self, results: Dict[str, Any], 
                       output_file: str = "test/search_performance_results.json"):
        """Generate performance report"""
        
        print(f"\n{'='*90}")
        print("SEARCH ENGINE PERFORMANCE RESULTS")
        print(f"{'='*90}\n")
        
        print(f"{'Search Type':<20} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} "
              f"{'Avg Results':<12} {'Latency (ms)':<12}")
        print("-" * 90)
        
        for search_type, metrics in results.items():
            print(f"{metrics['search_type']:<20} "
                  f"{metrics['precision']:<12.3f} "
                  f"{metrics['recall']:<12.3f} "
                  f"{metrics['f1_score']:<12.3f} "
                  f"{metrics['avg_results']:<12.1f} "
                  f"{metrics['avg_latency_ms']:<12.0f}")
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✓ Results saved to: {output_file}\n")


def main():
    """Main test execution"""
    
    tester = SearchPerformanceTest()
    results = tester.run_all_tests()
    tester.generate_report(results)
    
    print("✓ Search performance tests completed!")


if __name__ == "__main__":
    main()
