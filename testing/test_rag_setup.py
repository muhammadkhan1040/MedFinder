"""
Test RAG Setup - Verify index files and retrieval
"""
import os
import sys

# Add paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Testing RAG Setup")
print("=" * 60)

# 1. Check index files
print("\n1. Checking index files...")
from traditional_rag.config import INDEX_FILE, METADATA_FILE

if os.path.exists(INDEX_FILE):
    size_mb = os.path.getsize(INDEX_FILE) / (1024 * 1024)
    print(f"✓ Index file found: {INDEX_FILE}")
    print(f"  Size: {size_mb:.1f} MB")
else:
    print(f"✗ Index file NOT found: {INDEX_FILE}")

if os.path.exists(METADATA_FILE):
    size_mb = os.path.getsize(METADATA_FILE) / (1024 * 1024)
    print(f"✓ Metadata file found: {METADATA_FILE}")
    print(f"  Size: {size_mb:.1f} MB")
else:
    print(f"✗ Metadata file NOT found: {METADATA_FILE}")

# 2. Test embedding client
print("\n2. Testing embedding client...")
try:
    from llm_client import get_embedding_client
    embed_client = get_embedding_client()
    test_embedding = embed_client.embed("test query")
    print(f"✓ Embedding client working")
    print(f"  Embedding dimension: {len(test_embedding)}")
except Exception as e:
    print(f"✗ Embedding client error: {e}")

# 3. Test RAG retriever
print("\n3. Testing RAG retriever...")
try:
    from traditional_rag.retriever import TraditionalRetriever
    retriever = TraditionalRetriever()
    
    # Test query
    test_query = "What is paracetamol used for?"
    results = retriever.retrieve(test_query, top_k=3)
    
    print(f"✓ RAG retriever working")
    print(f"  Retrieved {len(results)} chunks")
    
    if results:
        print(f"\n  Top result:")
        print(f"    Score: {results[0]['score']:.4f}")
        print(f"    Text preview: {results[0]['text'][:100]}...")
        
except Exception as e:
    print(f"✗ RAG retriever error: {e}")
    import traceback
    print(traceback.format_exc())

# 4. Test Gemini LLM
print("\n4. Testing Gemini LLM...")
try:
    from llm_client import get_llm_client
    llm = get_llm_client()
    
    if llm.client:
        print(f"✓ Gemini LLM initialized")
        
        # Quick test
        response = llm.complete("Say 'Hello'", max_tokens=10)
        if response:
            print(f"  Test response: {response[:50]}...")
    else:
        print(f"✗ Gemini LLM not configured (check GEMINI_API_KEY)")
        
except Exception as e:
    print(f"✗ Gemini LLM error: {e}")

# 5. Test Symptom Search Agent
print("\n5. Testing Symptom Search Agent...")
try:
    from src.agents.symptom_search_agent import SymptomSearchAgent
    
    agent = SymptomSearchAgent()
    print(f"✓ Symptom search agent initialized")
    
    if agent.rag_retriever:
        print(f"  RAG retriever: ENABLED")
    else:
        print(f"  RAG retriever: DISABLED (will use LLM only)")
    
    # Quick search test
    print(f"\n  Testing search with 'headache'...")
    result = agent.search("headache", max_results=2)
    
    print(f"  ✓ Search completed")
    print(f"    RAG used: {result.get('rag_used', False)}")
    print(f"    RAG chunks: {result.get('rag_chunks', 0)}")
    print(f"    Recommendations: {len(result.get('recommendations', []))}")
    
except Exception as e:
    print(f"✗ Symptom search agent error: {e}")
    import traceback
    print(traceback.format_exc())

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
