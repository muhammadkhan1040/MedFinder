import faiss
import pickle
import numpy as np
import os
import sys
from typing import List, Dict, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import get_embedding_client
from traditional_rag.config import INDEX_FILE, METADATA_FILE

class TraditionalRetriever:
    def __init__(self):
        self.index = None
        self.metadata = None
        self.embed_client = get_embedding_client()
        self._load_data()

    def _load_data(self):
        """Load index and metadata from disk."""
        if not os.path.exists(INDEX_FILE) or not os.path.exists(METADATA_FILE):
            raise FileNotFoundError(f"Index or metadata file not found. Please run indexer.py first.")
            
        print(f"Loading FAISS index from {INDEX_FILE}...")
        self.index = faiss.read_index(INDEX_FILE)
        
        print(f"Loading metadata from {METADATA_FILE}...")
        with open(METADATA_FILE, 'rb') as f:
            self.metadata = pickle.load(f)
            
        # Move to GPU if available
        try:
            self.res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(self.res, 0, self.index)
            print("✅ Moved FAISS index to GPU for faster retrieval.")
        except (AttributeError, Exception):
            print("⚠️  Using CPU for FAISS retrieval (GPU not available).")
            
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks for a query.
        
        Returns:
            List of dicts containing:
            - text: str
            - metadata: dict
            - score: float
        """
        # 1. Embed Query
        query_embedding = self.embed_client.embed(query)
        query_embedding_np = np.array([query_embedding]).astype('float32')
        
        # Normalize query (same as index)
        faiss.normalize_L2(query_embedding_np)
        
        # 2. Search Index
        scores, indices = self.index.search(query_embedding_np, top_k)
        
        # 3. Fetch Metadata
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1: continue # No result found
            
            chunk_data = self.metadata.get(idx)
            if chunk_data:
                results.append({
                    "text": chunk_data.get("text"),
                    "metadata": chunk_data.get("metadata"),
                    "id": chunk_data.get("id"),
                    "score": float(score)
                })
                
        return results

if __name__ == "__main__":
    # Simple test
    try:
        retriever = TraditionalRetriever()
        results = retriever.retrieve("What are the symptoms of diabetes?")
        for res in results:
            print(f"\nScore: {res['score']:.4f}")
            print(f"Text: {res['text'][:100]}...")
            print(f"Metadata: {res['metadata']}")
    except Exception as e:
        print(f"Error: {e}")
