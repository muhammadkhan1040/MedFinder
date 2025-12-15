"""
Symptom Search Agent - RAG Based
Uses embedding model (port 8081) for retrieval + Gemini LLM with medical-only fallback
"""
import sys
import os
from typing import Dict, List, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from llm_client import get_llm_client
from utils import load_medicines

try:
    from traditional_rag.retriever import TraditionalRetriever
    HAS_RAG = True
except:
    HAS_RAG = False
    print("Warning: RAG retriever not available")


class SymptomSearchAgent:
    """RAG-based symptom search with embedding model + LLM fallback"""
    
    def __init__(self):
        self.llm_client = get_llm_client()
        self.medicines = load_medicines()
        
        # Initialize RAG retriever (uses embedding model on port 8081)
        self.rag_retriever = None
        if HAS_RAG:
            try:
                self.rag_retriever = TraditionalRetriever()
                print("✓ RAG retriever initialized with embedding model")
            except Exception as e:
                print(f"Warning: Could not initialize RAG retriever: {e}")
        
        if not self.llm_client or not self.llm_client.client:
            raise ImportError("Google Gemini API not configured. Please set GEMINI_API_KEY in .env file")
    
    def search(self, symptoms: str, max_results: int = 5) -> Dict[str, Any]:
        """
        RAG-based symptom search workflow:
        1. Retrieve relevant medical context using embedding model
        2. Send context + query to LLM
        3. LLM can use its knowledge if RAG context insufficient (medical-only)
        
        Args:
            symptoms: User-described symptoms
            max_results: Maximum number of recommendations
            
        Returns:
            Dict with recommendations and AI analysis
        """
        # Step 1: Retrieve relevant context using RAG  (embedding model on port 8081)
        rag_context = self._retrieve_rag_context(symptoms)
        
        # Step 2: Build prompt with RAG context + medical-only constraint
        prompt = self._build_rag_prompt(symptoms, rag_context, max_results)
        
        # Step 3: Get LLM response
        # Lower token limit forces concise responses
        ai_response = self.llm_client.complete(
            prompt=prompt,
            temperature=0.2,  # Slightly higher for faster completion
            max_tokens=1500   # REDUCED to force brief responses
        )
        
        if not ai_response:
            return {
                'recommendations': [],
                'analysis': 'Unable to get AI response. Please try again.',
                'rag_used': bool(rag_context),
                'error': 'No response from AI'
            }
        
        # Log for debugging
        print(f"\n{'='*60}")
        print(f"LLM Response (first 500 chars):\n{ai_response[:500]}...")
        print(f"LLM Response (last 200 chars):\n...{ai_response[-200:]}")
        print(f"Total response length: {len(ai_response)} characters")
        print(f"{'='*60}\n")
        
        # Step 4: Parse response and match with medicine database
        recommendations = self._parse_and_match_medicines(ai_response, max_results)
        
        return {
            'recommendations': recommendations,
            'analysis': ai_response[:1000],  # Limit raw response to 1000 chars for frontend
            'symptom_query': symptoms,
            'rag_used': bool(rag_context),
            'rag_chunks': len(rag_context) if rag_context else 0
        }
    
    def _retrieve_rag_context(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant medical context using RAG
        Uses embedding model (port 8081) for vector search
        """
        if not self.rag_retriever:
            return []
        
        try:
            # Retrieve top chunks from FAISS index
            results = self.rag_retriever.retrieve(query, top_k=5)
            
            # Filter by relevance score (>= 0.5)
            relevant_chunks = [r for r in results if r['score'] >= 0.5]
            
            return relevant_chunks
        except Exception as e:
            print(f"RAG retrieval error: {e}")
            return []
    
    def _build_rag_prompt(self, symptoms: str, rag_context: List[Dict], max_results: int) -> str:
        """Build prompt that forces LLM to return structured JSON - OPTIMIZED FOR CONCISENESS"""
        
        # Limit to 3 recommendations max for guaranteed complete JSON
        max_results = min(max_results, 3)
        
        # Build context section from RAG chunks
        context_section = ""
        if rag_context:
            context_section = "\n\nMEDICAL SOURCES:\n"
            for i, chunk in enumerate(rag_context[:2], 1):  # Only 2 chunks to reduce length
                context_section += f"[{i}] {chunk['text'][:250]}...\n"
        
        prompt = f"""Medical AI: Analyze symptoms, return ONLY valid JSON (no markdown).

SYMPTOMS: {symptoms}
{context_section}

Return {max_results} OTC medicines. USE PAKISTAN MEDICINES. KEEP BRIEF.

JSON FORMAT (copy exactly):
{{
  "is_medical_query": true,
  "analysis": "Brief 1-sentence analysis",
  "recommendations": [
    {{
      "rank": 1,
      "chemical_formula": "Paracetamol",
      "dosage": "500mg every 6 hours",
      "reason": "Brief reason",
      "warnings": "Brief warning",
      "requires_doctor": false
    }}
  ],
  "requires_immediate_attention": false,
  "disclaimer": "Consult healthcare professional"
}}

RULES:
- If not medical: {{"error": "Not medical"}}
- {'Use sources above' if rag_context else 'Use knowledge'}
- Generic names only
- Keep ALL text brief
- Close ALL brackets

RETURN ONLY JSON:"""
        
        return prompt
    
    def _parse_and_match_medicines(self, ai_response: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Parse structured JSON from LLM and match chemical formulas to database
        This is the core agentic pipeline step
        """
        import json
        import re
        
        recommendations = []
        
        try:
            # Step 1: Clean and extract JSON from response
            cleaned_response = ai_response.strip()
            
            # Remove markdown code blocks (```json ... ``` or ``` ... ```)
            if '```' in cleaned_response:
                # Extract content between code blocks
                code_block_pattern = r'```(?:json)?\s*(.*?)\s*```'
                matches = re.findall(code_block_pattern, cleaned_response, re.DOTALL)
                if matches:
                    cleaned_response = matches[0]  # Use first code block
                else:
                    # Remove ``` markers manually
                    cleaned_response = cleaned_response.replace('```json', '').replace('```', '')
            
            # Find JSON object boundaries
            start_idx = cleaned_response.find('{')
            end_idx = cleaned_response.rfind('}')
            
            if start_idx == -1:
                raise ValueError("No opening brace found in response")
            if end_idx == -1 or end_idx <= start_idx:
                # Try to find last complete recommendation
                print("⚠ JSON appears truncated, attempting partial parse...")
                # Find the last complete recommendation array item
                end_idx = cleaned_response.rfind('}', 0, len(cleaned_response))
                if end_idx == -1:
                    raise ValueError("No closing brace found - response severely truncated")
            
            json_str = cleaned_response[start_idx:end_idx + 1]
            
            # Attempt to parse JSON
            try:
                llm_output = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"⚠ JSON decode error: {e}")
                # Try to fix common issues
                # Add missing closing brackets if needed
                if json_str.count('{') > json_str.count('}'):
                    missing_braces = json_str.count('{') - json_str.count('}')
                    json_str += '}' * missing_braces
                    print(f"  Added {missing_braces} closing braces")
                
                if json_str.count('[') > json_str.count(']'):
                    missing_brackets = json_str.count('[') - json_str.count(']')
                    json_str += ']' * missing_brackets
                    print(f"  Added {missing_brackets} closing brackets")
                
                # Try parsing again
                llm_output = json.loads(json_str)
            
            print(f"✓ Parsed LLM JSON: {len(llm_output.get('recommendations', []))} recommendations")
            
            # Step 2: Check if medical query
            if not llm_output.get('is_medical_query', True):
                return [{
                    'medicine_name': 'Non-Medical Query',
                    'chemical_formula': None,
                    'dosage': 'N/A',
                    'explanation': llm_output.get('analysis', 'This query is not medical-related'),
                    'warnings': 'This assistant only handles medical/health queries',
                    'matched_medicines': [],
                    'available': False,
                    'rank': 1
                }]
            
            # Step 3: Extract analysis for display
            analysis = llm_output.get('analysis', '')
            
            # Step 4: Process each recommendation
            for rec in llm_output.get('recommendations', [])[:max_results]:
                chemical_formula = rec.get('chemical_formula', '').strip()
                
                if not chemical_formula:
                    continue
                
                # Step 5: Search database for medicines with this chemical formula
                matched_medicines = self._find_medicines_by_formula(chemical_formula)
                
                print(f"  Chemical: {chemical_formula} → {len(matched_medicines)} medicines found")
                
                # Step 6: Build structured recommendation
                recommendation = {
                    'rank': rec.get('rank', len(recommendations) + 1),
                    'chemical_formula': chemical_formula,
                    'dosage': rec.get('dosage', 'As directed by physician'),
                    'explanation': rec.get('reason', 'Recommended for your symptoms'),
                    'warnings': rec.get('warnings', 'Consult doctor if symptoms persist'),
                    'requires_doctor': rec.get('requires_doctor', False),
                    
                    # Database matches
                    'matched_medicines': matched_medicines,
                    'available': len(matched_medicines) > 0,
                    'medicine_count': len(matched_medicines),
                    
                    # Additional info
                    'ai_analysis': analysis,
                    'requires_immediate_attention': llm_output.get('requires_immediate_attention', False)
                }
                
                recommendations.append(recommendation)
            
            # Add overall analysis if no recommendations parsed
            if not recommendations and analysis:
                recommendations.append({
                    'rank': 1,
                    'chemical_formula': 'General Medical Advice',
                    'dosage': 'N/A',
                    'explanation': analysis[:400],
                    'warnings': llm_output.get('disclaimer', 'Consult healthcare professional'),
                    'requires_doctor': llm_output.get('requires_immediate_attention', True),
                    'matched_medicines': [],
                    'available': False,
                    'medicine_count': 0
                })
            
        except json.JSONDecodeError as e:
            print(f"⚠ JSON parsing failed completely: {e}")
            print(f"  Response preview: {ai_response[:200]}...")
            # Fallback: create generic recommendation
            recommendations.append({
                'rank': 1,
                'chemical_formula': 'Response Parsing Error',
                'dosage': 'N/A',
                'explanation': 'Unable to parse AI response. The response may be incomplete. Please try again with a shorter, more specific symptom description.',
                'warnings': 'If symptoms persist, consult a healthcare professional',
                'requires_doctor': False,
                'matched_medicines': [],
                'available': False,
                'medicine_count': 0
            })
        except Exception as e:
            print(f"⚠ Unexpected parsing error: {e}")
            import traceback
            traceback.print_exc()
            recommendations.append({
                'rank': 1,
                'chemical_formula': 'System Error',
                'dosage': 'N/A',
                'explanation': f'Error processing AI response: {str(e)}. Please try again.',
                'warnings': 'Contact support if this persists',
                'requires_doctor': False,
                'matched_medicines': [],
                'available': False,
                'medicine_count': 0
            })
        
        return recommendations
    
    def _find_medicines_by_formula(self, chemical_formula: str) -> List[Dict[str, Any]]:
        """
        Search database for medicines containing the chemical formula
        Returns list of matched medicines with full details
        """
        if not self.medicines or not chemical_formula:
            return []
        
        matched = []
        formula_lower = chemical_formula.lower()
        
        # Search through medicine database
        for med in self.medicines:
            med_formula = med.get('formula', '').lower()
            med_name = med.get('name', '').lower()
            
            # Match if:
            # 1. Chemical formula is in medicine formula
            # 2. Chemical formula is the medicine name
            if formula_lower in med_formula or formula_lower in med_name:
                matched.append({
                    'name': med.get('name'),
                    'formula': med.get('formula'),
                    'manufacturer': med.get('manufacturer'),
                    'pack_size': med.get('pack_size'),
                    'price': med.get('price'),
                    'type': med.get('type', 'N/A')
                })
        
        # Sort by price (cheapest first) with robust parsing
        def extract_price(med):
            """Extract numeric price from various formats"""
            price_str = str(med.get('price', '999999'))
            try:
                # Remove common text: Rs., /, per, tablet, etc.
                import re
                # Extract first number (with decimals)
                match = re.search(r'\d+\.?\d*', price_str)
                if match:
                    return float(match.group())
                return 999999
            except:
                return 999999
        
        matched.sort(key=extract_price)
        
        # Return top 10 matches
        return matched[:10]
    
    def _find_medicine_match(self, medicine_name: str) -> Dict[str, Any]:
        """Find matching medicine in database"""
        if not self.medicines:
            return None
        
        medicine_name_lower = medicine_name.lower()
        
        # Try exact match
        for med in self.medicines:
            if med.get('name', '').lower() == medicine_name_lower:
                return {
                    'name': med.get('name'),
                    'formula': med.get('formula'),
                    'manufacturer': med.get('manufacturer'),
                    'pack_size': med.get('pack_size'),
                    'price': med.get('price')
                }
        
        # Try partial/formula match
        for med in self.medicines:
            name = med.get('name', '').lower()
            formula = med.get('formula', '').lower()
            
            if medicine_name_lower in name or medicine_name_lower in formula:
                return {
                    'name': med.get('name'),
                    'formula': med.get('formula'),
                    'manufacturer': med.get('manufacturer'),
                    'pack_size': med.get('pack_size'),
                    'price': med.get('price')
                }
        
        return None
