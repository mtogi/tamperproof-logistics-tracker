#!/usr/bin/env python3
"""
Startup script for Tamper-Proof Logistics Tracker Streamlit App
Checks dependencies and environment before launching the dashboard
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'streamlit',
        'web3',
        'pandas',
        'plotly',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        print("\n   Or install all requirements:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_environment():
    """Check if .env file exists and has required variables"""
    env_path = Path(__file__).parent.parent / '.env'
    
    if not env_path.exists():
        print("⚠️  .env file not found")
        print("💡 Create .env file from template:")
        print(f"   cp {env_path.parent / '.env.example'} {env_path}")
        print("   Then edit .env with your configuration")
        return False
    
    # Load and check basic variables
    try:
        # Try to load dotenv if available
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
        except ImportError:
            print("⚠️  python-dotenv not installed, reading .env manually")
        
        required_vars = ['RPC_URL', 'PRIVATE_KEY', 'CONTRACT_ADDRESS']
        missing_vars = []
        
        for var in required_vars:
            value = os.getenv(var, '').strip()
            if not value or value.endswith('_here') or value == 'your_contract_address_here':
                missing_vars.append(var)
        
        if missing_vars:
            print("⚠️  Please configure these variables in .env:")
            for var in missing_vars:
                print(f"   - {var}")
            return False
        
        print("✅ Environment configuration looks good")
        return True
        
    except Exception as e:
        print(f"❌ Error checking environment: {e}")
        return False

def run_streamlit():
    """Launch the Streamlit app"""
    app_path = Path(__file__).parent / 'app.py'
    
    print("🚀 Starting Tamper-Proof Logistics Tracker...")
    print("📱 Dashboard will open in your browser")
    print("🔗 URL: http://localhost:8501")
    print("\n💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', str(app_path),
            '--server.headless', 'false',
            '--server.enableCORS', 'false'
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

def main():
    """Main startup function"""
    print("📦 Tamper-Proof Logistics Tracker - Day 7")
    print("🔍 Performing startup checks...\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    print("\n🎯 All checks passed! Starting the app...\n")
    
    # Run the app
    run_streamlit()

if __name__ == "__main__":
    main() 