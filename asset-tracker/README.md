# asset-tracker

This service is in charge to call the functions provided by the AssetTracker smart contract. It provides REST API.

In the **PUT** column, at the beginning there are the data sent with the **PUT** request, written in form ('data1', 'data2', ....). They are not part of the route. This data is provided by the client using flask-restful functionalities ([example](https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api)).


## Routes

|    ROUTE      |            GET           |             PUT            | POST | DELETE |
|:--------:|:------------------------:|:--------------------------:|:----:|:------:|
| / | Get connection status and number of blocks |  |      |        |
| /idCount/[contract] | Get idCount of a specific AssetTracker [contract] |  |      |        |
| /get/[contract]/[sender] | Get the current asset status of [sender] in [contract]  | |      |        |
| /obtain/[contract] |  | ('sender', 'assetName): 'sender' obtains the ownership of a particular asset named 'assetName' in [contract] |      |        |
| /transfer/[contract] |  | ('sender', 'to'): 'sender' transfers the ownership of its asset, if any, to 'to' in [contract] |      |        |