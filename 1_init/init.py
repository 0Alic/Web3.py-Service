import json
from web3 import Web3
import urllib.request
import requests
from requests import put, get

"""
    Initialize the blockchain deploying a contract
"""

"""
    API configuration server parameters
"""

# TODO read from config file?
host = "http://config:"
port = 80
route = host + str(port)
tracker = "tracker"


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
    Load contract json from url
"""

urlPath = 'https://gist.githubusercontent.com/0Alic/e266f13b4b473932b6ee068fbfd73f0f/raw/1da9bf2ce7429bd834c726995e39a117169790ca/AssetTracker.json'
abi = ""
bytecode = ""

with urllib.request.urlopen(urlPath) as url:
    obj = json.loads(url.read().decode())
    abi = obj["abi"]
    bytecode = obj["bytecode"]

"""
    Deploy contract
"""

#Create contract object    
contract = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor().transact({'from': alice})
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
#print(tx_receipt)

# Store contract address in config file
contract_address = Web3.toChecksumAddress(tx_receipt.contractAddress)
try:
    api_response = put(route + "/"+tracker, data={'data': contract_address}).json()
    print(api_response)
    api_response = get(route + "/"+tracker).json()
    print(api_response)
except requests.exceptions.ConnectionError as e:
    print(e)
    
# Get reference to the new contract
instance = web3.eth.contract(abi=abi, address=contract_address)
print("Contract address >>>> ", contract_address)
print("IdCount Should be 0 >>>> ", instance.functions.idCount().call())

# Play with the contract
tx_hash = instance.functions.obtainOwnership("Smart Box").transact({'from': alice, 'value': web3.toWei(0.001, 'ether')})
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
asset = instance.functions.getAsset(alice).call()
print("Alice's asset data: ", asset)

tx_hash = instance.functions.transferOwnership(bob).transact({'from': alice})
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
asset = instance.functions.getAsset(alice).call()
print("Alice's asset data: ", asset)
asset = instance.functions.getAsset(bob).call()
print("Bob's asset data: ", asset)
print("IdCount Should be 1 >>>> ", instance.functions.idCount().call())
