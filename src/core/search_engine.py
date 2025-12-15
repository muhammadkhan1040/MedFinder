"""
Formula-Based Search Engine for MedFinder

This module enables doctors to search for medicines by chemical formula/composition
instead of brand names. Results are sorted by price (cheapest first) to help patients
find affordable alternatives.

Key Features:
- Search by active ingredient (e.g., "Paracetamol")
- Search by exact composition (e.g., "Paracetamol (500mg)")
- Sort results by price (ascending)
- Filter by dosage strength
- Group by brand

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
    extract_active_ingredient,
    extract_dosage,
    parse_price,
    sort_by_price,
    contains_ignore_case
)
from typing import List, Dict, Optional

# ============================================================
# CORE SEARCH FUNCTIONS
# ============================================================

def search_by_composition(formula: str,
                         exact_match: bool = False,
                         dosage_filter: Optional[str] = None,
                         max_results: Optional[int] = None) -> List[Dict]:
    """
    Search medicines by chemical composition/formula

    Args:
        formula: Chemical formula to search (e.g., "Paracetamol" or "Paracetamol (500mg)")
        exact_match: If True, matches exact composition including dosage
                     If False, matches active ingredient only (default)
        dosage_filter: Optional dosage filter (e.g., "500mg")
        max_results: Maximum number of results to return (default: all)

    Returns:
        List of medicines matching the formula, sorted by price (cheapest first)

    Examples:
        >>> # Find all Paracetamol medicines
        >>> results = search_by_composition("Paracetamol")

        >>> # Find only Paracetamol 500mg
        >>> results = search_by_composition("Paracetamol", dosage_filter="500mg")

        >>> # Exact composition match
        >>> results = search_by_composition("Paracetamol (500mg)", exact_match=True)
    """
    medicines = load_medicines()
    results = []

    # Normalize search formula
    search_formula = normalize_composition(formula)
    search_ingredient = extract_active_ingredient(formula)

    for medicine in medicines:
        composition = medicine.get('composition', '')
        if not composition:
            continue

        # Check if composition matches
        matched = False

        if exact_match:
            # Exact match including dosage
            if normalize_composition(composition) == search_formula:
                matched = True
        else:
            # Match active ingredient
            ingredient = extract_active_ingredient(composition)
            if search_ingredient in ingredient or ingredient in search_ingredient:
                matched = True

        # Apply dosage filter if specified
        if matched and dosage_filter:
            dosage = extract_dosage(composition)
            if not dosage or dosage_filter.lower() not in dosage.lower():
                matched = False

        if matched:
            results.append(medicine)

    # Sort by price (cheapest first)
    results = sort_by_price(results, ascending=True)

    # Limit results if specified
    if max_results:
        results = results[:max_results]

    return results


def search_by_ingredient(ingredient: str,
                        max_results: Optional[int] = None) -> List[Dict]:
    """
    Search medicines by active ingredient name (without dosage)

    This is a convenience wrapper around search_by_composition with exact_match=False

    Args:
        ingredient: Active ingredient name (e.g., "Paracetamol", "Diclofenac")
        max_results: Maximum number of results to return

    Returns:
        List of medicines containing the ingredient, sorted by price

    Examples:
        >>> results = search_by_ingredient("Paracetamol")
        >>> results = search_by_ingredient("Diclofenac Sodium")
    """
    return search_by_composition(ingredient, exact_match=False, max_results=max_results)


def get_available_dosages(ingredient: str) -> List[str]:
    """
    Get all available dosages for a given ingredient

    Args:
        ingredient: Active ingredient name

    Returns:
        List of available dosages (e.g., ["500mg", "120mg", "75mg"])

    Examples:
        >>> dosages = get_available_dosages("Paracetamol")
        >>> # Returns: ["500mg", "120mg", "250mg", ...]
    """
    medicines = search_by_ingredient(ingredient)
    dosages = set()

    for medicine in medicines:
        dosage = extract_dosage(medicine.get('composition', ''))
        if dosage:
            dosages.add(dosage)

    return sorted(list(dosages))


def group_by_brand(medicines: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group medicines by brand name

    Args:
        medicines: List of medicine dictionaries

    Returns:
        Dictionary mapping brand names to list of medicines

    Examples:
        >>> results = search_by_ingredient("Paracetamol")
        >>> by_brand = group_by_brand(results)
        >>> # Returns: {"GlaxoSmithKline": [...], "Abbott": [...], ...}
    """
    grouped = {}

    for medicine in medicines:
        brand = medicine.get('brand', 'Unknown')
        if brand not in grouped:
            grouped[brand] = []
        grouped[brand].append(medicine)

    return grouped


# ============================================================
# ADVANCED SEARCH
# ============================================================

def search_by_category(category: str,
                      formula_filter: Optional[str] = None,
                      max_results: Optional[int] = None) -> List[Dict]:
    """
    Search medicines by category, optionally filtered by formula

    Args:
        category: Category name (e.g., "Pain", "Arthritis")
        formula_filter: Optional formula to filter results
        max_results: Maximum number of results

    Returns:
        List of medicines in the category, sorted by price

    Examples:
        >>> # All pain medicines
        >>> results = search_by_category("Pain")

        >>> # Paracetamol pain medicines
        >>> results = search_by_category("Pain", formula_filter="Paracetamol")
    """
    medicines = load_medicines()
    results = []

    for medicine in medicines:
        categories = medicine.get('categories', [])
        if not categories:
            continue

        # Check if any category matches
        if any(contains_ignore_case(cat, category) for cat in categories):
            # Apply formula filter if specified
            if formula_filter:
                composition = medicine.get('composition', '')
                ingredient = extract_active_ingredient(composition)
                search_ingredient = extract_active_ingredient(formula_filter)

                if search_ingredient not in ingredient:
                    continue

            results.append(medicine)

    # Sort by price
    results = sort_by_price(results, ascending=True)

    if max_results:
        results = results[:max_results]

    return results


def search_by_brand(brand: str,
                   formula_filter: Optional[str] = None,
                   max_results: Optional[int] = None) -> List[Dict]:
    """
    Search medicines by brand name

    Args:
        brand: Brand name (e.g., "GlaxoSmithKline", "Abbott")
        formula_filter: Optional formula to filter results
        max_results: Maximum number of results

    Returns:
        List of medicines from the brand, sorted by price

    Examples:
        >>> # All GlaxoSmithKline medicines
        >>> results = search_by_brand("GlaxoSmithKline")

        >>> # GlaxoSmithKline Paracetamol medicines
        >>> results = search_by_brand("GlaxoSmithKline", formula_filter="Paracetamol")
    """
    medicines = load_medicines()
    results = []

    for medicine in medicines:
        med_brand = medicine.get('brand', '')
        if not med_brand:
            continue

        # Check if brand matches
        if contains_ignore_case(med_brand, brand):
            # Apply formula filter if specified
            if formula_filter:
                composition = medicine.get('composition', '')
                ingredient = extract_active_ingredient(composition)
                search_ingredient = extract_active_ingredient(formula_filter)

                if search_ingredient not in ingredient:
                    continue

            results.append(medicine)

    # Sort by price
    results = sort_by_price(results, ascending=True)

    if max_results:
        results = results[:max_results]

    return results


# ============================================================
# STATISTICS & ANALYTICS
# ============================================================

def get_price_range(medicines: List[Dict]) -> Dict[str, float]:
    """
    Get price statistics for a list of medicines

    Args:
        medicines: List of medicine dictionaries

    Returns:
        Dictionary with min, max, and average prices

    Examples:
        >>> results = search_by_ingredient("Paracetamol")
        >>> stats = get_price_range(results)
        >>> # Returns: {"min": 0.24, "max": 0.99, "avg": 0.55}
    """
    prices = []
    for medicine in medicines:
        price = parse_price(medicine.get('price', ''))
        if price is not None:
            prices.append(price)

    if not prices:
        return {"min": 0.0, "max": 0.0, "avg": 0.0}

    return {
        "min": min(prices),
        "max": max(prices),
        "avg": sum(prices) / len(prices)
    }


def get_brand_count(medicines: List[Dict]) -> int:
    """
    Count unique brands in medicine list

    Args:
        medicines: List of medicine dictionaries

    Returns:
        Number of unique brands
    """
    brands = set(med.get('brand', '') for med in medicines)
    return len(brands)


# ============================================================
# DISPLAY HELPERS
# ============================================================

def format_search_result(medicine: Dict, index: int = 1) -> str:
    """
    Format a single medicine as a display string

    Args:
        medicine: Medicine dictionary
        index: Result number (for display)

    Returns:
        Formatted string for display

    Examples:
        >>> result = search_by_ingredient("Paracetamol")[0]
        >>> print(format_search_result(result, 1))
        1. Anapyrin 500mg tablet - Specific - Rs. 0.24/tablet
           Composition: Paracetamol (500mg)
    """
    name = medicine.get('name', 'Unknown')
    brand = medicine.get('brand', 'Unknown')
    price = medicine.get('price', 'N/A')
    composition = medicine.get('composition', 'N/A')

    return f"{index}. {name}\n   Brand: {brand} | Price: {price}\n   Composition: {composition}"


def display_search_results(medicines: List[Dict],
                          show_composition: bool = True,
                          max_display: int = 10):
    """
    Display search results in a formatted way

    Args:
        medicines: List of medicine dictionaries
        show_composition: Whether to show composition (default: True)
        max_display: Maximum results to display (default: 10)
    """
    if not medicines:
        print("No medicines found.")
        return

    print(f"\nFound {len(medicines)} medicine(s)")
    print("="*70)

    # Display results
    for i, medicine in enumerate(medicines[:max_display], 1):
        name = medicine.get('name', 'Unknown')
        brand = medicine.get('brand', 'Unknown')
        price = medicine.get('price', 'N/A')
        composition = medicine.get('composition', 'N/A')

        print(f"{i}. {name[:50]}")
        print(f"   Brand: {brand[:30]:30} | Price: {price}")
        if show_composition:
            print(f"   Composition: {composition}")
        print()

    # Show if there are more results
    if len(medicines) > max_display:
        print(f"... and {len(medicines) - max_display} more results")

    # Show price statistics
    stats = get_price_range(medicines)
    brands = get_brand_count(medicines)
    print("="*70)
    print(f"Price Range: Rs. {stats['min']:.2f} - Rs. {stats['max']:.2f}")
    print(f"Average Price: Rs. {stats['avg']:.2f}")
    print(f"Unique Brands: {brands}")
    print("="*70)


# ============================================================
# USAGE EXAMPLES
# ============================================================

if __name__ == "__main__":
    print("="*70)
    print("MedFinder Formula-Based Search Engine")
    print("="*70)

    # Example 1: Search by ingredient
    print("\n[Example 1] Search all Paracetamol medicines")
    print("-" * 70)
    results = search_by_ingredient("Paracetamol", max_results=10)
    display_search_results(results)

    # Example 2: Search specific dosage
    print("\n[Example 2] Search Paracetamol 500mg only")
    print("-" * 70)
    results = search_by_composition("Paracetamol", dosage_filter="500mg", max_results=10)
    display_search_results(results)

    # Example 3: Get available dosages
    print("\n[Example 3] Available Paracetamol dosages")
    print("-" * 70)
    dosages = get_available_dosages("Paracetamol")
    print(f"Available dosages: {', '.join(dosages[:10])}")
    if len(dosages) > 10:
        print(f"... and {len(dosages) - 10} more")

    # Example 4: Search by brand
    print("\n[Example 4] GlaxoSmithKline Paracetamol medicines")
    print("-" * 70)
    results = search_by_brand("GlaxoSmithKline", formula_filter="Paracetamol", max_results=5)
    display_search_results(results)

    # Example 5: Group by brand
    print("\n[Example 5] Top 5 brands for Paracetamol 500mg")
    print("-" * 70)
    results = search_by_composition("Paracetamol", dosage_filter="500mg")
    by_brand = group_by_brand(results)
    top_brands = sorted(by_brand.items(), key=lambda x: len(x[1]), reverse=True)[:5]

    for brand, medicines in top_brands:
        cheapest_price = parse_price(sort_by_price(medicines)[0].get('price', ''))
        print(f"{brand:30} - {len(medicines):3} medicines (from Rs. {cheapest_price:.2f})")

    print("\n" + "="*70)
