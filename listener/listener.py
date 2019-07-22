from web3 import Web3
from requests import put, get
import json
import asyncio
import urllib.request
import time

contracts = dict()
contractInfo = dict()

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

ganache_url = 'http://ganache:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))

urlPath = 'https://gist.githubusercontent.com/0Alic/e266f13b4b473932b6ee068fbfd73f0f/raw/1da9bf2ce7429bd834c726995e39a117169790ca/AssetTracker.json'

with urllib.request.urlopen(urlPath) as url:
    contractInfo = json.loads(url.read().decode())

# Get reference to the new contract
    # Retrieve the address from the configuration server
api_response = get(route + "/"+tracker).json()
address = api_response["result"]
    # Get the instance from Ethereum
instance = web3.eth.contract(abi=contractInfo['abi'], address=address)
    # Store it somewhere
contracts["tracker"] = instance

"""
    Build event listener
"""

event_filter = contracts["tracker"].events.NewOwnership.createFilter(fromBlock='latest')

while True:
    entries = event_filter.get_new_entries() # list
    for e in entries:
        if e['event'] == 'NewOwnership':
            args = e['args']
            print('owner = ', args['_owner'])
            print('assetId = ', args['_assetId'])
            print('assetName = ', args['_assetName'])

    print(event_filter.get_new_entries())
    time.sleep(3)


# def handle_event(event):
#     print("*************************")
#     print(event)
#     # and whatever

# async def log_loop(event_filter, poll_interval):
#     while True:
#         for event in event_filter.get_new_entries():
#             handle_event(event)
#         await asyncio.sleep(poll_interval)


# block_filter = web3.eth.filter('latest')
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(
#         asyncio.gather(
#             log_loop(block_filter, 2)))
# finally:
#     loop.close()