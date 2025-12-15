"""
Symptom Search API Route
Handles requests for symptom-based medicine recommendations.
"""
from flask import Blueprint, request, jsonify
import sys
import os

# Add project root to path to import src.agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agents.orchestrator import AgentOrchestrator

symptom_search_bp = Blueprint('symptom_search', __name__)

@symptom_search_bp.route('/api/symptom-search', methods=['POST'])
def search_symptoms():
    """
    Search medicines based on symptoms.
    
    Request Body:
    {
        "query": "I have a headache and fever",
        "top_k": 5 (optional)
    }
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
            
        # Instantiate Orchestrator
        # In a production app, you might want to reuse the instance or use a factory
        orchestrator = AgentOrchestrator()
        
        # Execute Pipeline
        result = orchestrator.execute(data)
        
        if result['status'] == 'error':
            return jsonify({
                'success': False,
                'error': result['output'].get('error', 'Unknown error processing request'),
                'details': result['output']
            }), 500
            
        return jsonify({
            'success': True,
            'result': result['output'],
            'execution_time': result['execution_time'],
            'timestamp': result['timestamp']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
