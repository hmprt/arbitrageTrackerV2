from tradingBot import tradingBot
import pdb

credentials = "data/credentials.json"
tokens = "data/tokens.json"
exchanges = "data/exchanges.json"

trader = tradingBot(credentials, tokens, exchanges)

trader.connect()
trader.generatePairs()

trader.initialisePairs()
