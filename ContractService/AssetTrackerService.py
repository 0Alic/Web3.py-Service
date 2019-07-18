import json
import urllib.request
from web3 import Web3
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

"""
    Variables
"""

contracts = dict()

"""
    Init Web3 and load contract
"""

ganache_url = 'http://ganache:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))

accounts = web3.eth.accounts
alice = accounts[0]
bob = accounts[1]
carl = accounts[2]
dave = accounts[3]

print("alice  ", alice)
print("bob  ", bob)
print("calr  ", carl)
print("dave  ", dave)


urlPath = 'https://gist.githubusercontent.com/0Alic/e266f13b4b473932b6ee068fbfd73f0f/raw/1da9bf2ce7429bd834c726995e39a117169790ca/AssetTracker.json'
abi = ""
bytecode = ""

with urllib.request.urlopen(urlPath) as url:
    obj = json.loads(url.read().decode())
    abi = obj["abi"]
    bytecode = obj["bytecode"]

"""
    Define initialization
"""
instace_address = ""

def init():

    #Create contract object    
    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact({'from': alice})
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print("Contract address >>>> ", tx_receipt.contractAddress)

    # Get reference to the new contract
    instance = web3.eth.contract(abi=abi, address=tx_receipt.contractAddress)
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

    # Store contract in "contracts" dict
    contracts[str(instance.address)] =  instance
    instace_address = str(instance.address)
    print(instace_address)
    contracts['0'] =  instance

    print(contracts)

"""
    Define REST routes
"""

class Connection(Resource):
    def get(self):
        status = web3.isConnected()
        number = web3.eth.blockNumber

        return {
            'result' : status,
            'number': number    
        }

class GetAsset(Resource):

    def get(self, address, account):

        instance = contracts[Web3.toChecksumAddress(address)]
        asset = instance.functions.getAsset(Web3.toChecksumAddress(account)).call()
        return {'result': asset}

class IdCount(Resource):

    def get(self, key):
                    
       instance = contracts[Web3.toChecksumAddress(key)]
       return {'idCount': instance.functions.idCount().call()}
        
class ObtainOwnership(Resource):

    def get(self, address, name):

        instance = contracts[Web3.toChecksumAddress(address)]
        tx_hash = instance.functions.obtainOwnership(name).transact({'from': alice, 'value': web3.toWei(0.001, 'ether')})
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        return {'receipt': tx_receipt}

#TODO
## return {tx_receipt  non funziona
## Inserisci mittente come paramentro
## Fai tabella stringa -> indirizzo per semplificare lo sviluppo
class TransferOwnership(Resource):

    def get(self, address, to):

        instance = contracts[Web3.toChecksumAddress(address)]
        tx_hash = instance.functions.transferOwnership(Web3.toChecksumAddress(to)).transact({'from': alice})
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        return {'receipt': tx_receipt}

"""
    Add services
"""


api.add_resource(Connection, '/')
api.add_resource(IdCount, '/idCount/<key>')
api.add_resource(GetAsset, '/get/<address>/<account>')
api.add_resource(ObtainOwnership, '/obtain/<address>/<name>')
api.add_resource(TransferOwnership, '/transfer/<address>/<to>')

if __name__ == '__main__':
    
    init()
    app.run(host="0.0.0.0", port=80, debug=True)