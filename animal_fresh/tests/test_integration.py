"""
Integration Test Suite for Veterinary AI System
Validates end-to-end flow: Predictive Logic -> API -> Monitoring -> Dashboard
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os
import json
import time

# Add root directory to sys.path so we can import modules
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from simple_api import app
from src.inference_nn import predict_disease_nn
from src.monitoring import SystemMonitor

client = TestClient(app)
monitor = SystemMonitor()

# 1. Core Model Inference Test
def test_vetnet_prediction():
    """Verify that VetNet model returns valid structure directly"""
    # NOTE: The model expects ALL numeric columns, even if default 0.
    sample_input = {
        'Animal': 'Dog',
        'Age': 5.0,
        'Gender': 'Male',
        'Breed': 'Mixed',
        'WBC': 20.0, # High WBC -> Expect Viral/Bacterial
        'RBC': 6.0,
        'Hemoglobin': 14.0,
        'Platelets': 200,
        'Glucose': 90,
        'ALT': 40,
        'AST': 40,
        'Urea': 20,
        'Creatinine': 1.0,
        'Symptom_Fever': 1,
        'Symptom_Lethargy': 1,
        'Symptom_Vomiting': 0, 'Symptom_Diarrhea': 0, 'Symptom_WeightLoss': 0, 
        'Symptom_SkinLesion': 0, 'Symptom_Coughing': 0, 'Symptom_Lameness': 0
    }
    result = predict_disease_nn(sample_input)
    
    if not result.get('success'):
        print(f"❌ Core Prediction Failed: {result.get('error')}")
        
    assert result['success'] == True
    assert 'predicted_category' in result
    assert 'treatment' in result # Phase 3 Feature
    print(f"✅ Core Model Prediction: {result['predicted_category']} -> {result['predicted_disease']}")

# 2. API Endpoint Test
def test_api_predict():
    """Verify API endpoint functionality"""
    # API model has defaults for missing fields, so this should pass easily
    payload = {
        "Animal": "Cat",
        "Age": 3.0,
        "Gender": "Female",
        "WBC": 15.0,
        "Symptom_Vomiting": 1
    }
    
    response = client.post("/predict", json=payload)
    if response.status_code != 200:
        print(f"API Error: {response.text}")
        
    assert response.status_code == 200
    data = response.json()
    
    assert data['success'] == True
    assert data['method'] == "VetNet (Deep Learning)"
    # Check Treatment Info
    assert 'treatment' in data
    assert 'treatment_plan' in data['treatment']
    print("✅ API Endpoint Verification Passed")

# 3. Monitoring System Test
def test_monitoring_logs():
    """Verify that API calls are logged correctly"""
    # clear logs or count before call?
    initial_count = len(monitor.get_recent_predictions(limit=10000))
    
    # Make a call
    payload = {
        "Animal": "Horse",
        "Age": 7.0,
        "Gender": "Male", 
        "Symptom_Lameness": 1
    }
    client.post("/predict", json=payload)
    
    # Wait a tiny bit for file write (though monitor is sync for log_prediction)
    time.sleep(0.1) 
    
    final_count = len(monitor.get_recent_predictions(limit=10000))
    assert final_count > initial_count, "Log file should have grown"
    
    # Verify last log content
    last_log = monitor.get_recent_predictions(limit=1).iloc[0]
    assert last_log['animal'] == 'Horse'
    assert last_log['status'] == 'success'
    print(f"✅ Monitoring Verification Passed (Total Logs: {final_count})")

# 4. Treatment Database Test
def test_treatment_retrieval():
    from src.treatment_db import get_treatment
    treatment = get_treatment("Parvovirus") # Should be partial match or specific?
    # Our DB has "Canine Parvovirus". Let's check exact match.
    treatment_cp = get_treatment("Canine Parvovirus")
    assert "IV fluid therapy" in treatment_cp['treatment_plan']
    print("✅ Treatment DB Verification Passed")

# 5. Knowledge Graph Export Test
def test_knowledge_graph_exists():
    path = "data/knowledge_graph.json"
    assert os.path.exists(path), "Knowledge Graph JSON should be exported"
    with open(path, 'r') as f:
        data = json.load(f)
    assert 'nodes' in data
    # networkx can use 'links' or 'edges' depending on version/args
    assert 'links' in data or 'edges' in data
    print(f"✅ Knowledge Graph Valid: {len(data['nodes'])} nodes")

if __name__ == "__main__":
    # Allow running directly
    print("Running Manual Integration Tests...")
    try:
        test_vetnet_prediction()
        test_api_predict()
        test_monitoring_logs()
        test_treatment_retrieval()
        test_knowledge_graph_exists()
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        # traceback
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
