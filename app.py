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

# Initialize session state to store chat history for saving
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# --- CUSTOM BACKGROUND CSS ---
st.markdown("""
    <style>
    /* Gradient Background for the entire app */
    .stApp {
        background: linear-gradient(135deg, #0f111a 0%, #171926 50%, #0f111a 100%);
        background-attachment: fixed;
    }
    
    /* Sleek card style for user inputs and responses */
    div.stTextArea textarea {
        background-color: #1e2235 !important;
        color: #ffffff !important;
        border: 1px solid #3d4466 !important;
        border-radius: 8px !important;
    }
    
    /* Customizing buttons */
    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff7676 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.5rem 2rem !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP INTERFACE ---
st.title("⚡ Quick-Solver AI")
st.write("Type your question below, and Gemini will solve it instantly!")

# User input text box
user_query = st.text_area("What can I help you solve today?", placeholder="Type your question or problem here...")

if st.button("Solve It"):
    if user_query.strip() == "":
        st.warning("Please type a question first!")
    else:
        with st.spinner("Analyzing and solving..."):
            try:
                # Call the Gemini 2.5 Flash model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_query,
                )
                
                # Save data to session state
                st.session_state.last_query = user_query
                st.session_state.last_response = response.text
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display answer and save option if available
if st.session_state.last_response:
    st.success("Solution Ready!")
    st.markdown("### 📋 Answer:")
    st.write(st.session_state.last_response)
    
    # Format the text file contents
    chat_download_text = f"--- QUICK-SOLVER AI LOG ---\n\nQUESTION:\n{st.session_state.last_query}\n\nANSWER:\n{st.session_state.last_response}\n"
    
    # Add spacing before the download button
    st.write("")
    
    # Save Chat Download Button
    st.download_button(
        label="📥 Save Chat history",
        data=chat_download_text,
        file_name="quick_solver_chat.txt",
        mime="text/plain"
    )
