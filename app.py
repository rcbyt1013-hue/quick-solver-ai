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
    
    /* Customizing the Solve button */
    div.stButton > button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff7676 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.5rem 2rem !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5);
    }
    </style>
    """, unsafe_allowed_html=True)

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
                
                # Display the answer
                st.success("Solution Ready!")
                st.markdown("### 📋 Answer:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
