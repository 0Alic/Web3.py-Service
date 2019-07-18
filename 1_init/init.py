import json
from web3 import Web3
import urllib.request

"""
    Initialize the blockchain deploying a contract
"""

"""
    Init Web3
"""

ganache_url = 'http://ganache:8545'

web3 = Web3(Web3.HTTPProvider(ganache_url))
print("**** ", web3.isConnected())
print("**** ", web3.eth.blockNumber)

# Test accounts
accounts = web3.eth.accounts
alice = accounts[0]
bob = accounts[1]

"""
    Load contract from url
"""

contractPath = './truffle/build/contracts/AssetTracker.json'
urlPath = 'https://gist.githubusercontent.com/0Alic/e266f13b4b473932b6ee068fbfd73f0f/raw/1da9bf2ce7429bd834c726995e39a117169790ca/AssetTracker.json'
abi = ""
bytecode = ""

with urllib.request.urlopen(urlPath) as url:
    obj = json.loads(url.read().decode())
    abi = obj["abi"]
    bytecode = obj["bytecode"]

# with open(contractPath) as json_obj:
#     contractObject = json.load(json_obj)
#     abi = contractObject["abi"]
#     bytecode = contractObject["bytecode"]

"""
    Deploy contract
"""

#Create contract object    
contract = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor().transact({'from': alice})
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)

# Get reference to the new contract
instance = web3.eth.contract(abi=abi, address=tx_receipt.contractAddress)
print(">>>> ", instance.functions.idCount().call())