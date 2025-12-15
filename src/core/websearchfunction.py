"""
Medicine Availability Checker using Hidden API

This module provides functionality to check medicine availability on dawaai.pk
using their hidden API endpoint. Includes smart caching for optimal performance.

Author: Auto-generated
Date: 2025-12-06
"""

import json
import requests
import re
from datetime import datetime, timedelta
import os
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

# Get project root directory (2 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data'

CACHE_FILE = str(DATA_DIR / 'availability_cache.json')
CACHE_DURATION_HOURS = 2
MEDICINES_FILE = str(DATA_DIR / 'medicines.json')
API_ENDPOINT = 'https://dawaai.pk/product/get_product'

# ============================================================
# STEP 1: Load medicines.json
# ============================================================
def load_medicines():
    """Load all medicines from medicines.json"""
    try:
        with open(MEDICINES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {MEDICINES_FILE} not found")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {MEDICINES_FILE}")
        return []

# ============================================================
# STEP 2: Find medicine by name
# ============================================================
def find_medicine(medicine_name, medicines):
    """
    Search for medicine by name (case-insensitive, partial match)
    
    Args:
        medicine_name: Name of the medicine to search for
        medicines: List of all medicines
    
    Returns:
        Medicine dict if found, None otherwise
    """
    search_name = medicine_name.lower().strip()
    
    # First try exact match
    for med in medicines:
        if search_name == med['name'].lower():
            return med
    
    # Then try partial match
    for med in medicines:
        if search_name in med['name'].lower():
            return med
    
    return None

# ============================================================
# STEP 3: Extract p_id from URL
# ============================================================
def extract_product_id(url):
    """
    Extract product ID from dawaai.pk URL
    
    Example:
        URL: https://dawaai.pk/medicine/panadol-5-24329.html
        Returns: "24329"
    
    Args:
        url: Medicine URL from dawaai.pk
    
    Returns:
        Product ID as string, or None if not found
    """
    if not url:
        return None
    
    # Pattern: medicine/anything-NUMBER.html
    match = re.search(r'-(\d+)\.html', url)
    if match:
        return match.group(1)
    
    return None

# ============================================================
# STEP 4: Call Hidden API
# ============================================================
def call_availability_api(p_id):
    """
    Call dawaai.pk hidden API to get product availability
    
    Args:
        p_id: Product ID (extracted from URL)
    
    Returns:
        API response as dict, or None if request fails
    """
    try:
        # Disable SSL verification warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        response = requests.post(
            API_ENDPOINT,
            data={"p_id": p_id},
            timeout=10,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            verify=False  # Bypass SSL verification (dawaai.pk certificate expired)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️  API returned status code: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"⚠️  API request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"⚠️  API request failed: {e}")
        return None
    except json.JSONDecodeError:
        print(f"⚠️  Invalid JSON response from API")
        return None

# ============================================================
# STEP 5: Parse availability from API response
# ============================================================
def parse_availability(api_response):
    """
    Parse API response to determine availability
    
    Args:
        api_response: JSON response from API
    
    Returns:
        1 if available, 0 if out of stock, None if cannot determine
    """
    if not api_response:
        return None
    
    # Primary check: out_of_stock field
    # 0 = Available, 1 = Out of stock
    out_of_stock = api_response.get('out_of_stock')
    if out_of_stock == 0:
        return 1  # Available
    elif out_of_stock == 1:
        return 0  # Out of stock
    
    # Backup check: p_stock_status in product object
    product = api_response.get('product', {})
    stock_status = product.get('p_stock_status', '').lower()
    
    if stock_status == 'yes':
        return 1  # Available
    elif stock_status == 'no':
        return 0  # Out of stock
    
    # If we can't determine, assume out of stock
    return 0

# ============================================================
# STEP 6: Cache Management
# ============================================================
def load_cache():
    """Load cache from file"""
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_cache(cache):
    """Save cache to file"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️  Could not save cache: {e}")

def is_cache_fresh(cached_item):
    """
    Check if cached data is still fresh (< CACHE_DURATION_HOURS old)
    
    Args:
        cached_item: Cached data dict with 'last_checked' field
    
    Returns:
        True if fresh, False if stale
    """
    try:
        last_checked = datetime.fromisoformat(cached_item['last_checked'])
        age = datetime.now() - last_checked
        return age < timedelta(hours=CACHE_DURATION_HOURS)
    except (KeyError, ValueError):
        return False

# ============================================================
# MAIN FUNCTION: Check Availability
# ============================================================
def check_medicine_availability(medicine_name, use_cache=True, verbose=True):
    """
    Main function to check medicine availability on dawaai.pk
    
    Args:
        medicine_name: Name of the medicine (e.g., "Panadol", "Brufen")
        use_cache: Whether to use cached data (default: True)
        verbose: Whether to print status messages (default: True)
    
    Returns:
        1 if available
        0 if out of stock
        None if medicine not found or error occurred
    
    Example:
        >>> result = check_medicine_availability("Panadol")
        >>> if result == 1:
        >>>     print("Available!")
    """
    
    # Step 1: Load medicines
    medicines = load_medicines()
    if not medicines:
        return None
    
    # Step 2: Find medicine
    medicine = find_medicine(medicine_name, medicines)
    if not medicine:
        if verbose:
            print(f"❌ Medicine '{medicine_name}' not found in database")
        return None
    
    if verbose:
        print(f"✅ Found: {medicine['name']}")
    
    # Step 3: Check cache (if enabled)
    if use_cache:
        cache = load_cache()
        cache_key = medicine['name']
        
        if cache_key in cache and is_cache_fresh(cache[cache_key]):
            if verbose:
                age_minutes = (datetime.now() - datetime.fromisoformat(cache[cache_key]['last_checked'])).seconds // 60
                print(f"📦 Using cached data ({age_minutes} minutes old)")
            return cache[cache_key]['available']
    
    # Step 4: Extract p_id from URL
    url = medicine.get('url', '')
    if not url:
        if verbose:
            print(f"❌ No URL found for {medicine['name']}")
        return None
    
    p_id = extract_product_id(url)
    if not p_id:
        if verbose:
            print(f"❌ Could not extract product ID from URL: {url}")
        return None
    
    if verbose:
        print(f"🔍 Product ID: {p_id}")
    
    # Step 5: Call API
    if verbose:
        print(f"🌐 Calling API...")
    
    api_response = call_availability_api(p_id)
    
    if not api_response:
        if verbose:
            print(f"❌ API call failed")
        return None
    
    # Step 6: Parse availability
    availability = parse_availability(api_response)
    
    # Step 7: Update cache
    if use_cache:
        cache = load_cache()
        cache[medicine['name']] = {
            'available': availability,
            'price': api_response.get('product', {}).get('p_price', ''),
            'out_of_stock': api_response.get('out_of_stock'),
            'p_id': p_id,
            'last_checked': datetime.now().isoformat()
        }
        save_cache(cache)
    
    return availability

# ============================================================
# BATCH CHECK: Check multiple medicines
# ============================================================
def check_multiple_medicines(medicine_names, use_cache=True):
    """
    Check availability for multiple medicines
    
    Args:
        medicine_names: List of medicine names
        use_cache: Whether to use cached data
    
    Returns:
        Dict mapping medicine names to availability (1/0/None)
    
    Example:
        >>> results = check_multiple_medicines(["Panadol", "Brufen", "Disprin"])
        >>> for name, available in results.items():
        >>>     print(f"{name}: {'Available' if available == 1 else 'Out of Stock'}")
    """
    results = {}
    
    for medicine_name in medicine_names:
        print(f"\n{'='*60}")
        print(f"Checking: {medicine_name}")
        print(f"{'='*60}")
        
        availability = check_medicine_availability(medicine_name, use_cache=use_cache)
        results[medicine_name] = availability
    
    return results

# ============================================================
# USAGE EXAMPLES
# ============================================================
if __name__ == "__main__":
    print("="*70)
    print("Medicine Availability Checker - dawaai.pk")
    print("="*70)
    
    # Example 1: Check single medicine
    print("\n📋 Example 1: Single Medicine Check")
    print("-" * 70)
    
    medicine_name = "Panadol"
    result = check_medicine_availability(medicine_name)
    
    if result == 1:
        print(f"\n✅ {medicine_name} is AVAILABLE")
    elif result == 0:
        print(f"\n❌ {medicine_name} is OUT OF STOCK")
    else:
        print(f"\n⚠️  Could not check availability for {medicine_name}")
    
    # Example 2: Check multiple medicines
    print("\n\n📋 Example 2: Batch Check")
    print("-" * 70)
    
    medicines_to_check = ["Panadol", "Brufen", "Disprin"]
    results = check_multiple_medicines(medicines_to_check)
    
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    
    for name, available in results.items():
        status = "✅ Available" if available == 1 else "❌ Out of Stock" if available == 0 else "⚠️  Unknown"
        print(f"{name:30} {status}")
    
    print(f"\n{'='*70}\n")
