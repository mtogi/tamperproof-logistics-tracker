# Tamper-Proof Component Logistics Tracker

A blockchain-based prototype that logs component handoffs in a secure, verifiable supply chain, designed to simulate military-grade logistics tracking.

## 📦 Features
- Smart contract to log checkpoint validations
- Streamlit dashboard to display transfers
- Optional IPFS support for document proofs
- Written whitepaper explaining system architecture

## 🚀 Stack
- Solidity (Smart Contracts)
- Hardhat (Testing/Deploy)
- Python + Streamlit (Frontend)
- Ethereum Sepolia Testnet
- IPFS via Web3.Storage (optional)

## 🛠 How to Run
```bash
npm install
npx hardhat compile
streamlit run streamlit_app/app.py
```

## 📄 Whitepaper

See /whitepaper/tracker_whitepaper.pdf