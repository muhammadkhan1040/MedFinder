import json

# Load data
with open('medicines.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"{'='*60}")
print(f"SCRAPING COMPLETE - FINAL STATISTICS")
print(f"{'='*60}\n")

# Basic stats
print(f"📊 Total Medicines: {len(data):,}")
print(f"📝 First Medicine: {data[0]['name']}")
print(f"📝 Last Medicine: {data[-1]['name']}\n")

# Brand analysis
brands = set(m.get('brand', '') for m in data if m.get('brand'))
print(f"🏢 Unique Brands: {len(brands):,}")

# Category analysis
all_categories = []
for m in data:
    all_categories.extend(m.get('categories', []))
unique_categories = set(all_categories)
print(f"🏷️  Unique Categories: {len(unique_categories):,}")

# Data completeness
with_price = len([m for m in data if m.get('price', 'N/A') != 'N/A'])
with_images = len([m for m in data if m.get('image_url', '')])
with_indications = len([m for m in data if m.get('indications', '')])
with_side_effects = len([m for m in data if m.get('side_effects', '')])

print(f"\n📈 Data Completeness:")
print(f"   - With Price: {with_price:,} ({with_price/len(data)*100:.1f}%)")
print(f"   - With Images: {with_images:,} ({with_images/len(data)*100:.1f}%)")
print(f"   - With Indications: {with_indications:,} ({with_indications/len(data)*100:.1f}%)")
print(f"   - With Side Effects: {with_side_effects:,} ({with_side_effects/len(data)*100:.1f}%)")

# Top brands
brand_counts = {}
for m in data:
    brand = m.get('brand', 'Unknown')
    brand_counts[brand] = brand_counts.get(brand, 0) + 1

top_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:10]
print(f"\n🏆 Top 10 Brands:")
for i, (brand, count) in enumerate(top_brands, 1):
    print(f"   {i}. {brand}: {count:,} medicines")

# Top categories
cat_counts = {}
for cat in all_categories:
    cat_counts[cat] = cat_counts.get(cat, 0) + 1

top_cats = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)[:10]
print(f"\n🏷️  Top 10 Categories:")
for i, (cat, count) in enumerate(top_cats, 1):
    print(f"   {i}. {cat}: {count:,} medicines")

print(f"\n{'='*60}")
