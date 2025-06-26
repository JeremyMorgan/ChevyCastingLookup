#!/usr/bin/env python3
"""
Example script demonstrating how to use the Chevrolet Casting API client.
"""

import json
import time
from examples.api_client import (
    get_castings,
    get_casting_by_id,
    create_casting,
    update_casting,
    delete_casting,
    search_castings
)

# Base URL of the API
BASE_URL = "http://localhost:8000"


def main():
    """Main function."""
    print("Casting API Client Example")
    print("=========================")
    
    # Wait for the API server to start
    print("\nEnsure the API server is running with:")
    print("  python run.py")
    print("\nPress Enter to continue...")
    input()
    
    try:
        # List all castings
        print("\n1. Listing all castings:")
        castings = get_castings(BASE_URL)
        print(f"Found {len(castings)} castings")
        
        if castings:
            # Get a specific casting
            casting_id = castings[0]["casting"]
            print(f"\n2. Getting casting with ID {casting_id}:")
            casting = get_casting_by_id(BASE_URL, casting_id)
            print(json.dumps(casting, indent=2))
            
            # Update a casting
            print(f"\n3. Updating casting with ID {casting_id}:")
            update_data = {
                "comments": f"Updated comments at {time.time()}"
            }
            updated_casting = update_casting(BASE_URL, casting_id, update_data)
            print(json.dumps(updated_casting, indent=2))
        
        # Create a new casting
        print("\n4. Creating a new casting:")
        new_casting_data = {
            "casting": "999999",
            "years": "2020-25",
            "cid": 350,
            "low_power": "250",
            "high_power": "300",
            "main_caps": "4",
            "comments": "A casting created by the example script"
        }
        
        try:
            new_casting = create_casting(BASE_URL, new_casting_data)
            print(json.dumps(new_casting, indent=2))
            
            # Search for castings
            print("\n5. Searching for castings with CID 350:")
            search_results = search_castings(BASE_URL, cid=350)
            print(f"Found {len(search_results)} castings")
            print(json.dumps(search_results, indent=2))
            
            # Delete the casting we created
            print(f"\n6. Deleting casting with ID {new_casting['casting']}:")
            deleted_casting = delete_casting(BASE_URL, new_casting["casting"])
            print(json.dumps(deleted_casting, indent=2))
            
            # Verify the casting was deleted
            print(f"\n7. Verifying casting with ID {new_casting['casting']} was deleted:")
            try:
                get_casting_by_id(BASE_URL, new_casting["casting"])
                print("Error: Casting still exists!")
            except Exception as e:
                print(f"Success: {e}")
        
        except Exception as e:
            print(f"Error: {e}")
            print("Note: If the casting already exists, try changing the casting_number in the example script.")
    
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the API server is running.")


if __name__ == "__main__":
    main()
