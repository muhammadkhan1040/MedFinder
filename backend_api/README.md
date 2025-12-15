# MedFinder Backend API (FastAPI)

🚀 **FastAPI** REST API for the MedFinder medicine search platform.

## ✨ Features

- **Automatic API Documentation** at `/docs` (Swagger UI)
- **Request Validation** with Pydantic models
- **Async Support** for better performance
- **Type Hints** throughout the codebase

## 🚀 Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/stats` | GET | Database statistics |
| `/api/search/ingredient` | POST | Search by active ingredient |
| `/api/search/composition` | POST | Search with dosage filter |
| `/api/autocomplete` | POST | Get autocomplete suggestions |
| `/api/search/multi` | POST | Multi-field search |
| `/api/search/fuzzy` | POST | Fuzzy search with typo tolerance |
| `/api/similar-medicines` | POST | Find alternative medicines |
| `/api/check-availability` | POST | Check medicine availability |
| `/api/symptom-search` | POST | AI symptom-based search |
| `/api/dosages` | POST | Get available dosages |
| `/api/medicine/<name>` | GET | Get medicine details |

## 📦 Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Server starts on `http://localhost:5000`

## 📚 API Documentation

Once the server is running:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## 🔧 Requirements

- Python 3.8+
- FastAPI 0.104+
- Uvicorn 0.24+
- Pydantic 2.5+

## 📝 API Examples

### Search by Ingredient

```bash
curl -X POST http://localhost:5000/api/search/ingredient \
  -H "Content-Type: application/json" \
  -d '{"ingredient": "Paracetamol", "max_results": 10}'
```

### Autocomplete

```bash
curl -X POST http://localhost:5000/api/autocomplete \
  -H "Content-Type: application/json" \
  -d '{"query": "para", "max_suggestions": 10}'
```

### Find Alternatives

```bash
curl -X POST http://localhost:5000/api/similar-medicines \
  -H "Content-Type: application/json" \
  -d '{"medicine_name": "Panadol", "max_results": 5}'
```

### Check Availability

```bash
curl -X POST http://localhost:5000/api/check-availability \
  -H "Content-Type: application/json" \
  -d '{"medicine_name": "Panadol"}'
```

## 🔗 CORS

CORS is enabled for:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000`
- `http://127.0.0.1:5173`

## 📁 Structure

```
backend_api/
├── app.py              # FastAPI application
├── requirements.txt    # Python dependencies
├── routes/             # Additional route modules
│   └── symptom_search.py
└── README.md           # This file
```

## 🔌 Backend Integration

The API wraps these modules from `src/core/`:
- `search_engine.py` - Formula-based search
- `similar_medicines.py` - Alternative finder
- `enhanced_search.py` - Autocomplete & fuzzy search
- `websearchfunction.py` - Availability checker
- `utils.py` - Shared utilities
