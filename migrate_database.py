#!/usr/bin/env python3
"""
Migration script to update the database schema and import the new Chevrolet casting data.
This script will:
1. Drop the existing database
2. Create the new tables
3. Import the data from chev-casting.csv
"""

import os
import sys
import argparse

# Add the current directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine, SessionLocal
from app.models import casting as casting_models
from app.utils.import_data import import_chev_casting_data


def drop_tables():
    """Drop all tables in the database."""
    print("Dropping existing tables...")
    casting_models.Base.metadata.drop_all(bind=engine)
    print("Tables dropped successfully.")


def create_tables():
    """Create all tables in the database."""
    print("Creating new tables...")
    casting_models.Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


def import_data(file_path, batch_size=100):
    """Import data from the CSV file."""
    print(f"Importing data from {file_path}...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Import data
        total_imported = import_chev_casting_data(
            file_path,
            db,
            batch_size=batch_size
        )
        
        print(f"Successfully imported {total_imported} records.")
    
    finally:
        # Close database session
        db.close()


def main():
    """Main function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Migrate database to the new schema and import Chevrolet casting data"
    )
    parser.add_argument(
        "--file",
        default="chev-casting.csv",
        help="Path to the CSV file (default: chev-casting.csv)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Number of records to insert at once (default: 100)"
    )
    parser.add_argument(
        "--skip-drop",
        action="store_true",
        help="Skip dropping existing tables"
    )
    args = parser.parse_args()
    
    # Confirm with the user
    if not args.skip_drop:
        confirm = input(
            "WARNING: This will drop all existing tables and data. "
            "Are you sure you want to continue? (y/n): "
        )
        
        if confirm.lower() != "y":
            print("Migration aborted.")
            return
    
    # Drop tables
    if not args.skip_drop:
        drop_tables()
    
    # Create tables
    create_tables()
    
    # Import data
    import_data(args.file, args.batch_size)
    
    print("Migration completed successfully.")


if __name__ == "__main__":
    main()
