import json
import urllib.request
from ethereumUtilities import EthereumUtilities
from web3 import Web3
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from requests import put, get

app = Flask(__name__)
api = Api(app)

"""
    Variables
"""

contracts = dict()
web3 = None
userMap = dict()

"""
    API configuration server parameters
"""

# TODO read from config file?
host = "http://config:"
port = 80
route = host + str(port)
tracker = "tracker"

"""
    Init Web3 and load contract
"""

web3 = EthereumUtilities.LoadWeb3(provider='http://ganache', port='8545')

accounts = web3.eth.accounts
userMap = {
    "alice": accounts[0],
    "bob": accounts[1],
    "carl": accounts[2],
    "dave": accounts[3]
}

urlPath = 'https://gist.githubusercontent.com/0Alic/e266f13b4b473932b6ee068fbfd73f0f/raw/1da9bf2ce7429bd834c726995e39a117169790ca/AssetTracker.json'
contractInfo = EthereumUtilities.LoadContractInformation(webUrl=urlPath)

"""
    Initialization
"""

def init():

    # Get reference to the new contract
        # Retrieve the address from the configuration server
    api_response = get(route + "/"+tracker).json()
    address = api_response["result"]
        # Get the instance from Ethereum
    instance = web3.eth.contract(abi=contractInfo['abi'], address=address)
        # Store it somewhere
    contracts["tracker"] = instance

"""
    Define REST services
"""

class Connection(Resource):
    def get(self):
        status = web3.isConnected()
        number = web3.eth.blockNumber

        return {
            'result' : status,
            'number': number    
        }

# TODO Temp solution, address the contract with a predefined name
class GetAsset(Resource):

    def get(self, contract, sender):

        instance = contracts[str(contract)]
        account = userMap[str(sender)]
        asset = instance.functions.getAsset(Web3.toChecksumAddress(account)).call()
        return {'result': asset}

class IdCount(Resource):

    def get(self, contract):
                    
        instance = contracts[str(contract)]
        return {'idCount': instance.functions.idCount().call()}
         
class ObtainOwnership(Resource):

    def put(self, contract):

        sender = request.form['sender']
        assetName = request.form['assetName']

        instance = contracts[str(contract)]
        sender = Web3.toChecksumAddress(userMap[str(sender)])

        tx_hash = instance.functions.obtainOwnership(assetName).transact({'from': sender, 'value': web3.toWei(0.001, 'ether')})
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        # TODO Trovare il modo per serializzare la receipt
        return {'receipt': "tx_receipt" }

#TODO
## return {tx_receipt  non funziona
class TransferOwnership(Resource):

    def put(self, contract):

        sender = Web3.toChecksumAddress(userMap[request.form['sender']])
        to = Web3.toChecksumAddress(userMap[request.form['to']])

        instance = contracts[str(contract)]

        tx_hash = instance.functions.transferOwnership(to).transact({'from': sender})
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        # TODO Trovare il modo per serializzare la receipt
        return {'receipt': "tx_receipt" }

"""
    Add services
"""

api.add_resource(Connection, '/')
api.add_resource(IdCount, '/idCount/<contract>')
api.add_resource(GetAsset, '/get/<contract>/<sender>')
api.add_resource(ObtainOwnership, '/obtain/<contract>')
api.add_resource(TransferOwnership, '/transfer/<contract>')

if __name__ == '__main__':
    
    init()
    app.run(host="0.0.0.0", port=80, debug=True)