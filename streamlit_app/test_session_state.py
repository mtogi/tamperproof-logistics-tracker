#!/usr/bin/env python3
"""
Simple Streamlit app to test session state functionality
Run this to verify session state works in your Streamlit installation
"""

import streamlit as st

st.title("🧪 Session State Test")
st.markdown("This app tests if session state works correctly in your Streamlit installation")

# Initialize session state
if 'test_data' not in st.session_state:
    st.session_state.test_data = None
if 'confirm_test' not in st.session_state:
    st.session_state.confirm_test = False
if 'awaiting_confirmation' not in st.session_state:
    st.session_state.awaiting_confirmation = False

# Form to simulate checkpoint form
with st.form("test_form"):
    st.subheader("Test Form")
    test_input = st.text_input("Test Input", placeholder="Enter anything")
    submitted = st.form_submit_button("Submit Test")

# Handle submission (similar to checkpoint logic)
if submitted:
    if test_input:
        # Store in session state and set awaiting confirmation
        st.session_state.test_data = test_input
        st.session_state.awaiting_confirmation = True
        st.session_state.confirm_test = False  # Reset confirm flag
        st.success(f"✅ Stored in session state: {test_input}")
        st.rerun()  # Rerun to show confirmation state
    else:
        st.error("❌ Please enter some text")

# Show confirmation if awaiting
if st.session_state.get('awaiting_confirmation') and st.session_state.get('test_data'):
    st.warning("⚠️ Click confirm to test session state persistence")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm Test"):
            st.session_state.confirm_test = True
            st.session_state.awaiting_confirmation = False
            st.rerun()
    with col2:
        if st.button("❌ Cancel"):
            st.session_state.test_data = None
            st.session_state.awaiting_confirmation = False
            st.session_state.confirm_test = False
            st.rerun()

# Handle confirmed state - show success
if st.session_state.get('confirm_test') and st.session_state.get('test_data') and not st.session_state.get('awaiting_confirmation'):
    st.success(f"🎉 Session state works! Data persisted: {st.session_state.test_data}")
    st.balloons()
    
    # Reset for next test
    if st.button("🔄 Reset Test"):
        st.session_state.test_data = None
        st.session_state.confirm_test = False
        st.session_state.awaiting_confirmation = False
        st.rerun()

# Debug info
st.markdown("---")
st.subheader("🔍 Debug Info")
st.markdown(f"**test_data in session state:** `{st.session_state.get('test_data', 'None')}`")
st.markdown(f"**confirm_test flag:** `{st.session_state.get('confirm_test', False)}`")
st.markdown(f"**awaiting_confirmation flag:** `{st.session_state.get('awaiting_confirmation', False)}`")

# ENHANCED DEBUG - Show what the condition evaluates to
confirm_condition = st.session_state.get('confirm_test', False)
data_condition = st.session_state.get('test_data') is not None
awaiting_condition = st.session_state.get('awaiting_confirmation', False)
success_conditions = confirm_condition and data_condition and not awaiting_condition

st.markdown("**🔍 State Machine Check:**")
st.markdown(f"- `test_data` exists: `{data_condition}`")
st.markdown(f"- `awaiting_confirmation`: `{awaiting_condition}`")
st.markdown(f"- `confirm_test` is True: `{confirm_condition}`")
st.markdown(f"- **Success conditions met**: `{success_conditions}`")

# Show current state
if awaiting_condition:
    st.info("📍 Current State: Awaiting Confirmation")
elif success_conditions:
    st.success("📍 Current State: Success (balloons should show above)")
elif data_condition and not confirm_condition:
    st.warning("📍 Current State: Data stored but not confirmed")
else:
    st.info("📍 Current State: Initial state")

# Instructions
st.markdown("---")
st.subheader("📋 Instructions")
st.markdown("""
1. Enter some text in the form above
2. Click "Submit Test"
3. You should see success message and warning
4. Click "Confirm Test" 
5. **Expected:** You should see balloons and "Session state works!" message
6. **If this fails:** There's a session state issue with your Streamlit installation
""")

if st.button("🔄 Clear All Session State"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()