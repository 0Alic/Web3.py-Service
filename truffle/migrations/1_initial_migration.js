const Migrations = artifacts.require("Migrations");
const AssetTracker = artifacts.require("AssetTracker");

module.exports = function(deployer) {
  deployer.deploy(Migrations);
  deployer.deploy(AssetTracker);
};
