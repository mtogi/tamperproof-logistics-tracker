const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploying SupplyChainTracker contract...");
  
  // Get the contract factory
  const SupplyChainTracker = await hre.ethers.getContractFactory("SupplyChainTracker");
  
  // Deploy the contract
  const contract = await SupplyChainTracker.deploy();
  
  // Wait for deployment
  await contract.waitForDeployment();
  
  // Get the contract address
  const contractAddress = await contract.getAddress();
  
  console.log("✅ SupplyChainTracker deployed successfully!");
  console.log(`📄 Contract address: ${contractAddress}`);
  console.log(`🔗 Network: ${hre.network.name}`);
  
  // Get deployer info
  const [deployer] = await hre.ethers.getSigners();
  console.log(`👤 Deployed by: ${deployer.address}`);
  
  // Check admin role
  const admin = await contract.admin();
  console.log(`🔑 Contract admin: ${admin}`);
  
  // Get deployer's role
  const deployerRole = await contract.getRole(deployer.address);
  console.log(`👥 Deployer role: ${deployerRole} (2 = Inspector)`);
  
  return contractAddress;
}

// Execute deployment
main()
  .then((contractAddress) => {
    console.log("\n💡 Next steps:");
    console.log(`1. Update your .env file with: CONTRACT_ADDRESS=${contractAddress}`);
    console.log("2. Run the simulation: python scripts/simulate_delivery.py");
    process.exit(0);
  })
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  }); 