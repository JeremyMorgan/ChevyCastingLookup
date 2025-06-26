import os
import sys
import unittest
from sqlalchemy.orm import Session

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine, Base, SessionLocal
from app.models.casting import Casting as CastingModel
from app.utils.import_data import import_csv_with_pandas, import_csv_with_csv_reader


class TestImportData(unittest.TestCase):
    """Test cases for the import_data module."""
    
    def setUp(self):
        """Set up test database."""
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Create session
        self.db = SessionLocal()
        
        # Clear existing data
        self.db.query(CastingModel).delete()
        self.db.commit()
        
        # Get sample data path
        self.sample_data_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "sample_data.csv"
        )
    
    def tearDown(self):
        """Clean up after tests."""
        # Close session
        self.db.close()
        
        # Drop tables
        Base.metadata.drop_all(bind=engine)
    
    def test_import_csv_with_pandas(self):
        """Test importing CSV data with pandas."""
        # Import data
        total_imported = import_csv_with_pandas(
            self.sample_data_path,
            self.db
        )
        
        # Check that data was imported
        self.assertGreater(total_imported, 0)
        
        # Check that data is in the database
        castings = self.db.query(CastingModel).all()
        self.assertEqual(len(castings), total_imported)
        
        # Check a specific casting
        casting = self.db.query(CastingModel).filter(
            CastingModel.casting_number == 1001
        ).first()
        self.assertIsNotNone(casting)
        self.assertEqual(casting.name, "Engine Block")
        self.assertEqual(casting.manufacturer, "ABC Castings")
    
    def test_import_csv_with_csv_reader(self):
        """Test importing CSV data with csv.DictReader."""
        # Import data
        total_imported = import_csv_with_csv_reader(
            self.sample_data_path,
            self.db
        )
        
        # Check that data was imported
        self.assertGreater(total_imported, 0)
        
        # Check that data is in the database
        castings = self.db.query(CastingModel).all()
        self.assertEqual(len(castings), total_imported)
        
        # Check a specific casting
        casting = self.db.query(CastingModel).filter(
            CastingModel.casting_number == 1001
        ).first()
        self.assertIsNotNone(casting)
        self.assertEqual(casting.name, "Engine Block")
        self.assertEqual(casting.manufacturer, "ABC Castings")
    
    def test_column_mapping(self):
        """Test importing CSV data with column mapping."""
        # Create a temporary CSV file with different column names
        temp_csv_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "temp_data.csv"
        )
        
        with open(temp_csv_path, "w", newline="", encoding="utf-8") as f:
            f.write("part_number,part_name,part_description\n")
            f.write("1001,Engine Block,V8 engine block\n")
            f.write("1002,Cylinder Head,4-cylinder head\n")
        
        try:
            # Import data with column mapping
            column_mapping = {
                "part_number": "casting_number",
                "part_name": "name",
                "part_description": "description"
            }
            
            total_imported = import_csv_with_pandas(
                temp_csv_path,
                self.db,
                column_mapping=column_mapping
            )
            
            # Check that data was imported
            self.assertEqual(total_imported, 2)
            
            # Check that data is in the database
            castings = self.db.query(CastingModel).all()
            self.assertEqual(len(castings), 2)
            
            # Check a specific casting
            casting = self.db.query(CastingModel).filter(
                CastingModel.casting_number == 1001
            ).first()
            self.assertIsNotNone(casting)
            self.assertEqual(casting.name, "Engine Block")
            self.assertEqual(casting.description, "V8 engine block")
        
        finally:
            # Remove temporary file
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)


if __name__ == "__main__":
    unittest.main()
