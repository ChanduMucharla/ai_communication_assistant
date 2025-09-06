
import re
from datetime import datetime

SUPPORT_TERMS = ["support", "query", "request", "help"]

PRIORITY_KEYWORDS = [
    "immediately", "critical", "urgent", "asap", "cannot access", "blocked", "down", "outage", "audit tomorrow"
]

PHONE_REGEX = r"(\+?\d[\d\-\s]{7,}\d)"
EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

def contains_support_term(subject: str) -> bool:
    if not subject:
        return False
    s = subject.lower()
    return any(term in s for term in SUPPORT_TERMS)

def detect_priority(text: str) -> str:
    text_l = (text or "").lower()
    return "Urgent" if any(k in text_l for k in PRIORITY_KEYWORDS) else "Not urgent"

def extract_contacts(text: str):
    phones = re.findall(PHONE_REGEX, text or "")
    emails = [e for e in re.findall(EMAIL_REGEX, text or "") if not e.lower().endswith("@example.com")]
    return list(set(phones)), list(set(emails))

def extract_product(text: str):
    # naive product extraction
    m = re.search(r"(Product|product)\s*:\s*([A-Za-z0-9\-\s]+)", text or "")
    return m.group(2).strip() if m else None

def parse_date(dt_str: str):
    try:
        return datetime.fromisoformat(dt_str)
    except Exception:
        return datetime.utcnow()
