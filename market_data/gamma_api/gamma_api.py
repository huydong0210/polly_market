import requests
from typing import Dict, List, Optional

class GammaAPI:
    def __init__(self):
        self.base_url = "https://gamma-api.polymarket.com"
    
    def search_dota_markets(self, 
                           query: str = "dota", 
                           limit_per_type: int = 10,
                           keep_closed_markets: int = 0) -> Dict:
        """
        Search for Dota-related markets on Polymarket
        
        Args:
            query: Search term (default: "dota")
            limit_per_type: Number of results per type (default: 10)
            keep_closed_markets: Include closed markets (0=no, 1=yes)
        
        Returns:
            Dict containing search results
        """
        endpoint = f"{self.base_url}/public-search"
        
        params = {
            "q": query,
            "limit_per_type": limit_per_type,
            "keep_closed_markets": keep_closed_markets,
            "optimized": True
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching markets: {e}")
            return {}

# Example usage
if __name__ == "__main__":
    api = GammaAPI()
    results = api.search_dota_markets()
    
    if results:
        print(f"Found {len(results.get('events', []))} events")
        for event in results.get('events', [])[:3]:
            print(f"- {event.get('title', 'N/A')}")
