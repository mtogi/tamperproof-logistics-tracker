#!/usr/bin/env python3
"""
Debug script for checkpoint creation issues
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'streamlit_app'))
from web3_utils import get_web3_manager
import time

def test_checkpoint_creation():
    print("🔧 Testing checkpoint creation...")
    
    # Get Web3 manager
    w3_manager = get_web3_manager()
    
    # Connect to blockchain
    print("🔗 Connecting to blockchain...")
    if not w3_manager.connect():
        print("❌ Failed to connect to blockchain")
        return False
    
    print("✅ Connected successfully!")
    
    # Check connection status
    status = w3_manager.get_connection_status()
    print(f"📊 Connection Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Check user role
    if w3_manager.account:
        role = w3_manager.get_user_role(w3_manager.account.address)
        print(f"👤 User role: {role}")
        
        if role == "None":
            print("❌ No role assigned - this would prevent checkpoint creation")
            return False
    
    # Test checkpoint creation
    print("\n🚀 Testing checkpoint creation...")
    
    test_data = {
        'shipment_id': 'TEST-DEBUG-001',
        'location': 'Test Location',
        'status': 'in-transit',
        'document_hash': 'test-hash-123'
    }
    
    print(f"📦 Test data: {test_data}")
    
    try:
        print("🔄 Calling add_checkpoint...")
        success, message, tx_details = w3_manager.add_checkpoint(
            shipment_id=test_data['shipment_id'],
            location=test_data['location'],
            status=test_data['status'],
            document_hash=test_data['document_hash']
        )
        
        print(f"\n🎯 Result:")
        print(f"✅ Success: {success}")
        print(f"📝 Message: {message}")
        print(f"🔗 Transaction details: {tx_details}")
        
        if success:
            print("\n🔍 Verifying checkpoint was added...")
            time.sleep(2)  # Wait for block confirmation
            
            # Check if checkpoint exists
            count = w3_manager.get_checkpoint_count(test_data['shipment_id'])
            print(f"📊 Checkpoint count for {test_data['shipment_id']}: {count}")
            
            if count > 0:
                history = w3_manager.get_shipment_history(test_data['shipment_id'])
                print(f"📋 History: {history}")
                print("✅ Checkpoint successfully created and verified!")
                return True
            else:
                print("❌ Checkpoint was not found in history")
                return False
        else:
            print("❌ Checkpoint creation failed")
            # Try to get more detailed error info
            if hasattr(w3_manager, 'w3') and w3_manager.w3:
                latest_block = w3_manager.w3.eth.block_number
                print(f"🔍 Latest block: {latest_block}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during checkpoint creation: {str(e)}")
        import traceback
        print("📋 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_checkpoint_creation()