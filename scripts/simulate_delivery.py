#!/usr/bin/env python3
"""
Tamper-Proof Logistics Tracker - Day 6 Simulation Script
========================================================

This script simulates a shipment moving through various checkpoints
by interacting with the deployed SupplyChainTracker.sol contract.

Author: Mustafa Toygar Baykal
Project: Tamper-Proof Component Logistics Tracker
Day: 6 - Off-chain Python Integration

Requirements:
- pip install web3 python-dotenv

Usage:
    python scripts/simulate_delivery.py

Features:
- Connects to local/testnet via Web3.py
- Loads contract ABI from build artifacts
- Simulates shipment lifecycle with multiple checkpoints
- Secure environment variable management
- Transaction monitoring and event logging
- Human-readable timestamp formatting
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any
from web3 import Web3
from dotenv import load_dotenv

# Handle middleware import based on web3 version
try:
    from web3.middleware import geth_poa_middleware
except ImportError:
    # For newer web3 versions
    try:
        from web3.middleware.geth_poa import geth_poa_middleware
    except ImportError:
        # Fallback - create a simple middleware function
        def geth_poa_middleware(w3, _):
            return lambda request, response: response

# Load environment variables
load_dotenv()

class SupplyChainSimulator:
    """Simulates supply chain interactions with the SupplyChainTracker contract"""
    
    def __init__(self):
        """Initialize the simulator with Web3 connection and contract setup"""
        self.w3 = None
        self.contract = None
        self.account = None
        self.contract_address = None
        
        # Simulation data
        self.shipment_id = "SHIP123"
        self.checkpoints = [
            {
                "location": "Factory",
                "status": "created",
                "document_hash": "QmFakeDocHash123_Factory"
            },
            {
                "location": "Transit Hub", 
                "status": "in-transit",
                "document_hash": "QmFakeDocHash123_Transit"
            },
            {
                "location": "Border",
                "status": "in-transit", 
                "document_hash": "QmFakeDocHash123_Border"
            },
            {
                "location": "Final Warehouse",
                "status": "delivered",
                "document_hash": "QmFakeDocHash123_Final"
            }
        ]
    
    def setup_web3_connection(self) -> bool:
        """
        Establish Web3 connection to blockchain network
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Get RPC URL from environment or use default
            rpc_url = os.getenv('RPC_URL', 'http://127.0.0.1:8545')
            print(f"🔗 Connecting to blockchain at: {rpc_url}")
            
            # Initialize Web3 connection
            self.w3 = Web3(Web3.HTTPProvider(rpc_url))
            
            # Add PoA middleware for some testnets (like Goerli, Sepolia)
            if 'goerli' in rpc_url.lower() or 'sepolia' in rpc_url.lower():
                self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            # Test connection
            if not self.w3.is_connected():
                print("❌ Failed to connect to blockchain")
                return False
                
            print(f"✅ Connected! Chain ID: {self.w3.eth.chain_id}")
            print(f"📦 Latest block: {self.w3.eth.block_number}")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def setup_account(self) -> bool:
        """
        Setup account from private key
        
        Returns:
            bool: True if account setup successful, False otherwise
        """
        try:
            private_key = os.getenv('PRIVATE_KEY')
            if not private_key:
                print("❌ PRIVATE_KEY not found in .env file")
                return False
            
            print(f"🔍 Debug: Private key from env: {private_key[:10]}...")
            
            # Ensure the private key has proper format
            if not private_key.startswith('0x'):
                private_key = '0x' + private_key
            
            # Create account from private key
            self.account = self.w3.eth.account.from_key(private_key)
            
            # Check balance
            balance = self.w3.eth.get_balance(self.account.address)
            balance_eth = self.w3.from_wei(balance, 'ether')
            
            print(f"🔑 Account: {self.account.address}")
            print(f"💰 Balance: {balance_eth:.4f} ETH")
            
            if balance == 0:
                print("⚠️  Warning: Account has zero balance!")
            
            return True
            
        except Exception as e:
            print(f"❌ Account setup error: {e}")
            return False
    
    def load_contract_abi(self) -> Dict[str, Any]:
        """
        Load contract ABI from Hardhat artifacts
        
        Returns:
            Dict: Contract ABI, or None if loading fails
        """
        try:
            # Path to compiled contract artifact
            artifact_path = "artifacts/contracts/SupplyChainTracker.sol/SupplyChainTracker.json"
            
            if not os.path.exists(artifact_path):
                print(f"❌ Contract artifact not found at: {artifact_path}")
                print("💡 Tip: Run 'npx hardhat compile' first")
                return None
            
            with open(artifact_path, 'r') as f:
                artifact = json.load(f)
            
            print(f"✅ Loaded contract ABI from: {artifact_path}")
            return artifact['abi']
            
        except Exception as e:
            print(f"❌ ABI loading error: {e}")
            return None
    
    def setup_contract(self) -> bool:
        """
        Setup contract instance
        
        Returns:
            bool: True if contract setup successful, False otherwise
        """
        try:
            # Get contract address from environment
            self.contract_address = os.getenv('CONTRACT_ADDRESS')
            if not self.contract_address:
                print("❌ CONTRACT_ADDRESS not found in .env file")
                print("💡 Deploy your contract first and add the address to .env")
                return False
            
            # Load ABI
            abi = self.load_contract_abi()
            if not abi:
                return False
            
            # Create contract instance
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=abi
            )
            
            print(f"📄 Contract loaded at: {self.contract_address}")
            
            # Test contract connection by calling a view function
            try:
                admin = self.contract.functions.admin().call()
                print(f"👤 Contract admin: {admin}")
            except Exception as e:
                print(f"⚠️  Warning: Could not verify contract: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Contract setup error: {e}")
            return False
    
    def format_timestamp(self, timestamp: int) -> str:
        """
        Convert Unix timestamp to human-readable format
        
        Args:
            timestamp (int): Unix timestamp
            
        Returns:
            str: Formatted timestamp string
        """
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    def add_checkpoint(self, location: str, status: str, document_hash: str) -> bool:
        """
        Add a checkpoint to the blockchain
        
        Args:
            location (str): Checkpoint location
            status (str): Shipment status
            document_hash (str): Document hash (IPFS or other)
            
        Returns:
            bool: True if checkpoint added successfully, False otherwise
        """
        try:
            print(f"\n📍 Adding checkpoint: {location} ({status})")
            
            # Build transaction
            transaction = self.contract.functions.addCheckpoint(
                self.shipment_id,
                location,
                status,
                document_hash
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 300000,  # Sufficient gas for the transaction
                'gasPrice': self.w3.to_wei('20', 'gwei')  # Adjust based on network
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=os.getenv('PRIVATE_KEY'))
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f"📤 Transaction sent: {tx_hash.hex()}")
            
            # Wait for confirmation
            print("⏳ Waiting for confirmation...")
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if receipt.status == 1:
                print(f"✅ Checkpoint confirmed! Block: {receipt.blockNumber}")
                print(f"⛽ Gas used: {receipt.gasUsed:,}")
                
                # Parse events
                self.parse_checkpoint_events(receipt)
                return True
            else:
                print(f"❌ Transaction failed! Receipt: {receipt}")
                return False
                
        except Exception as e:
            print(f"❌ Checkpoint addition error: {e}")
            return False
    
    def parse_checkpoint_events(self, receipt) -> None:
        """
        Parse and display CheckpointAdded events from transaction receipt
        
        Args:
            receipt: Transaction receipt
        """
        try:
            # Get CheckpointAdded events
            checkpoint_events = self.contract.events.CheckpointAdded().process_receipt(receipt)
            
            for event in checkpoint_events:
                args = event['args']
                timestamp_formatted = self.format_timestamp(args['timestamp'])
                
                print(f"🎉 Event: CheckpointAdded")
                print(f"   └─ Shipment ID: {args['shipmentId']}")
                print(f"   └─ Location: {args['location']}")
                print(f"   └─ Status: {args['status']}")
                print(f"   └─ Timestamp: {timestamp_formatted}")
                print(f"   └─ Submitted by: {args['submittedBy']}")
                
        except Exception as e:
            print(f"⚠️  Could not parse events: {e}")
    
    def get_shipment_history(self) -> bool:
        """
        Retrieve and display complete shipment history
        
        Returns:
            bool: True if history retrieved successfully, False otherwise
        """
        try:
            print(f"\n📊 Retrieving history for shipment: {self.shipment_id}")
            
            # Get checkpoint count
            count = self.contract.functions.getCheckpointCount(self.shipment_id).call()
            print(f"📈 Total checkpoints: {count}")
            
            if count == 0:
                print("📭 No checkpoints found for this shipment")
                return True
            
            # Get full history
            history = self.contract.functions.getShipmentHistory(self.shipment_id).call()
            
            print("\n📜 Complete Shipment History:")
            print("=" * 50)
            
            for i, checkpoint in enumerate(history, 1):
                timestamp_formatted = self.format_timestamp(checkpoint[1])  # timestamp is at index 1
                
                print(f"\n{i}. Checkpoint #{i}")
                print(f"   📍 Location: {checkpoint[2]}")  # location at index 2
                print(f"   📊 Status: {checkpoint[3]}")    # status at index 3
                print(f"   🕒 Time: {timestamp_formatted}")
                print(f"   📎 Document: {checkpoint[4]}")  # documentHash at index 4
                print(f"   👤 Submitted by: {checkpoint[5]}")  # submittedBy at index 5
            
            return True
            
        except Exception as e:
            print(f"❌ History retrieval error: {e}")
            return False
    
    def run_simulation(self) -> bool:
        """
        Run the complete simulation
        
        Returns:
            bool: True if simulation completed successfully, False otherwise
        """
        print("🚀 Starting Supply Chain Simulation")
        print("=" * 50)
        
        # Setup connections
        if not self.setup_web3_connection():
            return False
        
        if not self.setup_account():
            return False
        
        if not self.setup_contract():
            return False
        
        print(f"\n🚛 Simulating shipment: {self.shipment_id}")
        print("💼 Shipment will move through 4 checkpoints...")
        
        # Add each checkpoint with a small delay
        success_count = 0
        for i, checkpoint in enumerate(self.checkpoints, 1):
            print(f"\n--- Checkpoint {i}/{len(self.checkpoints)} ---")
            
            if self.add_checkpoint(
                checkpoint['location'],
                checkpoint['status'], 
                checkpoint['document_hash']
            ):
                success_count += 1
                
            # Small delay between checkpoints (in real scenario, these would be hours/days apart)
            if i < len(self.checkpoints):
                print("😴 Waiting 2 seconds before next checkpoint...")
                time.sleep(2)
        
        # Display final results
        print(f"\n📈 Simulation Summary:")
        print(f"✅ Successful checkpoints: {success_count}/{len(self.checkpoints)}")
        
        if success_count == len(self.checkpoints):
            print("🎉 Simulation completed successfully!")
            
            # Retrieve and display complete history
            self.get_shipment_history()
            return True
        else:
            print("⚠️  Simulation completed with some failures")
            return False

def main():
    """Main function to run the simulation"""
    print("🔧 Tamper-Proof Logistics Tracker - Day 6 Simulation")
    print("=" * 60)
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("\n❌ .env file not found!")
        print("📝 Please create a .env file with the following variables:")
        print("   PRIVATE_KEY=your_private_key_here")
        print("   RPC_URL=http://127.0.0.1:8545")
        print("   CONTRACT_ADDRESS=deployed_contract_address_here")
        print("\n💡 Example .env content:")
        print("   PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80")
        print("   RPC_URL=http://127.0.0.1:8545")
        print("   CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3")
        return False
    
    # Run simulation
    simulator = SupplyChainSimulator()
    success = simulator.run_simulation()
    
    if success:
        print("\n🏆 Day 6 Milestone Complete!")
        print("\n🔮 Next Steps for Expansion:")
        print("   • Add CLI arguments for custom shipment data")
        print("   • Import checkpoint data from CSV files")
        print("   • Implement role-based access (assign manufacturer/courier roles)")
        print("   • Add IPFS integration for real document storage")
        print("   • Create bulk checkpoint submission")
        print("   • Add error handling and retry logic")
        print("   • Implement real-time event monitoring")
        print("   • Add transaction cost estimation")
    
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Simulation interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc() 