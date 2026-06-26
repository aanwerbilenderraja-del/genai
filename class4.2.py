import streamlit as st
from google import genai
from google.genai import types

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Python AI Assistant",
    page_icon="🐍",
    layout="centered"
)

# -------------------------------
# API Key Check
# -------------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("""
Google API Key not found!

If you are running locally:
Create a file:
.streamlit/secrets.toml

Add:
GOOGLE_API_KEY = "YOUR_API_KEY"

If you are using Streamlit Cloud:
Go to App Settings → Secrets and add:
GOOGLE_API_KEY = "YOUR_API_KEY"
""")
    st.stop()

# -------------------------------
# Gemini Client
# -------------------------------
client = genai.Client(api_key=api_key)

# -------------------------------
# System Instruction
# -------------------------------
SYSTEM_PROMPT = """
You are an expert Python developer.

Answer only Python programming questions.

If the user asks anything unrelated to Python, reply exactly:

Please ask a Python-related question.
"""

# -------------------------------
# Title
# -------------------------------
st.markdown(
    """
    <h1 style='text-align:center;'>🐍 Python AI Assistant</h1>
    <p style='text-align:center;font-size:18px;'>
    Ask any Python programming question.
    </p>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# User Input
# -------------------------------
question = st.text_input(
    "",
    placeholder="Enter your Python question here..."
)

col1, col2, col3 = st.columns([4, 1, 4])

with col2:
    send = st.button("Send", use_container_width=True)

# -------------------------------
# Generate Response
# -------------------------------
if send:

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=question,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                )
            )

            st.markdown("### Response")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
