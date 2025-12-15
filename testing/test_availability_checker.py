"""
Comprehensive Testing Script for Medicine Availability Checker
Tests all functionality including loading, searching, API calls, caching, and error handling
"""

import sys
import io

# Set UTF-8 encoding for stdout to handle unicode characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, 'src/core')

from websearchfunction import (
    load_medicines,
    find_medicine,
    extract_product_id,
    call_availability_api,
    parse_availability,
    check_medicine_availability,
    check_multiple_medicines,
    load_cache,
    save_cache,
    is_cache_fresh
)
import time
from datetime import datetime

# Test results tracking
test_results = []

def log_test(test_name, passed, details=""):
    """Log test result"""
    status = "PASS" if passed else "FAIL"
    test_results.append({
        'test': test_name,
        'status': status,
        'details': details
    })
    symbol = "[+]" if passed else "[-]"
    print(f"{symbol} {status}: {test_name}")
    if details:
        print(f"    {details}")

print("="*80)
print("MEDICINE AVAILABILITY CHECKER - COMPREHENSIVE TESTING")
print("="*80)
print(f"Test Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# ============================================================
# TEST 1: Medicine Database Loading
# ============================================================
print("\n[TEST 1] Medicine Database Loading")
print("-" * 80)

try:
    medicines = load_medicines()
    test_passed = len(medicines) > 0
    log_test("Load medicines.json", test_passed, f"Loaded {len(medicines)} medicines")

    if test_passed:
        # Check data structure
        sample_med = medicines[0]
        required_fields = ['name', 'brand', 'price']
        has_fields = all(field in sample_med for field in required_fields)
        log_test("Medicine data structure", has_fields, f"Sample: {sample_med.get('name', 'N/A')}")
except Exception as e:
    log_test("Load medicines.json", False, f"Error: {str(e)}")

# ============================================================
# TEST 2: Medicine Search Functionality
# ============================================================
print("\n[TEST 2] Medicine Search Functionality")
print("-" * 80)

# Test exact match
try:
    med = find_medicine("Panadol CF  caplets 10x10's", medicines)
    test_passed = med is not None
    log_test("Exact medicine name match", test_passed, f"Found: {med['name'] if med else 'None'}")
except Exception as e:
    log_test("Exact medicine name match", False, f"Error: {str(e)}")

# Test partial match
try:
    med = find_medicine("Panadol", medicines)
    test_passed = med is not None and "panadol" in med['name'].lower()
    log_test("Partial medicine name match", test_passed, f"Found: {med['name'] if med else 'None'}")
except Exception as e:
    log_test("Partial medicine name match", False, f"Error: {str(e)}")

# Test case insensitive
try:
    med = find_medicine("PANADOL", medicines)
    test_passed = med is not None
    log_test("Case-insensitive search", test_passed, f"Found: {med['name'] if med else 'None'}")
except Exception as e:
    log_test("Case-insensitive search", False, f"Error: {str(e)}")

# Test non-existent medicine
try:
    med = find_medicine("NonExistentMedicine12345", medicines)
    test_passed = med is None
    log_test("Non-existent medicine returns None", test_passed, "Correctly returned None")
except Exception as e:
    log_test("Non-existent medicine returns None", False, f"Error: {str(e)}")

# ============================================================
# TEST 3: Product ID Extraction
# ============================================================
print("\n[TEST 3] Product ID Extraction from URLs")
print("-" * 80)

# Test valid URL
try:
    url = "https://dawaai.pk/medicine/panadol-cf-caplets-43759.html"
    p_id = extract_product_id(url)
    test_passed = p_id == "43759"
    log_test("Extract product ID from valid URL", test_passed, f"Extracted: {p_id}")
except Exception as e:
    log_test("Extract product ID from valid URL", False, f"Error: {str(e)}")

# Test invalid URL
try:
    url = "https://invalid-url.com"
    p_id = extract_product_id(url)
    test_passed = p_id is None
    log_test("Invalid URL returns None", test_passed, "Correctly returned None")
except Exception as e:
    log_test("Invalid URL returns None", False, f"Error: {str(e)}")

# Test empty URL
try:
    p_id = extract_product_id("")
    test_passed = p_id is None
    log_test("Empty URL returns None", test_passed, "Correctly returned None")
except Exception as e:
    log_test("Empty URL returns None", False, f"Error: {str(e)}")

# ============================================================
# TEST 4: Hidden API Calls
# ============================================================
print("\n[TEST 4] Hidden API Calls")
print("-" * 80)

# Test API call with valid product ID
api_response = None
try:
    print("      Calling API with product ID 43759 (Panadol CF)...")
    api_response = call_availability_api("43759")
    test_passed = api_response is not None and 'out_of_stock' in api_response
    details = f"Response received: {api_response is not None}"
    if api_response:
        details += f", out_of_stock={api_response.get('out_of_stock')}"
    log_test("API call with valid product ID", test_passed, details)
except Exception as e:
    error_msg = str(e)
    # Truncate error message if it contains problematic characters
    if len(error_msg) > 100:
        error_msg = error_msg[:100] + "..."
    log_test("API call with valid product ID", False, f"Error: API call exception")
    api_response = None

# Test parse availability
if api_response:
    try:
        availability = parse_availability(api_response)
        test_passed = availability in [0, 1]
        log_test("Parse availability from API response", test_passed, f"Availability: {availability} (1=Available, 0=Out of Stock)")
    except Exception as e:
        log_test("Parse availability from API response", False, f"Error: {str(e)[:100]}")

# ============================================================
# TEST 5: Cache Functionality
# ============================================================
print("\n[TEST 5] Cache Functionality")
print("-" * 80)

# Test cache save and load
try:
    test_cache = {
        "Test Medicine": {
            "available": 1,
            "price": "100.00",
            "out_of_stock": 0,
            "p_id": "12345",
            "last_checked": datetime.now().isoformat()
        }
    }
    save_cache(test_cache)
    loaded_cache = load_cache()
    test_passed = "Test Medicine" in loaded_cache
    log_test("Save and load cache", test_passed, f"Cache contains {len(loaded_cache)} items")
except Exception as e:
    log_test("Save and load cache", False, f"Error: {str(e)}")

# Test cache freshness
try:
    recent_item = {"last_checked": datetime.now().isoformat()}
    test_passed = is_cache_fresh(recent_item)
    log_test("Cache freshness check (recent)", test_passed, "Recent cache is fresh")
except Exception as e:
    log_test("Cache freshness check (recent)", False, f"Error: {str(e)}")

# ============================================================
# TEST 6: Complete Availability Check
# ============================================================
print("\n[TEST 6] Complete Availability Check Workflow")
print("-" * 80)

# Test with a real medicine (without cache first)
try:
    print("      Checking availability for 'Panadol' (first check, no cache)...")
    start_time = time.time()
    result = check_medicine_availability("Panadol", use_cache=False, verbose=False)
    elapsed_time = time.time() - start_time
    test_passed = result in [0, 1]
    status_text = "Available" if result == 1 else "Out of Stock" if result == 0 else "Unknown"
    log_test("Check medicine availability (no cache)", test_passed,
             f"Result: {status_text}, Time: {elapsed_time:.2f}s")
except Exception as e:
    log_test("Check medicine availability (no cache)", False, f"Error: {str(e)}")

# Test with cache (should be faster)
try:
    print("      Checking availability for 'Panadol' (using cache)...")
    start_time = time.time()
    result_cached = check_medicine_availability("Panadol", use_cache=True, verbose=False)
    elapsed_time_cached = time.time() - start_time
    test_passed = result_cached in [0, 1] and elapsed_time_cached < elapsed_time
    status_text = "Available" if result_cached == 1 else "Out of Stock" if result_cached == 0 else "Unknown"
    speedup = f"{elapsed_time / elapsed_time_cached:.1f}x faster" if elapsed_time_cached > 0 else "instant"
    log_test("Check medicine availability (with cache)", test_passed,
             f"Result: {status_text}, Time: {elapsed_time_cached:.3f}s ({speedup})")
except Exception as e:
    log_test("Check medicine availability (with cache)", False, f"Error: {str(e)}")

# ============================================================
# TEST 7: Error Handling
# ============================================================
print("\n[TEST 7] Error Handling")
print("-" * 80)

# Test with non-existent medicine
try:
    result = check_medicine_availability("NonExistentMedicine99999", verbose=False)
    test_passed = result is None
    log_test("Non-existent medicine handling", test_passed, "Correctly returned None")
except Exception as e:
    log_test("Non-existent medicine handling", False, f"Error: {str(e)}")

# ============================================================
# TEST 8: Batch Checking
# ============================================================
print("\n[TEST 8] Batch Medicine Checking")
print("-" * 80)

try:
    print("      Checking multiple medicines: Panadol, Brufen, Disprin...")
    medicines_to_check = ["Panadol", "Brufen", "Disprin"]
    start_time = time.time()
    results = {}

    # Check each medicine individually to avoid verbose output
    for med_name in medicines_to_check:
        results[med_name] = check_medicine_availability(med_name, use_cache=True, verbose=False)

    elapsed_time = time.time() - start_time
    test_passed = len(results) == 3 and all(v in [0, 1, None] for v in results.values())

    success_count = sum(1 for v in results.values() if v in [0, 1])
    log_test("Batch medicine checking", test_passed,
             f"Checked {len(results)} medicines in {elapsed_time:.2f}s, {success_count} successful")

    # Show results
    for name, available in results.items():
        status = "Available" if available == 1 else "Out of Stock" if available == 0 else "Not Found"
        print(f"      - {name}: {status}")

except Exception as e:
    log_test("Batch medicine checking", False, f"Error: {str(e)}")

# ============================================================
# TEST SUMMARY
# ============================================================
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)

passed_tests = sum(1 for t in test_results if t['status'] == 'PASS')
failed_tests = sum(1 for t in test_results if t['status'] == 'FAIL')
total_tests = len(test_results)
pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

print(f"Total Tests: {total_tests}")
print(f"Passed: {passed_tests}")
print(f"Failed: {failed_tests}")
print(f"Pass Rate: {pass_rate:.1f}%")

if failed_tests > 0:
    print("\nFailed Tests:")
    for t in test_results:
        if t['status'] == 'FAIL':
            print(f"  - {t['test']}: {t['details']}")

print("\n" + "="*80)
print(f"Test End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Final verdict
if pass_rate == 100:
    print("\n>>> ALL TESTS PASSED! System is ready for production.")
elif pass_rate >= 80:
    print(f"\n>>> Most tests passed ({pass_rate:.1f}%). Review failed tests.")
else:
    print(f"\n>>> Multiple test failures ({pass_rate:.1f}%). System needs fixes.")
