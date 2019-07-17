# Web3 Service: Solidity, Python, Docker

Process to learn how to build a simple REST service with web3.py and Docker.

I set up this repository as a tutorial to myself to learn Docker, and try to use it to build a little service talking to an Ethereum smart contract. Maybe this is not the correct way, but whatever.

Download the repository, and in the main folder run:

First, you might want to compile the contract. You can compile it with ``truffle``:

    cd truffle
    truffle compile
    
Then, on the main folder run:

    docker-compose build
    docker-compose up

This will set up ganache-cli as a local Ethereum blockchain and start the Python service, which exposes a Flask interface.

Go to the browser at: ``localhost:5001/`` to see if the service is connected to Ganache.

## What helped me

[Docker compose](https://www.youtube.com/watch?v=Qw9zlE3t8Ko)

[Ganache-cli on Docker](https://levelup.gitconnected.com/run-the-ganache-cli-inside-the-docker-container-5e70bc962bfe)

[No connection between my Flask Container and the Ganache Container (Stackoverflow)](https://stackoverflow.com/questions/56506935/no-connection-between-my-flask-container-and-the-ganache-container)