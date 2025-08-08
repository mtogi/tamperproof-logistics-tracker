"""
Tamper-Proof Component Logistics Tracker - Streamlit Frontend

A comprehensive blockchain-based logistics tracking system with:
- Real-time checkpoint monitoring
- Secure Web3 integration  
- Enhanced error handling and user feedback
- Professional UI/UX design
"""

import streamlit as st
import pandas as pd
from typing import List, Dict
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Import our Web3 utilities
from web3_utils import get_web3_manager, create_sample_env_file, clear_web3_manager_cache

# Page configuration
st.set_page_config(
    page_title="Tamper-Proof Logistics Tracker",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for professional UI/UX with mobile responsiveness
st.markdown("""
<style>
/* Global styles */
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2.5rem;
    font-weight: 600;
    letter-spacing: -0.5px;
}

/* Improved spacing for form elements */
.stTextInput > div > div > input {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 2px solid #e0e7ff;
    transition: all 0.2s ease;
    font-size: 1rem;
}

.stTextInput > div > div > input:focus {
    border-color: #1f77b4;
    box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
    outline: none;
}

.stSelectbox > div > div {
    padding: 0.5rem 0;
}

.stButton > button {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
    border: none;
    margin: 0.5rem 0;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Status cards with better spacing */
.status-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.status-card:hover {
    transform: translateY(-2px);
}

.success-card {
    background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.error-card {
    background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.warning-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.info-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Enhanced checkpoint cards */
.checkpoint-card {
    border-left: 4px solid #1f77b4;
    padding: 1.5rem;
    margin: 1rem 0;
    background-color: #fafbfc;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}

.checkpoint-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    transform: translateY(-1px);
}

/* Form sections with better spacing */
.form-section {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    margin: 1.5rem 0;
    border: 1px solid #e5e7eb;
}

.section-header {
    font-size: 1.25rem;
    font-weight: 600;
    color: #374151;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid #e5e7eb;
}

/* Loading spinner styles */
.loading-container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
}

.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 1s ease-in-out infinite;
    margin-right: 0.75rem;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .main-header {
        font-size: 2rem;
        margin-bottom: 1.5rem;
    }
    
    .status-card, .success-card, .error-card, .warning-card, .info-card {
        padding: 1rem;
        margin: 0.75rem 0;
    }
    
    .checkpoint-card {
        padding: 1rem;
        margin: 0.75rem 0;
    }
    
    .form-section {
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        padding: 0.875rem 1rem;
    }
}

/* Sidebar improvements for mobile */
@media (max-width: 768px) {
    .css-1d391kg {
        padding: 1rem;
    }
    
    .css-1y4p8pa {
        width: 100%;
        max-width: none;
    }
}

/* Table responsiveness */
.dataframe {
    font-size: 0.9rem;
}

@media (max-width: 768px) {
    .dataframe {
        font-size: 0.8rem;
    }
    
    .stDataFrame {
        overflow-x: auto;
    }
}

/* Etherscan link styling */
.etherscan-link {
    display: inline-flex;
    align-items: center;
    padding: 0.5rem 1rem;
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    text-decoration: none;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.2s ease;
    margin: 0.5rem 0.5rem 0.5rem 0;
}

.etherscan-link:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    text-decoration: none;
    color: white;
}

/* Success feedback styling */
.success-feedback {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

/* Better spacing for metrics */
.metric-container {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    margin: 0.5rem;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📦 Tamper-Proof Logistics Tracker</h1>', unsafe_allow_html=True)
    
    # Initialize Web3 manager
    w3_manager = get_web3_manager()
    
    # Sidebar for navigation and connection status
    with st.sidebar:
        st.header("🔗 Connection Status")
        
        # Connection control buttons
        status = w3_manager.get_connection_status()
        
        if status["connected"]:
            if st.button("🔌 Disconnect from Blockchain", type="secondary"):
                with st.spinner("Disconnecting..."):
                    try:
                        if w3_manager.disconnect():
                            # Clear the cached Web3Manager instance to ensure clean state
                            clear_web3_manager_cache()
                            st.success("✅ Disconnected!")
                            st.rerun()
                        else:
                            st.error("❌ Disconnect failed")
                    except Exception as e:
                        st.error(f"❌ Disconnect error: {str(e)}")
                        # Try to clear cache anyway
                        clear_web3_manager_cache()
                        st.rerun()
        else:
            if st.button("🔄 Connect to Blockchain", type="primary"):
                with st.spinner("Connecting..."):
                    if w3_manager.connect():
                        st.success("✅ Connected!")
                        st.rerun()
                    else:
                        st.error("❌ Connection failed")
        
        # Display connection status
        if status["connected"]:
            st.markdown(f"""
            <div class="status-card">
            <strong>✅ Connected</strong><br>
            🌐 Network: {status['network']}<br>
            📦 Block: {status['latest_block']}<br>
            👤 Account: {status['account'][:10]}...<br>
            💰 Balance: {status['balance']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="error-card">
            <strong>❌ Not Connected</strong><br>
            Error: {status.get('error', 'Unknown')}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📝 Create .env template"):
                env_path = create_sample_env_file()
                st.info(f"Template created at: {env_path}")
        
        st.markdown("---")
        
        # Live Events Section
        st.header("🔊 Live Events")
        if st.button("🔄 Refresh Events"):
            st.rerun()
        
        # Display recent events
        with st.spinner("🔍 Loading recent activity..."):
            try:
                recent_events = w3_manager.get_recent_events(limit=5)
                if recent_events:
                    st.markdown("**📈 Recent Activity:**")
                    for event in recent_events[-3:]:  # Show last 3
                        with st.container():
                            st.markdown(f"""
                            <div style="font-size: 0.8em; padding: 0.5rem; margin: 0.2rem 0; background-color: #f0f2f6; border-radius: 5px; border-left: 3px solid #1f77b4;">
                            📦 <strong>{event['shipmentId']}</strong><br>
                            📍 {event['location']} → {event['status']}<br>
                            🕒 {event['relative_time']}
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("📦 No recent events found. Create some checkpoints to see activity here!")
            except Exception as e:
                st.warning(f"⚠️ Could not load events: {str(e)}")
                st.info("💡 **Tip:** Make sure your blockchain connection is active and the contract is deployed.")
        
        st.markdown("---")
        
        # Navigation
        st.header("📋 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🔍 View Shipment History", "➕ Add Checkpoint", "📊 Analytics", "🔊 Event Monitor"]
        )
    
    # Main content area with better mobile messaging
    if not status["connected"]:
        st.markdown("""
        <div class="warning-card">
        <h4 style="margin: 0 0 1rem 0; color: white;">⚠️ Blockchain Connection Required</h4>
        <p style="margin: 0; color: white; opacity: 0.9;">
        Please connect to the blockchain first using the sidebar.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
        <h4 style="margin: 0 0 1rem 0; color: white;">💡 Setup Instructions:</h4>
        <ul style="margin: 0; color: white; opacity: 0.9;">
        <li>Make sure you have a <code>.env</code> file with RPC_URL, PRIVATE_KEY, and CONTRACT_ADDRESS</li>
        <li>Click the "Connect to Blockchain" button in the sidebar</li>
        <li>Check that your network connection is stable</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Route to different pages
    if page == "🔍 View Shipment History":
        view_shipment_history_page(w3_manager)
    elif page == "➕ Add Checkpoint":
        add_checkpoint_page(w3_manager)
    elif page == "📊 Analytics":
        analytics_page(w3_manager)
    elif page == "🔊 Event Monitor":
        event_monitor_page(w3_manager)

def view_shipment_history_page(w3_manager):
    """Page for viewing shipment checkpoint history"""
    
    st.markdown('<h2 class="section-header">🔍 View Shipment History</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="form-section">
    <p style="margin: 0; color: #6b7280; font-size: 1.1rem;">Enter a shipment ID to view its complete checkpoint timeline and tracking history.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for auto-populated shipment ID from session state
    default_shipment = st.session_state.get('view_shipment_id', '')
    
    # Input form
    with st.form("shipment_lookup"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            shipment_id = st.text_input(
                "Shipment ID",
                value=default_shipment,
                placeholder="Shipment-2025-001",
                help="Enter the unique identifier for the shipment (e.g., Shipment-2025-001, PKG-LOG-5432)"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            submitted = st.form_submit_button("🔍 Search", type="primary")
    
    # Clear session state after use
    if default_shipment and submitted:
        st.session_state.view_shipment_id = ''
    
    if submitted:
        # Validate input with friendly error message
        if not shipment_id or not shipment_id.strip():
            st.markdown("""
            <div class="error-card">
            <h4 style="margin: 0 0 0.5rem 0; color: white;">📦 Please enter a shipment ID</h4>
            <p style="margin: 0; color: white; opacity: 0.9;">Enter a shipment ID like "Shipment-2025-001" to view its tracking history.</p>
            </div>
            """, unsafe_allow_html=True)
            return
            
        shipment_id = shipment_id.strip()
        
        with st.spinner(f"Fetching history for {shipment_id}..."):
            try:
                # Get checkpoint count first
                count = w3_manager.get_checkpoint_count(shipment_id)
                
                if count == 0:
                    st.markdown(f"""
                    <div class="warning-card">
                    <h4 style="margin: 0 0 1rem 0; color: white;">📦 Shipment Not Found</h4>
                    <p style="margin: 0; color: white; opacity: 0.9;">
                    No checkpoints exist for shipment ID: <strong>{shipment_id}</strong><br>
                    💡 This shipment may not have been created yet, or the ID might be incorrect.
                    </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Suggest similar actions
                    st.markdown("""
                    <div class="info-card">
                    <h4 style="margin: 0 0 1rem 0; color: white;">💡 What you can do:</h4>
                    <ul style="margin: 0; color: white; opacity: 0.9;">
                    <li>Double-check the shipment ID spelling</li>
                    <li>Try a different shipment ID</li>
                    <li>Create a new checkpoint using the "Add Checkpoint" tab</li>
                    <li>Check recent activity in the sidebar</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    return
                
                # Fetch full history
                checkpoints = w3_manager.get_shipment_history(shipment_id)
                
                # Display summary
                st.success(f"✅ Found {count} checkpoint(s) for shipment `{shipment_id}`")
                
                # Display checkpoints in a timeline format with better mobile layout
                st.markdown('<h3 class="section-header">📅 Checkpoint Timeline</h3>', unsafe_allow_html=True)
                
                for i, checkpoint in enumerate(checkpoints):
                    with st.container():
                        # Use responsive columns for mobile
                        col1, col2, col3 = st.columns([1, 3, 2])
                        
                        with col1:
                            st.markdown(f"**#{i+1}**")
                            
                        with col2:
                            # Add relative time formatting
                            relative_time = w3_manager._format_relative_time(checkpoint['timestamp'])
                            st.markdown(f"""
                            <div class="checkpoint-card">
                            <strong>📍 {checkpoint['location']}</strong><br>
                            🏷️ Status: <code>{checkpoint['status']}</code><br>
                            🕒 {checkpoint['formatted_time']}<br>
                            <small>⏱️ {relative_time}</small>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with col3:
                            st.markdown(f"""
                            **📄 Document:** `{checkpoint['documentHash'] or 'None'}`  
                            **👤 Submitted by:** `{checkpoint['submittedBy'][:10]}...`
                            """)
                
                # Export option with better mobile layout
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("📥 Export as CSV", use_container_width=True):
                        df = pd.DataFrame(checkpoints)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📎 Download CSV",
                            data=csv,
                            file_name=f"shipment_{shipment_id}_history.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-card">
                <h4 style="margin: 0 0 1rem 0; color: white;">❌ Error Loading Shipment History</h4>
                <p style="margin: 0; color: white; opacity: 0.9;">
                We encountered an issue while fetching the shipment data.<br>
                <small>Technical details: {str(e)}</small>
                </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Provide troubleshooting tips
                st.markdown("""
                <div class="info-card">
                <h4 style="margin: 0 0 1rem 0; color: white;">🔧 Troubleshooting Steps:</h4>
                <ul style="margin: 0; color: white; opacity: 0.9;">
                <li>Check that the blockchain connection is active (see sidebar)</li>
                <li>Verify the shipment ID is correct (case-sensitive)</li>
                <li>Ensure the smart contract is properly deployed</li>
                <li>Try refreshing the page if the network is slow</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

def add_checkpoint_page(w3_manager):
    """Page for adding new checkpoints"""
    
    st.markdown('<h2 class="section-header">➕ Add New Checkpoint</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="form-section">
    <p style="margin: 0; color: #6b7280; font-size: 1.1rem;">Submit a new checkpoint to the blockchain to track your shipment's journey.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check user role
    try:
        if w3_manager.account:
            user_role = w3_manager.get_user_role(w3_manager.account.address)
            if user_role == "None":
                st.markdown("""
                <div class="warning-card">
                <h4 style="margin: 0 0 1rem 0; color: white;">⚠️ Account Role Required</h4>
                <p style="margin: 0; color: white; opacity: 0.9;">
                Your account has no assigned role. Contact the system administrator to assign a role before adding checkpoints.
                </p>
                </div>
                """, unsafe_allow_html=True)
                return
            else:
                st.markdown(f"""
                <div class="info-card">
                <p style="margin: 0; color: white;">👤 Your role: <strong>{user_role}</strong></p>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div class="error-card">
        <h4 style="margin: 0 0 1rem 0; color: white;">❌ Unable to Check Account Role</h4>
        <p style="margin: 0; color: white; opacity: 0.9;">
        We couldn't verify your account permissions. Please check your blockchain connection.
        <br><small>Technical details: {str(e)}</small>
        </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Enhanced checkpoint form with better styling
    st.markdown("""
    <div class="form-section">
    <h3 class="section-header">📝 Checkpoint Details</h3>
    """, unsafe_allow_html=True)
    
    with st.form("add_checkpoint"):
        
        # Form fields
        shipment_id = st.text_input(
            "Shipment ID *",
            placeholder="Shipment-2025-001",
            help="Unique identifier for the shipment (required)",
            key="add_checkpoint_shipment_id"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.text_input(
                "Location *",
                placeholder="Warehouse #3, New York",
                help="Current location of the shipment (required)",
                key="add_checkpoint_location"
            )
        
        with col2:
            status = st.selectbox(
                "Status *",
                options=["created", "in-transit", "customs", "delivered", "damaged", "delayed"],
                help="Current status of the shipment"
            )
        
        document_hash = st.text_input(
            "Document Hash (Optional)",
            placeholder="QmNLei78zWmzUdbeRB3CiUfAizWUrbeeZh5K1rhAQKCh51",
            help="Optional IPFS hash or document reference",
            key="add_checkpoint_document"
        )
        
        # Preview
        st.subheader("👀 Preview")
        if shipment_id and location and status:
            st.markdown(f"""
            **Shipment:** `{shipment_id}`  
            **Location:** {location}  
            **Status:** {status}  
            **Document:** {document_hash or 'None'}  
            **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} *(estimated)*
            """)
        
        # Submit button with enhanced styling
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Submit Checkpoint", type="primary", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Close form-section
    
    # Handle submission
    if submitted:
        # Comprehensive validation with better UX
        validation_errors = []
        
        if not shipment_id or not shipment_id.strip():
            validation_errors.append("Please enter a shipment ID")
        if not location or not location.strip():
            validation_errors.append("Please enter a location")
        if not status:
            validation_errors.append("Please select a status")
            
        if validation_errors:
            st.markdown("""
            <div class="error-card">
            <h4 style="margin: 0 0 1rem 0; color: white;">❌ Please Complete All Required Fields</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for error in validation_errors:
                st.markdown(f"""
                <div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 1rem; margin: 0.5rem 0; border-radius: 4px;">
                <p style="margin: 0; color: #dc2626;">• {error}</p>
                </div>
                """, unsafe_allow_html=True)
            return
            
        # Clean input data
        shipment_id = shipment_id.strip()
        location = location.strip()
        document_hash = document_hash.strip() if document_hash else ""
        
        # Check for duplicate checkpoint prevention
        try:
            # Get latest checkpoint for this shipment
            latest_checkpoints = w3_manager.get_shipment_history(shipment_id)
            if latest_checkpoints:
                latest_checkpoint = latest_checkpoints[-1]  # Get most recent
                
                # Check if the latest checkpoint has the same location and status
                if (latest_checkpoint['location'].lower().strip() == location.lower().strip() and 
                    latest_checkpoint['status'].lower().strip() == status.lower().strip()):
                    
                    st.warning("⚠️ **Duplicate Checkpoint Detected**")
                    st.markdown(f"""
                    <div class="warning-card">
                    <h4 style="margin: 0 0 1rem 0; color: white;">🔄 Last checkpoint for this shipment:</h4>
                    <p style="margin: 0; color: white; opacity: 0.9;">
                    📍 Location: {latest_checkpoint['location']}<br>
                    🏷️ Status: {latest_checkpoint['status']}<br>
                    🕒 Time: {latest_checkpoint['formatted_time']}
                    </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not st.checkbox("🚀 I want to add this duplicate checkpoint anyway", key="override_duplicate"):
                        st.info("💡 **Tip:** Try updating the location or status to make it more specific, or check if this checkpoint was already added.")
                        return
                    else:
                        st.info("✅ Proceeding with duplicate checkpoint as requested.")
        except Exception:
            # If we can't check for duplicates, continue anyway
            pass
        
        # Store form data in session state for persistence through rerun
        st.session_state.pending_checkpoint = {
            'shipment_id': shipment_id,
            'location': location,
            'status': status,
            'document_hash': document_hash
        }
        
        # Set state machine flags
        st.session_state.show_confirmation = True
        st.session_state.confirm_submission = False  # Reset confirm flag
        st.success("✅ Checkpoint data validated. Please confirm to submit to blockchain.")
        st.rerun()  # Rerun to show confirmation state
    
    # Show confirmation if we have pending data
    if st.session_state.get('show_confirmation') and st.session_state.get('pending_checkpoint'):
        pending = st.session_state.pending_checkpoint
        
        st.markdown("### 📝 Review Checkpoint Details")
        st.markdown(f"""
        **Shipment ID:** `{pending['shipment_id']}`  
        **Location:** {pending['location']}  
        **Status:** {pending['status']}  
        **Document Hash:** {pending['document_hash'] or 'None'}
        """)
        
        st.warning("⚠️ This will create a blockchain transaction. Click 'Confirm' to proceed.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm Submission", type="primary"):
                st.session_state.confirm_submission = True
                st.session_state.show_confirmation = False
                st.rerun()
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.pending_checkpoint = None
                st.session_state.show_confirmation = False
                st.session_state.confirm_submission = False
                st.rerun()
    
    # Handle confirmed submission (using session state data)
    if st.session_state.get('confirm_submission') == True and st.session_state.get('pending_checkpoint') and not st.session_state.get('show_confirmation'):
        pending = st.session_state.pending_checkpoint
        
        # Enhanced loading feedback with spinner
        loading_placeholder = st.empty()
        loading_placeholder.markdown("""
        <div class="loading-container">
        <div class="loading-spinner"></div>
        <strong>Processing transaction... Please wait</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Submit to blockchain
        with st.spinner("🔄 Submitting to blockchain..."):
            success, message, tx_details = w3_manager.add_checkpoint(
                shipment_id=pending['shipment_id'],
                location=pending['location'],
                status=pending['status'],
                document_hash=pending['document_hash']
            )
        
        # Clear loading indicator
        loading_placeholder.empty()
        
        # Clear all session state flags and pending data
        st.session_state.confirm_submission = False
        st.session_state.pending_checkpoint = None
        st.session_state.show_confirmation = False
        
        # Display enhanced result
        if success:
            # Clear form fields after successful submission
            if 'add_checkpoint_shipment_id' in st.session_state:
                del st.session_state['add_checkpoint_shipment_id']
            if 'add_checkpoint_location' in st.session_state:
                del st.session_state['add_checkpoint_location']
            if 'add_checkpoint_document' in st.session_state:
                del st.session_state['add_checkpoint_document']
            
            # Success feedback with enhanced styling
            st.markdown(f"""
            <div class="success-feedback">
            <h3 style="margin: 0 0 1rem 0; color: white;">✅ Checkpoint Added Successfully!</h3>
            <p style="margin: 0; color: white; opacity: 0.9;">{message}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show detailed transaction info with Etherscan link
            if tx_details:
                with st.expander("📊 Transaction Details", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        **🔗 Transaction Hash:**  
                        `{tx_details.get('hash', 'N/A')}`
                        
                        **📦 Block Number:**  
                        `{tx_details.get('block_number', 'N/A')}`
                        """)
                    with col2:
                        st.markdown(f"""
                        **⛽ Gas Used:**  
                        `{tx_details.get('gas_used', 'N/A'):,} / {tx_details.get('gas_limit', 'N/A'):,}`
                        
                        **💰 Gas Price:**  
                        `{tx_details.get('gas_price', 'N/A')} Gwei`
                        """)
                    
                    # Add Etherscan link (assuming mainnet/testnet)
                    if tx_details.get('hash'):
                        # Detect network for correct Etherscan link
                        network_prefix = ""
                        if "sepolia" in w3_manager.rpc_url.lower():
                            network_prefix = "sepolia."
                        elif "goerli" in w3_manager.rpc_url.lower():
                            network_prefix = "goerli."
                        elif "polygon" in w3_manager.rpc_url.lower():
                            network_prefix = "polygonscan.com/"
                            network_prefix = network_prefix.replace("etherscan.io", "polygonscan.com")
                        
                        etherscan_url = f"https://{network_prefix}etherscan.io/tx/{tx_details['hash']}"
                        if "polygonscan.com" in network_prefix:
                            etherscan_url = f"https://polygonscan.com/tx/{tx_details['hash']}"
                        
                        st.markdown(f"""
                        <a href="{etherscan_url}" target="_blank" class="etherscan-link">
                        🔍 View on Etherscan
                        </a>
                        """, unsafe_allow_html=True)
            
            # Show success toast
            if hasattr(st, 'toast'):
                st.toast('✅ Checkpoint added successfully!', icon='🎉')
            
            st.balloons()
            
            # Auto-refresh: reload shipment history
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 View Updated History", type="primary"):
                    st.session_state.view_shipment_id = pending['shipment_id']
                    st.info("💡 Switch to 'View Shipment History' tab to see the updated timeline for this shipment.")
            with col2:
                if st.button("➕ Add Another Checkpoint"):
                    st.rerun()
                
        else:
            st.markdown(f"""
            <div class="error-card">
            <h3 style="margin: 0 0 1rem 0; color: white;">❌ Transaction Failed</h3>
            <p style="margin: 0; color: white; opacity: 0.9;">{message}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show error details if available
            if tx_details and tx_details.get('hash'):
                with st.expander("🔍 Error Details"):
                    st.markdown(f"""
                    **Transaction Hash:** `{tx_details['hash']}`  
                    **Status:** Failed
                    """)
                    
                    # Add Etherscan link for failed transaction too
                    network_prefix = ""
                    if "sepolia" in w3_manager.rpc_url.lower():
                        network_prefix = "sepolia."
                    elif "goerli" in w3_manager.rpc_url.lower():
                        network_prefix = "goerli."
                    
                    etherscan_url = f"https://{network_prefix}etherscan.io/tx/{tx_details['hash']}"
                    st.markdown(f"""
                    <a href="{etherscan_url}" target="_blank" class="etherscan-link">
                    🔍 View on Etherscan
                    </a>
                    """, unsafe_allow_html=True)
            
            # Show error toast
            if hasattr(st, 'toast'):
                st.toast('❌ Transaction failed', icon='💥')
                
            # Provide actionable error guidance
            st.markdown("""
            <div class="info-card">
            <h4 style="margin: 0 0 1rem 0; color: white;">💡 What to try next:</h4>
            <ul style="margin: 0; color: white; opacity: 0.9;">
            <li>Check your account balance for gas fees</li>
            <li>Verify your account has the required role permissions</li>
            <li>Try again with a different gas price setting</li>
            <li>Check if the shipment ID follows the expected format</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

def analytics_page(w3_manager):
    """Basic analytics page"""
    
    st.markdown('<h2 class="section-header">📊 Analytics Dashboard</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="form-section">
    <p style="margin: 0; color: #6b7280; font-size: 1.1rem;">Monitor shipment performance and system statistics.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample analytics (in a real app, you'd aggregate data from multiple shipments)
    st.subheader("📈 Quick Stats")
    
    # Enhanced metrics with mobile-friendly layout
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="metric-container">
        <h3 style="margin: 0 0 0.5rem 0; color: #1f77b4;">🚛 Active Shipments</h3>
        <p style="margin: 0; font-size: 2rem; font-weight: bold; color: #111827;">42</p>
        <small style="color: #10b981;">+5 this week</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
        <h3 style="margin: 0 0 0.5rem 0; color: #10b981;">✅ Delivered Today</h3>
        <p style="margin: 0; font-size: 2rem; font-weight: bold; color: #111827;">15</p>
        <small style="color: #10b981;">+3 from yesterday</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
        <h3 style="margin: 0 0 0.5rem 0; color: #ef4444;">⚠️ Delayed Shipments</h3>
        <p style="margin: 0; font-size: 2rem; font-weight: bold; color: #111827;">3</p>
        <small style="color: #ef4444;">-1 resolved</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Sample shipment lookup
    st.subheader("🔍 Quick Lookup")
    
    # Note: Sample IDs shown here are for demonstration only
    # In production, these would be fetched from actual blockchain data
    sample_note = st.info("💡 **Note:** Sample lookups require actual shipment data on the blockchain. Create checkpoints first using the 'Add Checkpoint' page.")
    
    # Quick lookup by manual entry
    lookup_id = st.text_input(
        "Enter a shipment ID to check:",
        placeholder="Shipment-2025-001",
        help="Enter a shipment ID that has been created on the blockchain",
        key="analytics_lookup_id"
    )
    
    if st.button("🔍 Check Shipment") and lookup_id.strip():
        with st.spinner(f"Checking {lookup_id}..."):
            try:
                count = w3_manager.get_checkpoint_count(lookup_id.strip())
                if count > 0:
                    st.success(f"✅ Shipment `{lookup_id}` has {count} checkpoint(s)")
                    # Provide link to view full history
                    if st.button("📋 View Full History"):
                        st.session_state.view_shipment_id = lookup_id.strip()
                        st.info("💡 Switch to 'View Shipment History' tab to see the full timeline")
                else:
                    st.warning(f"⚠️ No checkpoints found for shipment `{lookup_id}`")
            except Exception as e:
                st.error(f"❌ Error checking shipment `{lookup_id}`: {str(e)}")
    
    # Chart placeholder
    st.subheader("📊 Status Distribution")
    
    # Sample data for demonstration
    status_data = {
        'Status': ['delivered', 'in-transit', 'customs', 'delayed'],
        'Count': [45, 23, 8, 3]
    }
    
    fig = px.pie(
        values=status_data['Count'],
        names=status_data['Status'],
        title="Shipment Status Distribution"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def event_monitor_page(w3_manager):
    """Live event monitoring page"""
    
    st.markdown('<h2 class="section-header">🔊 Live Event Monitor</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="form-section">
    <p style="margin: 0; color: #6b7280; font-size: 1.1rem;">Monitor real-time blockchain events and shipment activities.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Controls with responsive layout
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        shipment_filter = st.text_input(
            "Filter by Shipment ID (optional)",
            placeholder="Shipment-2025-001",
            help="Leave empty to see all events",
            key="event_monitor_filter"
        )
    
    with col2:
        event_limit = st.number_input(
            "Max Events",
            min_value=5,
            max_value=50,
            value=20
        )
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        auto_refresh = st.checkbox("🔄 Auto-refresh (30s)")
    
    # Add refresh button with mobile-friendly styling
    if st.button("🔄 Refresh Events", type="primary", use_container_width=True) or auto_refresh:
        if auto_refresh:
            time.sleep(30)
            st.rerun()
    
    # Fetch and display events
    with st.spinner("Loading events..."):
        try:
            events = w3_manager.get_recent_events(
                shipment_id=shipment_filter if shipment_filter else None,
                limit=event_limit
            )
            
            if events:
                st.success(f"✅ Found {len(events)} event(s)")
                
                # Display events in reverse chronological order
                for i, event in enumerate(reversed(events)):
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            # Event card
                            st.markdown(f"""
                            <div class="checkpoint-card" style="margin: 0.5rem 0;">
                            <strong>📦 Shipment: {event['shipmentId']}</strong><br>
                            📍 <strong>{event['location']}</strong> → <code>{event['status']}</code><br>
                            🕒 {event['formatted_time']} <small>({event['relative_time']})</small><br>
                            👤 Submitted by: <code>{event['submittedBy'][:10]}...</code><br>
                            📋 Block: {event['blockNumber']} | 🔗 <code>{event['transactionHash'][:10]}...</code>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            # Action buttons with mobile-friendly styling
                            if st.button(f"📋 View", key=f"view_{i}", use_container_width=True):
                                st.session_state.view_shipment_id = event['shipmentId']
                                st.info(f"Switch to 'View Shipment History' and search for: {event['shipmentId']}")
                
                # Export events with mobile-friendly layout
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("📥 Export Events as CSV", use_container_width=True):
                    df = pd.DataFrame(events)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📎 Download Events CSV",
                        data=csv,
                        file_name=f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
            else:
                st.info("📭 No events found for the specified criteria")
                st.markdown("""
                **Troubleshooting:**
                - Make sure the contract is deployed and has some checkpoint data
                - Try removing the shipment ID filter to see all events
                - Check if there are any recent blockchain transactions
                """)
                
        except Exception as e:
            st.error(f"❌ **Error loading events**")
            st.error(f"Details: {str(e)}")
            
            with st.expander("🔧 Troubleshooting"):
                st.markdown("""
                **Possible solutions:**
                - Check blockchain connection status in sidebar
                - Verify contract deployment and address
                - Try reducing the event limit or removing filters
                - Check if there are any recent transactions
                """)
    
    # Real-time monitoring section
    st.markdown("---")
    st.subheader("📡 Real-time Monitoring")
    
    if st.button("🔴 Start Live Monitoring", use_container_width=True):
        st.info("🔄 Live monitoring would start here (requires WebSocket or polling)")
        st.markdown("""
        **Note:** Full real-time monitoring requires:
        - WebSocket connection or background polling
        - Streamlit server-side state management
        - Consider using `st.empty()` containers for live updates
        """)
        
        # Placeholder for real-time events
        placeholder = st.empty()
        
        # Simulate real-time updates (in production, this would be actual event listening)
        for i in range(3):
            with placeholder.container():
                st.info(f"🔍 Checking for new events... ({i+1}/3)")
                time.sleep(2)
                
                # Get latest events
                latest_events = w3_manager.get_recent_events(limit=3)
                if latest_events:
                    st.success(f"📡 Latest activity: {len(latest_events)} events")
                    for event in latest_events[-1:]:  # Show just the latest
                        st.markdown(f"📦 **{event['shipmentId']}** - {event['location']} ({event['relative_time']})")
                else:
                    st.info("📭 No new events detected")

if __name__ == "__main__":
    main()