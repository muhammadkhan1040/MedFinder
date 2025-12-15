"""
Similar Medicine Recommendation Engine for MedFinder

This module finds alternative medicines (generics/other brands) with the same
pharmaceutical composition. Helps doctors prescribe affordable alternatives
when a specific brand is out of stock or too expensive.

Based on pharmaceutical equivalence standards:
- Exact active ingredient match
- Same dosage/strength
- Different brand/manufacturer

Author: MedFinder Team
Date: 2025-12-06
"""

import sys
from pathlib import Path

# Add src/core to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    load_medicines,
    normalize_composition,
    parse_price,
    sort_by_price,
    calculate_savings,
    contains_ignore_case
)
from typing import List, Dict, Optional, Tuple

# ============================================================
# CORE SIMILARITY FUNCTIONS
# ============================================================

def find_medicine_by_name(medicine_name: str) -> Optional[Dict]:
    """
    Find a medicine by name (case-insensitive, partial match)

    Args:
        medicine_name: Medicine name to search for

    Returns:
        Medicine dictionary or None if not found

    Examples:
        >>> med = find_medicine_by_name("Panadol")
        >>> med = find_medicine_by_name("Panadol CF")
    """
    medicines = load_medicines()
    search_name = medicine_name.lower().strip()

    # Try exact match first
    for medicine in medicines:
        if medicine.get('name', '').lower() == search_name:
            return medicine

    # Try partial match (contains)
    for medicine in medicines:
        if search_name in medicine.get('name', '').lower():
            return medicine

    return None


def get_similar_medicines(medicine_name: str,
                         exclude_same_brand: bool = True,
                         max_results: Optional[int] = None) -> List[Dict]:
    """
    Find similar medicines with the same composition as the input medicine

    This is the main function for finding pharmaceutical alternatives/generics.

    Args:
        medicine_name: Name of the reference medicine
        exclude_same_brand: If True, excludes medicines from the same brand (default)
        max_results: Maximum number of alternatives to return

    Returns:
        List of similar medicines sorted by price (cheapest first)

    Examples:
        >>> # Find alternatives to Panadol
        >>> alternatives = get_similar_medicines("Panadol")

        >>> # Include same brand medicines
        >>> all_similar = get_similar_medicines("Panadol", exclude_same_brand=False)
    """
    # Find the reference medicine
    reference = find_medicine_by_name(medicine_name)
    if not reference:
        return []

    # Get reference composition and brand
    ref_composition = normalize_composition(reference.get('composition', ''))
    ref_brand = reference.get('brand', '').lower()

    if not ref_composition:
        return []

    # Find all medicines with the same composition
    medicines = load_medicines()
    similar = []

    for medicine in medicines:
        composition = normalize_composition(medicine.get('composition', ''))

        # Check exact composition match
        if composition == ref_composition:
            # Exclude the reference medicine itself
            if medicine.get('name', '') == reference.get('name', ''):
                continue

            # Exclude same brand if specified
            if exclude_same_brand:
                brand = medicine.get('brand', '').lower()
                if brand == ref_brand:
                    continue

            similar.append(medicine)

    # Sort by price (cheapest first)
    similar = sort_by_price(similar, ascending=True)

    # Limit results if specified
    if max_results:
        similar = similar[:max_results]

    return similar


def get_alternatives_with_savings(medicine_name: str,
                                  max_results: Optional[int] = None) -> List[Tuple[Dict, float]]:
    """
    Get similar medicines with calculated savings percentage

    Args:
        medicine_name: Name of the reference medicine
        max_results: Maximum number of alternatives

    Returns:
        List of tuples: (medicine_dict, savings_percentage)
        Sorted by savings (highest savings first)

    Examples:
        >>> alternatives = get_alternatives_with_savings("Panadol")
        >>> for alt, savings in alternatives[:5]:
        >>>     print(f"{alt['name']} - Save {savings:.1f}%")
    """
    # Find reference medicine
    reference = find_medicine_by_name(medicine_name)
    if not reference:
        return []

    ref_price = parse_price(reference.get('price', ''))
    if ref_price is None:
        return []

    # Get similar medicines
    similar = get_similar_medicines(medicine_name, exclude_same_brand=True)

    # Calculate savings for each
    with_savings = []
    for medicine in similar:
        alt_price = parse_price(medicine.get('price', ''))
        if alt_price is not None:
            savings = calculate_savings(ref_price, alt_price)
            with_savings.append((medicine, savings))

    # Sort by savings (highest first)
    with_savings.sort(key=lambda x: x[1], reverse=True)

    if max_results:
        with_savings = with_savings[:max_results]

    return with_savings


def find_cheapest_alternative(medicine_name: str) -> Optional[Dict]:
    """
    Find the cheapest alternative to a given medicine

    Args:
        medicine_name: Name of the reference medicine

    Returns:
        Cheapest alternative medicine or None if no alternatives found

    Examples:
        >>> cheapest = find_cheapest_alternative("Panadol")
        >>> if cheapest:
        >>>     print(f"Cheapest: {cheapest['name']} - {cheapest['price']}")
    """
    similar = get_similar_medicines(medicine_name, exclude_same_brand=True, max_results=1)

    if similar:
        return similar[0]  # Already sorted by price
    return None


def compare_medicines(medicine1_name: str, medicine2_name: str) -> Dict:
    """
    Compare two medicines for pharmaceutical equivalence

    Args:
        medicine1_name: First medicine name
        medicine2_name: Second medicine name

    Returns:
        Comparison dictionary with keys:
        - equivalent: bool (same composition)
        - composition1: str
        - composition2: str
        - price_difference: float
        - cheaper: str (name of cheaper medicine)

    Examples:
        >>> comparison = compare_medicines("Panadol", "Anapyrin")
        >>> if comparison['equivalent']:
        >>>     print(f"These medicines are equivalent!")
    """
    med1 = find_medicine_by_name(medicine1_name)
    med2 = find_medicine_by_name(medicine2_name)

    result = {
        'equivalent': False,
        'composition1': None,
        'composition2': None,
        'price_difference': None,
        'cheaper': None
    }

    if not med1 or not med2:
        return result

    comp1 = normalize_composition(med1.get('composition', ''))
    comp2 = normalize_composition(med2.get('composition', ''))

    result['composition1'] = med1.get('composition')
    result['composition2'] = med2.get('composition')
    result['equivalent'] = (comp1 == comp2)

    # Compare prices
    price1 = parse_price(med1.get('price', ''))
    price2 = parse_price(med2.get('price', ''))

    if price1 is not None and price2 is not None:
        result['price_difference'] = abs(price1 - price2)
        result['cheaper'] = med1.get('name') if price1 < price2 else med2.get('name')

    return result


# ============================================================
# ADVANCED RECOMMENDATIONS
# ============================================================

def get_alternatives_by_price_range(medicine_name: str,
                                   max_price: Optional[float] = None,
                                   min_price: Optional[float] = None) -> List[Dict]:
    """
    Get similar medicines within a specific price range

    Args:
        medicine_name: Reference medicine name
        max_price: Maximum price (optional)
        min_price: Minimum price (optional)

    Returns:
        List of similar medicines within price range

    Examples:
        >>> # Alternatives under Rs. 1
        >>> cheap = get_alternatives_by_price_range("Panadol", max_price=1.0)

        >>> # Mid-range alternatives (Rs. 0.5 - Rs. 1.0)
        >>> mid = get_alternatives_by_price_range("Panadol", min_price=0.5, max_price=1.0)
    """
    similar = get_similar_medicines(medicine_name, exclude_same_brand=True)
    filtered = []

    for medicine in similar:
        price = parse_price(medicine.get('price', ''))
        if price is None:
            continue

        # Apply price filters
        if max_price is not None and price > max_price:
            continue
        if min_price is not None and price < min_price:
            continue

        filtered.append(medicine)

    return filtered


def get_brand_alternatives(medicine_name: str,
                          preferred_brands: List[str] = None) -> Dict[str, List[Dict]]:
    """
    Get alternatives grouped by brand, optionally filtered by preferred brands

    Args:
        medicine_name: Reference medicine name
        preferred_brands: List of preferred brand names (optional)

    Returns:
        Dictionary mapping brand names to list of medicines

    Examples:
        >>> # All brands
        >>> by_brand = get_brand_alternatives("Panadol")

        >>> # Only specific brands
        >>> trusted = get_brand_alternatives("Panadol",
        ...     preferred_brands=["Abbott", "GlaxoSmithKline"])
    """
    similar = get_similar_medicines(medicine_name, exclude_same_brand=True)
    grouped = {}

    for medicine in similar:
        brand = medicine.get('brand', 'Unknown')

        # Filter by preferred brands if specified
        if preferred_brands:
            if not any(contains_ignore_case(brand, pref) for pref in preferred_brands):
                continue

        if brand not in grouped:
            grouped[brand] = []
        grouped[brand].append(medicine)

    # Sort each brand's medicines by price
    for brand in grouped:
        grouped[brand] = sort_by_price(grouped[brand], ascending=True)

    return grouped


# ============================================================
# DISPLAY HELPERS
# ============================================================

def display_similar_medicines(medicine_name: str, max_display: int = 10):
    """
    Display similar medicines in a formatted comparison

    Args:
        medicine_name: Reference medicine name
        max_display: Maximum alternatives to display
    """
    # Find reference medicine
    reference = find_medicine_by_name(medicine_name)
    if not reference:
        print(f"Medicine '{medicine_name}' not found.")
        return

    # Get alternatives with savings
    alternatives = get_alternatives_with_savings(medicine_name, max_results=max_display)

    if not alternatives:
        print(f"\nNo alternatives found for {reference.get('name')}")
        print("This may be the only brand available for this composition.")
        return

    # Display reference medicine
    print("\n" + "="*70)
    print("CURRENT SELECTION")
    print("="*70)
    print(f"Medicine: {reference.get('name')}")
    print(f"Brand: {reference.get('brand')}")
    print(f"Composition: {reference.get('composition')}")
    print(f"Price: {reference.get('price')}")

    # Display alternatives
    print("\n" + "="*70)
    print(f"SIMILAR MEDICINES ({len(alternatives)} alternatives found)")
    print("="*70)

    for i, (medicine, savings) in enumerate(alternatives, 1):
        name = medicine.get('name', 'Unknown')
        brand = medicine.get('brand', 'Unknown')
        price = medicine.get('price', 'N/A')

        print(f"\n{i}. {name[:50]}")
        print(f"   Brand: {brand[:30]:30} | Price: {price}")
        if savings > 0:
            print(f"   Savings: {savings:.1f}% cheaper!")
        elif savings < 0:
            print(f"   Note: {abs(savings):.1f}% more expensive")

    print("\n" + "="*70)
    print(f"Showing top {len(alternatives)} alternatives sorted by savings")
    print("="*70)


def display_comparison(medicine1_name: str, medicine2_name: str):
    """
    Display a comparison between two medicines

    Args:
        medicine1_name: First medicine name
        medicine2_name: Second medicine name
    """
    comparison = compare_medicines(medicine1_name, medicine2_name)

    print("\n" + "="*70)
    print("MEDICINE COMPARISON")
    print("="*70)

    print(f"\nMedicine 1: {medicine1_name}")
    print(f"Composition: {comparison['composition1']}")

    print(f"\nMedicine 2: {medicine2_name}")
    print(f"Composition: {comparison['composition2']}")

    print("\n" + "-"*70)
    if comparison['equivalent']:
        print("✓ These medicines are PHARMACEUTICALLY EQUIVALENT")
        print("  (Same active ingredient and dosage)")
        if comparison['price_difference']:
            print(f"\nPrice difference: Rs. {comparison['price_difference']:.2f}")
            print(f"Cheaper option: {comparison['cheaper']}")
    else:
        print("✗ These medicines are NOT equivalent")
        print("  (Different composition - cannot substitute)")
    print("="*70)


# ============================================================
# USAGE EXAMPLES
# ============================================================

if __name__ == "__main__":
    print("="*70)
    print("MedFinder Similar Medicine Recommendation Engine")
    print("="*70)

    # Example 1: Find alternatives to Panadol
    print("\n[Example 1] Alternatives to Panadol CF")
    print("-" * 70)
    display_similar_medicines("Panadol CF", max_display=5)

    # Example 2: Find cheapest alternative
    print("\n[Example 2] Cheapest alternative to Panadol")
    print("-" * 70)
    cheapest = find_cheapest_alternative("Panadol")
    if cheapest:
        print(f"Cheapest: {cheapest.get('name')}")
        print(f"Brand: {cheapest.get('brand')}")
        print(f"Price: {cheapest.get('price')}")

    # Example 3: Compare two medicines
    print("\n[Example 3] Compare Panadol vs Anapyrin")
    print("-" * 70)
    display_comparison("Panadol", "Anapyrin")

    # Example 4: Alternatives by price range
    print("\n[Example 4] Panadol alternatives under Rs. 1")
    print("-" * 70)
    cheap = get_alternatives_by_price_range("Panadol", max_price=1.0)
    print(f"Found {len(cheap)} alternatives under Rs. 1")
    for i, med in enumerate(cheap[:5], 1):
        print(f"{i}. {med.get('name')[:40]:40} - {med.get('price')}")

    # Example 5: Group by brand
    print("\n[Example 5] Top brands offering Paracetamol alternatives")
    print("-" * 70)
    by_brand = get_brand_alternatives("Panadol")
    top_brands = sorted(by_brand.items(), key=lambda x: len(x[1]), reverse=True)[:5]

    for brand, medicines in top_brands:
        cheapest_price = parse_price(sort_by_price(medicines)[0].get('price', ''))
        print(f"{brand:30} - {len(medicines):2} options (from Rs. {cheapest_price:.2f})")

    print("\n" + "="*70)
