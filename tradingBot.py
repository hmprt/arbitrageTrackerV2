import json
from itertools import combinations
from tradingPair import tradingPair
from web3 import Web3
import pdb
from uniswapInterface import mapUniPairs

class tradingBot:

    def __init__(self, credentials, tokens, exchanges):
        # Import user credentials, token list and exchanges
        with open(credentials) as file1, open(tokens) as file2, open(exchanges) as file3:
            self.credentials = json.load(file1)
            self.tokens = json.load(file2)
            self.exchanges = json.load(file3)

    def connect(self):
        ## Starts a new Web3 session with the specified credentials
        self.w3 = Web3(Web3.HTTPProvider(self.credentials["Provider"]))

    def generatePairs(self):
        ## Use combinatorics to generate trading pairs. As pairs are reversible, we
        ## won't worry about ordering results ("WETH/USDT" is the same as "USDT/WETH"
        ## for our purposes")
        tokenList = list(self.tokens.keys())
        self.tradingPairs = []

        ## Combinatorics! Thanks, itertools

        for pair in combinations(tokenList, 2):

            ## Instantiating a new tradingPair instance
            newPair = tradingPair(

            name = pair[0] + "/" + pair[1],
            token1 = self.tokens[pair[0]],
            token2 = self.tokens[pair[1]],

            ## We leave these fields blank - we'll fill them in using another
            ## function. This is tangentially for performance, but mostly for
            ## readability
            exchanges = {},
            prices = {}
            )
            self.tradingPairs.append(newPair)

    def initialisePairs(self):
        self.tradingPairs = mapUniPairs(self.exchanges["UniswapV2"], self.tradingPairs, self.w3, self.credentials["ethscanAPI"])
        return
