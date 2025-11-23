# utils.py — helper functions (Groq version)
import os
import requests
import re
import json
from typing import List, Dict

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


# -------- Serper search --------

def search_serper(query: str) -> Dict:
    """Search using Serper's Google API. Returns JSON response or empty dict on failure."""
    if not SERPER_API_KEY:
        raise EnvironmentError("SERPER_API_KEY not set in environment")

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 10}

    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    if resp.status_code != 200:
        return {}

    return resp.json()

# -------- Email extraction --------

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def extract_emails_from_text(text: str) -> List[str]:
    if not text:
        return []
    found = EMAIL_RE.findall(text)
    cleaned = [e.strip(".,;:'\" ") for e in found]
    return list(dict.fromkeys(cleaned))

# -------- Groq LLM helpers --------

def call_groq_chat(messages: List[Dict]) -> str:
    """Minimal Groq chat completion wrapper."""
    if not GROQ_API_KEY:
        raise EnvironmentError("GROQ_API_KEY not set in environment")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 600,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Groq API error {resp.status_code}: {resp.text}")

    data = resp.json()
    return data["choices"][0]["message"]["content"]

def llm_extract_socials(text: str) -> Dict:
    """Ask LLM to extract LinkedIn, Twitter/X, Instagram."""
    prompt = (
        "Extract any social media links or usernames from the text. "
        "Return ONLY valid JSON with keys: linkedin, twitter, instagram.\n\n"
        f"Text:\n{text}"
    )

    messages = [{"role": "user", "content": prompt}]
    raw = call_groq_chat(messages)

    # JSON parsing fallback
    try:
        return json.loads(raw)
    except:
        obj = {"linkedin": "", "twitter": "", "instagram": ""}
        lk = re.search(r"https?://(www\.)?linkedin\.com/[A-Za-z0-9_/\-]+", text)
        if lk: obj["linkedin"] = lk.group(0)
        tx = re.search(r"https?://(www\.)?twitter\.com/[A-Za-z0-9_\-]+", text)
        if tx: obj["twitter"] = tx.group(0)
        ig = re.search(r"https?://(www\.)?instagram\.com/[A-Za-z0-9_\-]+", text)
        if ig: obj["instagram"] = ig.group(0)
        return obj

def llm_generate_email(name: str, outlet: str, emails: list, socials: dict) -> str:
    """Generate a short PR outreach email via Groq."""
    to_field = f"{name} at {outlet}" if outlet else name

    context = (
        f"Write a short, friendly PR outreach email to {to_field}.\n"
        f"Emails found: {emails}\n"
        f"Socials: {json.dumps(socials)}\n"
        "Return subject line, then body. Keep it 4-7 sentences."
    )

    messages = [{"role": "user", "content": context}]
    return call_groq_chat(messages)
