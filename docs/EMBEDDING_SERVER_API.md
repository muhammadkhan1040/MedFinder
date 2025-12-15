# Embedding Server API Specification

## Overview
MedFinder uses an embedding server running on **port 8081** for RAG retrieval.

## API Endpoints

### 1. Health Check
**GET** `http://localhost:8081/health`

Response:
```json
{
  "status": "healthy"
}
```

### 2. Single Text Embedding
**POST** `http://localhost:8081/embed`

Request body:
```json
{
  "text": "What is paracetamol used for?"
}
```

Response:
```json
{
  "embedding": [0.123, -0.456, ...],  // 768-dimensional vector
  "dimension": 768
}
```

### 3. Batch Text Embedding (Optional)
**POST** `http://localhost:8081/embed_batch`

Request body:
```json
{
  "texts": ["text 1", "text 2", "text 3"]
}
```

Response:
```json
{
  "embeddings": [
    [0.123, -0.456, ...],
    [0.789, -0.012, ...],
    [0.345, -0.678, ...]
  ],
  "dimension": 768,
  "count": 3
}
```

## Expected Model
- **Model**: Nomic Embed Text v1.5 or compatible
- **Dimension**: 768
- **Normalization**: L2 normalized (for cosine similarity)

## Usage in MedFinder

The embedding server is used by:
1. **RAG Retrieval** - Convert user queries to vectors for FAISS search
2. **Symptom Search** - Retrieve relevant medical book chunks

## Client Implementation

See `llm_client.py`:
```python
from llm_client import get_embedding_client

client = get_embedding_client()
embedding = client.embed("headache and fever")
# Returns 768-dim numpy array
```

## Fallback Behavior

If embedding server is unavailable:
- Client prints warning
- Returns random 768-dim vectors (fallback)
- Application continues but with degraded RAG performance

## Starting the Embedding Server

Your embedding server should:
1. Listen on `http://localhost:8081`
2. Implement `/health` and `/embed` endpoints
3. Use Nomic Embed or compatible 768-dim model
4. Return JSON responses as specified above

## Testing Connection

```python
import requests

# Test health
response = requests.get("http://localhost:8081/health")
print(response.json())

# Test embedding
response = requests.post(
    "http://localhost:8081/embed",
    json={"text": "test query"}
)
print(f"Embedding dimension: {len(response.json()['embedding'])}")
```

## Notes
- No local model loading in MedFinder
- All embedding computation happens on server
- Fast startup (no model download/loading)
- Easy to scale (separate embedding service)
