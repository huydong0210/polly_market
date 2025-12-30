from cache.market_cache import market_cache
from gamma_api.gamma_api_service import gamma_api_service

def main():
    dota_markets = gamma_api_service.get_active_dota_markets()
    for dota_market in dota_markets:
        market_cache.add_dota_market(dota_market)
    current_cache = market_cache.get_all_dota_market()
    for item in current_cache:
        print(item)
    
if __name__ == "__main__":
    main()
        





