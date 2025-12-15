"""
Enhanced Search Module for MedFinder

Provides advanced search capabilities with typo tolerance and autocomplete:
- Autocomplete: Real-time suggestions as user types
- Fuzzy Search: Finds matches even with spelling mistakes
- Multi-field Search: Search across medicine name, brand, composition, categories

Based on pharmaceutical database best practices (DrugBank, Clinical Tables).

Author: MedFinder Team
Date: 2025-12-06
"""

import sys
from pathlib import Path
from difflib import get_close_matches
import re

# Add src/core to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    load_medicines,
    normalize_composition,
    extract_active_ingredient,
    contains_ignore_case,
    starts_with_ignore_case,
    sort_by_price
)
from typing import List, Dict, Optional, Tuple

# ============================================================
# AUTOCOMPLETE
# ============================================================

def autocomplete_medicine(partial_name: str,
                         max_suggestions: int = 10,
                         search_fields: List[str] = None) -> List[str]:
    """
    Get medicine name suggestions based on partial input

    Uses intelligent ranking:
    1. Exact prefix match (highest priority)
    2. Word starts with prefix
    3. Contains prefix (lowest priority)

    Args:
        partial_name: Partial medicine name (e.g., "pana")
        max_suggestions: Maximum number of suggestions (default: 10)
        search_fields: Fields to search in (default: ['name', 'brand', 'composition'])

    Returns:
        List of suggested medicine names

    Examples:
        >>> suggestions = autocomplete_medicine("pana")
        >>> # Returns: ["Panadol CF", "Panadol Extra", "Panamol", ...]

        >>> suggestions = autocomplete_medicine("para", max_suggestions=5)
    """
    if not partial_name or len(partial_name) < 2:
        return []

    medicines = load_medicines()
    search_term = partial_name.lower().strip()

    if search_fields is None:
        search_fields = ['name']

    suggestions = []
    seen = set()  # Avoid duplicates

    # Score each medicine for ranking
    scored_suggestions = []

    for medicine in medicines:
        for field in search_fields:
            value = medicine.get(field, '')
            if not value:
                continue

            # Handle list fields (like categories)
            if isinstance(value, list):
                value = ' '.join(value)

            value_lower = value.lower()
            medicine_name = medicine.get('name', '')

            # Skip if already suggested
            if medicine_name in seen:
                continue

            # Rank by match quality
            score = 0

            # 1. Exact prefix match (highest score)
            if value_lower.startswith(search_term):
                score = 3
            # 2. Word starts with prefix
            elif any(word.startswith(search_term) for word in value_lower.split()):
                score = 2
            # 3. Contains prefix
            elif search_term in value_lower:
                score = 1

            if score > 0:
                scored_suggestions.append((medicine_name, score))
                seen.add(medicine_name)

    # Sort by score (descending) then alphabetically
    scored_suggestions.sort(key=lambda x: (-x[1], x[0]))

    # Extract names and limit
    suggestions = [name for name, score in scored_suggestions[:max_suggestions]]

    return suggestions


def autocomplete_brand(partial_brand: str, max_suggestions: int = 10) -> List[str]:
    """
    Get brand name suggestions

    Args:
        partial_brand: Partial brand name (e.g., "Gla")
        max_suggestions: Maximum suggestions

    Returns:
        List of brand names

    Examples:
        >>> brands = autocomplete_brand("Gla")
        >>> # Returns: ["GlaxoSmithKline", ...]
    """
    if not partial_brand or len(partial_brand) < 2:
        return []

    medicines = load_medicines()
    search_term = partial_brand.lower().strip()

    brands = set()
    for medicine in medicines:
        brand = medicine.get('brand', '')
        if brand and search_term in brand.lower():
            brands.add(brand)

    # Sort and limit
    sorted_brands = sorted(list(brands))
    return sorted_brands[:max_suggestions]


def autocomplete_composition(partial_comp: str, max_suggestions: int = 10) -> List[str]:
    """
    Get composition/ingredient suggestions

    Args:
        partial_comp: Partial composition (e.g., "Para")
        max_suggestions: Maximum suggestions

    Returns:
        List of unique compositions

    Examples:
        >>> comps = autocomplete_composition("Para")
        >>> # Returns: ["Paracetamol (500mg)", "Paracetamol (120mg)", ...]
    """
    if not partial_comp or len(partial_comp) < 2:
        return []

    medicines = load_medicines()
    search_term = partial_comp.lower().strip()

    compositions = set()
    for medicine in medicines:
        comp = medicine.get('composition', '')
        ingredient = extract_active_ingredient(comp)

        if search_term in ingredient:
            compositions.add(comp)

    # Sort and limit
    sorted_comps = sorted(list(compositions))
    return sorted_comps[:max_suggestions]


# ============================================================
# FUZZY SEARCH (Typo Tolerance)
# ============================================================

def fuzzy_search_medicine(query: str,
                         max_results: int = 10,
                         cutoff: float = 0.6) -> List[Tuple[str, float]]:
    """
    Search medicines with typo tolerance using fuzzy matching

    Uses Levenshtein distance algorithm to find close matches even with:
    - Spelling mistakes (e.g., "Panodol" -> "Panadol")
    - Transposed letters (e.g., "Bruffen" -> "Brufen")
    - Missing letters (e.g., "Panadl" -> "Panadol")

    Args:
        query: Search query (possibly misspelled)
        max_results: Maximum results to return
        cutoff: Similarity threshold (0.0-1.0, default: 0.6)
                Higher = stricter matching

    Returns:
        List of tuples: (medicine_name, similarity_score)
        Sorted by similarity (highest first)

    Examples:
        >>> results = fuzzy_search_medicine("Panodol")  # typo
        >>> # Returns: [("Panadol CF", 0.95), ("Panadol Extra", 0.92), ...]

        >>> results = fuzzy_search_medicine("Bruffen", cutoff=0.7)
        >>> # Returns: [("Brufen 400mg", 0.88), ...]
    """
    if not query:
        return []

    medicines = load_medicines()
    medicine_names = [med.get('name', '') for med in medicines if med.get('name')]

    # Get close matches using difflib
    matches = get_close_matches(query, medicine_names, n=max_results, cutoff=cutoff)

    # Calculate similarity scores
    # (get_close_matches uses SequenceMatcher internally)
    from difflib import SequenceMatcher

    results = []
    for match in matches:
        similarity = SequenceMatcher(None, query.lower(), match.lower()).ratio()
        results.append((match, similarity))

    # Already sorted by similarity (descending)
    return results


def suggest_correction(query: str, confidence_threshold: float = 0.85) -> Optional[str]:
    """
    Suggest a corrected medicine name if typo detected

    Args:
        query: Possibly misspelled query
        confidence_threshold: Minimum confidence to suggest (0.0-1.0)

    Returns:
        Suggested correction or None if no confident match

    Examples:
        >>> suggestion = suggest_correction("Panodol")
        >>> # Returns: "Panadol CF" (if confidence > threshold)

        >>> suggestion = suggest_correction("xyz123")
        >>> # Returns: None (no good match)
    """
    # First check if exact match exists
    medicines = load_medicines()
    for med in medicines:
        if med.get('name', '').lower() == query.lower():
            return None  # Exact match found, no correction needed

    # Try fuzzy search
    results = fuzzy_search_medicine(query, max_results=1, cutoff=confidence_threshold)

    if results:
        return results[0][0]  # Return top suggestion

    return None


def search_with_autocorrect(query: str, max_results: int = 10) -> Dict:
    """
    Search with automatic typo correction

    Args:
        query: Search query (possibly misspelled)
        max_results: Maximum results

    Returns:
        Dictionary with:
        - original_query: str
        - corrected_to: str (if correction applied)
        - results: List[Dict] (medicine dictionaries)

    Examples:
        >>> result = search_with_autocorrect("Panodol")
        >>> # Returns: {
        >>> #   "original_query": "Panodol",
        >>> #   "corrected_to": "Panadol",
        >>> #   "results": [...]
        >>> # }
    """
    medicines = load_medicines()

    # Try exact match first
    exact_matches = []
    query_lower = query.lower()

    for med in medicines:
        if query_lower in med.get('name', '').lower():
            exact_matches.append(med)

    if exact_matches:
        return {
            'original_query': query,
            'corrected_to': None,
            'results': sort_by_price(exact_matches[:max_results])
        }

    # Try fuzzy correction
    correction = suggest_correction(query, confidence_threshold=0.7)

    if correction:
        # Search with corrected term
        corrected_matches = []
        correction_lower = correction.lower()

        for med in medicines:
            if correction_lower in med.get('name', '').lower():
                corrected_matches.append(med)

        return {
            'original_query': query,
            'corrected_to': correction,
            'results': sort_by_price(corrected_matches[:max_results])
        }

    # No matches found
    return {
        'original_query': query,
        'corrected_to': None,
        'results': []
    }


# ============================================================
# MULTI-FIELD SEARCH
# ============================================================

def multi_field_search(query: str,
                      fields: List[str] = None,
                      max_results: int = 20) -> List[Dict]:
    """
    Search across multiple fields simultaneously

    Args:
        query: Search query
        fields: Fields to search (default: all searchable fields)
        max_results: Maximum results

    Returns:
        List of matching medicines, sorted by relevance

    Examples:
        >>> # Search in all fields
        >>> results = multi_field_search("Pain")

        >>> # Search only in specific fields
        >>> results = multi_field_search("Paracetamol",
        ...     fields=['composition', 'name'])
    """
    if fields is None:
        fields = ['name', 'brand', 'composition', 'categories', 'indications']

    medicines = load_medicines()
    query_lower = query.lower().strip()

    scored_results = []

    for medicine in medicines:
        score = 0

        for field in fields:
            value = medicine.get(field, '')
            if not value:
                continue

            # Handle list fields
            if isinstance(value, list):
                value = ' '.join(value)

            value_lower = value.lower()

            # Score based on match quality
            if query_lower == value_lower:
                score += 10  # Exact match
            elif value_lower.startswith(query_lower):
                score += 5  # Prefix match
            elif query_lower in value_lower:
                score += 1  # Contains match

        if score > 0:
            scored_results.append((medicine, score))

    # Sort by score (descending)
    scored_results.sort(key=lambda x: x[1], reverse=True)

    # Extract medicines and limit
    results = [med for med, score in scored_results[:max_results]]

    return results


# ============================================================
# DISPLAY HELPERS
# ============================================================

def display_autocomplete(partial_name: str, max_display: int = 10):
    """
    Display autocomplete suggestions

    Args:
        partial_name: Partial medicine name
        max_display: Maximum suggestions to display
    """
    suggestions = autocomplete_medicine(partial_name, max_suggestions=max_display)

    if not suggestions:
        print(f"No suggestions found for '{partial_name}'")
        return

    print(f"\nSuggestions for '{partial_name}':")
    print("-" * 70)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")


def display_fuzzy_search(query: str, max_display: int = 10):
    """
    Display fuzzy search results with similarity scores

    Args:
        query: Search query (possibly misspelled)
        max_display: Maximum results to display
    """
    results = fuzzy_search_medicine(query, max_results=max_display)

    if not results:
        print(f"No similar matches found for '{query}'")
        return

    # Check if correction is suggested
    correction = suggest_correction(query)
    if correction and correction != results[0][0]:
        print(f"\nDid you mean '{correction}'?\n")

    print(f"\nSearch results for '{query}' (with typo tolerance):")
    print("="*70)

    for i, (name, similarity) in enumerate(results, 1):
        confidence = int(similarity * 100)
        print(f"{i}. {name[:55]:55} ({confidence}% match)")

    print("="*70)


def display_search_with_autocorrect(query: str, max_display: int = 10):
    """
    Display search results with autocorrection

    Args:
        query: Search query
        max_display: Maximum results to display
    """
    result = search_with_autocorrect(query, max_results=max_display)

    if result['corrected_to']:
        print(f"\nSearching for '{result['original_query']}'...")
        print(f"Did you mean '{result['corrected_to']}'? Showing results for '{result['corrected_to']}':\n")

    medicines = result['results']

    if not medicines:
        print(f"No results found for '{query}'")
        if not result['corrected_to']:
            print("\nTry:")
            print("- Checking your spelling")
            print("- Using generic name (e.g., 'Paracetamol' instead of brand name)")
            print("- Searching by category (e.g., 'Pain', 'Fever')")
        return

    print("="*70)
    for i, med in enumerate(medicines, 1):
        name = med.get('name', 'Unknown')
        brand = med.get('brand', 'Unknown')
        price = med.get('price', 'N/A')
        print(f"{i}. {name[:50]}")
        print(f"   Brand: {brand[:30]:30} | Price: {price}\n")
    print("="*70)


# ============================================================
# USAGE EXAMPLES
# ============================================================

if __name__ == "__main__":
    print("="*70)
    print("MedFinder Enhanced Search Engine")
    print("="*70)

    # Example 1: Autocomplete
    print("\n[Example 1] Autocomplete for 'pana'")
    print("-" * 70)
    display_autocomplete("pana", max_display=10)

    # Example 2: Fuzzy search (typo)
    print("\n[Example 2] Fuzzy search for 'Panodol' (typo)")
    print("-" * 70)
    display_fuzzy_search("Panodol", max_display=10)

    # Example 3: Search with autocorrect
    print("\n[Example 3] Search with autocorrect for 'Bruffen' (typo)")
    print("-" * 70)
    display_search_with_autocorrect("Bruffen", max_display=5)

    # Example 4: Multi-field search
    print("\n[Example 4] Multi-field search for 'Pain'")
    print("-" * 70)
    results = multi_field_search("Pain", max_results=5)
    print(f"\nFound {len(results)} medicines related to 'Pain':")
    for i, med in enumerate(results, 1):
        print(f"{i}. {med.get('name')[:50]} - {med.get('brand')}")

    # Example 5: Autocomplete composition
    print("\n[Example 5] Autocomplete composition for 'Para'")
    print("-" * 70)
    comps = autocomplete_composition("Para", max_suggestions=10)
    print("\nCompositions starting with 'Para':")
    for i, comp in enumerate(comps, 1):
        print(f"{i}. {comp}")

    print("\n" + "="*70)
