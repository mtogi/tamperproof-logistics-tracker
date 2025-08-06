# 🚀 Streamlit Cloud Deployment Guide

## Quick Deployment Checklist

| Step | Task | Status |
|------|------|--------|
| 1️⃣ | Fork your repo on GitHub (optional) | ⬜ |
| 2️⃣ | Go to [streamlit.io/cloud](https://streamlit.io/cloud) | ⬜ |
| 3️⃣ | Click "New App" → Connect your GitHub repo | ⬜ |
| 4️⃣ | Select branch + `streamlit_app/app.py` as entry point | ⬜ |
| 5️⃣ | Go to Settings → Secrets and paste your .env as key-value pairs | ⬜ |
| 6️⃣ | Deploy the app! | ⬜ |
| 7️⃣ | Visit the URL and test it live | ⬜ |

## Detailed Instructions

### 1. Prepare Your Repository

Ensure your repository is on GitHub and accessible. If it's private, make sure your GitHub account has access.

### 2. Create Streamlit Cloud Account

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Grant necessary permissions

### 3. Create New App

1. Click **"New app"** button
2. Choose **"From existing repo"**
3. Select your repository: `your-username/tamperproof-logistics-tracker`
4. Set **Branch**: `main` (or your default branch)
5. Set **Main file path**: `streamlit_app/app.py`
6. Set **App URL** (optional): choose a custom subdomain

### 4. Configure Environment Variables

⚠️ **CRITICAL**: Configure these secrets before deployment:

1. Click **"Advanced settings"** → **"Secrets"**
2. Add the following key-value pairs:

```toml
RPC_URL = "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"
PRIVATE_KEY = "your_sepolia_testnet_private_key"
CONTRACT_ADDRESS = "your_deployed_contract_address"
```

### 5. Recommended Testnet Setup

For public deployment, use **Sepolia Testnet**:

- **RPC URL**: Get from [Infura](https://infura.io/) or [Alchemy](https://alchemy.com/)
- **Private Key**: Use a test account with Sepolia ETH
- **Contract**: Deploy your contract to Sepolia first

#### Getting Sepolia Testnet ETH
1. Visit [Sepolia Faucet](https://sepoliafaucet.com/)
2. Or use [Alchemy Faucet](https://sepoliafaucet.com/)
3. Enter your test wallet address

### 6. Deploy and Test

1. Click **"Deploy!"**
2. Wait for deployment (usually 2-3 minutes)
3. Visit your app URL
4. Test blockchain connection
5. Create a test checkpoint

## 🔧 Troubleshooting

### Common Issues:

**"Module not found" errors:**
- Check `streamlit_app/requirements.txt` is present
- Ensure all dependencies are listed

**Blockchain connection failed:**
- Verify RPC_URL is correct in secrets
- Check CONTRACT_ADDRESS format (should start with 0x)
- Ensure PRIVATE_KEY is valid (64 characters + optional 0x prefix)

**Contract interaction errors:**
- Make sure contract is deployed on the correct network
- Verify your account has the required role in the contract
- Check if the account has sufficient ETH for gas fees

### Advanced Configuration:

**Custom Python version:**
Add `.streamlit/config.toml`:
```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## 🎯 Pre-Deployment Testing

Before going live, test locally:

```bash
cd streamlit_app
streamlit run app.py
```

Verify:
- ✅ Blockchain connection works
- ✅ Can add checkpoints
- ✅ Can view shipment history
- ✅ Event monitoring works
- ✅ No console errors

## 📱 Mobile Optimization

The app is responsive, but test on mobile:
- Check sidebar navigation
- Verify form inputs work
- Test chart responsiveness

## 🔒 Security Best Practices

1. **Never use mainnet** for public demos
2. **Use test accounts only** with minimal funds
3. **Regularly rotate test keys**
4. **Monitor gas usage** to prevent exhaustion
5. **Set appropriate contract permissions**

---

🎉 **Your app will be live at**: `https://your-app-name.streamlit.app`