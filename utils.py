from datetime import datetime

def content_filter(text):
    banned_words = ["drugs", "violence", "hate"]
    return not any(word in text.lower() for word in banned_words)

def log_usage(user, query, log_path="usage_log.txt"):
    with open(log_path, "a") as log:
        log.write(f"{datetime.utcnow().isoformat()} - {user}: {query}\n")
