import pdb
import requests
def mapUniPairs(exchangeData, pairsList, w3, ethscanAPI):

    ## Let's pull the factory smart contract
    uniswap = w3.eth.contract(address = exchangeData["address"],
                                abi = exchangeData["ABI"])

    for pair in pairsList:

        ## Converting addresses to checksum to uniswap smart contract can
        ## work with them. Might as well leave them this way!
        pair.token1["address"] = w3.toChecksumAddress(pair.token1["address"])
        pair.token2["address"] = w3.toChecksumAddress(pair.token2["address"])

        ## Now, we get the exchange address
        pairAddress = uniswap.functions.getPair(pair.token1["address"], pair.token2["address"]).call()

        ## If lookup bounces, we won't bother searching for an ABI and will remove
        ## pair from circulation

        if (int(pairAddress[2:], 16) == 0):
            print("Removed " + pair.name + ": no exchange")
            pairsList.remove(pair)
            continue

        ## And we can grab the pair's ABI from the buggy-as-hell etherscan.io API
        req = requests.get("https://api.etherscan.io/api?module=contract&action=getabi&address="
        + pairAddress + "&apikey=" + ethscanAPI)


        ## Etherscan API is currently bugged, so have to clean up the HTTP response
        ABI = str(req.content)
        ABI = ABI.replace('\\\\\"', '"')
        ABI = ABI.replace("'", ' " ')
        ABI = ABI.replace(":", ' : ')
        ABI = ABI.lstrip("\"b\'{\\\"status\\\":\\\"1\\\",\\\"message\\\":\\\"OK\\\",\\\"result\\\":\\\"\" \" ")
        ABI = ABI.rstrip("\"}\\\' \" ")

        ## Catch bad responses
        if (ABI.find("Contract source code not verified") > -1):
            print("Contract source code not verified! \n Try https://etherscan.io/address/" + pairAddress)
            continue

        pair.exchanges["Uniswap"] = {"address" : pairAddress, "ABI" : ABI }
        print("Loaded " + pair.name)
    return(pairsList)
