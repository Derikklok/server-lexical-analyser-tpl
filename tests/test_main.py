# tests/test_main.py
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import app  # Import the FastAPI app from main.py

client = TestClient(app)

def test_process_string():
    # Test the process_string endpoint
    response = client.post("/process_string/", json={"input_str": "x = 10 + 5"})
    assert response.status_code == 200
    assert "tokens" in response.json()

def test_invalid_character():
    # Test error handling for an invalid character
    response = client.post("/process_string/", json={"input_str": "x = 10 @ 5"})
    assert response.status_code == 200
    assert "error" in response.json()