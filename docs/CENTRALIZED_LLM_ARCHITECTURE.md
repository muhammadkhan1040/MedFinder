# MedFinder - Centralized LLM Architecture

## Overview
All AI features in MedFinder now use a **centralized Google Gemini LLM client** for consistency and maintainability.

## Architecture

### Centralized LLM Client
**File**: `llm_client.py` (root directory)

This is the **single source of truth** for all LLM interactions in MedFinder.

```python
from llm_client import get_llm_client

# All modules use this
llm_client = get_llm_client()
response = llm_client.complete(prompt="...", temperature=0.7, max_tokens=500)
```

### Features Using Centralized LLM

#### 1. **Prescription Assistant** (`backend_api/routes/prescription.py`)
- Drug name validation
- Spelling correction for misspelled drugs
- Smart suggestions

**Usage**:
```python
from llm_client import get_llm_client  # Indirect via prescription.py imports

def validate_drug_with_ai(user_input):
    # Uses GEMINI_MODEL directly (configured at module load)
    response = GEMINI_MODEL.generate_content(prompt, generation_config)
```

#### 2. **Symptom Search** (`src/agents/symptom_search_agent.py`)
- AI-powered symptom analysis
- Medicine recommendations
- Dosage suggestions

**Usage**:
```python
from llm_client import get_llm_client

class SymptomSearchAgent:
    def __init__(self):
        self.llm_client = get_llm_client()
        
    def search(self, symptoms):
        response = self.llm_client.complete(prompt=...)
```

#### 3. **LLM Fallback Agent** (`src/agents/llm_fallback.py`)
- General medical knowledge queries
- Formula extraction fallback

**Usage**:
```python
from llm_client import get_llm_client

class LLMFallbackAgent:
    def __init__(self):
        self.llm_client = get_llm_client()
```

## Configuration

### Environment Variable
**Single API Key** for all features:

```env
GEMINI_API_KEY=your_api_key_here
```

Get from: https://aistudio.google.com/app/apikey

### LLM Client Initialization

The `llm_client.py` automatically:
1. Loads `.env` file via `load_dotenv()`
2. Checks for `GEMINI_API_KEY`
3. Configures Google Gemini
4. Creates `GenerativeModel('gemini-1.5-flash')`

```python
# In llm_client.py
load_dotenv()

class LLMClient:
    def __init__(self):
        if HAS_GEMINI:
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel('gemini-1.5-flash')
```

## Benefits of Centralized Architecture

### ✅ Consistency
- All features use the same LLM model
- Same configuration across the application
- Predictable behavior

### ✅ Maintainability
- Single point of configuration
- Easy to switch models (change once in llm_client.py)
- Easy to add new features

### ✅ Cost Efficiency
- Single API key
- Shared rate limits
- Easier to monitor usage

### ✅ Error Handling
- Centralized error handling
- Consistent fallback behavior
- Better logging

## How to Add New AI Features

When adding new AI features to MedFinder:

1. **Import the centralized client**:
   ```python
   from llm_client import get_llm_client
   ```

2. **Initialize in your class/module**:
   ```python
   def __init__(self):
       self.llm_client = get_llm_client()
   ```

3. **Use the complete method**:
   ```python
   response = self.llm_client.complete(
       prompt="Your prompt here",
       temperature=0.7,  # 0.0-1.0
       max_tokens=500
   )
   ```

4. **Handle errors gracefully**:
   ```python
   if not self.llm_client or not self.llm_client.client:
       raise ImportError("Gemini not configured")
   ```

## Model Configuration

### Current Model
- **Name**: `gemini-1.5-flash`
- **Provider**: Google
- **Use Case**: Fast, efficient responses
- **Cost**: Free tier available

### Switching Models

To switch to a different Gemini model, edit `llm_client.py`:

```python
# Change from:
self.client = genai.GenerativeModel('gemini-1.5-flash')

# To:
self.client = genai.GenerativeModel('gemini-1.5-pro')  # More capable
# or
self.client = genai.GenerativeModel('gemini-1.0-pro')  # Stable version
```

## Dependencies

Required Python packages:
```txt
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

Install:
```bash
pip install google-generativeai python-dotenv
```

## Troubleshooting

### "AI validation not available"
**Cause**: GEMINI_API_KEY not set or invalid

**Solution**:
1. Check `.env` file exists in root directory
2. Verify `GEMINI_API_KEY=your_key_here`
3. Restart backend server

### "Symptom search agent not configured"
**Cause**: LLM client can't initialize

**Solution**:
1. Ensure `google-generativeai` is installed
2. Check GEMINI_API_KEY is set
3. Verify no import errors in console

### "ImportError: google.generativeai"
**Cause**: Package not installed

**Solution**:
```bash
pip install google-generativeai
```

## Testing

### Test LLM Client:
```python
from llm_client import get_llm_client

client = get_llm_client()
if client.client:
    response = client.complete("Hello, how are you?")
    print(response)
else:
    print("LLM not configured")
```

### Test Prescription AI:
- Go to: http://localhost:5173/prescription
- Search: "Asprin" (misspelled)
- Should suggest: "Aspirin"

### Test Symptom Search:
- Go to: http://localhost:5173/symptom-search
- Enter: "headache and fever"
- Should get AI recommendations

## Summary

**All LLM features use centralized Google Gemini client**:

| Feature | File | Uses |
|---------|------|------|
| Prescription AI | `routes/prescription.py` | `GEMINI_MODEL` (direct) |
| Symptom Search | `agents/symptom_search_agent.py` | `get_llm_client()` |
| LLM Fallback | `agents/llm_fallback.py` | `get_llm_client()` |

**Single configuration point**: `llm_client.py`

**Single environment variable**: `GEMINI_API_KEY`

**Result**: Consistent, maintainable, efficient AI implementation! 🎯
