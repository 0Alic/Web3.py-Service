pragma solidity ^0.5.0;

contract AssetTracker {

    struct Asset {
        uint id;
        string name;
        bool isActive;
    }

    mapping(address => Asset) owners;
    uint public idCount = 0;

    event NewOwnership(address _owner, uint _assetId, string _assetName);
    event Transfer(address _sender, address _receiver, uint _assetId, string _assetName);

    function obtainOwnership(string memory _name) public payable {

        require(msg.value == 0.001 ether, "Incorrect price");
        require(owners[msg.sender].isActive == false, "The sender already is an owner");

        idCount++;

        owners[msg.sender] = Asset(idCount, _name, true);

        emit NewOwnership(msg.sender, idCount, _name);
    }

    function transferOwnership(address _receiver) public {

        require(owners[msg.sender].isActive == true && owners[_receiver].isActive == false);

        Asset storage _asset = owners[msg.sender];
        owners[_receiver] = _asset;
        delete owners[msg.sender];

        emit Transfer(msg.sender, _receiver, _asset.id, _asset.name);
    }

    function getAsset(address _of) public view returns(uint _id, string memory _name, bool _isActive) {
        Asset storage _asset = owners[_of];
        _id = _asset.id;
        _name = _asset.name;
        _isActive = _asset.isActive;
    }
}