"""
Tamper-Proof Component Logistics Tracker - Streamlit Frontend
Day 7: Web3 Integration Dashboard

Connects to deployed SupplyChainTracker smart contract via Web3.py
"""

import streamlit as st
import pandas as pd
from typing import List, Dict
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Import our Web3 utilities
from web3_utils import get_web3_manager, create_sample_env_file

# Page configuration
st.set_page_config(
    page_title="Tamper-Proof Logistics Tracker",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.status-card {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 0.5rem 0;
}
.success-card {
    background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
}
.error-card {
    background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
}
.checkpoint-card {
    border-left: 4px solid #1f77b4;
    padding: 1rem;
    margin: 0.5rem 0;
    background-color: #f8f9fa;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📦 Tamper-Proof Logistics Tracker</h1>', unsafe_allow_html=True)
    st.markdown("**Day 8: Live Events & Enhanced UX** - Real-time blockchain monitoring with auto-refresh", unsafe_allow_html=True)
    
    # Initialize Web3 manager
    w3_manager = get_web3_manager()
    
    # Sidebar for navigation and connection status
    with st.sidebar:
        st.header("🔗 Connection Status")
        
        # Try to connect on app start
        if st.button("🔄 Connect to Blockchain", type="primary"):
            with st.spinner("Connecting..."):
                if w3_manager.connect():
                    st.success("✅ Connected!")
                else:
                    st.error("❌ Connection failed")
        
        # Display connection status
        status = w3_manager.get_connection_status()
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
        try:
            recent_events = w3_manager.get_recent_events(limit=5)
            if recent_events:
                st.markdown("**Recent Activity:**")
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
                st.info("No recent events found")
        except Exception as e:
            st.warning(f"Could not load events: {str(e)}")
        
        st.markdown("---")
        
        # Navigation
        st.header("📋 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🔍 View Shipment History", "➕ Add Checkpoint", "📊 Analytics", "🔊 Event Monitor"]
        )
    
    # Main content area
    if not status["connected"]:
        st.warning("⚠️ Please connect to the blockchain first using the sidebar.")
        st.info("💡 Make sure you have a `.env` file with RPC_URL, PRIVATE_KEY, and CONTRACT_ADDRESS")
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
    
    st.header("🔍 View Shipment History")
    st.markdown("Enter a shipment ID to view its complete checkpoint timeline")
    
    # Check for auto-populated shipment ID from session state
    default_shipment = st.session_state.get('view_shipment_id', '')
    
    # Input form
    with st.form("shipment_lookup"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            shipment_id = st.text_input(
                "Shipment ID",
                value=default_shipment,
                placeholder="e.g., SHIP-001, PKG-2024-001",
                help="Enter the unique identifier for the shipment"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            submitted = st.form_submit_button("🔍 Search", type="primary")
    
    # Clear session state after use
    if default_shipment and submitted:
        st.session_state.view_shipment_id = ''
    
    if submitted and shipment_id:
        with st.spinner(f"Fetching history for {shipment_id}..."):
            try:
                # Get checkpoint count first
                count = w3_manager.get_checkpoint_count(shipment_id)
                
                if count == 0:
                    st.warning(f"⚠️ No checkpoints found for shipment ID: `{shipment_id}`")
                    return
                
                # Fetch full history
                checkpoints = w3_manager.get_shipment_history(shipment_id)
                
                # Display summary
                st.success(f"✅ Found {count} checkpoint(s) for shipment `{shipment_id}`")
                
                # Display checkpoints in a timeline format
                st.subheader("📅 Checkpoint Timeline")
                
                for i, checkpoint in enumerate(checkpoints):
                    with st.container():
                        col1, col2, col3 = st.columns([1, 2, 2])
                        
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
                
                # Export option
                if st.button("📥 Export as CSV"):
                    df = pd.DataFrame(checkpoints)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"shipment_{shipment_id}_history.csv",
                        mime="text/csv"
                    )
                
            except Exception as e:
                st.error(f"❌ Error fetching shipment history: {str(e)}")

def add_checkpoint_page(w3_manager):
    """Page for adding new checkpoints"""
    
    st.header("➕ Add New Checkpoint")
    st.markdown("Submit a new checkpoint to the blockchain")
    
    # Check user role
    try:
        if w3_manager.account:
            user_role = w3_manager.get_user_role(w3_manager.account.address)
            if user_role == "None":
                st.warning("⚠️ Your account has no assigned role. Contact the admin to assign a role.")
                return
            else:
                st.info(f"👤 Your role: **{user_role}**")
    except Exception as e:
        st.error(f"❌ Error checking user role: {str(e)}")
        return
    
    # Checkpoint form
    with st.form("add_checkpoint"):
        st.subheader("📝 Checkpoint Details")
        
        # Form fields
        shipment_id = st.text_input(
            "Shipment ID *",
            placeholder="e.g., SHIP-001",
            help="Unique identifier for the shipment"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            location = st.text_input(
                "Location *",
                placeholder="e.g., New York Warehouse",
                help="Current location of the shipment"
            )
        
        with col2:
            status = st.selectbox(
                "Status *",
                options=["created", "in-transit", "customs", "delivered", "damaged", "delayed"],
                help="Current status of the shipment"
            )
        
        document_hash = st.text_input(
            "Document Hash (Optional)",
            placeholder="e.g., QmXYZ... (IPFS hash)",
            help="Optional hash of related documents"
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
        
        # Submit button
        submitted = st.form_submit_button("🚀 Submit Checkpoint", type="primary")
    
    # Handle submission
    if submitted:
        if not all([shipment_id, location, status]):
            st.error("❌ Please fill in all required fields (marked with *)")
            return
        
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
        st.success("✅ Checkpoint data stored. Please confirm to submit to blockchain.")
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
        
        # Submit to blockchain
        with st.spinner("🔄 Submitting to blockchain..."):
            success, message, tx_details = w3_manager.add_checkpoint(
                shipment_id=pending['shipment_id'],
                location=pending['location'],
                status=pending['status'],
                document_hash=pending['document_hash']
            )
        
        # Clear all session state flags and pending data
        st.session_state.confirm_submission = False
        st.session_state.pending_checkpoint = None
        st.session_state.show_confirmation = False
        
        # Display enhanced result
        if success:
            st.success(f"✅ {message}")
            
            # Show detailed transaction info
            if tx_details:
                with st.expander("📊 Transaction Details"):
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
            
            # Show success toast
            if hasattr(st, 'toast'):
                st.toast('✅ Checkpoint added successfully!', icon='🎉')
            
            st.balloons()
            
            # Auto-refresh: reload shipment history
            if st.button("🔄 View Updated History") or st.session_state.get('auto_refresh', False):
                st.session_state.view_shipment_id = pending['shipment_id']
                st.session_state.auto_refresh = False
                st.switch_page("🔍 View Shipment History") if hasattr(st, 'switch_page') else st.info("Click 'View Shipment History' to see the update")
            
            if st.button("🔄 Auto-Refresh History"):
                st.session_state.auto_refresh = True
                st.rerun()
                
        else:
            st.error(f"❌ {message}")
            
            # Show error details if available
            if tx_details and tx_details.get('hash'):
                with st.expander("🔍 Error Details"):
                    st.markdown(f"""
                    **Transaction Hash:** `{tx_details['hash']}`  
                    **Status:** Failed
                    """)
            
            # Show error toast
            if hasattr(st, 'toast'):
                st.toast('❌ Transaction failed', icon='💥')

def analytics_page(w3_manager):
    """Basic analytics page"""
    
    st.header("📊 Analytics Dashboard")
    st.markdown("Basic analytics for the logistics system")
    
    # Sample analytics (in a real app, you'd aggregate data from multiple shipments)
    st.subheader("📈 Quick Stats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🚛 Active Shipments", "42", "+5")
    
    with col2:
        st.metric("✅ Delivered Today", "15", "+3")
    
    with col3:
        st.metric("⚠️ Delayed Shipments", "3", "-1")
    
    # Sample shipment lookup
    st.subheader("🔍 Quick Lookup")
    
    sample_ids = ["SHIP-001", "PKG-2024-001", "DEMO-123"]
    selected_id = st.selectbox("Try a sample shipment ID:", sample_ids)
    
    if st.button("🔍 View Sample"):
        try:
            count = w3_manager.get_checkpoint_count(selected_id)
            st.info(f"Shipment `{selected_id}` has {count} checkpoint(s)")
        except Exception as e:
            st.warning(f"No data found for `{selected_id}`: {str(e)}")
    
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
    
    st.header("🔊 Live Event Monitor")
    st.markdown("Real-time monitoring of blockchain events")
    
    # Controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        shipment_filter = st.text_input(
            "Filter by Shipment ID (optional)",
            placeholder="e.g., SHIP-001",
            help="Leave empty to see all events"
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
    
    # Add refresh button
    if st.button("🔄 Refresh Events", type="primary") or auto_refresh:
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
                            # Action buttons
                            if st.button(f"📋 View Shipment", key=f"view_{i}"):
                                st.session_state.view_shipment_id = event['shipmentId']
                                st.info(f"Switch to 'View Shipment History' and search for: {event['shipmentId']}")
                
                # Export events
                if st.button("📥 Export Events as CSV"):
                    df = pd.DataFrame(events)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Events CSV",
                        data=csv,
                        file_name=f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
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
            st.error(f"❌ Error loading events: {str(e)}")
    
    # Real-time monitoring section
    st.markdown("---")
    st.subheader("📡 Real-time Monitoring")
    
    if st.button("🔴 Start Live Monitoring"):
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