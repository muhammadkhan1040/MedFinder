"""
Cost Savings Analysis Test
Tests pharmaceutical equivalence matching and calculates potential savings
"""

import sys
import os
import json
from typing import Dict, Any, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.similar_medicines import get_alternatives_with_savings
from src.core.utils import load_medicines


class CostSavingsTest:
    """Test cost savings through generic substitution"""
    
    def __init__(self):
        self.medicines = load_medicines()
        self.test_medicines = [
            'Panadol CF',
            'Brufen 400mg',
            'Augmentin 625mg',
            'Norvasc 5mg',
            'Glucophage 500mg',
            'Losec 20mg',
            'Lipitor 10mg',
            'Crestor 10mg',
            'Januvia 100mg',
            'Nexium 40mg'
        ]
    
    def test_savings_by_medicine(self) -> List[Dict[str, Any]]:
        """Test savings for individual medicines"""
        print("\n" + "="*60)
        print("Testing Cost Savings by Medicine")
        print("="*60 + "\n")
        
        results = []
        
        for medicine_name in self.test_medicines:
            print(f"Medicine: {medicine_name}")
            
            alternatives = get_alternatives_with_savings(medicine_name, max_results=10)
            
            if alternatives:
                max_savings = max(alt.get('savings_percentage', 0) for alt in alternatives)
                avg_savings = sum(alt.get('savings_percentage', 0) for alt in alternatives) / len(alternatives)
                
                # Find original medicine price
                original = next((m for m in self.medicines if m.get('name') == medicine_name), None)
                original_price = float(original.get('price', 0)) if original else 0
                
                # Calculate annual savings (assuming 1 pack per month)
                monthly_saving = original_price * (max_savings / 100)
                annual_saving = monthly_saving * 12
                
                result = {
                    'medicine': medicine_name,
                    'original_price': original_price,
                    'alternatives_found': len(alternatives),
                    'max_savings_percent': max_savings,
                    'avg_savings_percent': avg_savings,
                    'annual_savings_pkr': annual_saving
                }
                
                results.append(result)
                
                print(f"  Original Price: Rs. {original_price:.2f}")
                print(f"  Alternatives Found: {len(alternatives)}")
                print(f"  Max Savings: {max_savings:.1f}%")
                print(f"  Annual Savings: Rs. {annual_saving:.2f}\n")
            else:
                print(f"  No alternatives found\n")
        
        return results
    
    def test_savings_by_category(self) -> Dict[str, Any]:
        """Test savings by therapeutic category"""
        print("\n" + "="*60)
        print("Testing Savings by Therapeutic Category")
        print("="*60 + "\n")
        
        # Group medicines by category
        categories = {}
        
        for med in self.medicines:
            category = med.get('categories', ['Uncategorized'])[0] if med.get('categories') else 'Uncategorized'
            
            if category not in categories:
                categories[category] = []
            
            categories[category].append(med)
        
        # Calculate savings for top categories
        category_results = []
        
        for category, meds in list(categories.items())[:10]:  # Top 10 categories
            if len(meds) < 5:  # Skip small categories
                continue
            
            savings_list = []
            
            # Sample 5 medicines from this category
            for med in meds[:5]:
                alternatives = get_alternatives_with_savings(med.get('name'), max_results=5)
                
                if alternatives:
                    max_savings = max(alt.get('savings_percentage', 0) for alt in alternatives)
                    savings_list.append(max_savings)
            
            if savings_list:
                avg_savings = sum(savings_list) / len(savings_list)
                max_savings = max(savings_list)
                
                category_results.append({
                    'category': category,
                    'medicines_tested': len(savings_list),
                    'avg_savings_percent': avg_savings,
                    'max_savings_percent': max_savings
                })
                
                print(f"{category}:")
                print(f"  Avg Savings: {avg_savings:.1f}%")
                print(f"  Max Savings: {max_savings:.1f}%\n")
        
        return {'categories': category_results}
    
    def calculate_population_impact(self, savings_results: List[Dict]) -> Dict[str, Any]:
        """Calculate potential population-level impact"""
        print("\n" + "="*60)
        print("Population Impact Analysis")
        print("="*60 + "\n")
        
        # Average across all tested medicines
        total_annual_savings = sum(r.get('annual_savings_pkr', 0) for r in savings_results)
        avg_annual_savings = total_annual_savings / len(savings_results) if savings_results else 0
        
        # Estimate for 1000 patients
        population_1000 = avg_annual_savings * 1000
        
        # Estimate for 10,000 patients
        population_10000 = avg_annual_savings * 10000
        
        print(f"Average Annual Savings per Patient: Rs. {avg_annual_savings:,.2f}")
        print(f"Potential Savings for 1,000 patients: Rs. {population_1000:,.2f}")
        print(f"Potential Savings for 10,000 patients: Rs. {population_10000:,.2f}\n")
        
        return {
            'avg_annual_savings_per_patient': avg_annual_savings,
            'savings_1000_patients': population_1000,
            'savings_10000_patients': population_10000
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all cost savings tests"""
        
        results = {}
        
        # Test individual medicines
        medicine_results = self.test_savings_by_medicine()
        results['by_medicine'] = medicine_results
        
        # Test by category
        category_results = self.test_savings_by_category()
        results['by_category'] = category_results
        
        # Calculate population impact
        impact = self.calculate_population_impact(medicine_results)
        results['population_impact'] = impact
        
        return results
    
    def generate_report(self, results: Dict[str, Any],
                       output_file: str = "test/cost_savings_results.json"):
        """Generate savings report"""
        
        print("\n" + "="*60)
        print("COST SAVINGS ANALYSIS SUMMARY")
        print("="*60 + "\n")
        
        medicine_results = results['by_medicine']
        
        if medicine_results:
            avg_max_savings = sum(r['max_savings_percent'] for r in medicine_results) / len(medicine_results)
            total_annual = sum(r['annual_savings_pkr'] for r in medicine_results)
            
            print(f"Medicines Tested: {len(medicine_results)}")
            print(f"Average Max Savings: {avg_max_savings:.1f}%")
            print(f"Total Annual Savings: Rs. {total_annual:,.2f}\n")
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Results saved to: {output_file}\n")


def main():
    """Main test execution"""
    
    tester = CostSavingsTest()
    results = tester.run_all_tests()
    tester.generate_report(results)
    
    print("✓ Cost savings analysis completed!")


if __name__ == "__main__":
    main()
