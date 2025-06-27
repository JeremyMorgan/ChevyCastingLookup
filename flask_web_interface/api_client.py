import requests
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class CastingAPIClient:
    """Client for communicating with the FastAPI casting lookup service."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api/castings"
        self.timeout = 10
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to the API with error handling."""
        url = f"{self.api_base}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            logger.error(f"Failed to connect to API at {url}")
            raise Exception("Unable to connect to the casting lookup API. Please ensure the API server is running.")
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {url}")
            raise Exception("Request timed out. Please try again.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            logger.error(f"HTTP error {e.response.status_code} for {url}")
            raise Exception(f"API request failed: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {str(e)}")
            raise Exception("An unexpected error occurred while contacting the API.")
    
    def get_casting_by_id(self, casting_id: str) -> Optional[Dict]:
        """Get a specific casting by its ID."""
        return self._make_request(f"/{casting_id}")
    
    def get_all_castings(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all castings with pagination."""
        params = {"skip": skip, "limit": limit}
        result = self._make_request("/", params=params)
        return result if result else []
    
    def search_castings(self, years: str = None, cid: int = None, 
                       main_caps: str = None, comments: str = None,
                       skip: int = 0, limit: int = 100) -> List[Dict]:
        """Search castings based on criteria."""
        params = {"skip": skip, "limit": limit}
        
        if years:
            params["years"] = years
        if cid:
            params["cid"] = cid
        if main_caps:
            params["main_caps"] = main_caps
        if comments:
            params["comments"] = comments
        
        result = self._make_request("/search/", params=params)
        return result if result else []
    
    def health_check(self) -> bool:
        """Check if the API is accessible."""
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False
