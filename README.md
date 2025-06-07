# Secure Enterprise Chat using Amazon Bedrock

This is a simple Streamlit-based enterprise chat application powered by **Amazon Bedrock** and **Claude 3** via the `langchain_community` integration.

## ✨ Features

- Streamlit chat interface
- Amazon Bedrock (Claude 3 Sonnet) for LLM
- API token-based user authentication
- Simple local logging (`chat_audit.log`)
- `.env` support for managing credentials securely

## 🧰 Setup

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
pip install -r requirements.txt
```

### 2. Set up your `.env` file

Copy and configure the `.env.example` file:

```bash
cp .env.example .env
```

Update it with a secure token and your AWS credentials (or use IAM roles if hosted on AWS).

### 3. Run the app

```bash
streamlit run streamlit_bedrock_chat.py
```

## 🛡️ Security Notes

- This example uses environment variables for AWS credentials. In production, prefer IAM roles and do **not** hardcode keys.
- Token validation is simple string matching. For real systems, use Cognito or other identity providers.

## 🗃️ Files

- `streamlit_bedrock_chat.py`: main application
- `.env.example`: example environment variable setup
- `requirements.txt`: dependencies
- `chat_audit.log`: local audit log (created at runtime)

