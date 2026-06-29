import streamlit as st
import os
from google import genai

# Fetch the API key safely from environment variables
api_key = os.environ.get("GEMINI_API_KEY")

# Initialize the Gemini client
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.error("Missing GEMINI_API_KEY. Please add it to your secrets/environment variables.")
    st.stop()

# App configuration
st.set_page_config(page_title="Quick-Solver AI", page_icon="⚡", layout="centered")

# --- INITIALIZE DATABASE SIMULATION ---
if "user_db" not in st.session_state:
    # A local dictionary simulating a user database
    st.session_state.user_db = {} 

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {} # Format: {email: [list of chats]}

if "current_response" not in st.session_state:
    st.session_state.current_response = ""
if "current_query" not in st.session_state:
    st.session_state.current_query = ""

# --- CUSTOM DESIGN CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f111a 0%, #171926 50%, #0f111a 100%);
        background-attachment: fixed;
    }
    div.stTextArea textarea {
        background-color: #1e2235 !important;
        color: #ffffff !important;
        border: 1px solid #3d4466 !important;
        border-radius: 8px !important;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff7676 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        width: 100%;
    }
    .history-card {
        background-color: #1e2235;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION INTERFACE ---
if st.session_state.logged_in_user is None:
    st.title("🔐 Quick-Solver AI Gateway")
    st.write("Please sign in or register with your email to start solving.")
    
    tab1, tab2 = st.tabs(["📧 Sign In", "📝 Register New Account"])
    
    with tab1:
        login_email = st.text_input("Email Address", key="login_email_input").strip().lower()
        if st.button("Log In"):
            if login_email in st.session_state.user_db:
                st.session_state.logged_in_user = login_email
                st.rerun()
            else:
                st.error("Email not found. Please register first!")
                
    with tab2:
        reg_email = st.text_input("Email Address", key="reg_email_input").strip().lower()
        if st.button("Create Account"):
            if reg_email == "":
                st.warning("Email cannot be empty.")
            elif reg_email in st.session_state.user_db:
                st.warning("Account already exists! Please go to Sign In.")
            else:
                st.session_state.user_db[reg_email] = True
                st.session_state.chat_history[reg_email] = []
                st.success("Registration successful! You can now switch tabs and Log In.")
                
else:
    # --- LOGGED IN APP INTERFACE ---
    current_user = st.session_state.logged_in_user
    
    # Sidebar layout for Profile & Chat History
    with st.sidebar:
        st.markdown(f"### 👤 Logged in as:\n`{current_user}`")
        if st.button("🚪 Log Out"):
            st.session_state.logged_in_user = None
            st.session_state.current_response = ""
            st.session_state.current_query = ""
            st.rerun()
            
        st.write("---")
        st.markdown("### 📚 Saved Dashboard Chats")
        
        # Display saved records
        user_saved_chats = st.session_state.chat_history.get(current_user, [])
        if not user_saved_chats:
            st.info("No saved solutions yet.")
        else:
            for i, item in enumerate(reversed(user_saved_chats)):
                st.markdown(f"""
                <div class="history-card">
                    <strong>❓ Q: {item['query'][:30]}...</strong><br>
                    <small>💡 {item['response'][:50]}...</small>
                </div>
                """, unsafe_allow_html=True)

    # Main dashboard application area
    st.title("⚡ Quick-Solver AI")
    st.write("Type your query below, analyze the solution, and archive it to your account.")
    
    user_query = st.text_area("What can I help you solve today?", placeholder="Type your question here...")
    
    if st.button("Solve It"):
        if user_query.strip() == "":
            st.warning("Please type a question first!")
        else:
            with st.spinner("Analyzing and solving..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_query,
                    )
                    st.session_state.current_query = user_query
                    st.session_state.current_response = response.text
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Render Active Response & Save Dashboard Mechanics
    if st.session_state.current_response:
        st.success("Solution Ready!")
        st.markdown("### 📋 Answer:")
        st.write(st.session_state.current_response)
        
        if st.button("💾 Save to Dashboard"):
            # Append to user data map
            st.session_state.chat_history[current_user].append({
                "query": st.session_state.current_query,
                "response": st.session_state.current_response
            })
            st.toast("Saved successfully to your sidebar history!", icon="🚀")
            # Clear current panel selection
            st.session_state.current_response = ""
            st.session_state.current_query = ""
            st.rerun()
