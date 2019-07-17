import json
import web3
from web3 import Web3
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

"""
    Init Web3
"""

ganache_url = 'http://ganache:8545'

web3 = Web3(Web3.HTTPProvider(ganache_url))

class Connection(Resource):
    def get(self):
        status = web3.isConnected()
        number = web3.eth.blockNumber

        return {
            'result' : status,
            'number': number    
        }

api.add_resource(Connection, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)