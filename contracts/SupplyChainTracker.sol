// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title SupplyChainTracker
/// @author Mustafa Toygar Baykal
/// @notice Tracks verified checkpoints of components on Ethereum

contract SupplyChainTracker {
    // ========== STATE VARIABLES ==========

    address public admin;

    enum Role { None, Manufacturer, Courier, Inspector }

    mapping(address => Role) public roles;

    struct Checkpoint {
        string shipmentId;
        uint256 timestamp;
        string location;
        string status; // e.g. "created", "in-transit", "delivered"
        string documentHash; // Optional IPFS hash or doc ID
        address submittedBy;
    }

    mapping(string => Checkpoint[]) private shipmentHistory;

    // ========== EVENTS ==========

    event RoleAssigned(address indexed user, Role role);
    event CheckpointAdded(
        string indexed shipmentId,
        uint256 timestamp,
        string location,
        string status,
        address submittedBy
    );

    // ========== MODIFIERS ==========

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can do this");
        _;
    }

    modifier onlyAuthorized() {
        require(roles[msg.sender] != Role.None, "Unauthorized: No role assigned");
        _;
    }

    // ========== CONSTRUCTOR ==========

    constructor() {
        admin = msg.sender;
        roles[admin] = Role.Inspector; // Admin is also a superuser
    }

    // ========== ROLE MANAGEMENT ==========

    function assignRole(address user, Role role) external onlyAdmin {
        roles[user] = role;
        emit RoleAssigned(user, role);
    }

    function getRole(address user) external view returns (Role) {
        return roles[user];
    }

    // ========== CORE LOGIC ==========

    function addCheckpoint(
        string memory _shipmentId,
        string memory _location,
        string memory _status,
        string memory _documentHash
    ) external onlyAuthorized {
        Checkpoint memory cp = Checkpoint({
            shipmentId: _shipmentId,
            timestamp: block.timestamp,
            location: _location,
            status: _status,
            documentHash: _documentHash,
            submittedBy: msg.sender
        });

        shipmentHistory[_shipmentId].push(cp);

        emit CheckpointAdded(_shipmentId, block.timestamp, _location, _status, msg.sender);
    }

    function getShipmentHistory(string memory _shipmentId) external view returns (Checkpoint[] memory) {
        return shipmentHistory[_shipmentId];
    }

    function getCheckpointCount(string memory _shipmentId) external view returns (uint256) {
        return shipmentHistory[_shipmentId].length;
    }
}
