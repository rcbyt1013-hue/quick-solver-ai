import streamlit as st
import os
from google import genai

# App configuration
st.set_page_config(page_title="Quick-Solver AI", page_icon="⚡", layout="centered")

# --- INITIALIZE DATABASE SIMULATION ---
if "user_db" not in st.session_state:
    st.session_state.user_db = {} 

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {} 

if "current_response" not in st.session_state:
    st.session_state.current_response = ""
if "current_query" not in st.session_state:
    st.session_state.current_query = ""

# --- ULTRA-VIBRANT NEON DESIGN CSS ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 20% 30%, rgba(0, 242, 254, 0.15), transparent 50%),
                    radial-gradient(circle at 80% 70%, rgba(253, 0, 245, 0.15), transparent 50%),
                    linear-gradient(135deg, #0b0d19 0%, #111428 100%);
        background-attachment: fixed;
    }
    h1, h2 {
        background: linear-gradient(90deg, #00f2fe, #fd00f5, #ff4b4b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
    }
    div.stTextArea textarea, div.stTextInput input {
        background-color: #0b0d19 !important;
        color: #ffffff !important;
        border: 2px solid #fd00f5 !important;
        border-radius: 10px !important;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #ff4b2b 0%, #ff416c 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        width: 100%;
    }
    .answer-box {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1), rgba(253, 0, 245, 0.1));
        border: 2px solid #00f2fe;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
    }
    .history-card {
        background: rgba(30, 34, 53, 0.9);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #fd00f5;
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AUTHENTICATION INTERFACE ---
if st.session_state.logged_in_user is None:
    st.markdown("<h1 style='text-align: center;'>🔐 Quick-Solver AI Gateway</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center; color: #8a99ad;'>Please sign in or register with your email to access the neon interface.</p>", unsafe_allow_html=True)
    
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
                st.warning("Account already exists!")
            else:
                st.session_state.user_db[reg_email] = True
                st.session_state.chat_history[reg_email] = []
                st.success("Registration successful! Go log in.")
                
else:
    # --- LOGGED IN APP INTERFACE ---
    current_user = st.session_state.logged_in_user
    
    with st.sidebar:
        st.markdown("### 👤 Account Panel")
        st.markdown(f"Logged in as: <span style='color: #00f2fe; font-weight: bold;'>{current_user}</span>", unsafe_allow_html=True)
        
        # ONSCREEN KEY BACKUP INPUT
        st.write("---")
        st.markdown("### 🔑 API Key Override")
        custom_key = st.text_input("Paste Fresh API Key Here", type="password")
        
        st.write("---")
        if st.button("Door Log Out"):
            st.session_state.logged_in_user = None
            st.session_state.current_response = ""
            st.session_state.current_query = ""
            st.rerun()
            
        st.write("---")
        st.markdown("### 📚 Saved Dashboard Chats")
        
        user_saved_chats = st.session_state.chat_history.get(current_user, [])
        if not user_saved_chats:
            st.info("No saved solutions yet.")
        else:
            for item in reversed(user_saved_chats):
                st.markdown(f"""
                <div class="history-card">
                    <strong style="color: #fd00f5;">❓ Q: {item['query'][:35]}...</strong><br>
                    <span style="color: #ffffff;">💡 {item['response'][:55]}...</span>
                </div>
                """, unsafe_allow_html=True)

    # Main dashboard application area
    st.markdown("<h1>⚡ Quick-Solver AI</h1>", unsafe_allow_html=True)
    st.write("Type your question below, analyze the solution, and archive it to your account.")
    
    user_query = st.text_area("What can I help you solve today?", placeholder="Type your question or problem here...")
    
    if st.button("SOLVE IT"):
        if user_query.strip() == "":
            st.warning("Please type a question first!")
        else:
            with st.spinner("Analyzing and solving..."):
                try:
                    # Select the correct key: Custom manual key first, environment secret second
                    final_key = custom_key.strip() if custom_key.strip() else os.environ.get("GEMINI_API_KEY")
                    
                    if not final_key:
                        st.error("No API key detected. Please add it to Secrets or paste it in the sidebar box.")
                    else:
                        client = genai.Client(api_key=final_key)
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=user_query,
                        )
                        st.session_state.current_query = user_query
                        st.session_state.current_response = response.text
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Render Active Response Container
    if st.session_state.current_response:
        st.markdown("""
            <div class="answer-box">
                <h3 style="margin-top:0; color:#00f2fe;">✨ Solution Ready!</h3>
            </div>
        """, unsafe_allow_html=True)
        st.write(st.session_state.current_response)
        
        st.write("") 
        if st.button("SAVE TO DASHBOARD"):
            st.session_state.chat_history[current_user].append({
                "query": st.session_state.current_query,
                "response": st.session_state.current_response
            })
            st.toast("Saved to your dashboard panel history!", icon="🔥")
            st.session_state.current_response = ""
            st.session_state.current_query = ""
            st.rerun()
