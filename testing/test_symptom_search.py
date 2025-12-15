"""
Manual Test Script for Symptom Search Agent
Tests the complete pipeline and saves responses for analysis
"""
import sys
import os
import json
from datetime import datetime

# Add paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'core'))

print("="*80)
print("SYMPTOM SEARCH AGENT - MANUAL TEST")
print("="*80)

# Test symptoms
test_symptoms = "high fever, body aches, and chills"
print(f"\n📝 Test Query: '{test_symptoms}'")

# Step 1: Load LLM Client
print("\n[Step 1] Loading LLM Client...")
try:
    from llm_client import get_llm_client
    llm = get_llm_client()
    if llm.client:
        print("✓ Gemini LLM loaded successfully")
    else:
        print("✗ Gemini LLM not configured")
        sys.exit(1)
except Exception as e:
    print(f"✗ Error loading LLM: {e}")
    sys.exit(1)

# Step 2: Load RAG Retriever
print("\n[Step 2] Loading RAG Retriever...")
try:
    from traditional_rag.retriever import TraditionalRetriever
    rag = TraditionalRetriever()
    print("✓ RAG retriever loaded")
    
    # Test retrieval
    rag_results = rag.retrieve(test_symptoms, top_k=5)
    print(f"  Retrieved {len(rag_results)} chunks")
    for i, r in enumerate(rag_results[:3], 1):
        print(f"    [{i}] Score: {r['score']:.4f} | Text: {r['text'][:80]}...")
except Exception as e:
    print(f"✗ Error loading RAG: {e}")
    rag_results = []

# Step 3: Build Prompt
print("\n[Step 3] Building Prompt...")
from src.agents.symptom_search_agent import SymptomSearchAgent

# Create minimal instance to use prompt builder
class TestAgent:
    def _build_rag_prompt(self, symptoms, rag_context, max_results):
        # Copy the prompt building logic
        context_section = ""
        if rag_context:
            context_section = "\n\nMEDICAL CONTEXT FROM BOOKS:\n"
            for i, chunk in enumerate(rag_context[:3], 1):
                context_section += f"\n[Source {i}] (Relevance: {chunk['score']:.2f})\n"
                context_section += f"{chunk['text'][:400]}...\n"
        
        prompt = f"""You are a medical AI assistant. Analyze symptoms and recommend medicines in STRICT JSON format.

USER SYMPTOMS: {symptoms}
{context_section}

TASK:
Analyze the symptoms and recommend {max_results} medicines. Return ONLY a valid JSON object (no markdown, no explanation).

IMPORTANT CONSTRAINTS:
1. ONLY answer medical/health queries
2. If not medical, return: {{"error": "Not a medical query"}}
3. {'Use information from sources above' if rag_context else 'Use medical knowledge'}
4. Focus on OTC medicines available in Pakistan
5. Return chemical/generic names (e.g., "Paracetamol", "Ibuprofen")

REQUIRED JSON FORMAT:
{{
  "is_medical_query": true,
  "analysis": "Brief analysis of symptoms (2-3 sentences)",
  "recommendations": [
    {{
      "rank": 1,
      "chemical_formula": "Paracetamol",
      "dosage": "500mg every 6 hours",
      "reason": "Why this helps (1-2 sentences)",
      "warnings": "Precautions (1 sentence)",
      "requires_doctor": false
    }},
    {{
      "rank": 2,
      "chemical_formula": "Ibuprofen",
      "dosage": "200-400mg every 8 hours",
      "reason": "Anti-inflammatory for pain relief",
      "warnings": "Avoid on empty stomach",
      "requires_doctor": false
    }}
  ],
  "requires_immediate_attention": false,
  "disclaimer": "Consult healthcare professional for proper diagnosis"
}}

RETURN ONLY THE JSON OBJECT (no other text):"""
        
        return prompt

agent_helper = TestAgent()
prompt = agent_helper._build_rag_prompt(test_symptoms, rag_results, 5)

print(f"✓ Prompt built ({len(prompt)} chars)")
print(f"\n  Prompt Preview:")
print(f"  {prompt[:300]}...")
print(f"  ...{prompt[-200:]}")

# Save prompt
with open('test_prompt.txt', 'w', encoding='utf-8') as f:
    f.write(prompt)
print(f"\n  💾 Saved to: test_prompt.txt")

# Step 4: Call LLM
print("\n[Step 4] Calling Gemini LLM...")
print("  (This may take 10-30 seconds...)")

try:
    llm_response = llm.complete(
        prompt=prompt,
        temperature=0.1,
        max_tokens=3000
    )
    
    print(f"\n✓ LLM Response received ({len(llm_response)} chars)")
    print(f"\n  First 500 chars:")
    print(f"  {llm_response[:500]}...")
    print(f"\n  Last 300 chars:")
    print(f"  ...{llm_response[-300:]}")
    
    # Save raw response
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    response_file = f'test_llm_response_{timestamp}.txt'
    with open(response_file, 'w', encoding='utf-8') as f:
        f.write(llm_response)
    print(f"\n  💾 Saved to: {response_file}")
    
except Exception as e:
    print(f"✗ LLM call failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: Parse JSON
print("\n[Step 5] Parsing JSON...")
import re

try:
    # Clean response
    cleaned = llm_response.strip()
    
    # Remove markdown
    if '```' in cleaned:
        code_block_pattern = r'```(?:json)?\s*(.*?)\s*```'
        matches = re.findall(code_block_pattern, cleaned, re.DOTALL)
        if matches:
            cleaned = matches[0]
            print("  ℹ Extracted from markdown code block")
    
    # Find JSON
    start_idx = cleaned.find('{')
    end_idx = cleaned.rfind('}')
    
    if start_idx == -1:
        raise ValueError("No opening brace found")
    if end_idx == -1:
        print("  ⚠ No closing brace - attempting to fix...")
        # Add missing braces
        missing = cleaned[start_idx:].count('{') - cleaned[start_idx:].count('}')
        if missing > 0:
            cleaned += '}' * missing
            end_idx = len(cleaned) - 1
            print(f"  ℹ Added {missing} closing braces")
    
    json_str = cleaned[start_idx:end_idx + 1]
    
    # Parse
    parsed_json = json.loads(json_str)
    
    print(f"✓ JSON parsed successfully!")
    print(f"\n  is_medical_query: {parsed_json.get('is_medical_query')}")
    print(f"  analysis: {parsed_json.get('analysis', '')[:100]}...")
    print(f"  recommendations: {len(parsed_json.get('recommendations', []))}")
    
    # Save parsed JSON
    json_file = f'test_parsed_json_{timestamp}.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_json, f, indent=2, ensure_ascii=False)
    print(f"\n  💾 Saved to: {json_file}")
    
    # Show recommendations
    print(f"\n  Recommendations:")
    for i, rec in enumerate(parsed_json.get('recommendations', []), 1):
        print(f"    {i}. {rec.get('chemical_formula')} - {rec.get('dosage')}")
        print(f"       Reason: {rec.get('reason', '')[:60]}...")
    
except json.JSONDecodeError as e:
    print(f"✗ JSON parsing failed: {e}")
    print(f"  Problem at position: {e.pos}")
    print(f"  Context: ...{json_str[max(0, e.pos-50):e.pos+50]}...")
    parsed_json = None
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    parsed_json = None

# Step 6: Match with Database
if parsed_json:
    print("\n[Step 6] Matching with Medicine Database...")
    try:
        from utils import load_medicines
        medicines = load_medicines()
        print(f"✓ Loaded {len(medicines)} medicines from database")
        
        matches_summary = []
        for rec in parsed_json.get('recommendations', []):
            formula = rec.get('chemical_formula', '').lower()
            
            # Search
            matched = []
            for med in medicines:
                med_formula = med.get('formula', '').lower()
                med_name = med.get('name', '').lower()
                
                if formula in med_formula or formula in med_name:
                    matched.append(med)
            
            # Sort by price
            matched.sort(key=lambda x: float(x.get('price', 999999)) if x.get('price') else 999999)
            
            matches_summary.append({
                'chemical_formula': rec.get('chemical_formula'),
                'matched_count': len(matched),
                'top_3_medicines': [
                    {
                        'name': m.get('name'),
                        'price': m.get('price'),
                        'manufacturer': m.get('manufacturer')
                    }
                    for m in matched[:3]
                ]
            })
            
            print(f"\n  {rec.get('chemical_formula')}: {len(matched)} matches")
            for m in matched[:3]:
                print(f"    - {m.get('name')} | Rs.{m.get('price')} | {m.get('manufacturer')}")
        
        # Save matches
        matches_file = f'test_matches_{timestamp}.json'
        with open(matches_file, 'w', encoding='utf-8') as f:
            json.dump(matches_summary, f, indent=2, ensure_ascii=False)
        print(f"\n  💾 Saved to: {matches_file}")
        
    except Exception as e:
        print(f"✗ Database matching failed: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
print("✅ MANUAL TEST COMPLETE")
print("="*80)
print("\nGenerated Files:")
print("  - test_prompt.txt (LLM prompt)")
print(f"  - {response_file} (Raw LLM response)")
if parsed_json:
    print(f"  - {json_file} (Parsed JSON)")
    print(f"  - {matches_file} (Database matches)")
print("\n Review these files to verify the pipeline!")
print("="*80)
