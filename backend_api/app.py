"""
MedFinder Backend API Server - FastAPI Edition

FastAPI server with automatic documentation, request validation,
and async support for the medicine search platform.

Author: MedFinder Team
Date: 2025-12-10
"""

import sys
import os

# Add the src/core directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'core'))
# Add project root to Python path for agents and other modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Any
import uvicorn

# Import backend modules
from search_engine import (
    search_by_ingredient,
    search_by_composition,
    get_available_dosages,
    get_price_range,
    get_brand_count
)
from similar_medicines import (
    get_similar_medicines,
    get_alternatives_with_savings,
    find_cheapest_alternative,
    find_medicine_by_name
)
from enhanced_search import (
    autocomplete_medicine,
    autocomplete_composition,
    multi_field_search,
    fuzzy_search_medicine,
    search_with_autocorrect
)
from websearchfunction import check_medicine_availability
from utils import load_medicines

# Import prescription routes
from routes import prescription as prescription_routes

# ============================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================

class SearchIngredientRequest(BaseModel):
    ingredient: str = Field(..., description="Active ingredient to search for", min_length=1)
    max_results: int = Field(20, description="Maximum number of results", ge=1, le=100)

class SearchCompositionRequest(BaseModel):
    formula: str = Field(..., description="Chemical formula to search for", min_length=1)
    dosage_filter: Optional[str] = Field(None, description="Optional dosage filter (e.g., '500mg')")
    max_results: int = Field(20, description="Maximum number of results", ge=1, le=100)

class AutocompleteRequest(BaseModel):
    query: str = Field(..., description="Search query for autocomplete", min_length=2)
    max_suggestions: int = Field(10, description="Maximum suggestions", ge=1, le=20)

class MultiSearchRequest(BaseModel):
    query: str = Field(..., description="Search query", min_length=1)
    max_results: int = Field(20, description="Maximum results", ge=1, le=100)

class FuzzySearchRequest(BaseModel):
    query: str = Field(..., description="Search query with potential typos", min_length=1)
    max_results: int = Field(10, description="Maximum results", ge=1, le=50)

class SimilarMedicinesRequest(BaseModel):
    medicine_name: str = Field(..., description="Medicine name to find alternatives for", min_length=1)
    max_results: int = Field(10, description="Maximum alternatives", ge=1, le=50)

class AvailabilityRequest(BaseModel):
    medicine_name: str = Field(..., description="Medicine name to check", min_length=1)

class DosagesRequest(BaseModel):
    ingredient: str = Field(..., description="Ingredient to get dosages for", min_length=1)

class SymptomSearchRequest(BaseModel):
    symptoms: str = Field(..., description="Symptoms description", min_length=3)
    max_results: int = Field(10, description="Maximum results", ge=1, le=20)

# ============================================================
# FASTAPI APP SETUP
# ============================================================

app = FastAPI(
    title="MedFinder API",
    description="🏥 Medicine search API with 20,000+ medicines from Pakistan. Search by name, formula, or symptoms.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include prescription routes
app.include_router(prescription_routes.router, prefix="/api/prescription", tags=["Prescription Assistant"])

# ============================================================
# SEARCH ENDPOINTS
# ============================================================

@app.post("/api/search/ingredient", tags=["Search"])
async def api_search_ingredient(request: SearchIngredientRequest):
    """
    Search medicines by active ingredient.
    
    Example: Search for "Paracetamol" to find all medicines containing it.
    """
    try:
        results = search_by_ingredient(request.ingredient, max_results=request.max_results)
        
        stats = get_price_range(results) if results else {'min': 0, 'max': 0, 'avg': 0}
        brand_count = get_brand_count(results) if results else 0
        
        return {
            'success': True,
            'query': request.ingredient,
            'count': len(results),
            'brand_count': brand_count,
            'price_stats': stats,
            'results': results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search/composition", tags=["Search"])
async def api_search_composition(request: SearchCompositionRequest):
    """
    Search medicines by chemical composition with optional dosage filter.
    
    Example: Search for "Ibuprofen" with dosage_filter="400mg"
    """
    try:
        results = search_by_composition(
            request.formula,
            dosage_filter=request.dosage_filter,
            max_results=request.max_results
        )
        
        dosages = get_available_dosages(request.formula)
        stats = get_price_range(results) if results else {'min': 0, 'max': 0, 'avg': 0}
        
        return {
            'success': True,
            'query': request.formula,
            'dosage_filter': request.dosage_filter,
            'count': len(results),
            'available_dosages': dosages,
            'price_stats': stats,
            'results': results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# AUTOCOMPLETE ENDPOINTS
# ============================================================

@app.post("/api/autocomplete", tags=["Autocomplete"])
async def api_autocomplete(request: AutocompleteRequest):
    """
    Get medicine name and composition suggestions for autocomplete.
    
    Returns both medicine names and chemical compositions matching the query.
    """
    try:
        medicine_suggestions = autocomplete_medicine(request.query, max_suggestions=request.max_suggestions)
        composition_suggestions = autocomplete_composition(request.query, max_suggestions=5)
        
        return {
            'success': True,
            'query': request.query,
            'medicines': medicine_suggestions,
            'compositions': composition_suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search/multi", tags=["Search"])
async def api_multi_search(request: MultiSearchRequest):
    """
    Search across multiple fields (name, brand, composition, categories).
    
    Useful for general searches like "pain relief" or brand names.
    """
    try:
        results = multi_field_search(request.query, max_results=request.max_results)
        
        return {
            'success': True,
            'query': request.query,
            'count': len(results),
            'results': results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search/fuzzy", tags=["Search"])
async def api_fuzzy_search(request: FuzzySearchRequest):
    """
    Fuzzy search with typo tolerance and autocorrect.
    
    Example: "Panodol" will find "Panadol"
    """
    try:
        result = search_with_autocorrect(request.query, max_results=request.max_results)
        
        return {
            'success': True,
            'original_query': result.get('original_query', request.query),
            'corrected_to': result.get('corrected_to'),
            'count': len(result.get('results', [])),
            'results': result.get('results', [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# SIMILAR MEDICINES ENDPOINTS
# ============================================================

@app.post("/api/similar-medicines", tags=["Alternatives"])
async def api_similar_medicines(request: SimilarMedicinesRequest):
    """
    Find cheaper alternative medicines with the same composition.
    
    Shows savings percentage compared to the reference medicine.
    """
    try:
        reference = find_medicine_by_name(request.medicine_name)
        if not reference:
            raise HTTPException(
                status_code=404,
                detail=f'Medicine "{request.medicine_name}" not found'
            )
        
        alternatives = get_alternatives_with_savings(request.medicine_name, max_results=request.max_results)
        
        formatted_alternatives = []
        for med, savings in alternatives:
            alt_data = dict(med)
            alt_data['savings_percent'] = round(savings, 1)
            formatted_alternatives.append(alt_data)
        
        cheapest = find_cheapest_alternative(request.medicine_name)
        
        return {
            'success': True,
            'reference_medicine': reference,
            'alternatives_count': len(formatted_alternatives),
            'alternatives': formatted_alternatives,
            'cheapest': cheapest
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# AVAILABILITY ENDPOINTS
# ============================================================

@app.post("/api/check-availability", tags=["Availability"])
async def api_check_availability(request: AvailabilityRequest):
    """
    Check medicine availability on dawaai.pk in real-time.
    
    Returns stock status: in_stock, out_of_stock, or unknown.
    """
    try:
        result = check_medicine_availability(request.medicine_name, use_cache=True, verbose=False)
        
        if result == 1:
            status = 'in_stock'
            status_text = 'In Stock'
        elif result == 0:
            status = 'out_of_stock'
            status_text = 'Out of Stock'
        else:
            status = 'unknown'
            status_text = 'Unknown'
        
        return {
            'success': True,
            'medicine_name': request.medicine_name,
            'available': result,
            'status': status,
            'status_text': status_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# UTILITY ENDPOINTS
# ============================================================

@app.post("/api/dosages", tags=["Utilities"])
async def api_get_dosages(request: DosagesRequest):
    """
    Get all available dosages for a specific ingredient.
    
    Example: "Paracetamol" returns ["250mg", "500mg", "650mg", ...]
    """
    try:
        dosages = get_available_dosages(request.ingredient)
        
        return {
            'success': True,
            'ingredient': request.ingredient,
            'dosages': dosages,
            'count': len(dosages)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/medicine/{medicine_name}", tags=["Utilities"])
async def api_get_medicine(medicine_name: str):
    """
    Get details for a specific medicine by name.
    """
    try:
        medicine = find_medicine_by_name(medicine_name)
        
        if not medicine:
            raise HTTPException(
                status_code=404,
                detail=f'Medicine "{medicine_name}" not found'
            )
        
        return {
            'success': True,
            'medicine': medicine
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats", tags=["Utilities"])
async def api_stats():
    """
    Get database statistics including total medicines, brands, and categories.
    """
    try:
        medicines = load_medicines()
        
        brands = set()
        categories = set()
        compositions = set()
        
        for med in medicines:
            if med.get('brand'):
                brands.add(med.get('brand'))
            if med.get('categories'):
                for cat in med.get('categories', []):
                    categories.add(cat)
            if med.get('composition'):
                compositions.add(med.get('composition'))
        
        prices = []
        for med in medicines:
            price_str = med.get('price', '')
            if price_str:
                try:
                    price_val = float(''.join(c for c in price_str.replace(',', '') if c.isdigit() or c == '.'))
                    prices.append(price_val)
                except:
                    pass
        
        avg_price = sum(prices) / len(prices) if prices else 0
        
        return {
            'success': True,
            'total_medicines': len(medicines),
            'total_brands': len(brands),
            'total_categories': len(categories),
            'total_compositions': len(compositions),
            'avg_price': round(avg_price, 2),
            'data_completeness': '99%+'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# SYMPTOM SEARCH ENDPOINT
# ============================================================

@app.post("/api/symptom-search", tags=["AI Search"])
async def api_symptom_search(request: SymptomSearchRequest):
    """
    AI-powered symptom-based medicine search using Google Gemini.
    
    Describe your symptoms in natural language to get medicine recommendations.
    """
    try:
        # Import the symptom search agent (correct path)
        from src.agents.symptom_search_agent import SymptomSearchAgent
        
        agent = SymptomSearchAgent()
        result = agent.search(request.symptoms, max_results=request.max_results)
        
        # Build response with all data
        response = {
            'success': True,
            'symptoms': request.symptoms,
            'recommendations': result.get('recommendations', []),
            'ai_analysis': result.get('analysis', ''),
            'rag_used': result.get('rag_used', False),
            'rag_chunks': result.get('rag_chunks', 0),
            'disclaimer': 'This is for informational purposes only. Always consult a healthcare professional.'
        }
        
        print(f"✓ Symptom search completed: {len(response['recommendations'])} recommendations, RAG used: {response['rag_used']}")
        
        return response
        
    except ImportError as ie:
        # Fallback if agent not available - show actual error
        import traceback
        error_details = traceback.format_exc()
        print(f"ImportError in symptom search: {error_details}")
        return {
            'success': False,
            'error': f'Symptom search agent import failed: {str(ie)}',
            'symptoms': request.symptoms,
            'details': error_details if os.getenv('DEBUG') else 'Enable DEBUG mode for details'
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in symptom search: {error_details}")
        return {
            'success': False,
            'error': f'Symptom search error: {str(e)}',
            'symptoms': request.symptoms
        }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {
        'status': 'healthy',
        'service': 'MedFinder API',
        'version': '2.0.0',
        'framework': 'FastAPI'
    }


@app.get("/", tags=["Documentation"])
async def index():
    """API documentation redirect."""
    return {
        'service': 'MedFinder API',
        'version': '2.0.0',
        'framework': 'FastAPI',
        'documentation': '/docs',
        'alternative_docs': '/redoc',
        'endpoints': {
            'GET /api/health': 'Health check',
            'GET /api/stats': 'Database statistics',
            'POST /api/search/ingredient': 'Search by ingredient',
            'POST /api/search/composition': 'Search by composition with dosage filter',
            'POST /api/autocomplete': 'Get autocomplete suggestions',
            'POST /api/search/multi': 'Multi-field search',
            'POST /api/search/fuzzy': 'Fuzzy search with typo tolerance',
            'POST /api/similar-medicines': 'Find alternative medicines',
            'POST /api/check-availability': 'Check medicine availability',
            'POST /api/symptom-search': 'AI symptom-based search',
            'POST /api/dosages': 'Get available dosages',
            'GET /api/medicine/<name>': 'Get medicine details',
            'POST /api/prescription/search': 'Drug information from FDA/NIH',
            'POST /api/prescription/interaction-check': 'Check drug interactions'
        }
    }


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 MedFinder API Server (FastAPI)")
    print("=" * 60)
    print("\n🚀 Starting server on http://localhost:5000")
    print("\n📚 API Documentation:")
    print("   - Swagger UI: http://localhost:5000/docs")
    print("   - ReDoc:      http://localhost:5000/redoc")
    print("\n📡 Available endpoints:")
    print("   - GET  /api/health           - Health check")
    print("   - GET  /api/stats            - Database statistics")
    print("   - POST /api/search/ingredient - Search by ingredient")
    print("   - POST /api/autocomplete     - Autocomplete suggestions")
    print("   - POST /api/similar-medicines - Find alternatives")
    print("   - POST /api/check-availability - Check stock")
    print("   - POST /api/symptom-search   - AI symptom search")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    # Use import string format for reload support
    uvicorn.run("app:app", host='0.0.0.0', port=5000, reload=True)
