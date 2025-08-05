# 📦 Tamper-Proof Component Logistics Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Solidity](https://img.shields.io/badge/Solidity-^0.8.24-363636?logo=solidity)](https://soliditylang.org/)
[![Hardhat](https://img.shields.io/badge/Built%20with-Hardhat-FFDB1C)](https://hardhat.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)](https://streamlit.io/)
[![Sepolia](https://img.shields.io/badge/Deployed%20on-Sepolia%20Testnet-blue)](https://sepolia.etherscan.io/address/0xC9A0B51D65BC2E11cE056594D585FAAdBD3c22De)

A blockchain-based prototype that logs component handoffs in a secure, verifiable supply chain, designed to simulate military-grade logistics tracking. This system ensures complete traceability and tamper-proof record keeping for high-value component movements.

## 🌟 Live Demo

**Smart Contract on Sepolia Testnet:**  
🔗 [View on Etherscan](https://sepolia.etherscan.io/address/0xC9A0B51D65BC2E11cE056594D585FAAdBD3c22De)

Contract Address: `0xC9A0B51D65BC2E11cE056594D585FAAdBD3c22De`

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Quick Start](#-quick-start)
- [Detailed Setup](#-detailed-setup)
- [Usage](#-usage)
- [Scripts](#-available-scripts)
- [Environment Configuration](#-environment-configuration)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

## ✨ Features

### 🔐 Core Blockchain Features
- **Smart Contract Security**: Immutable checkpoint logging on Ethereum
- **Role-Based Access Control**: Manufacturer, Courier, and Inspector roles
- **Event-Driven Architecture**: Real-time blockchain event monitoring
- **Gas-Optimized**: Efficient Solidity implementation for cost-effective operations

### 📊 User Interface
- **Interactive Dashboard**: Real-time supply chain visualization
- **Checkpoint Timeline**: Complete shipment journey tracking
- **Status Monitoring**: Live updates on shipment status and location
- **Analytics**: Visual insights with charts and graphs
- **Responsive Design**: Professional UI built with Streamlit

### 🛠 Developer Tools
- **Comprehensive Testing**: Full test suite with Hardhat
- **Simulation Scripts**: Automated delivery lifecycle simulation
- **Deployment Automation**: One-command deployment to any network
- **Debug Tools**: Event monitoring and transaction debugging

### 🔄 Integration Capabilities
- **IPFS Support**: Optional document storage for proof attachments
- **Multi-Network**: Supports Ethereum mainnet, testnets, and local development
- **Web3 Integration**: Full blockchain interaction via Python

## 🛠 Tech Stack

### Blockchain & Smart Contracts
- **Solidity ^0.8.24** - Smart contract development
- **Hardhat** - Development environment and testing framework
- **Ethers.js** - Ethereum library for contract interaction
- **OpenZeppelin** - Security-audited contract libraries

### Frontend & User Interface
- **Streamlit** - Interactive web application framework
- **Plotly** - Data visualization and charts
- **Pandas** - Data manipulation and analysis
- **CSS/HTML** - Custom styling and responsive design

### Backend & Integration
- **Python 3.8+** - Backend scripting and automation
- **Web3.py** - Python library for Ethereum interaction
- **python-dotenv** - Environment variable management
- **JSON-RPC** - Blockchain node communication

### Infrastructure & Deployment
- **Ethereum Sepolia Testnet** - Live deployment environment
- **Alchemy/Infura** - Blockchain node providers
- **MetaMask** - Wallet integration
- **IPFS (Web3.Storage)** - Decentralized file storage (optional)

## 📸 Screenshots

![Dashboard Overview](./assets/dashboard-overview.png)
*Main dashboard showing real-time shipment tracking*

![Checkpoint Timeline](./assets/checkpoint-timeline.png)
*Detailed checkpoint timeline with status updates*

![Contract Interaction](./assets/contract-interaction.png)
*Smart contract interaction interface*

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v16+ recommended)
- **Python** (3.8+ recommended)
- **Git**
- **MetaMask** wallet (for testnet interaction)

### One-Command Setup
```bash
# Clone and setup the project
git clone https://github.com/yourusername/tamperproof-logistics-tracker
cd tamperproof-logistics-tracker

# Install dependencies
npm install
pip install -r streamlit_app/requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Deploy contract (optional - use existing deployed contract)
npx hardhat run scripts/deploy.js --network sepolia

# Launch the application
streamlit run streamlit_app/app.py
```

## 🔧 Detailed Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/tamperproof-logistics-tracker
cd tamperproof-logistics-tracker
```

### 2. Install Dependencies

#### Node.js Dependencies
```bash
npm install
```

#### Python Dependencies
```bash
# Navigate to Streamlit app directory
cd streamlit_app
pip install -r requirements.txt
cd ..
```

### 3. Environment Configuration

Copy the example environment file and configure it:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```bash
# Blockchain connection
RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID

# Your wallet private key (testnet only!)
PRIVATE_KEY=your_sepolia_testnet_private_key

# Deployed contract address
CONTRACT_ADDRESS=0xC9A0B51D65BC2E11cE056594D585FAAdBD3c22De
```

### 4. Smart Contract Setup

#### Option A: Use Existing Deployed Contract
The contract is already deployed on Sepolia testnet at:
`0xC9A0B51D65BC2E11cE056594D585FAAdBD3c22De`

#### Option B: Deploy Your Own Contract
```bash
# Compile contracts
npx hardhat compile

# Deploy to Sepolia testnet
npx hardhat run scripts/deploy.js --network sepolia

# Deploy to local network
npx hardhat node  # In separate terminal
npx hardhat run scripts/deploy.js --network localhost
```

### 5. Launch the Application
```bash
streamlit run streamlit_app/app.py
```

Navigate to `http://localhost:8501` to access the dashboard.

## 📖 Usage

### Getting Started
1. **Open the Dashboard**: Launch the Streamlit app and navigate to the web interface
2. **Connect Your Wallet**: Ensure MetaMask is configured for Sepolia testnet
3. **Check Contract Connection**: Verify the app connects to the smart contract
4. **Create Checkpoints**: Use the interface to add new shipment checkpoints
5. **Monitor Progress**: Track shipments in real-time through the dashboard

### Key Workflows

#### Creating a New Shipment
1. Navigate to "Add Checkpoint" section
2. Enter shipment ID, location, and status
3. Optionally attach document hash
4. Submit transaction via MetaMask
5. Monitor transaction confirmation

#### Tracking Shipments
1. Enter shipment ID in the "Track Shipment" section
2. View complete checkpoint history
3. Analyze timeline and status progression
4. Export data for reporting

#### Role Management (Admin Only)
1. Access admin panel
2. Assign roles to wallet addresses
3. Manage permissions and access control

## ⚡ Available Scripts

### Blockchain Scripts
```bash
# Compile smart contracts
npm run compile
# or
npx hardhat compile

# Run test suite
npm test
# or
npx hardhat test

# Deploy to network
npx hardhat run scripts/deploy.js --network <network-name>
```

### Python Simulation Scripts
```bash
# Simulate complete delivery lifecycle
python scripts/simulate_delivery.py

# Run comprehensive testing
python comprehensive_test.py

# Demo simulation with multiple checkpoints
python scripts/demo_simulation.py
```

### Development Scripts
```bash
# Start local Hardhat node
npx hardhat node

# Run Streamlit app in development mode
streamlit run streamlit_app/app.py --server.runOnSave true

# Debug specific functionality
python debug_checkpoint.py
python test_checkpoint_functionality.py
```

## 🔐 Environment Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `RPC_URL` | Blockchain RPC endpoint | `https://sepolia.infura.io/v3/YOUR_PROJECT_ID` |
| `PRIVATE_KEY` | Wallet private key (testnet only) | `0x1234...` |
| `CONTRACT_ADDRESS` | Deployed contract address | `0xC9A0B51D65BC2E11cE056594D585FAAdBD3c22De` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GAS_LIMIT` | Transaction gas limit | `2000000` |
| `GAS_PRICE` | Gas price in gwei | `20` |
| `APP_ENV` | Application environment | `development` |
| `DEBUG_MODE` | Enable debug logging | `false` |

### Network Configurations

#### Sepolia Testnet (Recommended)
```bash
RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
# Get testnet ETH from: https://sepoliafaucet.com/
```

#### Local Development
```bash
RPC_URL=http://127.0.0.1:8545
# Use with: npx hardhat node
```

#### Polygon Mumbai (Alternative)
```bash
RPC_URL=https://polygon-mumbai.infura.io/v3/YOUR_PROJECT_ID
# Get testnet MATIC from: https://faucet.polygon.technology/
```

## 🚀 Deployment

### Deploying to Sepolia Testnet

1. **Get Testnet ETH**:
   - Visit [Sepolia Faucet](https://sepoliafaucet.com/)
   - Request testnet ETH for your wallet

2. **Configure RPC Provider**:
   - Sign up for [Alchemy](https://www.alchemy.com/) or [Infura](https://infura.io/)
   - Create a new project and get your API key

3. **Deploy Contract**:
   ```bash
   npx hardhat run scripts/deploy.js --network sepolia
   ```

4. **Update Environment**:
   - Copy the deployed contract address to your `.env` file
   - Verify deployment on [Sepolia Etherscan](https://sepolia.etherscan.io/)

### Deploying Frontend

#### Local Development
```bash
streamlit run streamlit_app/app.py
```

#### Production Deployment (Streamlit Cloud)
1. Fork this repository
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add environment variables in the Streamlit Cloud dashboard
4. Deploy with one click

## 📁 Project Structure

```
tamperproof-logistics-tracker/
├── 📁 contracts/                    # Smart contracts
│   └── SupplyChainTracker.sol      # Main tracking contract
├── 📁 scripts/                     # Deployment & simulation scripts
│   ├── deploy.js                   # Contract deployment
│   ├── simulate_delivery.py        # Delivery simulation
│   └── demo_simulation.py          # Demo script
├── 📁 streamlit_app/               # Frontend application
│   ├── app.py                      # Main Streamlit app
│   ├── web3_utils.py              # Web3 utilities
│   └── requirements.txt           # Python dependencies
├── 📁 tests/                       # Test suite
│   └── SupplyChainTracker.test.js # Smart contract tests
├── 📁 whitepaper/                  # Project documentation
│   ├── architecture.md            # System architecture
│   ├── components.md               # Component specifications
│   └── prd.md                      # Product requirements
├── 📁 artifacts/                   # Compiled contracts
├── .env.example                    # Environment template
├── hardhat.config.js              # Hardhat configuration
├── package.json                    # Node.js dependencies
└── README.md                       # This file
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Your Changes**
4. **Add Tests** (if applicable)
5. **Commit Your Changes**:
   ```bash
   git commit -m "Add: your feature description"
   ```
6. **Push to Your Branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

### Development Guidelines
- Follow Solidity best practices and security guidelines
- Write comprehensive tests for new features
- Ensure code is well-documented
- Use conventional commit messages
- Test on Sepolia testnet before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mustafa Toygar Baykal**
- GitHub: [@mtogi](https://github.com/mtogi)
- LinkedIn: [Mustafa Toygar Baykal](https://linkedin.com/in/mbaykal)
- Email: mtoygarby@gmail.com

## 🙏 Acknowledgments

- **OpenZeppelin** for secure smart contract libraries
- **Hardhat** team for excellent development tools
- **Streamlit** for the amazing frontend framework
- **Ethereum Foundation** for the blockchain infrastructure
- **Web3.py** contributors for Python blockchain integration

## 📚 Additional Resources

- [Smart Contract Documentation](./whitepaper/components.md)
- [System Architecture](./whitepaper/architecture.md)
- [Product Requirements](./whitepaper/prd.md)
- [Hardhat Documentation](https://hardhat.org/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Solidity Documentation](https://docs.soliditylang.org/)

---

<div align="center">

**Built with ❤️ for secure, transparent supply chain management**

[⭐ Star this repo](https://github.com/mtogi/tamperproof-logistics-tracker/stargazers) • 
[🐛 Report Bug](https://github.com/mtogi/tamperproof-logistics-tracker/issues) • 
[✨ Request Feature](https://github.com/mtogi/tamperproof-logistics-tracker/issues)

</div>
