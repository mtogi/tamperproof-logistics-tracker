# Supply Chain Simulation Scripts

This directory contains Python scripts for simulating off-chain interactions with the SupplyChainTracker smart contract.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r scripts/requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Deploy your contract first:**
   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   # Copy the deployed contract address to .env
   ```

## Scripts

### `simulate_delivery.py`
Simulates a complete shipment lifecycle by adding multiple checkpoints to the blockchain.

**Features:**
- Connects to local Hardhat network or testnets
- Adds 4 sample checkpoints (Factory → Transit Hub → Border → Final Warehouse)
- Displays transaction hashes and event logs
- Shows complete shipment history

**Usage:**
```bash
python scripts/simulate_delivery.py
```

**Sample Output:**
```
🚀 Starting Supply Chain Simulation
🔗 Connecting to blockchain at: http://127.0.0.1:8545
✅ Connected! Chain ID: 31337
🔑 Account: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
📄 Contract loaded at: 0x5FbDB2315678afecb367f032d93F642f64180aa3

📍 Adding checkpoint: Factory (created)
📤 Transaction sent: 0x...
✅ Checkpoint confirmed! Block: 2
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `RPC_URL` | Blockchain RPC endpoint | `http://127.0.0.1:8545` |
| `PRIVATE_KEY` | Account private key (no 0x prefix) | `ac0974bec39a17e36ba4...` |
| `CONTRACT_ADDRESS` | Deployed contract address | `0x5FbDB2315678afecb367...` |

## Expansion Ideas

- **CLI Arguments:** Accept custom shipment IDs and checkpoint data
- **CSV Import:** Bulk load checkpoint data from files
- **Role Management:** Simulate different user roles (manufacturer, courier, inspector)
- **Real-time Monitoring:** Listen for blockchain events continuously
- **IPFS Integration:** Store and retrieve documents from IPFS
- **Error Recovery:** Implement transaction retry logic
- **Cost Estimation:** Calculate gas costs before transactions

## Troubleshooting

**Connection Issues:**
- Ensure Hardhat node is running: `npx hardhat node`
- Check RPC_URL in .env file

**Transaction Failures:**
- Verify account has sufficient ETH balance
- Ensure contract address is correct
- Check if account has required role in contract

**ABI Loading Errors:**
- Run `npx hardhat compile` to generate artifacts
- Verify contract compilation was successful 