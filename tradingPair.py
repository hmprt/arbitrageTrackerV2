import json


class tradingPair:
    def __init__(self, name, token1, token2, exchanges, prices):
        self.name = name
        self.token1 = token1
        self.token2 = token2
        self.exchanges = exchanges
        self.prices = prices
    
