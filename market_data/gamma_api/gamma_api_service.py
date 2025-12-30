import requests
from typing import Dict, List, Optional

class GammaAPIService:
    def __init__(self):
        self.base_url = "https://gamma-api.polymarket.com"
    
    def get_active_dota_markets(self, limit: int = 100) -> List[Dict]:
        """
        Get all active (open) Dota markets
        
        Args:
            limit: Maximum number of markets to fetch
        
        Returns:
            List of active Dota markets
        """
        endpoint = f"{self.base_url}/markets"
        
        
        limit = 100
        offset =0
        dota_markets = []
        while True:
            offset +=limit
            params = {
            "closed": False,  # Only open markets
            "limit": limit,
            "offset": offset
            }
            
            try:
                print(f"start fetch from offet {offset}")
                response = requests.get(endpoint, params=params)
                response.raise_for_status()
                all_markets = response.json()

                # Filter for Dota markets
                if len(all_markets) == 0:
                    break
                for market in all_markets:
                    question = market.get('question', '').lower()
                    if "dota 2:" in question:
                        dota_markets.append(market)
            
            except requests.exceptions.RequestException as e:
                print(f"Error getting active dota markets: {e}")
                break
        return dota_markets
    
gamma_api_service = GammaAPIService()

# Example usage
if __name__ == "__main__":
    api = GammaAPIService()
    dota_markets = api.get_active_dota_markets()
    print(f"found {len(dota_markets)} dota market")
    for dota_market in dota_markets:
        print(dota_market["question"])
        
    
        

    
