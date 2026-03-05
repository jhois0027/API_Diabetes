from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "modelo_cargado" in response.json()

def test_prediccion():
    response = client.post("/prediccion", json={"glucosa": 120, "edad": 50})
    assert response.status_code == 200
    assert "prediccion_riesgo" in response.json()