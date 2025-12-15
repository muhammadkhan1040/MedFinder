"""
Configuration for the agent system.
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEDICINES_DB = os.path.join(BASE_DIR, "data", "medicines.json")

# RAG Configuration
RAG_TOP_K = 5  # Number of chunks to retrieve
RAG_SCORE_THRESHOLD = 0.5  # Minimum relevance score
MAX_CHUNK_LENGTH = 500  # Maximum tokens per chunk

# LLM Configuration
LLM_MODEL = "gpt-3.5-turbo"  # Or whatever model you're using
LLM_TEMPERATURE = 0.3  # Lower = more deterministic
LLM_MAX_TOKENS = 500

# Formula Extraction
FORMULA_REGEX_PATTERNS = [
    r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\((\d+\s*mg|mg)\)',  # Paracetamol (500mg)
    r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(\d+\s*mg|mg)',      # Paracetamol 500mg
]

# Cache Configuration
ENABLE_CACHE = True
CACHE_FILE = os.path.join(BASE_DIR, "data", "symptom_cache.json")
CACHE_EXPIRY_HOURS = 24

# Agent Settings
ENABLE_LLM_FALLBACK = True  # Use LLM if RAG insufficient
CONFIDENCE_THRESHOLD = 0.7   # Minimum confidence for formula extraction
