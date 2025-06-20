import os
from utils import content_filter, log_usage

def test_content_filter_passes_clean_prompt():
    assert content_filter("How are you?") is True

def test_content_filter_blocks_banned_word():
    assert content_filter("What drugs should I take?") is False

def test_log_usage_creates_log(tmp_path):
    log_path = tmp_path / "test_log.txt"
    log_usage("testuser", "sample query", str(log_path))
    with open(log_path) as f:
        content = f.read()
    assert "testuser" in content
    assert "sample query" in content
