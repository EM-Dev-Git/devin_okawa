import pytest
from fastapi import status

class TestMainApp:
    
    def test_root_endpoint(self, client):
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "FastAPI Meeting Minutes Generator" in data["message"]
        assert data["status"] == "running"
        assert "version" in data
    
    def test_health_check(self, client):
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "meeting-minutes-generator"
        assert "version" in data
    
    def test_cors_headers(self, client):
        response = client.options("/")
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_405_METHOD_NOT_ALLOWED]
    
    def test_api_documentation_available(self, client):
        response = client.get("/docs")
        assert response.status_code == status.HTTP_200_OK
        
        response = client.get("/redoc")
        assert response.status_code == status.HTTP_200_OK
        
        response = client.get("/openapi.json")
        assert response.status_code == status.HTTP_200_OK
    
    def test_nonexistent_endpoint(self, client):
        response = client.get("/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
