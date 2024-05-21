import os
import json
import requests
import streamlit as st
from config import AGENT_API_URL, AGENT_PROJECT_DIR

test_cases_dir = os.path.join(AGENT_PROJECT_DIR, "auto_test")
SESSION_RECORDS_FILE = os.path.join(test_cases_dir, "session_records.json")

# Read JSON file
with open(SESSION_RECORDS_FILE, 'r', encoding='utf-8') as f:
    conversation_data = json.load(f)

# Streamlit app
st.title("Test State Route of the Agent")

def get_bg_color(session_valid):
    return "lightgreen" if session_valid else "lightcoral"

# Initialize session state to store results
if "session_results" not in st.session_state:
    st.session_state.session_results = [None] * len(conversation_data)

# Button to check all sessions
if st.button("Check All Sessions"):
    session_validity = []

    # Process each session
    for i, session in enumerate(conversation_data):
        session_valid = True
        user_queries = []
        expected_state_path = []
        state_path = []

        # Collect user queries and assistant responses
        for record in session:
            if record['role'] == 'user':
                user_queries.append(record['content'])
            elif record['role'] == 'assistant':
                expected_state_path.append(record['content'].get('state', None))

        # Perform API calls and compare results
        for user_query in user_queries:
            payload = {
                "session_id": f"{i+1}",
                "user_input": user_query
            }
            response = requests.post(AGENT_API_URL, json=payload).json()
            actual_state = response.get('additional_info', {}).get('state', '')
            state_path.append(actual_state)

        if expected_state_path != state_path:
            session_valid = False
        
        session_validity.append(session_valid)
        
        # Determine background color
        bg_color = get_bg_color(session_valid)
        
        # Prepare session details with appropriate background color
        html_content = f"""
        <div style="border: 3px solid {bg_color}; padding: 10px; margin-bottom: 10px; border-radius: 12px;">
            <span>用户 Queries:</span>
        """
        for round, user_query in enumerate(user_queries, start=1):
            html_content += f"<li>用户 Round {round}: {user_query}</li>"
        
        html_content += f"""
            <p style="font-weight: bold;">State Path: {' -> '.join(state_path)}</p>
        </div>
        """
        
        # Update session state with the results
        st.session_state.session_results[i] = {
            "valid": session_valid,
            "html_content": html_content
        }

# Display user queries and session details
for i, session in enumerate(conversation_data):
    user_queries = [record['content'] for record in session if record['role'] == 'user']
    
    if st.session_state.session_results[i] is None:
        with st.expander(f"Session {i+1}"):
            st.markdown("**User Queries:**")
            for round, user_query in enumerate(user_queries, start=1):
                st.markdown(f"- **Round {round}:** {user_query}")
    else:
        result = st.session_state.session_results[i]
        if result["valid"]:
            with st.expander(f"Session {i+1}"):
                st.markdown(result["html_content"], unsafe_allow_html=True)
        else:
            with st.expander(f"Session {i+1}", expanded=True):
                st.markdown(result["html_content"], unsafe_allow_html=True)
