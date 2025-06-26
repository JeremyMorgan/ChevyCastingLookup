import os
import sys
import unittest

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine, Base, SessionLocal
from app.models.casting import Casting


class TestModels(unittest.TestCase):
    """Test cases for the SQLAlchemy models."""
    
    def setUp(self):
        """Set up test database."""
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Create session
        self.db = SessionLocal()
    
    def tearDown(self):
        """Clean up after tests."""
        # Close session
        self.db.close()
        
        # Drop tables
        Base.metadata.drop_all(bind=engine)
    
    def test_casting_model(self):
        """Test the Casting model."""
        # Create a casting
        casting = Casting(
            casting_number=1001,
            name="Engine Block",
            description="V8 engine block",
            material="Cast Iron",
            weight=75.5,
            dimensions="24x18x12",
            manufacturer="ABC Castings",
            year_introduced=1985
        )
        
        # Add to session
        self.db.add(casting)
        self.db.commit()
        
        # Refresh from database
        self.db.refresh(casting)
        
        # Check attributes
        self.assertEqual(casting.casting_number, 1001)
        self.assertEqual(casting.name, "Engine Block")
        self.assertEqual(casting.description, "V8 engine block")
        self.assertEqual(casting.material, "Cast Iron")
        self.assertEqual(casting.weight, 75.5)
        self.assertEqual(casting.dimensions, "24x18x12")
        self.assertEqual(casting.manufacturer, "ABC Castings")
        self.assertEqual(casting.year_introduced, 1985)
    
    def test_casting_model_query(self):
        """Test querying the Casting model."""
        # Create castings
        castings = [
            Casting(
                casting_number=1001,
                name="Engine Block",
                material="Cast Iron"
            ),
            Casting(
                casting_number=1002,
                name="Cylinder Head",
                material="Aluminum"
            ),
            Casting(
                casting_number=1003,
                name="Crankshaft",
                material="Steel"
            )
        ]
        
        # Add to session
        self.db.add_all(castings)
        self.db.commit()
        
        # Query all castings
        all_castings = self.db.query(Casting).all()
        self.assertEqual(len(all_castings), 3)
        
        # Query by casting number
        casting = self.db.query(Casting).filter(
            Casting.casting_number == 1001
        ).first()
        self.assertEqual(casting.name, "Engine Block")
        
        # Query by name
        castings = self.db.query(Casting).filter(
            Casting.name.like("%Engine%")
        ).all()
        self.assertEqual(len(castings), 1)
        self.assertEqual(castings[0].casting_number, 1001)
        
        # Query by material
        castings = self.db.query(Casting).filter(
            Casting.material == "Aluminum"
        ).all()
        self.assertEqual(len(castings), 1)
        self.assertEqual(castings[0].casting_number, 1002)
    
    def test_casting_model_update(self):
        """Test updating a Casting model."""
        # Create a casting
        casting = Casting(
            casting_number=1001,
            name="Engine Block",
            description="V8 engine block"
        )
        
        # Add to session
        self.db.add(casting)
        self.db.commit()
        
        # Update the casting
        casting.name = "Updated Engine Block"
        casting.description = "Updated V8 engine block"
        self.db.commit()
        
        # Query the casting
        updated_casting = self.db.query(Casting).filter(
            Casting.casting_number == 1001
        ).first()
        
        # Check attributes
        self.assertEqual(updated_casting.name, "Updated Engine Block")
        self.assertEqual(updated_casting.description, "Updated V8 engine block")
    
    def test_casting_model_delete(self):
        """Test deleting a Casting model."""
        # Create a casting
        casting = Casting(
            casting_number=1001,
            name="Engine Block"
        )
        
        # Add to session
        self.db.add(casting)
        self.db.commit()
        
        # Delete the casting
        self.db.delete(casting)
        self.db.commit()
        
        # Query the casting
        deleted_casting = self.db.query(Casting).filter(
            Casting.casting_number == 1001
        ).first()
        
        # Check that the casting was deleted
        self.assertIsNone(deleted_casting)


if __name__ == "__main__":
    unittest.main()
