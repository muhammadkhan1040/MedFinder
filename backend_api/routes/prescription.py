"""
Prescription Assistant API Routes for MedFinder
================================================
Uses OpenFDA + AI for intelligent drug validation.
Optimized for speed with concurrent requests.

Trusted Sources:
- RxNorm (NIH/NLM) - Drug nomenclature and spelling
- OpenFDA - Drug labeling, interactions, adverse events
- DailyMed - FDA-approved drug information
- AI - Smart drug/condition validation
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import re
import os
from dotenv import load_dotenv
from functools import lru_cache
import difflib
import json

load_dotenv()

router = APIRouter()

# =============================================================================
# API Configuration
# =============================================================================
RXNAV_BASE = "https://rxnav.nlm.nih.gov/REST"
OPENFDA_BASE = "https://api.fda.gov/drug"
DAILYMED_BASE = "https://dailymed.nlm.nih.gov/dailymed/services/v2"

# Google Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Import Google Gemini
try:
    import google.generativeai as genai
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_MODEL = genai.GenerativeModel('gemini-1.5-flash')
        print("✓ Google Gemini configured for prescription assistant")
    else:
        GEMINI_MODEL = None
        print("ℹ Gemini API key not found - AI validation will be limited")
except ImportError:
    GEMINI_MODEL = None
    print("ℹ google-generativeai not installed - AI validation disabled")

# Faster timeout for better UX
TIMEOUT = 8
MISTRAL_TIMEOUT = 10

# Thread pool for concurrent requests
executor = ThreadPoolExecutor(max_workers=5)

# =============================================================================
# Pydantic Models
# =============================================================================
class DrugSearchRequest(BaseModel):
    drug_name: Optional[str] = None
    condition: Optional[str] = None
    search_type: str = "drug"
    drugs_for_interaction: Optional[List[str]] = None


class SpellingSuggestion(BaseModel):
    original: str
    suggestions: List[str]


class DrugBasicInfo(BaseModel):
    rxcui: str
    name: str
    synonym: Optional[str] = None
    tty: Optional[str] = None


class DrugInteraction(BaseModel):
    drug1: str
    drug2: str
    severity: str
    description: str
    source: str


class DosageInfo(BaseModel):
    form: str
    strength: str
    route: str
    instructions: Optional[str] = None


class DrugWarning(BaseModel):
    type: str
    description: str


class DrugSearchResponse(BaseModel):
    query: str
    drug_found: bool
    drug_info: Optional[DrugBasicInfo] = None
    spelling_suggestion: Optional[SpellingSuggestion] = None
    indications: List[str] = []
    dosage_forms: List[DosageInfo] = []
    contraindications: List[str] = []
    warnings: List[DrugWarning] = []
    interactions: List[DrugInteraction] = []
    interaction_text: Optional[str] = None
    side_effects: List[str] = []
    sources: List[dict] = []
    search_time_ms: int = 0


# =============================================================================
# Local Drug Index
# =============================================================================
COMMON_DRUGS = []


def load_common_drugs():
    """Load common drugs from JSON file"""
    global COMMON_DRUGS
    try:
        json_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "drug_index.json")
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                COMMON_DRUGS = json.load(f)
            print(f"✓ Loaded {len(COMMON_DRUGS)} drugs from local index.")
        else:
            print("Warning: drug_index.json not found. Using fallback list.")
            COMMON_DRUGS = ["Acetaminophen", "Advil", "Amoxicillin", "Aspirin", "Benadryl", 
                           "Ciprofloxacin", "Digoxin", "Ibuprofen", "Lisinopril", "Metformin",
                           "Naproxen", "Omeprazole", "Prednisone", "Simvastatin", "Tylenol",
                           "Verapamil", "Xanax", "Zyrtec"]
    except Exception as e:
        print(f"Error loading drug index: {e}")
        COMMON_DRUGS = ["Acetaminophen", "Ibuprofen", "Aspirin", "Metformin", "Lisinopril"]


# Load on module import
load_common_drugs()


@lru_cache(maxsize=1000)
def get_local_fuzzy_matches(term: str) -> List[str]:
    """Get instant suggestions using local fuzzy matching"""
    matches = difflib.get_close_matches(term.title(), COMMON_DRUGS, n=10, cutoff=0.5)
    return matches


# =============================================================================
# RxNorm API Functions
# =============================================================================
def get_spelling_suggestions(term: str) -> List[str]:
    """Get spelling suggestions from RxNorm"""
    try:
        url = f"{RXNAV_BASE}/spellingsuggestions.json"
        response = requests.get(url, params={"name": term}, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            suggestions = data.get("suggestionGroup", {}).get("suggestionList", {}).get("suggestion", [])
            return suggestions[:5] if suggestions else []
        return []
    except Exception as e:
        print(f"Spelling suggestion error: {e}")
        return []


def search_drug_by_name(drug_name: str) -> Optional[DrugBasicInfo]:
    """Search for drug using RxNorm"""
    try:
        # Try getDrugs for better results
        url = f"{RXNAV_BASE}/drugs.json"
        response = requests.get(url, params={"name": drug_name}, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            concept_groups = data.get("drugGroup", {}).get("conceptGroup", [])
            
            for group in concept_groups:
                concepts = group.get("conceptProperties", [])
                if concepts:
                    c = concepts[0]
                    return DrugBasicInfo(
                        rxcui=c.get("rxcui", ""),
                        name=c.get("name", drug_name),
                        synonym=c.get("synonym"),
                        tty=c.get("tty")
                    )
        
        # Fallback to rxcui search
        url = f"{RXNAV_BASE}/rxcui.json"
        response = requests.get(url, params={"name": drug_name, "search": 2}, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            rxcui_list = data.get("idGroup", {}).get("rxnormId", [])
            
            if rxcui_list:
                return DrugBasicInfo(
                    rxcui=rxcui_list[0],
                    name=drug_name,
                    tty="IN"
                )
        
        return None
    except Exception as e:
        print(f"Drug search error: {e}")
        return None


# =============================================================================
# AI Validation Functions
# =============================================================================
@lru_cache(maxsize=100)
def validate_drug_with_ai_cached(user_input: str) -> dict:
    """Cached wrapper for AI validation"""
    return validate_drug_with_ai(user_input)


def validate_drug_with_ai(user_input: str) -> dict:
    """
    Use Google Gemini AI to validate if input is a valid drug/condition 
    and suggest corrections for misspellings.
    """
    if not GEMINI_MODEL:
        return {"valid": None, "suggestions": [], "message": "AI validation not available"}
    
    try:
        prompt = f"""You are a medical/pharmaceutical expert. Analyze this drug name: "{user_input}"

Is this a valid drug name? If it's misspelled, what is the correct spelling?

Respond in this exact format:
VALID: yes/no
CORRECT_NAME: [correct drug name if misspelled, otherwise same name]
SUGGESTIONS: [comma-separated list of similar drug names]

Example response:
VALID: no
CORRECT_NAME: Aspirin
SUGGESTIONS: Aspirin, Acetylsalicylic acid

Your response:"""

        generation_config = genai.types.GenerationConfig(
            temperature=0.1,
            max_output_tokens=150,
        )
        
        response = GEMINI_MODEL.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        if response and response.text:
            message = response.text.strip()
            
            # Parse the response
            is_valid = "VALID: yes" in message or "VALID:yes" in message
            
            is_valid_drug = False
            if bool(is_valid):
                 is_valid_drug = True

            # Extract corrected name
            corrected_name = user_input
            if "CORRECT_NAME:" in message:
                lines = message.split('\n')
                for line in lines:
                    if "CORRECT_NAME:" in line:
                        parts = line.split("CORRECT_NAME:")
                        if len(parts) > 1:
                            name_part = parts[1].strip()
                            corrected_name = name_part.split(',')[0].strip()
                            break
            
            # Extract suggestions
            suggestions = []
            if "SUGGESTIONS:" in message:
                lines = message.split('\n')
                for line in lines:
                    if "SUGGESTIONS:" in line:
                        parts = line.split("SUGGESTIONS:")
                        if len(parts) > 1:
                            sugg_part = parts[1].strip()
                            suggestions = [s.strip() for s in sugg_part.split(",") if s.strip()]
                            break
            
            # If no suggestions but got corrected name, add it
            if corrected_name.lower() != user_input.lower() and corrected_name not in suggestions:
                suggestions.insert(0, corrected_name)
            
            return {
                "valid": is_valid_drug,
                "corrected_name": corrected_name if corrected_name.lower() != user_input.lower() else None,
                "suggestions": suggestions[:5],
                "raw_response": message
            }
        else:
            return {"valid": None, "suggestions": [], "message": "No response from AI"}
        
    except Exception as e:
        print(f"Gemini AI validation error: {e}")
        return {"valid": None, "suggestions": [], "message": str(e)}


def get_smart_suggestions(user_input: str) -> dict:
    """
    Get smart suggestions combining Local, RxNorm and AI.
    Optimized for speed.
    """
    result = {
        "original": user_input,
        "corrected": None,
        "suggestions": [],
        "is_valid": False,
        "message": None
    }
    
    # 1. Try local fuzzy matching (INSTANT <1ms)
    local_matches = get_local_fuzzy_matches(user_input)
    if local_matches:
        # If we have a high-confidence match (exact (ignoring case) or very close)
        if local_matches[0].lower() == user_input.lower():
            result["is_valid"] = True
            result["corrected"] = local_matches[0]
            return result
            
        result["suggestions"].extend(local_matches)
        result["corrected"] = local_matches[0]
        # Return immediately if we have any local matches (skip API calls for speed)
        if len(local_matches) > 0:
             result["message"] = f"Did you mean: {', '.join(local_matches[:3])}?"
             return result

    # 2. Run API checks in parallel (concurrent)
    with ThreadPoolExecutor(max_workers=2) as ex:
        # RxNorm usually faster
        rxnorm_future = ex.submit(get_spelling_suggestions, user_input)
        # AI slower but smarter
        ai_future = ex.submit(validate_drug_with_ai_cached, user_input)
        
        rxnorm_suggestions = rxnorm_future.result()
        mistral_result = ai_future.result()
    
    # Combine results
    if mistral_result.get("valid"):
        result["is_valid"] = True
        result["corrected"] = mistral_result.get("corrected_name", user_input)
    
    # Merge suggestions (Priority: AI > Local > RxNorm)
    all_suggestions = []
    
    if mistral_result.get("corrected_name") and mistral_result["corrected_name"].lower() != user_input.lower():
        all_suggestions.append(mistral_result["corrected_name"])
    
    all_suggestions.extend(mistral_result.get("suggestions", []))
    all_suggestions.extend(local_matches) # Add local matches if AI didn't catch them
    all_suggestions.extend(rxnorm_suggestions)
    
    # Deduplicate and limit
    seen = set()
    unique_suggestions = []
    # Normalize input for comparison
    input_lower = user_input.lower()
    
    for s in all_suggestions:
        if s and s.lower() not in seen:
            # Don't suggest the misspelled word itself
            if s.lower() != input_lower:
                seen.add(s.lower())
                unique_suggestions.append(s)
    
    result["suggestions"] = unique_suggestions[:10]
    
    if not result["is_valid"] and result["suggestions"]:
        result["message"] = f"Did you mean: {', '.join(result['suggestions'][:3])}?"
    
    return result


# =============================================================================
# OpenFDA API Functions
# =============================================================================
def get_drug_label_info(drug_name: str) -> dict:
    """Get drug labeling from OpenFDA - includes interactions"""
    try:
        url = f"{OPENFDA_BASE}/label.json"
        # Search both brand and generic names
        search_query = f'openfda.brand_name:"{drug_name}" OR openfda.generic_name:"{drug_name}"'
        response = requests.get(url, params={"search": search_query, "limit": 1}, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                label = results[0]
                openfda = label.get("openfda", {})
                
                # Get the set_id for DailyMed link
                set_id = label.get("set_id", openfda.get("spl_set_id", [""])[0] if openfda.get("spl_set_id") else "")
                
                return {
                    "indications": label.get("indications_and_usage", []),
                    "contraindications": label.get("contraindications", []),
                    "warnings": label.get("warnings", []),
                    "boxed_warning": label.get("boxed_warning", []),
                    "dosage": label.get("dosage_and_administration", []),
                    "adverse_reactions": label.get("adverse_reactions", []),
                    "drug_interactions": label.get("drug_interactions", []),
                    "pregnancy": label.get("pregnancy", []),
                    "set_id": set_id,
                    "brand_name": openfda.get("brand_name", [""])[0] if openfda.get("brand_name") else drug_name,
                    "generic_name": openfda.get("generic_name", [""])[0] if openfda.get("generic_name") else "",
                    "manufacturer": openfda.get("manufacturer_name", [""])[0] if openfda.get("manufacturer_name") else ""
                }
        return {}
    except Exception as e:
        print(f"OpenFDA label error: {e}")
        return {}


def get_adverse_events(drug_name: str) -> List[str]:
    """Get top reported adverse events from OpenFDA"""
    try:
        url = f"{OPENFDA_BASE}/event.json"
        params = {
            "search": f'patient.drug.medicinalproduct:"{drug_name}"',
            "count": "patient.reaction.reactionmeddrapt.exact",
            "limit": 10
        }
        response = requests.get(url, params=params, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            return [r.get("term", "") for r in data.get("results", []) if r.get("term")]
        return []
    except Exception as e:
        print(f"Adverse events error: {e}")
        return []


def check_drug_interaction_fda(drug1: str, drug2: str) -> Optional[dict]:
    """Check if drug2 is mentioned in drug1's interaction section"""
    try:
        label = get_drug_label_info(drug1)
        interaction_sections = label.get("drug_interactions", [])
        
        if not interaction_sections:
            return None
            
        interactions_text = " ".join(interaction_sections)
        interactions_lower = interactions_text.lower()
        
        if drug2.lower() in interactions_lower:
            # Extract context around drug2 mention
            paragraphs = interactions_text.split('\n')
            relevant_parts = []
            
            for para in paragraphs:
                if drug2.lower() in para.lower() and len(para.strip()) > 30:
                    clean_para = re.sub(r'\s+', ' ', para).strip()
                    if len(clean_para) > 50:
                        relevant_parts.append(clean_para)
            
            if not relevant_parts:
                sentences = re.split(r'[.!?]', interactions_text)
                for sent in sentences:
                    if drug2.lower() in sent.lower() and len(sent.strip()) > 30:
                        relevant_parts.append(sent.strip() + ".")
            
            if relevant_parts:
                description = relevant_parts[0][:600]
                
                # Add severity indicator based on keywords
                severity = "Moderate"
                if any(word in description.lower() for word in ['contraindicated', 'avoid', 'do not', 'serious', 'fatal', 'death']):
                    severity = "Major - Avoid"
                elif any(word in description.lower() for word in ['caution', 'monitor', 'adjust', 'reduce']):
                    severity = "Moderate - Monitor"
                
                return {
                    "found": True,
                    "drug1": drug1.title(),
                    "drug2": drug2.title(),
                    "description": description,
                    "severity": severity,
                    "source": "OpenFDA Drug Label"
                }
        return None
    except Exception as e:
        print(f"Interaction check error: {e}")
        return None


def check_interactions_between_drugs(drugs: List[str]) -> List[DrugInteraction]:
    """Check interactions between a list of drugs using FDA labels"""
    interactions = []
    
    # Check each pair
    for i, drug1 in enumerate(drugs):
        for drug2 in drugs[i+1:]:
            # Check both directions concurrently
            futures = []
            with ThreadPoolExecutor(max_workers=2) as ex:
                futures.append(ex.submit(check_drug_interaction_fda, drug1, drug2))
                futures.append(ex.submit(check_drug_interaction_fda, drug2, drug1))
                
                for future in as_completed(futures):
                    result = future.result()
                    if result and result.get("found"):
                        interactions.append(DrugInteraction(
                            drug1=result["drug1"],
                            drug2=result["drug2"],
                            severity=result.get("severity", "Check Label"),
                            description=result["description"],
                            source=result["source"]
                        ))
    
    # Deduplicate
    seen = set()
    unique = []
    for i in interactions:
        key = tuple(sorted([i.drug1.lower(), i.drug2.lower()]))
        if key not in seen:
            seen.add(key)
            unique.append(i)
    
    return unique


# =============================================================================
# Text Processing
# =============================================================================
def clean_fda_text(text_list: List[str], max_items: int = 5) -> List[str]:
    """Clean FDA label text"""
    if not text_list:
        return []
    
    cleaned = []
    for text in text_list:
        if not text:
            continue
        # Remove section headers like "7.1 DRUG INTERACTIONS"
        text = re.sub(r'^\d+(\.\d+)?\s+[A-Z\s]+\s+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split and filter
        sentences = text.split('.')
        for sent in sentences:
            sent = sent.strip()
            if len(sent) > 30 and len(sent) < 400:
                cleaned.append(sent + ".")
                if len(cleaned) >= max_items:
                    return cleaned
    
    return cleaned[:max_items]


def extract_interaction_drugs(interaction_text: str) -> List[str]:
    """Extract drug names mentioned in interaction text"""
    common_drugs = [
        'warfarin', 'digoxin', 'verapamil', 'aspirin', 'ibuprofen', 'metformin',
        'lisinopril', 'amlodipine', 'omeprazole', 'simvastatin', 'atorvastatin',
        'metoprolol', 'losartan', 'gabapentin', 'hydrocodone', 'tramadol',
        'cyclosporine', 'lithium', 'phenytoin', 'carbamazepine', 'rifampin'
    ]
    
    found = []
    text_lower = interaction_text.lower()
    for drug in common_drugs:
        if drug in text_lower:
            found.append(drug.title())
    
    return found[:10]


# =============================================================================
# API Endpoints
# =============================================================================
@router.post("/search")
async def search_prescription(request: DrugSearchRequest) -> DrugSearchResponse:
    """Search for drug information from trusted sources"""
    start_time = datetime.now()
    
    try:
        response = DrugSearchResponse(
            query=request.drug_name or request.condition or "",
            drug_found=False,
            sources=[]
        )
        
        if not request.drug_name:
            return response
        
        drug_name = request.drug_name.strip()
        
        # STEP 1: LOCAL VALIDATION FIRST
        local_matches = get_local_fuzzy_matches(drug_name)
        
        if local_matches:
            top_match = local_matches[0]
            ratio = difflib.SequenceMatcher(None, drug_name.lower(), top_match.lower()).ratio()
            
            # If NOT an exact match and we have suggestions, return them
            if ratio < 1.0 and ratio >= 0.5:
                end_time = datetime.now()
                response.search_time_ms = int((end_time - start_time).total_seconds() * 1000)
                response.spelling_suggestion = SpellingSuggestion(
                    original=drug_name,
                    suggestions=local_matches[:10]
                )
                return response
            
            # If exact match found locally, use canonical name
            if ratio == 1.0:
                drug_name = top_match
        
        # STEP 2: Make API calls only for valid/corrected names
        with ThreadPoolExecutor(max_workers=3) as ex:
            drug_future = ex.submit(search_drug_by_name, drug_name)
            label_future = ex.submit(get_drug_label_info, drug_name)
            adverse_future = ex.submit(get_adverse_events, drug_name)
            
            # Get drug info
            drug_info = drug_future.result()
            if drug_info:
                response.drug_found = True
                response.drug_info = drug_info
                response.query = drug_info.name
                response.sources.append({
                    "name": "RxNorm (NIH/NLM)",
                    "url": f"https://mor.nlm.nih.gov/RxNav/search?searchBy=String&searchTerm={drug_info.name}"
                })
            
            # Get FDA label info
            fda_info = label_future.result()
            if fda_info:
                response.drug_found = True
                
                # Indications
                if fda_info.get("indications"):
                    response.indications = clean_fda_text(fda_info["indications"])
                
                # Contraindications
                if fda_info.get("contraindications"):
                    response.contraindications = clean_fda_text(fda_info["contraindications"])
                
                # Warnings
                warnings = []
                if fda_info.get("boxed_warning"):
                    for w in clean_fda_text(fda_info["boxed_warning"], 2):
                        warnings.append(DrugWarning(type="blackbox", description=w))
                if fda_info.get("warnings"):
                    for w in clean_fda_text(fda_info["warnings"], 3):
                        warnings.append(DrugWarning(type="warning", description=w))
                response.warnings = warnings
                
                # Dosage
                if fda_info.get("dosage"):
                    for d in clean_fda_text(fda_info["dosage"], 3):
                        response.dosage_forms.append(DosageInfo(
                            form="See label",
                            strength="As prescribed",
                            route="See label",
                            instructions=d
                        ))
                
                # Drug interactions
                if fda_info.get("drug_interactions"):
                    interaction_text = " ".join(fda_info["drug_interactions"])
                    response.interaction_text = interaction_text[:2000]
                    
                    # Extract specific drug interactions
                    mentioned_drugs = extract_interaction_drugs(interaction_text)
                    for mentioned in mentioned_drugs:
                        if mentioned.lower() != drug_name.lower():
                            response.interactions.append(DrugInteraction(
                                drug1=drug_name,
                                drug2=mentioned,
                                severity="See Label",
                                description=f"See drug interactions section for details about {mentioned}",
                                source="OpenFDA"
                            ))
                
                # DailyMed source
                set_id = fda_info.get("set_id")
                if set_id:
                    response.sources.append({
                        "name": "DailyMed (FDA)",
                        "url": f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={set_id}"
                    })
                
                # OpenFDA source
                brand = fda_info.get("brand_name", drug_name)
                response.sources.append({
                    "name": "OpenFDA Label",
                    "url": f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:\"{brand}\"&limit=1"
                })
            
            # Get adverse events
            adverse = adverse_future.result()
            if adverse:
                response.side_effects = adverse
                response.sources.append({
                    "name": "FDA Adverse Event Reports",
                    "url": f"https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:\"{drug_name}\"&count=patient.reaction.reactionmeddrapt.exact"
                })
            
            # Spelling suggestions if no drug found
            if not response.drug_found:
                smart = get_smart_suggestions(drug_name)
                if smart.get("suggestions"):
                    response.spelling_suggestion = SpellingSuggestion(
                        original=drug_name,
                        suggestions=smart["suggestions"]
                    )
        
        end_time = datetime.now()
        response.search_time_ms = int((end_time - start_time).total_seconds() * 1000)
        
        return response
    
    except Exception as e:
        import traceback
        print(f"Prescription search error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.post("/interaction-check")
async def check_interactions(drugs: List[str]) -> dict:
    """Check drug-drug interactions between multiple drugs using FDA labels"""
    if len(drugs) < 2:
        raise HTTPException(status_code=400, detail="At least 2 drugs required")
    
    if len(drugs) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 drugs allowed")
    
    start_time = datetime.now()
    
    # Clean drug names
    clean_drugs = [d.strip() for d in drugs if d.strip()]
    
    if len(clean_drugs) < 2:
        raise HTTPException(status_code=400, detail="At least 2 valid drug names required")
    
    # Validate each drug using LOCAL fuzzy matching
    validated_drugs = []
    drug_suggestions = {}
    has_corrections = False
    
    for drug in clean_drugs:
        local_matches = get_local_fuzzy_matches(drug)
        
        if local_matches:
            top_match = local_matches[0]
            ratio = difflib.SequenceMatcher(None, drug.lower(), top_match.lower()).ratio()
            
            if ratio == 1.0:
                validated_drugs.append(top_match)
            elif ratio >= 0.5:
                drug_suggestions[drug] = {
                    "corrected": top_match,
                    "suggestions": local_matches[:5]
                }
                has_corrections = True
                validated_drugs.append(top_match)
            else:
                validated_drugs.append(drug)
        else:
            validated_drugs.append(drug)
    
    # Check interactions using FDA labels
    interactions = check_interactions_between_drugs(validated_drugs)
    
    end_time = datetime.now()
    search_time = int((end_time - start_time).total_seconds() * 1000)
    
    result = {
        "drugs_checked": validated_drugs,
        "original_input": clean_drugs,
        "interactions_found": len(interactions),
        "interactions": [i.dict() for i in interactions],
        "source": "OpenFDA Drug Labels",
        "search_time_ms": search_time,
        "note": "Interactions are extracted from FDA-approved drug labeling. Always verify with a healthcare professional."
    }
    
    if has_corrections:
        result["spelling_corrections"] = drug_suggestions
        result["had_corrections"] = True
    
    return result
