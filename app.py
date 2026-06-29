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
    /* Vibrant abstract neon wavy mesh background */
    .stApp {
        background: radial-gradient(circle at 20% 30%, rgba(0, 242, 254, 0.15), transparent 50%),
                    radial-gradient(circle at 80% 70%, rgba(253, 0, 245, 0.15), transparent 50%),
                    linear-gradient(135deg, #0b0d19 0%, #111428 100%);
        background-attachment: fixed;
    }
    
    /* Glowing Neon Titles */
    h1, h2 {
        background: linear-gradient(90deg, #00f2fe, #fd00f5, #ff4b4b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
    }
    
    /* Center Application Main Card Container */
    [data-testid="stVerticalBlock"] > div:has(div.stTextArea) {
        background: rgba(30, 34, 53, 0.75);
        padding: 30px;
        border-radius: 16px;
        border: 2px solid rgba(0, 242, 254, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.15);
        backdrop-filter: blur(8px);
    }
    
    /* Neon Pink Border Input Field Box */
    div.stTextArea textarea {
        background-color: #0b0d19 !important;
        color: #ffffff !important;
        border: 2px solid #fd00f5 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 10px rgba(253, 0, 245, 0.2);
    }
    
    /* Bright Orange/Red Action Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #ff4b2b 0%, #ff416c 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        letter-spacing: 1px;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 0 15px rgba(255, 75, 43, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(255, 75, 43, 0.7);
    }
    
    /* Electric Teal Sidebar Log Out Button */
    .sidebar .stButton > button {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%) !important;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.4);
    }
    
    /* Bright Neon Answer Card Wrapper */
    .answer-box {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1), rgba(253, 0, 245, 0.1));
        border: 2px solid #00f2fe;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
        margin-top: 15px;
    }
    
    /* Dashboard History Cards with Purple Accents */
    .history-card {
        background: rgba(30, 34, 53, 0.9);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #fd00f5;
        border-right: 1px solid rgba(253, 0, 245, 0.2);
        border-top: 1px solid rgba(253, 0, 245, 0.2);
        border-bottom: 1px solid rgba(253, 0, 245, 0.2);
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    /* Customization for Workspace Tabs */
    button[data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: bold !important;
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
                st.warning("Account already exists! Please go to Sign In.")
            else:
                st.session_state.user_db[reg_email] = True
                st.session_state.chat_history[reg_email] = []
                st.success("Registration successful! Go log in.")
                
else:
    # --- LOGGED IN APP INTERFACE ---
    current_user = st.session_state.logged_in_user
    
    # Sidebar design element layout
    with st.sidebar:
        st.markdown("### 👤 Account Panel")
        st.markdown(f"Logged in as: <span style='color: #00f2fe; font-weight: bold;'>{current_user}</span>", unsafe_allow_html=True)
        
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
            for i, item in enumerate(reversed(user_saved_chats)):
                st.markdown(f"""
                <div class="history-card">
                    <strong style="color: #fd00f5;">❓ Q: {item['query'][:35]}...</strong><br>
                    <span style="color: #ffffff; size: 12px;">💡 {item['response'][:55]}...</span>
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
        
        st.write("") # Spacer
        if st.button("SAVE TO DASHBOARD"):
            st.session_state.chat_history[current_user].append({
                "query": st.session_state.current
