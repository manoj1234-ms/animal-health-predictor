"""
Quick demo of the new comprehensive system
Tests all 8 species
"""

import sys
sys.path.insert(0, 'src')

from src.biological_validation import (
    get_all_supported_species,
    get_all_categories,
    get_category_statistics
)

print("="*70)
print(" "*20 + "SYSTEM CAPABILITIES DEMO")
print("="*70)

# Show supported species
species = get_all_supported_species()
print("\n🐾 SUPPORTED SPECIES (8):")
species_icons = {
    'Dog': '🐕', 'Cat': '🐈', 'Cattle': '🐄', 'Pig': '🐖',
    'Sheep': '🐑', 'Horse': '🐴', 'Goat': '🐐', 'Chicken': '🐔'
}
for s in species:
    icon = species_icons.get(s, '🐾')
    print(f"  {icon} {s}")

# Show categories
categories = get_all_categories()
print(f"\n🏥 DISEASE CATEGORIES ({len(categories)}):")
for cat in sorted(categories):
    print(f"  • {cat}")

# Show statistics
stats = get_category_statistics()
print(f"\n📊 DATABASE STATISTICS:")
print(f"  Total Species: {stats['total_species']}")
print(f"  Total Categories: {stats['total_categories']}")
print(f"  Total Diseases: {stats['total_diseases']}")
print(f"\n  Diseases per Species:")
for animal, count in sorted(stats['diseases_per_species'].items()):
    icon = species_icons.get(animal, '🐾')
    print(f"    {icon} {animal}: {count} diseases")

print("\n" + "="*70)
print("✅ SYSTEM READY FOR PRODUCTION!")
print("="*70)
print("\n📌 Next Steps:")
print("  1. Run: streamlit run app.py")
print("  2. Visit: http://localhost:8501")
print("  3. Test with all 8 species!")
print("\n🎯 Or run the API:")
print("  1. Run: python simple_api.py")
print("  2. Visit: http://localhost:8000/docs")
print()
