import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

# Initialize the TestClient with the app as a positional argument, not a keyword argument
client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_graphql_query():
    query = """
    query {
        branches {
            edges {
                node {
                    branch
                    ifsc
                    bank {
                        name
                    }
                }
            }
        }
    }
    """
    
    response = client.post("/gql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "branches" in data["data"]
    assert "edges" in data["data"]["branches"]