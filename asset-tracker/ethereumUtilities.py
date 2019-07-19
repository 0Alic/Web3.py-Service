import urllib.request
import json
from web3 import Web3

class EthereumUtilities():
    
    @staticmethod
    def LoadWeb3(provider=None, port=None):
        # TODO parse input, error handling
        url = provider + ':' + str(port)
        web3 = Web3(Web3.HTTPProvider(url))
        return web3

    @staticmethod
    def LoadContractInformation(webUrl=None, localUrl=None):
        # TODO parse input, error handling
        obj = dict()

        if not webUrl is None:
            with urllib.request.urlopen(webUrl) as url:
                obj = json.loads(url.read().decode())

        elif not localUrl is None:
            with open(localUrl) as jsn:
                obj = json.load(jsn)

        return {
            "abi": obj["abi"],
            "bytecode": obj["bytecode"]
        }