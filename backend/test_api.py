"""
Script de teste da API
"""

import requests
import json

API_URL = "http://localhost:5020"

def test_health():
    """Testa endpoint de health"""
    print("Testando /health...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_predict():
    """Testa endpoint de predição"""
    print("Testando /predict...")
    
    data = {
        "area": 70.0,
        "bedrooms": 2,
        "bathrooms": 2,
        "parking_spaces": 1,
        "furnished": False,
        "hoa": 400.0,
        "property_type": "UNIT",
        "city": "Brasília",
        "neighborhood": "Asa Norte",
        "suites": 0
    }
    
    response = requests.post(f"{API_URL}/predict", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_model_info():
    """Testa endpoint de informações do modelo"""
    print("Testando /model/info...")
    response = requests.get(f"{API_URL}/model/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DA API ALUGAI")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_model_info()
        test_predict()
        
        print("=" * 60)
        print("TESTES CONCLUÍDOS!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("ERRO: Não foi possível conectar à API.")
        print("Certifique-se de que a API está rodando em http://localhost:5000")
    except Exception as e:
        print(f"ERRO: {e}")

