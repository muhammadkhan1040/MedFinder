# MedFinder Testing Suite

This directory contains comprehensive testing scripts for the MedFinder system.

## Test Scripts

### 1. `test_llm_comparison.py`
**LLM Comparison Test Suite**

Evaluates three LLMs (Gemini-1.5-Flash, DeepSeek-V2, Mistral-7B) on medicine recommendation tasks.

**Metrics:**
- Precision@5
- Recall@10
- MAP@10 (Mean Average Precision)
- NDCG@5 (Normalized Discounted Cumulative Gain)
- Response Latency

**Usage:**
```bash
python test/test_llm_comparison.py
```

**Output:** `test/llm_comparison_results.json`

---

### 2. `test_search_performance.py`
**Search Engine Performance Test Suite**

Tests all search functionalities across the system.

**Search Types Tested:**
- Ingredient Search
- Formula Search
- Alternative Finder
- Autocomplete
- Fuzzy Search

**Metrics:**
- Precision
- Recall
- F1-Score
- Average Results
- Latency (milliseconds)

**Usage:**
```bash
python test/test_search_performance.py
```

**Output:** `test/search_performance_results.json`

---

### 3. `test_ablation_study.py`
**Ablation Study Test Suite**

Systematic evaluation of RAG architecture components.

**Ablations Tested:**
- **Chunk Size Variations:** 256, 512, 1024 tokens
- **Retrieval Depth:** top-3, top-5, top-10 chunks
- **Temperature:** 0.0, 0.1, 0.3, 0.7
- **Component Removal:** No RAG, No LLM, No threshold

**Usage:**
```bash
python test/test_ablation_study.py
```

**Output:** `test/ablation_results.json`

---

### 4. `test_availability.py`
**Availability Checker Performance Test**

Tests real-time medicine availability checking system.

**Tests:**
- First Check Latency (API calls)
- Cached Check Latency
- API Reliability
- Cache Hit Rate

**Usage:**
```bash
python test/test_availability.py
```

**Output:** `test/availability_test_results.json`

---

### 5. `test_cost_savings.py`
**Cost Savings Analysis Test**

Analyzes potential cost savings through generic substitution.

**Analyses:**
- Savings by Individual Medicine
- Savings by Therapeutic Category
- Population-Level Impact

**Usage:**
```bash
python test/test_cost_savings.py
```

**Output:** `test/cost_savings_results.json`

---

## Test Data

### `test_queries.json`
Contains 150 symptom queries across 12 therapeutic categories with ground truth annotations by pharmacists.

**Format:**
```json
{
  "category": "pain_management",
  "query": "I have severe headache and fever",
  "ground_truth": ["Paracetamol", "Ibuprofen"]
}
```

---

## Running All Tests

To run the complete test suite:

```bash
# Run all tests sequentially
python test/test_llm_comparison.py
python test/test_search_performance.py
python test/test_ablation_study.py
python test/test_availability.py
python test/test_cost_savings.py
```

---

## Expected Results

Based on the research paper, expected performance:

### LLM Comparison
| Model | Precision@5 | Recall@10 | MAP@10 | NDCG@5 |
|-------|-------------|-----------|--------|---------|
| Gemini-1.5-Flash | 0.942 | 0.918 | 0.887 | 0.912 |
| DeepSeek-V2 | 0.876 | 0.853 | 0.821 | 0.869 |
| Mistral-7B | 0.831 | 0.804 | 0.778 | 0.825 |

### Search Performance
| Search Type | Precision | Recall | F1-Score | Latency |
|-------------|-----------|---------|----------|---------|
| Ingredient | 0.983 | 0.976 | 0.979 | 67ms |
| Formula | 1.000 | 0.994 | 0.997 | 53ms |
| Alternative | 1.000 | 0.982 | 0.991 | 41ms |
| Autocomplete | 0.957 | 0.941 | 0.949 | 8ms |
| Fuzzy | 0.891 | 0.923 | 0.907 | 124ms |

### Ablation Study
- **Optimal Chunk Size:** 512 tokens
- **Optimal Top-K:** 5 chunks
- **Optimal Temperature:** 0.1
- **RAG Improvement:** 23.8% over LLM-only

### Availability
- **First Check:** ~500ms
- **Cached Check:** ~80ms
- **Cache Hit Rate:** 73.2%
- **Reliability:** 99.7%

### Cost Savings
- **Average Savings:** 50-90%
- **Max Savings (Diabetes):** 81.4%
- **Annual Impact:** Rs. 12,300 - 89,400

---

## Prerequisites

Ensure all dependencies are installed:

```bash
pip install -r backend_api/requirements.txt
```

Required packages:
- Python 3.8+
- fastapi
- requests
- google-generativeai
- faiss-cpu
- scikit-learn

---

## Notes

- Tests use real medicine database (20,469 medicines)
- LLM tests require valid API keys in `.env` file
- Some tests may take several minutes to complete
- Results are saved as JSON for further analysis

---

## Troubleshooting

**Issue:** Import errors
**Solution:** Ensure you run tests from project root directory

**Issue:** API timeouts
**Solution:** Check internet connection and API key validity

**Issue:** Missing test data
**Solution:** Verify `data/medicines.json` exists

---

## Contributing

To add new tests:
1. Create test script in `test/` directory
2. Follow naming convention: `test_*.py`
3. Include docstring explaining test purpose
4. Save results to `test/*_results.json`
5. Update this README

---

## Citation

If you use these testing scripts, please cite:

```bibtex
@article{medfinder2024,
  title={MedFinder: An Intelligent Medicine Search and Recommendation System Using RAG},
  author={Khan, Muhammad and Tariq, Ubaida},
  year={2024},
  institution={FAST-NUCES}
}
```
