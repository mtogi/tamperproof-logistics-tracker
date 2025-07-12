# 🧩 System Components

## 1. Checkpoint Contract (Solidity)
- Stores shipment state
- Enforces ordered handoffs
- Emits tamper alerts
- Tracks user roles (e.g. manufacturer, courier)

## 2. Simulator Script (Python)
- Mimics shipment moving through stages
- Sends write transactions to contract
- Can be run from CLI to test changes

## 3. Streamlit UI
- Displays shipment status map
- Lets user enter shipment ID
- Shows detailed timeline
- Displays alerts if tampering is detected

## 4. IPFS (Optional)
- Stores delivery documents or metadata
- Returns hash for contract storage
