"""
Availability Checker Performance Test
Tests real-time medicine availability checking with caching
"""

import sys
import os
import json
import time
from typing import Dict, Any, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.websearchfunction import check_medicine_availability


class AvailabilityTest:
    """Test availability checking system"""
    
    def __init__(self):
        self.test_medicines = [
            'Panadol',
            'Brufen',
            'Augmentin',
            'Paracetamol',
            'Disprin',
            'Calpol',
            'Aspirin',
            'Metformin',
            'Amlodipine',
            'Omeprazole'
        ]
    
    def test_first_check_latency(self) -> Dict[str, Any]:
        """Test latency for first availability check (API call)"""
        print("\n" + "="*60)
        print("Testing First Check Latency (API Calls)")
        print("="*60 + "\n")
        
        latencies = []
        success_count = 0
        
        for medicine in self.test_medicines:
            print(f"Checking: {medicine}")
            
            start_time = time.time()
            result = check_medicine_availability(medicine)
            latency = time.time() - start_time
            
            latencies.append(latency)
            
            if result.get('available') is not None:
                success_count += 1
                status = "Available" if result['available'] else "Out of Stock"
                print(f"  Status: {status} | Latency: {latency*1000:.0f}ms\n")
            else:
                print(f"  Status: Not Found | Latency: {latency*1000:.0f}ms\n")
        
        avg_latency = sum(latencies) / len(latencies)
        success_rate = success_count / len(self.test_medicines)
        
        return {
            'avg_first_check_latency_ms': avg_latency * 1000,
            'success_rate': success_rate,
            'total_queries': len(self.test_medicines)
        }
    
    def test_cached_check_latency(self) -> Dict[str, Any]:
        """Test latency for cached availability check"""
        print("\n" + "="*60)
        print("Testing Cached Check Latency")
        print("="*60 + "\n")
        
        # First, populate cache
        for medicine in self.test_medicines:
            check_medicine_availability(medicine)
        
        # Now test cached retrieval
        latencies = []
        cache_hits = 0
        
        for medicine in self.test_medicines:
            print(f"Checking (cached): {medicine}")
            
            start_time = time.time()
            result = check_medicine_availability(medicine)
            latency = time.time() - start_time
            
            latencies.append(latency)
            
            if latency < 0.2:  # Less than 200ms indicates cache hit
                cache_hits += 1
            
            print(f"  Latency: {latency*1000:.0f}ms\n")
        
        avg_latency = sum(latencies) / len(latencies)
        cache_hit_rate = cache_hits / len(self.test_medicines)
        
        return {
            'avg_cached_latency_ms': avg_latency * 1000,
            'cache_hit_rate': cache_hit_rate,
            'total_queries': len(self.test_medicines)
        }
    
    def test_reliability(self) -> Dict[str, Any]:
        """Test API reliability over multiple requests"""
        print("\n" + "="*60)
        print("Testing API Reliability")
        print("="*60 + "\n")
        
        total_requests = 0
        successful_requests = 0
        timeouts = 0
        errors = 0
        
        # Test each medicine 3 times
        for medicine in self.test_medicines:
            for i in range(3):
                total_requests += 1
                
                try:
                    result = check_medicine_availability(medicine)
                    
                    if result.get('available') is not None:
                        successful_requests += 1
                    elif result.get('error'):
                        if 'timeout' in result['error'].lower():
                            timeouts += 1
                        else:
                            errors += 1
                except Exception as e:
                    errors += 1
        
        reliability = successful_requests / total_requests
        
        print(f"Total Requests: {total_requests}")
        print(f"Successful: {successful_requests}")
        print(f"Timeouts: {timeouts}")
        print(f"Errors: {errors}")
        print(f"Reliability: {reliability*100:.1f}%\n")
        
        return {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'timeouts': timeouts,
            'errors': errors,
            'reliability_rate': reliability
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all availability tests"""
        
        results = {}
        
        results['first_check'] = self.test_first_check_latency()
        results['cached_check'] = self.test_cached_check_latency()
        results['reliability'] = self.test_reliability()
        
        return results
    
    def generate_report(self, results: Dict[str, Any], 
                       output_file: str = "test/availability_test_results.json"):
        """Generate test report"""
        
        print("\n" + "="*60)
        print("AVAILABILITY CHECKER TEST SUMMARY")
        print("="*60 + "\n")
        
        print(f"First Check (API Call):")
        print(f"  Avg Latency: {results['first_check']['avg_first_check_latency_ms']:.0f}ms")
        print(f"  Success Rate: {results['first_check']['success_rate']*100:.1f}%\n")
        
        print(f"Cached Check:")
        print(f"  Avg Latency: {results['cached_check']['avg_cached_latency_ms']:.0f}ms")
        print(f"  Cache Hit Rate: {results['cached_check']['cache_hit_rate']*100:.1f}%\n")
        
        print(f"Reliability:")
        print(f"  Success Rate: {results['reliability']['reliability_rate']*100:.1f}%")
        print(f"  Timeouts: {results['reliability']['timeouts']}")
        print(f"  Errors: {results['reliability']['errors']}\n")
        
        # Calculate speedup
        speedup = results['first_check']['avg_first_check_latency_ms'] / results['cached_check']['avg_cached_latency_ms']
        print(f"Cache Speedup: {speedup:.1f}x faster\n")
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Results saved to: {output_file}\n")


def main():
    """Main test execution"""
    
    tester = AvailabilityTest()
    results = tester.run_all_tests()
    tester.generate_report(results)
    
    print("✓ Availability checker tests completed!")


if __name__ == "__main__":
    main()
