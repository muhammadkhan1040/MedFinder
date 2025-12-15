# MedFinder Prescription Assistant

## Overview
The Prescription Assistant feature provides evidence-based drug information from trusted medical sources including FDA, NIH, and DailyMed.

## Features
- **Drug Information Search**: Get comprehensive information about any drug including:
  - Indications and approved uses
  - Dosage and administration guidelines
  - Warnings and contraindications
  - Known drug interactions
  - Reported side effects
  
- **Drug Interaction Checker**: Check for potential interactions between multiple drugs (2-5 drugs)

- **AI-Powered Validation**: Smart drug name validation and spelling correction using AI

- **Trusted Sources**:
  - RxNorm (NIH/NLM) - Drug nomenclature
  - OpenFDA - Drug labeling and safety information
  - DailyMed - FDA-approved drug information

## Setup

### Backend Setup

1. **Environment Variables**
   Copy `.env.example` to `.env` and add your HuggingFace API token:
   ```bash
   HF_TOKEN=your_huggingface_token_here
   ```
   
   Get your API token from: https://huggingface.co/settings/tokens

2. **Dependencies**
   The required dependencies are already in `backend_api/requirements.txt`:
   ```bash
   cd backend_api
   pip install -r requirements.txt
   ```

3. **Drug Index Data**
   The drug index file (`drug_index.json`) is located in the `data` folder and contains 
   a comprehensive list of common drug names for fast local fuzzy matching.

### Frontend Setup
No additional setup required. The prescription assistant is integrated into the main MedFinder frontend.

## Usage

### Accessing the Feature
Navigate to `/prescription` in the MedFinder application or click "Prescription" in the navbar.

### Drug Search
1. Select "Drug Search" tab
2. Enter a drug name (e.g., "Aspirin", "Metformin", "Lisinopril")
3. Click "Search Drug Information"
4. View comprehensive drug information including:
   - Uses and indications
   - Dosage guidelines
   - Warnings and precautions
   - Known interactions
   - Side effects
   - Links to official sources

### Interaction Check
1. Select "Interaction Check" tab
2. Enter 2-5 drug names
3. Click "Check Drug Interactions"
4. Review interaction analysis and severity ratings

## API Endpoints

### POST /api/prescription/search
Search for drug information.

**Request Body:**
```json
{
  "drug_name": "Aspirin",
  "search_type": "drug"
}
```

**Response:**
```json
{
  "query": "Aspirin",
  "drug_found": true,
  "drug_info": {
    "rxcui": "1191",
    "name": "Aspirin",
    "tty": "IN"
  },
  "indications": [...],
  "dosage_forms": [...],
  "contraindications": [...],
  "warnings": [...],
  "interactions": [...],
  "side_effects": [...],
  "sources": [...],
  "search_time_ms": 1234
}
```

### POST /api/prescription/interaction-check
Check drug-drug interactions.

**Request Body:**
```json
["Warfarin", "Aspirin", "Ibuprofen"]
```

**Response:**
```json
{
  "drugs_checked": ["Warfarin", "Aspirin", "Ibuprofen"],
  "interactions_found": 2,
  "interactions": [
    {
      "drug1": "Warfarin",
      "drug2": "Aspirin",
      "severity": "Major - Avoid",
      "description": "...",
      "source": "OpenFDA Drug Label"
    }
  ],
  "search_time_ms": 2345
}
```

## Data Sources

### Local Drug Index
- **File**: `data/drug_index.json`
- **Purpose**: Fast local fuzzy matching for instant suggestions
- **Contains**: ~20,000+ common drug names

### External APIs

1. **RxNorm (NIH/NLM)**
   - Drug nomenclature and spelling suggestions
   - No API key required
   - Base URL: https://rxnav.nlm.nih.gov/REST

2. **OpenFDA**
   - Drug labeling information
   - Adverse event reports
   - Drug interactions
   - No API key required
   - Base URL: https://api.fda.gov/drug

3. **DailyMed (FDA)**
   - FDA-approved drug information
   - Official drug labels
   - Base URL: https://dailymed.nlm.nih.gov/dailymed

4. **HuggingFace AI (Optional)**
   - Smart drug name validation
   - Spelling correction
   - Requires API token
   - Model: meta-llama/Meta-Llama-3-70B-Instruct

## Technology Stack

### Backend
- FastAPI - API framework
- Python 3.8+
- Concurrent request processing (ThreadPoolExecutor)
- LRU caching for performance

### Frontend
- React with Hooks
- Framer Motion for animations
- Lucide React icons
- Tailwind CSS (white/purple theme)

## Performance Optimizations

1. **Local Fuzzy Matching**: Instant suggestions (<1ms) using local drug index
2. **Concurrent API Requests**: Parallel requests to multiple sources
3. **LRU Caching**: Cached AI validation responses
4. **Smart Timeouts**: Fast timeouts (8s) for better UX

## Important Disclaimers

⚠️ **Medical Disclaimer**:
- Information is for educational and research purposes only
- Always consult a qualified healthcare professional
- Drug information may change; verify with current prescribing information
- Not a substitute for professional medical advice

## Troubleshooting

### Common Issues

1. **"AI validation not available"**
   - Ensure `HF_TOKEN` is set in `.env`
   - Verify your HuggingFace token is valid
   - AI validation is optional; drug search still works without it

2. **"Drug not found"**
   - Check spelling
   - Try generic name instead of brand name (or vice versa)
   - Use the spelling suggestions provided

3. **"No interactions found"**
   - Interactions are only shown if documented in FDA labels
   - Absence of documented interaction doesn't mean drugs are safe together
   - Always consult a healthcare professional

## Future Enhancements
- Support for herbal supplements and OTC medications
- Pregnancy and breastfeeding safety information
- Dosage calculators based on weight/age
- Drug comparison tool
- Printable medication guides

## License
This feature uses publicly available data from FDA, NIH, and other government sources.
