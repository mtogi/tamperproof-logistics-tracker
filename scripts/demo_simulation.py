#!/usr/bin/env python3
"""
Tamper-Proof Logistics Tracker - Day 6 Complete Simulation
==========================================================

Working demonstration of off-chain interaction with SupplyChainTracker contract.
Simulates a complete shipment journey through multiple checkpoints.
"""

import json
import time
from datetime import datetime
from web3 import Web3

class WorkingSimulation:
    """Complete working simulation of supply chain tracking"""
    
    def __init__(self):
        # Working configuration (from successful test)
        self.rpc_url = "http://127.0.0.1:8545"
        self.private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
        self.contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
        
        # Simulation data
        self.shipment_id = "SHIP123"
        self.checkpoints = [
            {"location": "Factory", "status": "created", "document": "QmFakeDocHash123_Factory"},
            {"location": "Transit Hub", "status": "in-transit", "document": "QmFakeDocHash123_Transit"},
            {"location": "Border Crossing", "status": "in-transit", "document": "QmFakeDocHash123_Border"},
            {"location": "Final Warehouse", "status": "delivered", "document": "QmFakeDocHash123_Final"}
        ]
        
        self.w3 = None
        self.contract = None
        self.account = None
    
    def setup(self):
        """Initialize Web3 connection and contract"""
        print("🔧 Setting up simulation...")
        
        # Connect to blockchain
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        if not self.w3.is_connected():
            print("❌ Failed to connect to blockchain")
            return False
        
        print(f"✅ Connected to blockchain (Chain ID: {self.w3.eth.chain_id})")
        
        # Setup account
        self.account = self.w3.eth.account.from_key(self.private_key)
        balance = self.w3.eth.get_balance(self.account.address)
        print(f"👤 Account: {self.account.address}")
        print(f"💰 Balance: {self.w3.from_wei(balance, 'ether'):.4f} ETH")
        
        # Load contract
        with open("artifacts/contracts/SupplyChainTracker.sol/SupplyChainTracker.json", 'r') as f:
            artifact = json.load(f)
        
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=artifact['abi'])
        print(f"📄 Contract loaded: {self.contract_address}")
        
        # Verify contract
        try:
            admin = self.contract.functions.admin().call()
            print(f"🔑 Contract admin: {admin}")
            return True
        except Exception as e:
            print(f"❌ Contract verification failed: {e}")
            return False
    
    def format_timestamp(self, timestamp):
        """Convert Unix timestamp to readable format"""
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    def add_checkpoint(self, location, status, document):
        """Add a checkpoint to the blockchain"""
        print(f"\n📍 Adding checkpoint: {location} ({status})")
        
        try:
            # Build transaction
            transaction = self.contract.functions.addCheckpoint(
                self.shipment_id,
                location,
                status,
                document
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 300000,
                'gasPrice': self.w3.to_wei('20', 'gwei')
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f"📤 Transaction sent: {tx_hash.hex()}")
            
            # Wait for confirmation
            print("⏳ Waiting for confirmation...")
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
            
            if receipt.status == 1:
                print(f"✅ Checkpoint confirmed! Block: {receipt.blockNumber}")
                print(f"⛽ Gas used: {receipt.gasUsed:,}")
                
                # Parse events
                try:
                    events = self.contract.events.CheckpointAdded().process_receipt(receipt)
                    for event in events:
                        args = event['args']
                        timestamp = self.format_timestamp(args['timestamp'])
                        print(f"🎉 Event: CheckpointAdded")
                        print(f"   └─ Shipment: {args['shipmentId']}")
                        print(f"   └─ Location: {args['location']}")
                        print(f"   └─ Status: {args['status']}")
                        print(f"   └─ Time: {timestamp}")
                        print(f"   └─ Submitted by: {args['submittedBy']}")
                except Exception as e:
                    print(f"⚠️  Event parsing error: {e}")
                
                return True
            else:
                print(f"❌ Transaction failed!")
                return False
                
        except Exception as e:
            print(f"❌ Transaction error: {e}")
            return False
    
    def get_complete_history(self):
        """Retrieve and display complete shipment history"""
        print(f"\n📊 Retrieving complete history for shipment: {self.shipment_id}")
        
        try:
            # Get checkpoint count
            count = self.contract.functions.getCheckpointCount(self.shipment_id).call()
            print(f"📈 Total checkpoints: {count}")
            
            if count == 0:
                print("📭 No checkpoints found")
                return
            
            # Get full history
            history = self.contract.functions.getShipmentHistory(self.shipment_id).call()
            
            print("\n📜 Complete Shipment Journey:")
            print("=" * 60)
            
            for i, checkpoint in enumerate(history, 1):
                timestamp = self.format_timestamp(checkpoint[1])
                print(f"\n{i}. Checkpoint #{i}")
                print(f"   📍 Location: {checkpoint[2]}")
                print(f"   📊 Status: {checkpoint[3]}")
                print(f"   🕒 Timestamp: {timestamp}")
                print(f"   📎 Document: {checkpoint[4]}")
                print(f"   👤 Submitted by: {checkpoint[5]}")
                
        except Exception as e:
            print(f"❌ History retrieval error: {e}")
    
    def run_simulation(self):
        """Run the complete simulation"""
        print("🚀 Tamper-Proof Logistics Tracker - Day 6 Simulation")
        print("=" * 60)
        
        # Setup
        if not self.setup():
            return False
        
        print(f"\n🚛 Simulating shipment journey: {self.shipment_id}")
        print("💼 Moving through 4 strategic checkpoints...")
        
        # Process each checkpoint
        success_count = 0
        for i, checkpoint in enumerate(self.checkpoints, 1):
            print(f"\n{'='*20} Checkpoint {i}/{len(self.checkpoints)} {'='*20}")
            
            if self.add_checkpoint(
                checkpoint['location'],
                checkpoint['status'],
                checkpoint['document']
            ):
                success_count += 1
            
            # Realistic delay between checkpoints
            if i < len(self.checkpoints):
                print("😴 Simulating real-world delay (3 seconds)...")
                time.sleep(3)
        
        # Final summary
        print(f"\n🏁 Simulation Complete!")
        print("=" * 40)
        print(f"✅ Successful checkpoints: {success_count}/{len(self.checkpoints)}")
        
        if success_count == len(self.checkpoints):
            print("🎉 All checkpoints processed successfully!")
            self.get_complete_history()
            
            print(f"\n🔮 Next Steps for Expansion:")
            print("   • Add CLI arguments for custom shipment data")
            print("   • Import checkpoint data from CSV files")
            print("   • Implement role-based access control")
            print("   • Add IPFS integration for document storage")
            print("   • Create real-time event monitoring")
            print("   • Add transaction cost optimization")
            
            print(f"\n🏆 Day 6 Milestone: COMPLETE! ✅")
            return True
        else:
            print("⚠️  Some checkpoints failed - check logs above")
            return False

def main():
    """Main execution function"""
    try:
        sim = WorkingSimulation()
        success = sim.run_simulation()
        return success
    except KeyboardInterrupt:
        print("\n\n⏹️  Simulation interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main() 