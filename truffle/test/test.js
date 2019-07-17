const AssetTracker = artifacts.require("AssetTracker");

contract("AssetTracker", accounts => {

    const alice = accounts[1]; // System creator
    const bob = accounts[8];   // User of the System
    const carl = accounts[7];  // Rater EOA user
    const dave = accounts[6];  // Error Test user

    const price = web3.utils.toWei('0.001', 'ether');

    /////////////////
    // Deployment ownership test
    /////////////////


    it("Should test Obtain ownership", async() => {
    
        let tracker = await AssetTracker.deployed();
        let tx = await tracker.obtainOwnership("Box", {from: alice, value: price});
        let asset = await tracker.getAsset(alice);

        assert.equal(asset._isActive, true, "Is Valid should be true");
        assert.equal(asset._id, 1, "Id should be 1");
        assert.equal(asset._name, "Box", "Name should be 'Box'");
    });

    it("Should test Transfer ownership", async() => {
    
        let tracker = await AssetTracker.deployed();
        let tx = await tracker.transferOwnership(bob, {from: alice});
        let assetAlice = await tracker.getAsset(alice);
        let assetBob = await tracker.getAsset(bob);

        assert.equal(assetBob._isActive, true, "Bob: Is Valid should be true");
        assert.equal(assetBob._id, 1, "Bob: Id should be 1");
        assert.equal(assetBob._name, "Box", "Bob: Name should be 'Box'");

        assert.equal(assetAlice._isActive, false, "Alice: Is Valid should be false");
        assert.equal(assetAlice._id, 0, "Alice: Id should be 0");
        assert.equal(assetAlice._name, "", "Alice: Name should be ''");

    });


});