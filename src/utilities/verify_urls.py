import json

# Load medicines and check URL status
with open('medicines.json', 'r', encoding='utf-8') as f:
    medicines = json.load(f)

with_urls = sum(1 for m in medicines if m.get('url'))
without_urls = len(medicines) - with_urls

print("="*70)
print("URL Matching Results")
print("="*70)
print(f"\nTotal medicines: {len(medicines)}")
print(f"With URLs: {with_urls} ({with_urls/len(medicines)*100:.1f}%)")
print(f"Without URLs: {without_urls} ({without_urls/len(medicines)*100:.1f}%)")

print(f"\n{'='*70}")
print("Sample medicines with URLs:")
print(f"{'='*70}")
for i, med in enumerate(medicines[:10]):
    if med.get('url'):
        print(f"{i+1}. {med['name'][:45]:45} -> {med['url']}")

print(f"\n{'='*70}")
print("Sample medicines without URLs:")
print(f"{'='*70}")
count = 0
for med in medicines:
    if not med.get('url') and count < 10:
        print(f"{count+1}. {med['name']}")
        count += 1
print(f"{'='*70}\n")
