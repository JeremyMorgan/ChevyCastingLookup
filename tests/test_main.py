import os
import sys
import unittest
from fastapi.testclient import TestClient

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app


class TestMain(unittest.TestCase):
    """Test cases for the main application."""
    
    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)
    
    def test_read_root(self):
        """Test the root endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertIn("docs", response.json())
    
    def test_docs_endpoint(self):
        """Test the docs endpoint."""
        response = self.client.get("/docs")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
    
    def test_redoc_endpoint(self):
        """Test the redoc endpoint."""
        response = self.client.get("/redoc")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
    
    def test_openapi_endpoint(self):
        """Test the openapi endpoint."""
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/json", response.headers["content-type"])
        
        # Check that the openapi schema contains the expected endpoints
        schema = response.json()
        self.assertIn("paths", schema)
        self.assertIn("/api/castings/", schema["paths"])
        self.assertIn("/api/castings/{casting_number}", schema["paths"])
        self.assertIn("/api/castings/search/", schema["paths"])


if __name__ == "__main__":
    unittest.main()
