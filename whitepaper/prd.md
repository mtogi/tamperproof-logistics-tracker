# 📘 Product Requirements Document (PRD)

## 🎯 Project Overview
Tamper-Proof Component Logistics Tracker simulates secure military-grade logistics. It allows stakeholders to verify the authenticity, status, and timeline of components as they pass through verified checkpoints — using blockchain and a web-based dashboard.

## 🛠 MVP Features
- Record checkpoints (manufacturer, warehouse, transport, delivery)
- Display full delivery trail in a dashboard
- Detect and flag tamper attempts (e.g. invalid sequence or missing step)

## 🧱 Architecture Overview
- **Frontend**: Streamlit UI (dashboard, checkpoint viewer)
- **Smart Contract**: Solidity contract deployed to Sepolia testnet
- **Simulation**: Python script mimics asset movement
- **Storage**: Ethereum (on-chain checkpoints), optional IPFS

## 🧪 Functional Requirements
- User can input or simulate shipment ID
- System shows map + delivery status
- Contract enforces role-based checkpoint logging
- Alert appears if checkpoint order is broken or unauthorized

## 🧰 Tools / Stack
- Hardhat, Solidity, Streamlit, Python, Web3.py, IPFS, Alchemy
