#!/usr/bin/env python3
"""
Script to reset the database and import the Chevrolet casting data.
This script will:
1. Drop the existing database
2. Create the new tables
3. Import the data from chev-casting.csv
"""

import os
import sys
import pandas as pd

# Add the current directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine, SessionLocal
from app.models import casting as casting_models
from app.models.casting import Casting as CastingModel
from app.utils.import_data import clean_data


def import_data(file_path, db):
    """
    Import data from CSV file, handling duplicates by skipping them.
    """
    # Define column mapping for the Chevrolet casting data
    column_mapping = {
        "Years": "years",
        "Casting": "casting",
        "CID": "cid",
        "Low Power": "low_power",
        "High Power": "high_power",
        "Main Caps": "main_caps",
        "Comments": "comments"
    }
    
    # Read CSV file
    df = pd.read_csv(file_path)
    
    # Drop any unnamed columns
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
        print(f"Dropped unnamed columns: {unnamed_cols}")
    
    # Apply column mapping
    df = df.rename(columns=column_mapping)
    
    # Convert DataFrame to list of dictionaries
    records = df.to_dict(orient="records")
    
    # Track unique casting numbers to avoid duplicates
    unique_castings = set()
    total_imported = 0
    skipped = 0
    
    for record in records:
        # Clean data
        cleaned_record = clean_data(record)
        
        # Skip if casting number already processed
        casting_number = cleaned_record.get("casting")
        if casting_number in unique_castings:
            skipped += 1
            continue
        
        # Add to unique set
        unique_castings.add(casting_number)
        
        # Create model instance
        model_instance = CastingModel(**cleaned_record)
        
        # Add to session
        db.add(model_instance)
        
        # Commit each record individually to handle errors
        try:
            db.commit()
            total_imported += 1
            if total_imported % 10 == 0:
                print(f"Imported {total_imported} records")
        except Exception as e:
            db.rollback()
            print(f"Error importing record with casting {casting_number}: {e}")
            skipped += 1
    
    print(f"Total imported: {total_imported}, Skipped: {skipped}")
    return total_imported


def main():
    """Main function."""
    print("Dropping existing tables...")
    casting_models.Base.metadata.drop_all(bind=engine)
    print("Tables dropped successfully.")
    
    print("Creating new tables...")
    casting_models.Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    
    print("Importing data from chev-casting.csv...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Import data
        total_imported = import_data("chev-casting.csv", db)
        
        print(f"Successfully imported {total_imported} records.")
    
    finally:
        # Close database session
        db.close()
    
    print("Database reset completed successfully.")


if __name__ == "__main__":
    main()
