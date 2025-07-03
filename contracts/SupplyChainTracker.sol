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
    
    // Mapping to track authorized validators
    mapping(address => bool) public authorizedValidators;
    
    event CheckpointAdded(
        string shipmentId,
        string location,
        uint256 timestamp,
        address validator,
        string status
    );
    
    constructor() {
        owner = msg.sender;
        // Owner is automatically an authorized validator
        authorizedValidators[owner] = true;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier onlyAuthorized() {
        require(authorizedValidators[msg.sender], "Caller is not authorized");
        _;
    }
    
    // Function to add or remove validators
    function setValidatorStatus(address _validator, bool _status) public onlyOwner {
        authorizedValidators[_validator] = _status;
    }
    
    // Function placeholders to be implemented later
    
    function addCheckpoint(
        string memory _shipmentId,
        string memory _location,
        string memory _status,
        bytes32 _documentHash
    ) public onlyAuthorized {
        // Input validation
        require(bytes(_shipmentId).length > 0, "Shipment ID cannot be empty");
        require(bytes(_location).length > 0, "Location cannot be empty");
        require(bytes(_status).length > 0, "Status cannot be empty");
        
        // Create new checkpoint
        Checkpoint memory newCheckpoint = Checkpoint({
            location: _location,
            timestamp: block.timestamp,
            validator: msg.sender,
            status: _status,
            documentHash: _documentHash
        });
        
        // Add checkpoint to shipment
        shipments[_shipmentId].push(newCheckpoint);
        
        // Emit event
        emit CheckpointAdded(
            _shipmentId,
            _location,
            block.timestamp,
            msg.sender,
            _status
        );
    }
    
    function getCheckpoints(string memory _shipmentId) public view returns (Checkpoint[] memory) {
        // Implementation will come in Phase 2
        return shipments[_shipmentId];
    }
} 