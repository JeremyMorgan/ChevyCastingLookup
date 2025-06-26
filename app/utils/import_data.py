import argparse
import csv
import os
import sys
from typing import Dict, List, Optional, Union

import pandas as pd
from sqlalchemy.orm import Session

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.database import SessionLocal, engine
from app.models.casting import Casting as CastingModel
from app.models import casting as casting_models


def create_tables():
    """Create database tables."""
    casting_models.Base.metadata.create_all(bind=engine)


def clean_data(record: Dict) -> Dict:
    """
    Clean and prepare data for database insertion.
    
    Args:
        record: Dictionary containing record data
        
    Returns:
        Cleaned record
    """
    # Make a copy to avoid modifying the original
    cleaned = record.copy()
    
    # Convert empty strings to None
    for key, value in cleaned.items():
        if value == "" or value == "-":
            cleaned[key] = None
    
    # Convert CID to integer if possible
    if cleaned.get("cid") and cleaned["cid"] not in (None, "-"):
        try:
            cleaned["cid"] = int(cleaned["cid"])
        except (ValueError, TypeError):
            # If conversion fails, keep as is
            pass
    
    return cleaned


def import_csv_with_pandas(
    file_path: str,
    db: Session,
    column_mapping: Optional[Dict[str, str]] = None,
    batch_size: int = 1000
) -> int:
    """
    Import data from a CSV file using pandas.
    
    Args:
        file_path: Path to the CSV file
        db: Database session
        column_mapping: Mapping from CSV columns to database columns
        batch_size: Number of records to insert at once
        
    Returns:
        Number of records imported
    """
    # Read CSV file
    df = pd.read_csv(file_path)
    
    # Drop any unnamed columns
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
        print(f"Dropped unnamed columns: {unnamed_cols}")
    
    # Apply column mapping if provided
    if column_mapping:
        df = df.rename(columns=column_mapping)
    
    # Convert DataFrame to list of dictionaries
    records = df.to_dict(orient="records")
    
    # Insert records in batches
    total_imported = 0
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        
        # Clean data
        cleaned_batch = [clean_data(record) for record in batch]
        
        # Create model instances
        model_instances = [CastingModel(**record) for record in cleaned_batch]
        
        # Add to session
        db.add_all(model_instances)
        
        # Commit
        db.commit()
        
        total_imported += len(batch)
        print(f"Imported {total_imported} records")
    
    return total_imported


def import_csv_with_csv_reader(
    file_path: str,
    db: Session,
    column_mapping: Optional[Dict[str, str]] = None,
    batch_size: int = 1000
) -> int:
    """
    Import data from a CSV file using csv.DictReader.
    
    Args:
        file_path: Path to the CSV file
        db: Database session
        column_mapping: Mapping from CSV columns to database columns
        batch_size: Number of records to insert at once
        
    Returns:
        Number of records imported
    """
    # Read CSV file
    with open(file_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        # Process records in batches
        batch = []
        total_imported = 0
        
        for row in reader:
            # Apply column mapping if provided
            if column_mapping:
                mapped_row = {}
                for csv_col, db_col in column_mapping.items():
                    if csv_col in row:
                        mapped_row[db_col] = row[csv_col]
                row = mapped_row
            
            # Clean data
            cleaned_row = clean_data(row)
            
            # Add to batch
            batch.append(cleaned_row)
            
            # Process batch if it reaches the batch size
            if len(batch) >= batch_size:
                # Create model instances
                model_instances = [CastingModel(**record) for record in batch]
                
                # Add to session
                db.add_all(model_instances)
                
                # Commit
                db.commit()
                
                total_imported += len(batch)
                print(f"Imported {total_imported} records")
                
                # Clear batch
                batch = []
        
        # Process remaining records
        if batch:
            # Create model instances
            model_instances = [CastingModel(**record) for record in batch]
            
            # Add to session
            db.add_all(model_instances)
            
            # Commit
            db.commit()
            
            total_imported += len(batch)
            print(f"Imported {total_imported} records")
        
        return total_imported


def import_chev_casting_data(file_path: str, db: Session, batch_size: int = 1000) -> int:
    """
    Import Chevrolet casting data from the specific CSV format.
    
    Args:
        file_path: Path to the CSV file
        db: Database session
        batch_size: Number of records to insert at once
        
    Returns:
        Number of records imported
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
    
    return import_csv_with_pandas(
        file_path,
        db,
        column_mapping=column_mapping,
        batch_size=batch_size
    )


def main():
    """Main function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Import CSV data into the database")
    parser.add_argument("file_path", help="Path to the CSV file")
    parser.add_argument(
        "--method",
        choices=["pandas", "csv", "chev"],
        default="chev",
        help="Method to use for importing data (default: chev)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Number of records to insert at once (default: 1000)"
    )
    args = parser.parse_args()
    
    # Create database tables
    create_tables()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Import data
        if args.method == "pandas":
            total_imported = import_csv_with_pandas(
                args.file_path,
                db,
                batch_size=args.batch_size
            )
        elif args.method == "csv":
            total_imported = import_csv_with_csv_reader(
                args.file_path,
                db,
                batch_size=args.batch_size
            )
        else:  # chev
            total_imported = import_chev_casting_data(
                args.file_path,
                db,
                batch_size=args.batch_size
            )
        
        print(f"Successfully imported {total_imported} records")
    
    finally:
        # Close database session
        db.close()


if __name__ == "__main__":
    main()
