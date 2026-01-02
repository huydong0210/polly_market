

class MarketCache:
    def __init__(self):
        self.dota_markets = []
    def add_dota_market(self, dota_market):
        to_append = {
            "question" : dota_market["question"],
            "clobTokenIds" : dota_market["clobTokenIds"]
        }
        for market in self.dota_markets:
            if dota_market["question"] == market["question"]:
                return
        self.dota_markets.append(to_append)
    def get_all_dota_market(self):
        return self.dota_markets
    
    def load_fake_data(self, fake_data_list):
        for data in fake_data_list:
            self.add_dota_market(data)
    
    
market_cache = MarketCache()
        