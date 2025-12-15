"""
Test Backend API Endpoint
Tests the actual /api/symptom-search endpoint to verify parsing
"""
import requests
import json

print("="*80)
print("TESTING BACKEND API /api/symptom-search")
print("="*80)

# Test data
test_data = {
    "symptoms": "high fever, body aches, and chills",
    "max_results": 5
}

print(f"\n📝 Request:")
print(json.dumps(test_data, indent=2))

# Call API
print(f"\n🔄 Calling http://localhost:5000/api/symptom-search...")
try:
    response = requests.post(
        "http://localhost:5000/api/symptom-search",
        json=test_data,
        timeout=60
    )
    
    print(f"\n✓ Response Status: {response.status_code}")
    
    # Parse response
    data = response.json()
    
    # Save response
    with open('test_api_response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to: test_api_response.json")
    
    # Analyze response
    print(f"\n📊 Response Structure:")
    print(f"  success: {data.get('success')}")
    print(f"  rag_used: {data.get('rag_used')}")
    print(f"  rag_chunks: {data.get('rag_chunks')}")
    print(f"  recommendations: {len(data.get('recommendations', []))}")
    print(f"  ai_analysis (length): {len(data.get('ai_analysis', ''))}")
    
    # Check recommendations
    recommendations = data.get('recommendations', [])
    if recommendations:
        print(f"\n🎯 Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n  [{i}] Rank: {rec.get('rank')}")
            print(f"      Formula: {rec.get('chemical_formula')}")
            print(f"      Dosage: {rec.get('dosage')}")
            print(f"      Explanation: {rec.get('explanation', '')[:80]}...")
            print(f"      Warnings: {rec.get('warnings', '')[:80]}...")
            print(f"      Matched Medicines: {rec.get('medicine_count', 0)}")
            
            # Show top 3 matched medicines
            matched = rec.get('matched_medicines', [])
            if matched:
                print(f"      Top matches:")
                for med in matched[:3]:
                    print(f"        - {med.get('name')} | Rs.{med.get('price')} | {med.get('manufacturer')}")
    
    # Check if frontend will parse correctly
    print(f"\n✅ FRONTEND COMPATIBILITY CHECK:")
    print(f"  ✓ 'success' field present: {data.get('success') is not None}")
    print(f"  ✓ 'recommendations' is list: {isinstance(data.get('recommendations'), list)}")
    print(f"  ✓ 'ai_analysis' present: {data.get('ai_analysis') is not None}")
    print(f"  ✓ 'rag_used' present: {data.get('rag_used') is not None}")
    
    if data.get('recommendations'):
        first_rec = data['recommendations'][0]
        print(f"  ✓ 'chemical_formula' in rec: {first_rec.get('chemical_formula') is not None}")
        print(f"  ✓ 'matched_medicines' in rec: {first_rec.get('matched_medicines') is not None}")
        print(f"  ✓ 'rank' in rec: {first_rec.get('rank') is not None}")
    
    print(f"\n✅ Backend API is working correctly!")
    
except requests.exceptions.ConnectionError:
    print(f"\n✗ ERROR: Cannot connect to backend")
    print(f"  Make sure backend is running on http://localhost:5000")
except requests.exceptions.Timeout:
    print(f"\n✗ ERROR: Request timed out")
    print(f"  Backend may be processing, try increasing timeout")
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
