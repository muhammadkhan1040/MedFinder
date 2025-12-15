import os
import numpy as np
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Try importing Gemini
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

class EmbeddingClient:
    """
    Embedding client using llama-server API on port 8081 (OpenAI-compatible)
    No local model loading - just HTTP requests
    """
    def __init__(self):
        self.base_url = "http://localhost:8081/v1"
        self.embeddings_url = f"{self.base_url}/embeddings"
        self.embedding_dim = 768  # Nomic embed dimension
        
        # Test connection (use embeddings endpoint as health check)
        try:
            response = requests.post(
                self.embeddings_url,
                json={"input": "test"},
                timeout=5
            )
            if response.status_code == 200:
                print("✓ Connected to embedding server on port 8081")
            else:
                print(f"⚠ Embedding server responded with status {response.status_code}")
        except Exception as e:
            print(f"⚠ Embedding server on port 8081 not reachable: {e}")

    def embed(self, text: str):
        """Get embedding from server using OpenAI-compatible API"""
        try:
            response = requests.post(
                self.embeddings_url,
                json={
                    "input": text,
                    "model": "nomic-embed-text-v1.5"  # Model name for llama-server teh Nomic embedding model 
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # OpenAI format: data[0].embedding
                embedding = data.get("data", [{}])[0].get("embedding", [])
                return np.array(embedding, dtype='float32')
            else:
                print(f"Embedding server error: {response.status_code}")
                return self._fallback_embedding()
                
        except Exception as e:
            print(f"Embedding request failed: {e}")
            return self._fallback_embedding()
    
    def embed_batch(self, texts):
        """Get embeddings for multiple texts from server"""
        try:
            response = requests.post(
                self.embeddings_url,
                json={
                    "input": texts,  # Send as list
                    "model": "nomic-embed-text-v1.5"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                # OpenAI format: data is list of {embedding: [...]}
                embeddings = [item.get("embedding", []) for item in data.get("data", [])]
                return np.array(embeddings, dtype='float32')
            else:
                # Fallback: embed one by one
                return np.array([self.embed(text) for text in texts])
                
        except:
            # Fallback: embed one by one
            return np.array([self.embed(text) for text in texts])
    
    def _fallback_embedding(self):
        """Fallback: return random vector if server unavailable"""
        return np.random.rand(self.embedding_dim).astype('float32')

class LLMClient:
    """LLM Client using Google Gemini"""
    def __init__(self):
        self.client = None
        if HAS_GEMINI:
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel('gemini-2.5-flash')
                print("✓ Google Gemini initialized")
            else:
                print("Warning: GEMINI_API_KEY not found. LLM features will be limited.")
        else:
            print("Warning: google-generativeai not installed. Run: pip install google-generativeai")
    
    def complete(self, prompt, model="gemini-2.5-flash", temperature=0.7, max_tokens=500):
        """
        Complete a prompt using Google Gemini
        
        Args:
            prompt: The prompt text
            model: Model name (ignored, uses gemini-2.5-flash)
            temperature: Generation temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text or None if error
        """
        if self.client:
            try:
                # Configure generation parameters
                generation_config = genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
                
                response = self.client.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                return response.text
            except Exception as e:
                print(f"Gemini LLM Error: {e}")
                return None
        return None

def get_embedding_client():
    return EmbeddingClient()

def get_llm_client():
    return LLMClient()
