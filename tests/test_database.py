import os
import sys
import unittest
from sqlalchemy import text

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine, Base, SessionLocal


class TestDatabase(unittest.TestCase):
    """Test cases for the database connection."""
    
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
    
    def test_database_connection(self):
        """Test that the database connection is working."""
        # Execute a simple query
        result = self.db.execute(text("SELECT 1")).scalar()
        self.assertEqual(result, 1)
    
    def test_database_transaction(self):
        """Test that database transactions are working."""
        # Start a transaction
        self.db.begin()
        
        # Execute a query
        self.db.execute(text("CREATE TABLE test_table (id INTEGER PRIMARY KEY)"))
        self.db.execute(text("INSERT INTO test_table (id) VALUES (1)"))
        
        # Commit the transaction
        self.db.commit()
        
        # Check that the table exists
        result = self.db.execute(text("SELECT id FROM test_table")).scalar()
        self.assertEqual(result, 1)
        
        # Start another transaction
        self.db.begin()
        
        # Execute a query
        self.db.execute(text("INSERT INTO test_table (id) VALUES (2)"))
        
        # Rollback the transaction
        self.db.rollback()
        
        # Check that the second insert was rolled back
        result = self.db.execute(text("SELECT COUNT(*) FROM test_table")).scalar()
        self.assertEqual(result, 1)
        
        # Drop the test table
        self.db.execute(text("DROP TABLE test_table"))
        self.db.commit()


if __name__ == "__main__":
    unittest.main()
