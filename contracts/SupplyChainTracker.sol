// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title SupplyChainTracker
 * @dev A simple contract to track checkpoints in a supply chain
 */
contract SupplyChainTracker {
    address public owner;
    
    struct Checkpoint {
        string location;
        uint256 timestamp;
        address validator;
        string status;
        bytes32 documentHash; // Optional: for IPFS document hash
    }
    
    // Maps shipmentId to array of checkpoints
    mapping(string => Checkpoint[]) public shipments;
    
    event CheckpointAdded(
        string shipmentId,
        string location,
        uint256 timestamp,
        address validator,
        string status
    );
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    // Function placeholders to be implemented later
    
    function addCheckpoint(
        string memory _shipmentId,
        string memory _location,
        string memory _status,
        bytes32 _documentHash
    ) public {
        // Implementation will come in Phase 2
    }
    
    function getCheckpoints(string memory _shipmentId) public view returns (Checkpoint[] memory) {
        // Implementation will come in Phase 2
        return shipments[_shipmentId];
    }
} 