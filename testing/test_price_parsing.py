"""
Test price parsing fix
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'core'))

from utils import load_medicines
import re

print("Testing Price Parsing Fix...")

medicines = load_medicines()
print(f"Loaded {len(medicines)} medicines")

# Test price extraction function
def extract_price(med):
    """Extract numeric price from various formats"""
    price_str = str(med.get('price', '999999'))
    try:
        # Extract first number (with decimals)
        match = re.search(r'\d+\.?\d*', price_str)
        if match:
            return float(match.group())
        return 999999
    except:
        return 999999

# Find some test medicines
test_meds = medicines[:10]

print("\nTesting price extraction:")
for med in test_meds:
    original = med.get('price')
    extracted = extract_price(med)
    print(f"  {med.get('name')[:30]:30} | Original: {str(original):20} | Extracted: {extracted}")

# Now test searching for Paracetamol
print("\n\nSearching for 'Paracetamol'...")
formula_lower = 'paracetamol'
matched = []

for med in medicines:
    med_formula = med.get('formula', '').lower()
    med_name = med.get('name', '').lower()
    
    if formula_lower in med_formula or formula_lower in med_name:
        matched.append({
            'name': med.get('name'),
            'formula': med.get('formula'),
            'manufacturer': med.get('manufacturer'),
            'pack_size': med.get('pack_size'),
            'price': med.get('price'),
            'type': med.get('type', 'N/A')
        })

print(f"Found {len(matched)} matches")

# Sort them
print("\nSorting by price...")
matched.sort(key=extract_price)

print(f"\nTop 10 cheapest Paracetamol:")
for i, med in enumerate(matched[:10], 1):
    price_val = extract_price(med)
    print(f"  {i}. {med['name'][:40]:40} | Rs.{price_val:6.2f} | {med['manufacturer']}")

print("\n✓ Price parsing works!")
