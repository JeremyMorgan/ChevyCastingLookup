import argparse
import json
import requests


def get_castings(base_url, skip=0, limit=100):
    """
    Get a list of castings.
    
    Args:
        base_url: Base URL of the API
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of castings
    """
    url = f"{base_url}/api/castings/"
    params = {"skip": skip, "limit": limit}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()


def get_casting_by_id(base_url, casting_id):
    """
    Get a specific casting by its ID.
    
    Args:
        base_url: Base URL of the API
        casting_id: Casting ID to look up
        
    Returns:
        Casting data
    """
    url = f"{base_url}/api/castings/{casting_id}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()


def create_casting(base_url, casting_data):
    """
    Create a new casting.
    
    Args:
        base_url: Base URL of the API
        casting_data: Casting data to create
        
    Returns:
        Created casting data
    """
    url = f"{base_url}/api/castings/"
    
    response = requests.post(url, json=casting_data)
    response.raise_for_status()
    
    return response.json()


def update_casting(base_url, casting_id, casting_data):
    """
    Update an existing casting.
    
    Args:
        base_url: Base URL of the API
        casting_id: Casting ID to update
        casting_data: Casting data to update
        
    Returns:
        Updated casting data
    """
    url = f"{base_url}/api/castings/{casting_id}"
    
    response = requests.put(url, json=casting_data)
    response.raise_for_status()
    
    return response.json()


def delete_casting(base_url, casting_id):
    """
    Delete a casting.
    
    Args:
        base_url: Base URL of the API
        casting_id: Casting ID to delete
        
    Returns:
        Deleted casting data
    """
    url = f"{base_url}/api/castings/{casting_id}"
    
    response = requests.delete(url)
    response.raise_for_status()
    
    return response.json()


def search_castings(base_url, **search_params):
    """
    Search for castings.
    
    Args:
        base_url: Base URL of the API
        **search_params: Search parameters
        
    Returns:
        List of castings matching the search criteria
    """
    url = f"{base_url}/api/castings/search/"
    
    response = requests.get(url, params=search_params)
    response.raise_for_status()
    
    return response.json()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Casting API Client")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--action",
        choices=[
            "list",
            "get",
            "create",
            "update",
            "delete",
            "search"
        ],
        required=True,
        help="Action to perform"
    )
    parser.add_argument(
        "--casting-id",
        help="Casting ID for get, update, and delete actions"
    )
    parser.add_argument(
        "--data",
        help="JSON data for create and update actions"
    )
    parser.add_argument(
        "--years",
        help="Years for search action (e.g., '1980-85')"
    )
    parser.add_argument(
        "--cid",
        type=int,
        help="Cubic Inch Displacement for search action"
    )
    parser.add_argument(
        "--main-caps",
        help="Main caps for search action"
    )
    parser.add_argument(
        "--comments",
        help="Comments for search action"
    )
    parser.add_argument(
        "--skip",
        type=int,
        default=0,
        help="Number of records to skip for list and search actions"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of records to return for list and search actions"
    )
    args = parser.parse_args()
    
    try:
        if args.action == "list":
            result = get_castings(
                args.base_url,
                skip=args.skip,
                limit=args.limit
            )
        
        elif args.action == "get":
            if args.casting_id is None:
                parser.error("--casting-id is required for get action")
            
            result = get_casting_by_id(
                args.base_url,
                args.casting_id
            )
        
        elif args.action == "create":
            if args.data is None:
                parser.error("--data is required for create action")
            
            try:
                casting_data = json.loads(args.data)
            except json.JSONDecodeError as e:
                parser.error(f"Invalid JSON data: {e}")
            
            result = create_casting(
                args.base_url,
                casting_data
            )
        
        elif args.action == "update":
            if args.casting_id is None:
                parser.error("--casting-id is required for update action")
            
            if args.data is None:
                parser.error("--data is required for update action")
            
            try:
                casting_data = json.loads(args.data)
            except json.JSONDecodeError as e:
                parser.error(f"Invalid JSON data: {e}")
            
            result = update_casting(
                args.base_url,
                args.casting_id,
                casting_data
            )
        
        elif args.action == "delete":
            if args.casting_id is None:
                parser.error("--casting-id is required for delete action")
            
            result = delete_casting(
                args.base_url,
                args.casting_id
            )
        
        elif args.action == "search":
            search_params = {}
            
            if args.years is not None:
                search_params["years"] = args.years
            
            if args.cid is not None:
                search_params["cid"] = args.cid
            
            if args.main_caps is not None:
                search_params["main_caps"] = args.main_caps
            
            if args.comments is not None:
                search_params["comments"] = args.comments
            
            search_params["skip"] = args.skip
            search_params["limit"] = args.limit
            
            result = search_castings(
                args.base_url,
                **search_params
            )
        
        # Print result
        print(json.dumps(result, indent=2))
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        
        if hasattr(e, "response") and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"API Error: {json.dumps(error_data, indent=2)}")
            except json.JSONDecodeError:
                print(f"API Response: {e.response.text}")


if __name__ == "__main__":
    main()
