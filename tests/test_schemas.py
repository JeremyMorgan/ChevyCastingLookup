import os
import sys
import unittest
from pydantic import ValidationError

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.schemas.casting import CastingBase, CastingCreate, CastingUpdate, CastingInDB, Casting


class TestSchemas(unittest.TestCase):
    """Test cases for the Pydantic schemas."""
    
    def test_casting_base(self):
        """Test the CastingBase schema."""
        # Valid data
        data = {
            "casting_number": 1001,
            "name": "Engine Block",
            "description": "V8 engine block",
            "material": "Cast Iron",
            "weight": 75.5,
            "dimensions": "24x18x12",
            "manufacturer": "ABC Castings",
            "year_introduced": 1985
        }
        
        casting = CastingBase(**data)
        self.assertEqual(casting.casting_number, 1001)
        self.assertEqual(casting.name, "Engine Block")
        self.assertEqual(casting.description, "V8 engine block")
        self.assertEqual(casting.material, "Cast Iron")
        self.assertEqual(casting.weight, 75.5)
        self.assertEqual(casting.dimensions, "24x18x12")
        self.assertEqual(casting.manufacturer, "ABC Castings")
        self.assertEqual(casting.year_introduced, 1985)
        
        # Missing required field
        with self.assertRaises(ValidationError):
            CastingBase()
        
        # Invalid data type
        with self.assertRaises(ValidationError):
            CastingBase(casting_number="not_a_number")
    
    def test_casting_create(self):
        """Test the CastingCreate schema."""
        # Valid data
        data = {
            "casting_number": 1001,
            "name": "Engine Block",
            "description": "V8 engine block",
            "material": "Cast Iron",
            "weight": 75.5,
            "dimensions": "24x18x12",
            "manufacturer": "ABC Castings",
            "year_introduced": 1985
        }
        
        casting = CastingCreate(**data)
        self.assertEqual(casting.casting_number, 1001)
        self.assertEqual(casting.name, "Engine Block")
        
        # Minimal data
        minimal_data = {
            "casting_number": 1001
        }
        
        casting = CastingCreate(**minimal_data)
        self.assertEqual(casting.casting_number, 1001)
        self.assertIsNone(casting.name)
        self.assertIsNone(casting.description)
    
    def test_casting_update(self):
        """Test the CastingUpdate schema."""
        # Valid data
        data = {
            "name": "Updated Engine Block",
            "description": "Updated V8 engine block"
        }
        
        casting = CastingUpdate(**data)
        self.assertEqual(casting.name, "Updated Engine Block")
        self.assertEqual(casting.description, "Updated V8 engine block")
        
        # Empty data
        casting = CastingUpdate()
        self.assertIsNone(casting.name)
        self.assertIsNone(casting.description)
    
    def test_casting_in_db(self):
        """Test the CastingInDB schema."""
        # Valid data
        data = {
            "id": 1,
            "casting_number": 1001,
            "name": "Engine Block",
            "description": "V8 engine block",
            "material": "Cast Iron",
            "weight": 75.5,
            "dimensions": "24x18x12",
            "manufacturer": "ABC Castings",
            "year_introduced": 1985
        }
        
        casting = CastingInDB(**data)
        self.assertEqual(casting.id, 1)
        self.assertEqual(casting.casting_number, 1001)
        self.assertEqual(casting.name, "Engine Block")
        
        # Missing required field
        with self.assertRaises(ValidationError):
            CastingInDB(casting_number=1001)
        
        with self.assertRaises(ValidationError):
            CastingInDB(id=1)
    
    def test_casting(self):
        """Test the Casting schema."""
        # Valid data
        data = {
            "id": 1,
            "casting_number": 1001,
            "name": "Engine Block",
            "description": "V8 engine block",
            "material": "Cast Iron",
            "weight": 75.5,
            "dimensions": "24x18x12",
            "manufacturer": "ABC Castings",
            "year_introduced": 1985
        }
        
        casting = Casting(**data)
        self.assertEqual(casting.id, 1)
        self.assertEqual(casting.casting_number, 1001)
        self.assertEqual(casting.name, "Engine Block")


if __name__ == "__main__":
    unittest.main()
