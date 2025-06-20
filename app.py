import streamlit as st
import boto3
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.chat_models import BedrockChat


load_dotenv()
VALID_API_KEY = os.getenv("VALID_API_KEY")


st.set_page_config(page_title="Secure Enterprise Chat", layout="centered")
st.title("Secure Enterprise Chat with Bedrock")


with st.sidebar:
    st.header("🔐 Authentication")
    api_key_input = st.text_input("Enter API Key", type="password")
    user_id = st.text_input("User ID", value="anonymous")
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.button("Validate API Key"):
        if api_key_input == VALID_API_KEY:
            st.session_state.authenticated = True
            st.success("API Key is valid.")
        else:
            st.session_state.authenticated = False
            st.error("Invalid API Key.")

if not st.session_state.authenticated:
    st.stop()

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
llm = BedrockChat(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    client=bedrock_client,
    model_kwargs={"temperature": 0.7, "max_tokens": 1024}
)


prompt = st.text_area("Enter your prompt:")


def content_filter(text):
    banned_words = ["kill", "violence", "hate"]
    return not any(word in text.lower() for word in banned_words)


def log_usage(user, query):
    with open("usage_log.txt", "a") as log:
        log.write(f"{datetime.utcnow().isoformat()} - {user}: {query}\n")


if st.button("Generate"):
    if not content_filter(prompt):
        st.warning("Your prompt contains restricted content.")
    else:
        with st.spinner("Generating response..."):
            try:
                response = llm.invoke(prompt)
                log_usage(user_id, prompt)
                st.success("Response:")
                st.markdown(response.content.strip())
            except Exception as e:
                st.error(f"Error generating response: {e}")

with st.sidebar:
    if st.checkbox("Show usage log"):
        try:
            with open("usage_log.txt", "r") as log:
                st.text_area("Usage Log", log.read(), height=200)
        except FileNotFoundError:
            st.info("No logs found yet.")
