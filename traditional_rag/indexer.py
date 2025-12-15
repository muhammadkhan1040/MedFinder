import json
import pickle
import os
import numpy as np
import faiss
from tqdm import tqdm
from typing import List, Dict
import sys

# Add parent directory to path to import llm_client
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import get_embedding_client
from traditional_rag.config import INPUT_FILE, INDEX_FILE, METADATA_FILE, EMBEDDING_DIM, BATCH_SIZE

def load_chunks(file_path: str) -> List[Dict]:
    """Load chunks from JSONL file."""
    chunks = []
    print(f"Loading chunks from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                chunks.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    print(f"Loaded {len(chunks)} chunks.")
    return chunks

def build_index():
    """Build FAISS index from chunks."""
    
    # 1. Load Data
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file {INPUT_FILE} not found.")
        return

    chunks = load_chunks(INPUT_FILE)
    if not chunks:
        print("No chunks found.")
        return

    # 2. Initialize Embedding Client
    embed_client = get_embedding_client()
    
    # 3. Generate Embeddings
    print("Generating embeddings...")
    embeddings = []
    metadata_map = {} # ID -> Chunk Data
    
    # Process in batches
    batch_texts = []
    batch_ids = []
    
    for i, chunk in tqdm(enumerate(chunks), total=len(chunks)):
        text = chunk.get('text', '')
        chunk_id = chunk.get('id', str(i))
        
        # Store metadata
        metadata_map[i] = chunk # Store by integer index for FAISS mapping
        
        batch_texts.append(text)
        batch_ids.append(i)
        
        if len(batch_texts) >= BATCH_SIZE:
            try:
                batch_embeddings = embed_client.embed_batch(batch_texts)
                embeddings.extend(batch_embeddings)
            except Exception as e:
                print(f"Error embedding batch: {e}")
                # Handle error (maybe skip or retry)
            
            batch_texts = []
            batch_ids = []
            
    # Process remaining
    if batch_texts:
        try:
            batch_embeddings = embed_client.embed_batch(batch_texts)
            embeddings.extend(batch_embeddings)
        except Exception as e:
            print(f"Error embedding final batch: {e}")

    # 4. Build FAISS Index
    print("Building FAISS index...")
    embeddings_np = np.array(embeddings).astype('float32')
    
    # Normalize for cosine similarity (if model requires it, usually good practice)
    faiss.normalize_L2(embeddings_np)
    
    # Create Index
    # IndexFlatIP = Inner Product (Cosine similarity if normalized)
    index = faiss.IndexFlatIP(EMBEDDING_DIM) 
    
    # GPU Support with Fallback
    try:
        print("Attempting to use GPU for indexing...")
        res = faiss.StandardGpuResources()
        # Move index to GPU
        # use float16 for memory efficiency if needed, but standard is fine
        gpu_index = faiss.index_cpu_to_gpu(res, 0, index)
        gpu_index.add(embeddings_np)
        
        # Move back to CPU for saving
        index = faiss.index_gpu_to_cpu(gpu_index)
        print(f"✅ Indexed {index.ntotal} vectors using GPU.")
        
    except (AttributeError, Exception) as e:
        print(f"⚠️  GPU indexing failed or not available ({e}). Falling back to CPU.")
        index.add(embeddings_np)
        print(f"✅ Indexed {index.ntotal} vectors using CPU.")

    # 5. Save to Disk
    print(f"Saving index to {INDEX_FILE}...")
    faiss.write_index(index, INDEX_FILE)
    
    print(f"Saving metadata to {METADATA_FILE}...")
    with open(METADATA_FILE, 'wb') as f:
        pickle.dump(metadata_map, f)
        
    print("Done!")

if __name__ == "__main__":
    build_index()
