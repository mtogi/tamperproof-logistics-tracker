"""
Web3 Utilities for Tamper-Proof Logistics Tracker
Handles blockchain connection and smart contract interactions
"""

import os
import json
import streamlit as st
from web3 import Web3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import threading
import time

# Try to import python-dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
    # Load .env file from parent directory (project root)
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()  # Try to load from current directory or parent
except ImportError:
    DOTENV_AVAILABLE = False

class Web3Manager:
    """Manages Web3 connection and contract interactions"""
    
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.account = None
        self._load_config()
        
    def _load_config(self):
        """Load configuration from environment variables"""
        try:
            # Force reload .env file to ensure fresh environment variables
            if DOTENV_AVAILABLE:
                env_path = Path(__file__).parent.parent / ".env"
                if env_path.exists():
                    load_dotenv(env_path, override=True)
                    print(f"🔄 Reloaded .env from {env_path}")
                else:
                    load_dotenv(override=True)
                    
            # Get environment variables with defaults for development
            self.rpc_url = os.getenv('RPC_URL', 'http://127.0.0.1:8545')  # Default to local Hardhat
            self.private_key = os.getenv('PRIVATE_KEY', '')
            self.contract_address = os.getenv('CONTRACT_ADDRESS', '')
            
            # Debug: Print loaded values (without exposing private key)
            print(f"🔧 Debug - RPC_URL: {self.rpc_url}")
            print(f"🔧 Debug - CONTRACT_ADDRESS: {self.contract_address}")
            print(f"🔧 Debug - PRIVATE_KEY loaded: {'Yes' if self.private_key else 'No'}")
            
            if not self.private_key:
                st.error("❌ PRIVATE_KEY not found in environment variables")
                return
                
            if not self.contract_address:
                st.error("❌ CONTRACT_ADDRESS not found in environment variables")
                return
                
        except Exception as e:
            st.error(f"❌ Error loading configuration: {str(e)}")
    
    def connect(self) -> bool:
        """Establish Web3 connection and load contract"""
        try:
            # Connect to Web3 provider
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            
            if not self.w3.is_connected():
                st.error(f"❌ Failed to connect to blockchain at {self.rpc_url}")
                return False
            
            # Load account from private key
            if self.private_key:
                self.account = self.w3.eth.account.from_key(self.private_key)
            
            # Load contract ABI and create contract instance
            contract_abi = self._load_contract_abi()
            if not contract_abi:
                return False
                
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.contract_address),
                abi=contract_abi
            )
            
            return True
            
        except Exception as e:
            st.error(f"❌ Web3 connection error: {str(e)}")
            return False
    
    def _load_contract_abi(self) -> Optional[List]:
        """Load contract ABI from artifacts"""
        try:
            # Path to contract artifacts (relative to project root)
            artifact_path = Path(__file__).parent.parent / "artifacts" / "contracts" / "SupplyChainTracker.sol" / "SupplyChainTracker.json"
            
            if not artifact_path.exists():
                st.error(f"❌ Contract artifact not found at {artifact_path}")
                return None
                
            with open(artifact_path, 'r') as f:
                contract_data = json.load(f)
                return contract_data['abi']
                
        except Exception as e:
            st.error(f"❌ Error loading contract ABI: {str(e)}")
            return None
    
    def get_connection_status(self) -> Dict[str, any]:
        """Get current connection status for display"""
        if not self.w3:
            return {"connected": False, "error": "Not initialized"}
            
        try:
            latest_block = self.w3.eth.block_number
            balance = "0"
            
            if self.account:
                balance_wei = self.w3.eth.get_balance(self.account.address)
                balance = self.w3.from_wei(balance_wei, 'ether')
            
            return {
                "connected": True,
                "network": self.rpc_url,
                "latest_block": latest_block,
                "account": self.account.address if self.account else "Not loaded",
                "balance": f"{balance:.4f} ETH" if self.account else "N/A"
            }
            
        except Exception as e:
            return {"connected": False, "error": str(e)}
    
    def get_shipment_history(self, shipment_id: str) -> List[Dict]:
        """Fetch shipment checkpoint history from contract"""
        if not self.contract:
            raise Exception("Contract not connected")
            
        try:
            # Call the contract function
            checkpoints = self.contract.functions.getShipmentHistory(shipment_id).call()
            
            # Format the response
            formatted_checkpoints = []
            for checkpoint in checkpoints:
                formatted_checkpoints.append({
                    'shipmentId': checkpoint[0],
                    'timestamp': checkpoint[1],
                    'location': checkpoint[2],
                    'status': checkpoint[3],
                    'documentHash': checkpoint[4],
                    'submittedBy': checkpoint[5],
                    'formatted_time': self._format_timestamp(checkpoint[1])
                })
            
            return formatted_checkpoints
            
        except Exception as e:
            raise Exception(f"Error fetching shipment history: {str(e)}")
    
    def get_checkpoint_count(self, shipment_id: str) -> int:
        """Get total number of checkpoints for a shipment"""
        if not self.contract:
            raise Exception("Contract not connected")
            
        try:
            return self.contract.functions.getCheckpointCount(shipment_id).call()
        except Exception as e:
            raise Exception(f"Error getting checkpoint count: {str(e)}")
    
    def add_checkpoint(self, shipment_id: str, location: str, status: str, document_hash: str = "") -> Tuple[bool, str, Dict]:
        """Add a new checkpoint to the blockchain with detailed transaction info"""
        if not self.contract or not self.account:
            return False, "Contract or account not connected", {}
        
        try:
            # Build the transaction
            transaction = self.contract.functions.addCheckpoint(
                shipment_id,
                location,
                status,
                document_hash
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 2000000,
                'gasPrice': self.w3.to_wei('20', 'gwei')
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            # Prepare transaction details
            tx_details = {
                'hash': tx_hash.hex(),
                'block_number': receipt.blockNumber,
                'gas_used': receipt.gasUsed,
                'gas_limit': transaction['gas'],
                'gas_price': self.w3.from_wei(transaction['gasPrice'], 'gwei'),
                'status': receipt.status
            }
            
            if receipt.status == 1:
                return True, f"Checkpoint added successfully!", tx_details
            else:
                return False, f"Transaction failed.", tx_details
                
        except Exception as e:
            return False, f"Transaction error: {str(e)}", {}
    
    def get_user_role(self, address: str) -> str:
        """Get the role of a user address"""
        if not self.contract:
            raise Exception("Contract not connected")
            
        try:
            role_num = self.contract.functions.getRole(Web3.to_checksum_address(address)).call()
            role_names = {0: "None", 1: "Manufacturer", 2: "Courier", 3: "Inspector"}
            return role_names.get(role_num, "Unknown")
        except Exception as e:
            raise Exception(f"Error getting user role: {str(e)}")
    
    @staticmethod
    def _format_timestamp(timestamp: int) -> str:
        """Convert Unix timestamp to readable UTC string"""
        try:
            dt = datetime.utcfromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except Exception:
            return "Invalid timestamp"
    
    @staticmethod
    def _format_relative_time(timestamp: int) -> str:
        """Convert Unix timestamp to relative time (e.g., '5 minutes ago')"""
        try:
            dt = datetime.utcfromtimestamp(timestamp)
            now = datetime.utcnow()
            diff = now - dt
            
            if diff.days > 0:
                return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            else:
                return "Just now"
        except Exception:
            return "Unknown time"
    
    def get_recent_events(self, shipment_id: str = None, from_block: str = None, limit: int = 10) -> List[Dict]:
        """Get recent CheckpointAdded events"""
        if not self.contract:
            return []
        
        try:
            # If no from_block specified, look back a reasonable number of blocks
            if from_block is None:
                current_block = self.w3.eth.block_number
                # Look back 1000 blocks or from genesis, whichever is more recent
                from_block = max(0, current_block - 1000)
            
            # Create event filter
            if shipment_id:
                event_filter = self.contract.events.CheckpointAdded.create_filter(
                    from_block=from_block,
                    argument_filters={'shipmentId': shipment_id}
                )
            else:
                event_filter = self.contract.events.CheckpointAdded.create_filter(
                    from_block=from_block
                )
            
            # Get events
            events = event_filter.get_all_entries()
            
            # Format events
            formatted_events = []
            for event in events[-limit:]:  # Get last N events
                # Handle indexed string issue - shipmentId is hashed
                # We need to get the original shipment ID from the transaction data
                try:
                    # Get the transaction receipt to extract the original shipment ID
                    receipt = self.w3.eth.get_transaction_receipt(event.transactionHash)
                    processed_logs = self.contract.events.CheckpointAdded().process_receipt(receipt)
                    
                    if processed_logs:
                        # The shipment ID is in the transaction input data, not the indexed field
                        # For now, we'll extract it from the transaction
                        tx = self.w3.eth.get_transaction(event.transactionHash)
                        decoded_input = self.contract.decode_function_input(tx.input)
                        original_shipment_id = decoded_input[1].get('_shipmentId', 'Unknown')
                    else:
                        original_shipment_id = 'Unknown'
                except:
                    original_shipment_id = 'Unknown'
                
                formatted_events.append({
                    'shipmentId': original_shipment_id,
                    'timestamp': event.args.timestamp,
                    'location': event.args.location,
                    'status': event.args.status,
                    'submittedBy': event.args.submittedBy,
                    'blockNumber': event.blockNumber,
                    'transactionHash': event.transactionHash.hex(),
                    'formatted_time': self._format_timestamp(event.args.timestamp),
                    'relative_time': self._format_relative_time(event.args.timestamp)
                })
            
            return formatted_events
            
        except Exception as e:
            st.warning(f"Could not fetch events: {str(e)}")
            return []
    
    def listen_for_new_events(self, callback_function=None, poll_interval: int = 5):
        """Listen for new events in a separate thread (polling-based)"""
        if not self.contract:
            return
        
        def poll_events():
            last_block = self.w3.eth.block_number
            
            while True:
                try:
                    current_block = self.w3.eth.block_number
                    
                    if current_block > last_block:
                        # Get new events from the last processed block
                        events = self.get_recent_events(from_block=last_block + 1)
                        
                        if events and callback_function:
                            callback_function(events)
                        
                        last_block = current_block
                    
                    time.sleep(poll_interval)
                    
                except Exception as e:
                    print(f"Event listening error: {str(e)}")
                    time.sleep(poll_interval)
        
        # Start polling in background thread
        thread = threading.Thread(target=poll_events, daemon=True)
        thread.start()

    @staticmethod
    def validate_ethereum_address(address: str) -> bool:
        """Validate if string is a valid Ethereum address"""
        try:
            Web3.to_checksum_address(address)
            return True
        except:
            return False


# Create a singleton instance
@st.cache_resource
def get_web3_manager():
    """Get or create Web3Manager instance with Streamlit caching"""
    return Web3Manager()


def create_sample_env_file():
    """Create a sample .env file template"""
    sample_content = """# Tamper-Proof Logistics Tracker Configuration
# Copy this file to .env and update with your values

# Blockchain RPC URL (use your Infura/Alchemy URL for mainnet/testnet)
RPC_URL=http://127.0.0.1:8545

# Your private key (NEVER commit this to version control)
PRIVATE_KEY=your_private_key_here

# Deployed contract address
CONTRACT_ADDRESS=your_contract_address_here
"""
    
    env_path = Path(__file__).parent.parent / ".env.example"
    with open(env_path, 'w') as f:
        f.write(sample_content)
    
    return str(env_path) 