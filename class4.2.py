import streamlit as st
from google import genai
from google.genai import types

# Configure system instruction
config = types.GenerateContentConfig(
    system_instruction="""
You are an expert Python developer.

Answer only questions related to Python programming.

For any non-Python question, reply exactly:
Please ask a Python-related question.

Do not answer questions outside the Python domain.
"""
)

# App Title
st.markdown(
    """
    <h1 style='text-align:center;'>🐍 Python AI Assistant</h1>
    <p style='text-align:center; font-size:18px;'>
        Ask any Python programming question.
    </p>
    """,
    unsafe_allow_html=True,
)

# Create Gemini Client
client = genai.Client(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# Create Chat with system instruction
chat = client.chats.create(
    model="gemini-2.5-flash-lite",
    config=config
)

# Placeholder for response
response_placeholder = st.empty()

# User Input
question = st.text_input(
    "",
    placeholder="Enter your Python question here..."
)

# Button
col1, col2, col3 = st.columns([4, 1, 4])

with col2:
    send = st.button("Send")

# Generate Response
if send:
    if question.strip():
        try:
            response = chat.send_message(question)
            response_placeholder.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")
