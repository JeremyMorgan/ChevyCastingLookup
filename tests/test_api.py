import os
import sys
import unittest
from fastapi.testclient import TestClient

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.db.database import engine, Base, get_db
from app.models.casting import Casting as CastingModel
from app.utils.import_data import import_csv_with_pandas


class TestCastingAPI(unittest.TestCase):
    """Test cases for the Casting API."""
    
    def setUp(self):
        """Set up test database and client."""
        # Create test client
        self.client = TestClient(app)
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Import sample data
        db = next(get_db())
        try:
            # Clear existing data
            db.query(CastingModel).delete()
            db.commit()
            
            # Import sample data
            sample_data_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "sample_data.csv"
            )
            import_csv_with_pandas(sample_data_path, db)
        finally:
            db.close()
    
    def tearDown(self):
        """Clean up after tests."""
        # Drop tables
        Base.metadata.drop_all(bind=engine)
    
    def test_read_root(self):
        """Test the root endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertIn("docs", response.json())
    
    def test_get_castings(self):
        """Test getting a list of castings."""
        response = self.client.get("/api/castings/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertGreater(len(response.json()), 0)
    
    def test_get_casting_by_number(self):
        """Test getting a specific casting by number."""
        # Get a casting that exists
        response = self.client.get("/api/castings/1001")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["casting_number"], 1001)
        
        # Get a casting that doesn't exist
        response = self.client.get("/api/castings/9999")
        self.assertEqual(response.status_code, 404)
    
    def test_create_casting(self):
        """Test creating a new casting."""
        # Create a new casting
        new_casting = {
            "casting_number": 2001,
            "name": "Test Casting",
            "description": "A test casting",
            "material": "Test Material",
            "weight": 10.5,
            "dimensions": "10x10x10",
            "manufacturer": "Test Manufacturer",
            "year_introduced": 2000
        }
        response = self.client.post("/api/castings/", json=new_casting)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["casting_number"], 2001)
        
        # Try to create a casting with a duplicate number
        response = self.client.post("/api/castings/", json=new_casting)
        self.assertEqual(response.status_code, 400)
    
    def test_update_casting(self):
        """Test updating an existing casting."""
        # Update a casting that exists
        update_data = {
            "name": "Updated Casting",
            "description": "An updated casting"
        }
        response = self.client.put("/api/castings/1001", json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Casting")
        self.assertEqual(response.json()["description"], "An updated casting")
        
        # Update a casting that doesn't exist
        response = self.client.put("/api/castings/9999", json=update_data)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_casting(self):
        """Test deleting a casting."""
        # Delete a casting that exists
        response = self.client.delete("/api/castings/1001")
        self.assertEqual(response.status_code, 200)
        
        # Verify that the casting was deleted
        response = self.client.get("/api/castings/1001")
        self.assertEqual(response.status_code, 404)
        
        # Delete a casting that doesn't exist
        response = self.client.delete("/api/castings/9999")
        self.assertEqual(response.status_code, 404)
    
    def test_search_castings(self):
        """Test searching for castings."""
        # Search by name
        response = self.client.get("/api/castings/search/?name=Engine")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)
        
        # Search by manufacturer
        response = self.client.get("/api/castings/search/?manufacturer=ABC")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)
        
        # Search by material
        response = self.client.get("/api/castings/search/?material=Aluminum")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)
        
        # Search by year
        response = self.client.get("/api/castings/search/?year_introduced=1985")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)
        
        # Search with no results
        response = self.client.get("/api/castings/search/?name=NonExistent")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)


if __name__ == "__main__":
    unittest.main()
