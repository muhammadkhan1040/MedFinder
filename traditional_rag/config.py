import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "traditional_rag_data")
INPUT_FILE = os.path.join(BASE_DIR, "data", "combined_chunks.jsonl")

# Output files
INDEX_FILE = os.path.join(DATA_DIR, "medical_book.index")
METADATA_FILE = os.path.join(DATA_DIR, "medical_book_meta.pkl")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Embedding Config
EMBEDDING_DIM = 768  # Nomic embedding dimension
BATCH_SIZE = 32
