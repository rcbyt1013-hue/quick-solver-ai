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