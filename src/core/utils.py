"""
Shared Utility Functions for MedFinder Backend

This module provides common utility functions used across all search modules:
- Medicine data loading and caching
- Composition parsing and normalization
- Price extraction and parsing

Author: MedFinder Team
Date: 2025-12-06
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional

# ============================================================
# CONFIGURATION
# ============================================================

# Get project root directory (2 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
MEDICINES_FILE = str(DATA_DIR / 'medicines.json')

# Cache for loaded medicines data
_MEDICINES_CACHE = None

# ============================================================
# MEDICINE DATA LOADING
# ============================================================

def load_medicines(use_cache=True) -> List[Dict]:
    """
    Load all medicines from medicines.json

    Args:
        use_cache: Whether to use cached data (default: True)

    Returns:
        List of medicine dictionaries
    """
    global _MEDICINES_CACHE

    # Return cached data if available
    if use_cache and _MEDICINES_CACHE is not None:
        return _MEDICINES_CACHE

    try:
        with open(MEDICINES_FILE, 'r', encoding='utf-8') as f:
            medicines = json.load(f)

        # Cache the data
        if use_cache:
            _MEDICINES_CACHE = medicines

        return medicines

    except FileNotFoundError:
        print(f"Error: {MEDICINES_FILE} not found")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {MEDICINES_FILE}")
        return []


def clear_cache():
    """Clear the medicines cache (useful for testing)"""
    global _MEDICINES_CACHE
    _MEDICINES_CACHE = None


# ============================================================
# COMPOSITION PARSING & NORMALIZATION
# ============================================================

def normalize_composition(composition: str) -> str:
    """
    Normalize composition string for consistent matching

    Handles:
    - Case normalization (lowercase)
    - Whitespace trimming
    - Extra spaces removal

    Args:
        composition: Raw composition string (e.g., "Paracetamol (500mg)")

    Returns:
        Normalized composition string

    Examples:
        >>> normalize_composition("Paracetamol (500mg)")
        "paracetamol (500mg)"

        >>> normalize_composition("  DICLOFENAC   SODIUM  (75mg)  ")
        "diclofenac sodium (75mg)"
    """
    if not composition:
        return ""

    # Convert to lowercase
    normalized = composition.lower()

    # Remove extra whitespace
    normalized = ' '.join(normalized.split())

    return normalized.strip()


def extract_active_ingredient(composition: str) -> str:
    """
    Extract the active ingredient name (without dosage)

    Args:
        composition: Full composition string (e.g., "Paracetamol (500mg)")

    Returns:
        Active ingredient name without dosage

    Examples:
        >>> extract_active_ingredient("Paracetamol (500mg)")
        "paracetamol"

        >>> extract_active_ingredient("Diclofenac Sodium (75mg)")
        "diclofenac sodium"

        >>> extract_active_ingredient("Paracetamol")
        "paracetamol"
    """
    if not composition:
        return ""

    # Normalize first
    normalized = normalize_composition(composition)

    # Remove content in parentheses (dosage information)
    # Pattern: Remove (anything) or [anything]
    ingredient = re.sub(r'\([^)]*\)|\[[^\]]*\]', '', normalized)

    # Remove extra whitespace
    ingredient = ' '.join(ingredient.split())

    return ingredient.strip()


def extract_dosage(composition: str) -> Optional[str]:
    """
    Extract dosage from composition string

    Args:
        composition: Full composition string (e.g., "Paracetamol (500mg)")

    Returns:
        Dosage string or None if not found

    Examples:
        >>> extract_dosage("Paracetamol (500mg)")
        "500mg"

        >>> extract_dosage("Diclofenac Sodium (75mg)")
        "75mg"

        >>> extract_dosage("Paracetamol")
        None
    """
    if not composition:
        return None

    # Pattern: Extract content inside parentheses
    match = re.search(r'\(([^)]+)\)', composition)
    if match:
        return match.group(1).strip()

    return None


def compositions_match(comp1: str, comp2: str, exact=True) -> bool:
    """
    Check if two compositions match

    Args:
        comp1: First composition string
        comp2: Second composition string
        exact: If True, requires exact match including dosage
               If False, only matches active ingredient

    Returns:
        True if compositions match, False otherwise

    Examples:
        >>> compositions_match("Paracetamol (500mg)", "Paracetamol (500mg)", exact=True)
        True

        >>> compositions_match("Paracetamol (500mg)", "Paracetamol (120mg)", exact=True)
        False

        >>> compositions_match("Paracetamol (500mg)", "Paracetamol (120mg)", exact=False)
        True
    """
    if exact:
        # Exact match including dosage
        return normalize_composition(comp1) == normalize_composition(comp2)
    else:
        # Match only active ingredient
        return extract_active_ingredient(comp1) == extract_active_ingredient(comp2)


# ============================================================
# PRICE PARSING
# ============================================================

def parse_price(price_str: str) -> Optional[float]:
    """
    Extract numeric price value from price string

    Handles formats:
    - "Rs. 6.75/tablet"
    - "Rs.63.21/suspension"
    - "Rs. 100"

    Args:
        price_str: Price string from medicines.json

    Returns:
        Numeric price value or None if parsing fails

    Examples:
        >>> parse_price("Rs. 6.75/tablet")
        6.75

        >>> parse_price("Rs.63.21/suspension")
        63.21

        >>> parse_price("N/A")
        None
    """
    if not price_str:
        return None

    try:
        # Remove "Rs." and everything after "/"
        # Pattern: Extract numbers (with decimal point)
        match = re.search(r'(\d+\.?\d*)', price_str)
        if match:
            return float(match.group(1))
    except (ValueError, AttributeError):
        pass

    return None


def format_price(price: float, unit: str = "tablet") -> str:
    """
    Format price value as display string

    Args:
        price: Numeric price value
        unit: Unit type (tablet, suspension, etc.)

    Returns:
        Formatted price string

    Examples:
        >>> format_price(6.75, "tablet")
        "Rs. 6.75/tablet"

        >>> format_price(63.21, "suspension")
        "Rs. 63.21/suspension"
    """
    return f"Rs. {price:.2f}/{unit}"


def get_price_unit(price_str: str) -> str:
    """
    Extract price unit from price string

    Args:
        price_str: Price string (e.g., "Rs. 6.75/tablet")

    Returns:
        Unit string or "unit" if not found

    Examples:
        >>> get_price_unit("Rs. 6.75/tablet")
        "tablet"

        >>> get_price_unit("Rs.63.21/suspension")
        "suspension"

        >>> get_price_unit("Rs. 100")
        "unit"
    """
    if not price_str:
        return "unit"

    # Extract text after "/"
    match = re.search(r'/(\w+)', price_str)
    if match:
        return match.group(1)

    return "unit"


# ============================================================
# SORTING HELPERS
# ============================================================

def sort_by_price(medicines: List[Dict], ascending=True) -> List[Dict]:
    """
    Sort medicines by price

    Args:
        medicines: List of medicine dictionaries
        ascending: If True, sort cheapest first (default)

    Returns:
        Sorted list of medicines
    """
    def get_price_key(med):
        price = parse_price(med.get('price', ''))
        # Put medicines without price at the end
        if price is None:
            return float('inf') if ascending else float('-inf')
        return price

    return sorted(medicines, key=get_price_key, reverse=not ascending)


def calculate_savings(original_price: float, alternative_price: float) -> float:
    """
    Calculate percentage savings

    Args:
        original_price: Original medicine price
        alternative_price: Alternative medicine price

    Returns:
        Percentage savings (0-100)

    Examples:
        >>> calculate_savings(10.0, 2.5)
        75.0

        >>> calculate_savings(10.0, 10.0)
        0.0
    """
    if original_price <= 0:
        return 0.0

    savings = ((original_price - alternative_price) / original_price) * 100
    return max(0.0, savings)  # Ensure non-negative


# ============================================================
# STRING MATCHING HELPERS
# ============================================================

def contains_ignore_case(text: str, search: str) -> bool:
    """
    Case-insensitive substring matching

    Args:
        text: Text to search in
        search: Search string

    Returns:
        True if search string is found in text (case-insensitive)
    """
    if not text or not search:
        return False

    return search.lower() in text.lower()


def starts_with_ignore_case(text: str, prefix: str) -> bool:
    """
    Case-insensitive prefix matching

    Args:
        text: Text to check
        prefix: Prefix to match

    Returns:
        True if text starts with prefix (case-insensitive)
    """
    if not text or not prefix:
        return False

    return text.lower().startswith(prefix.lower())


# ============================================================
# VALIDATION
# ============================================================

def validate_medicine(medicine: Dict) -> bool:
    """
    Validate that a medicine dictionary has required fields

    Args:
        medicine: Medicine dictionary

    Returns:
        True if valid, False otherwise
    """
    required_fields = ['name', 'brand', 'composition', 'price']
    return all(field in medicine and medicine[field] for field in required_fields)


# ============================================================
# USAGE EXAMPLE
# ============================================================

if __name__ == "__main__":
    # Test utilities
    print("="*70)
    print("MedFinder Utilities - Test Suite")
    print("="*70)

    # Test 1: Load medicines
    print("\n[TEST 1] Loading medicines...")
    medicines = load_medicines()
    print(f"Loaded {len(medicines)} medicines")

    # Test 2: Composition parsing
    print("\n[TEST 2] Composition parsing...")
    test_comp = "Paracetamol (500mg)"
    print(f"Original: {test_comp}")
    print(f"Normalized: {normalize_composition(test_comp)}")
    print(f"Active ingredient: {extract_active_ingredient(test_comp)}")
    print(f"Dosage: {extract_dosage(test_comp)}")

    # Test 3: Price parsing
    print("\n[TEST 3] Price parsing...")
    test_price = "Rs. 6.75/tablet"
    print(f"Price string: {test_price}")
    print(f"Numeric value: {parse_price(test_price)}")
    print(f"Unit: {get_price_unit(test_price)}")

    # Test 4: Composition matching
    print("\n[TEST 4] Composition matching...")
    comp1 = "Paracetamol (500mg)"
    comp2 = "Paracetamol (120mg)"
    print(f"Comp 1: {comp1}")
    print(f"Comp 2: {comp2}")
    print(f"Exact match: {compositions_match(comp1, comp2, exact=True)}")
    print(f"Ingredient match: {compositions_match(comp1, comp2, exact=False)}")

    # Test 5: Savings calculation
    print("\n[TEST 5] Savings calculation...")
    original = 10.0
    alternative = 2.5
    savings = calculate_savings(original, alternative)
    print(f"Original price: Rs. {original}")
    print(f"Alternative price: Rs. {alternative}")
    print(f"Savings: {savings:.1f}%")

    print("\n" + "="*70)
    print("All tests completed!")
    print("="*70)
