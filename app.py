import streamlit as st
import boto3
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.chat_models import BedrockChat

load_dotenv()
VALID_API_KEY = os.getenv("VALID_API_KEY")

# Assume AWS credentials are already configured in your environment
# (via ~/.aws/credentials or environment variables)

# Initialize Bedrock client
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
llm = BedrockChat(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    client=bedrock_client,
    model_kwargs={"temperature": 0.7, "max_tokens": 1024}
)

# Streamlit UI
st.set_page_config(page_title="Enterprise Chat with Bedrock")
st.title("Secure Enterprise Chat (No Backend)")

# API Token Authentication
token = st.text_input("Enter API token", type="password")
if VALID_API_KEY and token != VALID_API_KEY:
    st.error("Invalid API key.")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("You:", key="user_input")

if st.button("Send") and user_input:
    try:
        response = llm.invoke(user_input)
        bot_reply = response.content.strip()

        # Save to chat history
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", bot_reply))

        # Log audit
        with open("chat_audit.log", "a") as log:
            log.write(f"{datetime.utcnow().isoformat()} - Token: {token} - Q: {user_input} - A: {bot_reply}\n")

    except Exception as e:
        st.error(f"Error communicating with Bedrock: {e}")

# Display chat history
for speaker, text in st.session_state.history:
    st.markdown(f"**{speaker}:** {text}")
