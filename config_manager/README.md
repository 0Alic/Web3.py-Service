# config_manager

This service is in charge to update and provide a configuration file common to the other services. It provides REST API to modify it. 

At the moment, it does not implement any access control mechanism.

## Routes

|          |            GET           |             PUT            | POST | DELETE |
|:--------:|:------------------------:|:--------------------------:|:----:|:------:|
| /tracker | Get the contract address | ('data'): Store the contract address |      |        |