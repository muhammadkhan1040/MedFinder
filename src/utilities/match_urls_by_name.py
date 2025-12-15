import json
import re
from datetime import datetime

def normalize_name(name):
    """Normalize medicine name for better matching"""
    # Convert to lowercase
    name = name.lower().strip()
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name)
    return name

def get_base_name(full_name):
    """Extract base medicine name (before dosage/pack info)"""
    # Remove dosage patterns like "75mg", "10x10's", "5 g", etc.
    base = re.sub(r'\d+(\.\d+)?\s*(mg|g|ml|mcg|iu|%|x\d+\'s|tablet|capsule|injection|syrup|ointment|cream|drops|suspension).*$', '', full_name, flags=re.IGNORECASE)
    return base.strip()

def match_medicines_with_urls():
    """Match medicines with URLs using fuzzy matching"""
    
    print("="*70)
    print("Matching Medicines with URLs (Fuzzy Matching)")
    print("="*70)
    
    # Load medicines
    print("\n📂 Loading medicines.json...")
    with open('medicines.json', 'r', encoding='utf-8') as f:
        medicines = json.load(f)
    print(f"   Loaded {len(medicines)} medicines")
    
    # Load URL mapping
    print("\n📂 Loading medicine_url_mapping.json...")
    with open('medicine_url_mapping.json', 'r', encoding='utf-8') as f:
        url_mapping = json.load(f)
    print(f"   Loaded {len(url_mapping)} URL mappings")
    
    # Create mapping dictionaries for different matching strategies
    # Strategy 1: Exact normalized match
    exact_map = {}
    for item in url_mapping:
        normalized = normalize_name(item['name'])
        if normalized not in exact_map:
            exact_map[normalized] = item['url']
    
    # Strategy 2: Base name match
    base_map = {}
    for item in url_mapping:
        base = get_base_name(normalize_name(item['name']))
        if base and base not in base_map:
            base_map[base] = item['url']
    
    # Strategy 3: Starts with match (for cases like "Arnil" matches "Arnil 75mg tablet")
    starts_map = {}
    for item in url_mapping:
        normalized = normalize_name(item['name'])
        if normalized not in starts_map:
            starts_map[normalized] = item['url']
    
    print(f"\n🔍 Matching strategies prepared:")
    print(f"   Exact matches available: {len(exact_map)}")
    print(f"   Base name matches available: {len(base_map)}")
    print(f"   Starts-with matches available: {len(starts_map)}")
    
    # Match medicines
    print(f"\n🔗 Matching medicines with URLs...")
    matched_exact = 0
    matched_base = 0
    matched_starts = 0
    unmatched = 0
    
    for medicine in medicines:
        med_name = medicine.get('name', '')
        normalized_med = normalize_name(med_name)
        base_med = get_base_name(normalized_med)
        
        url = None
        match_type = None
        
        # Try exact match first
        if normalized_med in exact_map:
            url = exact_map[normalized_med]
            matched_exact += 1
            match_type = "exact"
        # Try base name match
        elif base_med in base_map:
            url = base_map[base_med]
            matched_base += 1
            match_type = "base"
        # Try starts-with match
        else:
            for key, value in starts_map.items():
                if normalized_med.startswith(key + " ") or normalized_med.startswith(key):
                    url = value
                    matched_starts += 1
                    match_type = "starts"
                    break
        
        if url:
            medicine['url'] = url
        else:
            medicine['url'] = ""
            unmatched += 1
    
    # Create backup
    backup_file = f'medicines_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    print(f"\n💾 Creating backup: {backup_file}")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(medicines, f, indent=2, ensure_ascii=False)
    
    # Save updated medicines
    print(f"\n💾 Saving updated medicines.json...")
    with open('medicines.json', 'w', encoding='utf-8') as f:
        json.dump(medicines, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"✅ Matching Complete!")
    print(f"{'='*70}")
    print(f"   Exact matches: {matched_exact}")
    print(f"   Base name matches: {matched_base}")
    print(f"   Starts-with matches: {matched_starts}")
    print(f"   Total matched: {matched_exact + matched_base + matched_starts}")
    print(f"   Unmatched: {unmatched}")
    print(f"   Total medicines: {len(medicines)}")
    print(f"   Match rate: {((matched_exact + matched_base + matched_starts) / len(medicines) * 100):.1f}%")
    print(f"\n   Backup saved as: {backup_file}")
    print(f"{'='*70}\n")
    
    # Show some examples
    print("📝 Sample matched medicines:")
    count = 0
    for med in medicines:
        if med.get('url') and count < 5:
            print(f"   {med['name'][:50]:50} -> {med['url']}")
            count += 1
    
    print(f"\n📝 Sample unmatched medicines:")
    count = 0
    for med in medicines:
        if not med.get('url') and count < 5:
            print(f"   {med['name']}")
            count += 1

if __name__ == "__main__":
    match_medicines_with_urls()
