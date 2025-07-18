const { expect } = require("chai");
const { ethers } = require("hardhat");
const { loadFixture } = require("@nomicfoundation/hardhat-toolbox/network-helpers");

describe("SupplyChainTracker", function () {
  // Sample test data
  const SAMPLE_SHIPMENT_ID = "ABC123";
  const SAMPLE_LOCATION = "New York Warehouse";
  const SAMPLE_STATUS = "in-transit";
  const SAMPLE_DOC_HASH = "QmSampleIPFSHash123";

  // Role enum values (matching the Solidity contract)
  const Role = {
    None: 0,
    Manufacturer: 1,
    Courier: 2,
    Inspector: 3
  };

  // Fixture to deploy contract and set up sample roles
  async function deploySupplyChainTrackerFixture() {
    // Get test accounts
    const [admin, manufacturer, courier, inspector, unauthorized] = await ethers.getSigners();

    // Deploy the contract
    const SupplyChainTracker = await ethers.getContractFactory("SupplyChainTracker");
    const contract = await SupplyChainTracker.deploy();

    // Assign roles to test accounts
    await contract.connect(admin).assignRole(manufacturer.address, Role.Manufacturer);
    await contract.connect(admin).assignRole(courier.address, Role.Courier);
    await contract.connect(admin).assignRole(inspector.address, Role.Inspector);

    return {
      contract,
      admin,
      manufacturer,
      courier,
      inspector,
      unauthorized
    };
  }

  describe("Deployment and Initialization", function () {
    it("Should set the deployer as admin", async function () {
      const { contract, admin } = await loadFixture(deploySupplyChainTrackerFixture);
      expect(await contract.admin()).to.equal(admin.address);
    });

    it("Should assign Inspector role to admin by default", async function () {
      const { contract, admin } = await loadFixture(deploySupplyChainTrackerFixture);
      expect(await contract.getRole(admin.address)).to.equal(Role.Inspector);
    });
  });

  describe("Role Management", function () {
    it("Should allow admin to assign roles", async function () {
      const { contract, admin, manufacturer } = await loadFixture(deploySupplyChainTrackerFixture);
      
      // Check the role was assigned in fixture
      expect(await contract.getRole(manufacturer.address)).to.equal(Role.Manufacturer);
    });

    it("Should emit RoleAssigned event when assigning roles", async function () {
      const { contract, admin, unauthorized } = await loadFixture(deploySupplyChainTrackerFixture);
      
      await expect(contract.connect(admin).assignRole(unauthorized.address, Role.Courier))
        .to.emit(contract, "RoleAssigned")
        .withArgs(unauthorized.address, Role.Courier);
    });

    it("Should reject role assignment from non-admin", async function () {
      const { contract, manufacturer, unauthorized } = await loadFixture(deploySupplyChainTrackerFixture);
      
      await expect(
        contract.connect(manufacturer).assignRole(unauthorized.address, Role.Courier)
      ).to.be.revertedWith("Only admin can do this");
    });

    it("Should allow admin to change existing roles", async function () {
      const { contract, admin, manufacturer } = await loadFixture(deploySupplyChainTrackerFixture);
      
      // Change manufacturer to courier
      await contract.connect(admin).assignRole(manufacturer.address, Role.Courier);
      expect(await contract.getRole(manufacturer.address)).to.equal(Role.Courier);
    });

    it("Should allow admin to revoke roles by setting to None", async function () {
      const { contract, admin, manufacturer } = await loadFixture(deploySupplyChainTrackerFixture);
      
      // Revoke role
      await contract.connect(admin).assignRole(manufacturer.address, Role.None);
      expect(await contract.getRole(manufacturer.address)).to.equal(Role.None);
    });
  });

  describe("Adding Checkpoints", function () {
    it("Should allow authorized users to add checkpoints", async function () {
      const { contract, manufacturer } = await loadFixture(deploySupplyChainTrackerFixture);
      
      await expect(
        contract.connect(manufacturer).addCheckpoint(
          SAMPLE_SHIPMENT_ID,
          SAMPLE_LOCATION,
          SAMPLE_STATUS,
          SAMPLE_DOC_HASH
        )
      ).to.not.be.reverted;
    });

    it("Should emit CheckpointAdded event with correct data", async function () {
      const { contract, courier } = await loadFixture(deploySupplyChainTrackerFixture);
      
      const tx = await contract.connect(courier).addCheckpoint(
        SAMPLE_SHIPMENT_ID,
        SAMPLE_LOCATION,
        SAMPLE_STATUS,
        SAMPLE_DOC_HASH
      );

      const receipt = await tx.wait();
      const block = await ethers.provider.getBlock(receipt.blockNumber);

      await expect(tx)
        .to.emit(contract, "CheckpointAdded")
        .withArgs(SAMPLE_SHIPMENT_ID, block.timestamp, SAMPLE_LOCATION, SAMPLE_STATUS, courier.address);
    });

    it("Should reject checkpoint addition from unauthorized users", async function () {
      const { contract, unauthorized } = await loadFixture(deploySupplyChainTrackerFixture);
      
      await expect(
        contract.connect(unauthorized).addCheckpoint(
          SAMPLE_SHIPMENT_ID,
          SAMPLE_LOCATION,
          SAMPLE_STATUS,
          SAMPLE_DOC_HASH
        )
      ).to.be.revertedWith("Unauthorized: No role assigned");
    });

    it("Should store checkpoint data correctly", async function () {
      const { contract, inspector } = await loadFixture(deploySupplyChainTrackerFixture);
      
      await contract.connect(inspector).addCheckpoint(
        SAMPLE_SHIPMENT_ID,
        SAMPLE_LOCATION,
        SAMPLE_STATUS,
        SAMPLE_DOC_HASH
      );

      const history = await contract.getShipmentHistory(SAMPLE_SHIPMENT_ID);
      expect(history.length).to.equal(1);
      
      const checkpoint = history[0];
      expect(checkpoint.shipmentId).to.equal(SAMPLE_SHIPMENT_ID);
      expect(checkpoint.location).to.equal(SAMPLE_LOCATION);
      expect(checkpoint.status).to.equal(SAMPLE_STATUS);
      expect(checkpoint.documentHash).to.equal(SAMPLE_DOC_HASH);
      expect(checkpoint.submittedBy).to.equal(inspector.address);
      expect(checkpoint.timestamp).to.be.greaterThan(0);
    });

    it("Should allow multiple checkpoints for the same shipment", async function () {
      const { contract, manufacturer, courier } = await loadFixture(deploySupplyChainTrackerFixture);
      
      // Add first checkpoint
      await contract.connect(manufacturer).addCheckpoint(
        SAMPLE_SHIPMENT_ID,
        "Factory Floor",
        "created",
        "QmHash1"
      );

      // Add second checkpoint
      await contract.connect(courier).addCheckpoint(
        SAMPLE_SHIPMENT_ID,
        "Distribution Center",
        "picked-up",
        "QmHash2"
      );

      const history = await contract.getShipmentHistory(SAMPLE_SHIPMENT_ID);
      expect(history.length).to.equal(2);
      
      expect(history[0].location).to.equal("Factory Floor");
      expect(history[0].status).to.equal("created");
      expect(history[1].location).to.equal("Distribution Center");
      expect(history[1].status).to.equal("picked-up");
    });

    it("Should handle empty document hash", async function () {
      const { contract, manufacturer } = await loadFixture(deploySupplyChainTrackerFixture);
      
      await contract.connect(manufacturer).addCheckpoint(
        SAMPLE_SHIPMENT_ID,
        SAMPLE_LOCATION,
        SAMPLE_STATUS,
        "" // Empty document hash
      );

      const history = await contract.getShipmentHistory(SAMPLE_SHIPMENT_ID);
      expect(history[0].documentHash).to.equal("");
    });
  });

  describe("Shipment History Retrieval", function () {
    it("Should return empty array for non-existent shipment", async function () {
      const { contract } = await loadFixture(deploySupplyChainTrackerFixture);
      
      const history = await contract.getShipmentHistory("NON_EXISTENT");
      expect(history.length).to.equal(0);
    });

    it("Should return correct checkpoint count", async function () {
      const { contract, manufacturer, courier, inspector } = await loadFixture(deploySupplyChainTrackerFixture);
      
      // Add three checkpoints
      await contract.connect(manufacturer).addCheckpoint(SAMPLE_SHIPMENT_ID, "Location1", "status1", "hash1");
      await contract.connect(courier).addCheckpoint(SAMPLE_SHIPMENT_ID, "Location2", "status2", "hash2");
      await contract.connect(inspector).addCheckpoint(SAMPLE_SHIPMENT_ID, "Location3", "status3", "hash3");

      expect(await contract.getCheckpointCount(SAMPLE_SHIPMENT_ID)).to.equal(3);
    });

    it("Should maintain checkpoint order (chronological)", async function () {
      const { contract, manufacturer, courier } = await loadFixture(deploySupplyChainTrackerFixture);
      
      const tx1 = await contract.connect(manufacturer).addCheckpoint(SAMPLE_SHIPMENT_ID, "First", "created", "hash1");
      const receipt1 = await tx1.wait();
      const block1 = await ethers.provider.getBlock(receipt1.blockNumber);

      // Add small delay to ensure different timestamps
      await new Promise(resolve => setTimeout(resolve, 1000));

      const tx2 = await contract.connect(courier).addCheckpoint(SAMPLE_SHIPMENT_ID, "Second", "shipped", "hash2");
      const receipt2 = await tx2.wait();
      const block2 = await ethers.provider.getBlock(receipt2.blockNumber);

      const history = await contract.getShipmentHistory(SAMPLE_SHIPMENT_ID);
      
      expect(history[0].location).to.equal("First");
      expect(history[1].location).to.equal("Second");
      expect(Number(history[0].timestamp)).to.be.lessThanOrEqual(Number(history[1].timestamp));
    });

    it("Should isolate shipment histories", async function () {
      const { contract, manufacturer } = await loadFixture(deploySupplyChainTrackerFixture);
      
      // Add checkpoints to different shipments
      await contract.connect(manufacturer).addCheckpoint("SHIPMENT_A", "LocationA", "statusA", "hashA");
      await contract.connect(manufacturer).addCheckpoint("SHIPMENT_B", "LocationB", "statusB", "hashB");

      const historyA = await contract.getShipmentHistory("SHIPMENT_A");
      const historyB = await contract.getShipmentHistory("SHIPMENT_B");

      expect(historyA.length).to.equal(1);
      expect(historyB.length).to.equal(1);
      expect(historyA[0].location).to.equal("LocationA");
      expect(historyB[0].location).to.equal("LocationB");
    });
  });

  describe("Access Control Edge Cases", function () {
    it("Should reject checkpoint from user whose role was revoked", async function () {
      const { contract, admin, manufacturer } = await loadFixture(deploySupplyChainTrackerFixture);
      
      // First, manufacturer should be able to add checkpoint
      await contract.connect(manufacturer).addCheckpoint(SAMPLE_SHIPMENT_ID, SAMPLE_LOCATION, SAMPLE_STATUS, SAMPLE_DOC_HASH);

      // Revoke manufacturer's role
      await contract.connect(admin).assignRole(manufacturer.address, Role.None);

      // Now manufacturer should be rejected
      await expect(
        contract.connect(manufacturer).addCheckpoint(SAMPLE_SHIPMENT_ID, "New Location", "New Status", "New Hash")
      ).to.be.revertedWith("Unauthorized: No role assigned");
    });

    it("Should allow admin to add checkpoints (admin has Inspector role)", async function () {
      const { contract, admin } = await loadFixture(deploySupplyChainTrackerFixture);
      
      await expect(
        contract.connect(admin).addCheckpoint(SAMPLE_SHIPMENT_ID, SAMPLE_LOCATION, SAMPLE_STATUS, SAMPLE_DOC_HASH)
      ).to.not.be.reverted;
    });
  });

  describe("Data Integrity", function () {
    it("Should preserve all checkpoint data accurately", async function () {
      const { contract, courier } = await loadFixture(deploySupplyChainTrackerFixture);
      
      const testData = {
        shipmentId: "TEST_SHIPMENT_2024",
        location: "Special Characters: åöä & <script>alert('test')</script>",
        status: "in-transit-with-special-handling",
        documentHash: "QmVeryLongIPFSHashExample1234567890ABCDEFabcdef"
      };

      await contract.connect(courier).addCheckpoint(
        testData.shipmentId,
        testData.location,
        testData.status,
        testData.documentHash
      );

      const history = await contract.getShipmentHistory(testData.shipmentId);
      const checkpoint = history[0];

      expect(checkpoint.shipmentId).to.equal(testData.shipmentId);
      expect(checkpoint.location).to.equal(testData.location);
      expect(checkpoint.status).to.equal(testData.status);
      expect(checkpoint.documentHash).to.equal(testData.documentHash);
      expect(checkpoint.submittedBy).to.equal(courier.address);
    });
  });
}); 