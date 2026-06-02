"""Minimal tests for FastAPI web application"""
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent))
from dilution_web_app import app

client = TestClient(app)


class TestWebInterface:
    def test_root_returns_html(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "html" in response.text.lower()

    def test_health_check(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestCalculateC1:
    def test_success(self):
        response = client.post("/api/calculate/c1", json={"C2": 2.0, "V2": 100, "V1": 50})
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["result"] == 4.0

    def test_zero_input_rejected(self):
        response = client.post("/api/calculate/c1", json={"C2": 2.0, "V2": 100, "V1": 0})
        assert response.status_code == 422


class TestCalculateV1:
    def test_success(self):
        response = client.post("/api/calculate/v1", json={"C1": 4.0, "C2": 2.0, "V2": 100})
        assert response.status_code == 200
        assert response.json()["result"] == 50.0


class TestCalculateC2:
    def test_success(self):
        response = client.post("/api/calculate/c2", json={"C1": 4.0, "V1": 50, "V2": 100})
        assert response.status_code == 200
        assert response.json()["result"] == 2.0


class TestCalculateV2:
    def test_success(self):
        response = client.post("/api/calculate/v2", json={"C1": 4.0, "V1": 50, "C2": 2.0})
        assert response.status_code == 200
        assert response.json()["result"] == 100.0

