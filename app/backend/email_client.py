
import os, imaplib, email, smtplib, ssl, json
from email.message import EmailMessage
from datetime import datetime
from typing import List, Dict

FILTER_TERMS = ["support","query","request","help"]

def _env(k, default=""):
    return os.getenv(k, default).strip()

def can_use_live():
    return all(_env(k) for k in ["IMAP_HOST","IMAP_PORT","IMAP_USER","IMAP_PASSWORD","SMTP_HOST","SMTP_PORT","SMTP_USER","SMTP_PASSWORD"])

def fetch_demo_emails(path: str) -> List[Dict]:
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return data
    except Exception:
        return []

def fetch_imap(max_count=50) -> List[Dict]:
    host = _env("IMAP_HOST")
    user = _env("IMAP_USER")
    pw = _env("IMAP_PASSWORD")
    port = int(_env("IMAP_PORT","993") or "993")
    mails = []
    M = imaplib.IMAP4_SSL(host, port)
    M.login(user, pw)
    M.select("INBOX")
    # Search last N
    typ, data = M.search(None, "ALL")
    ids = data[0].split()[-max_count:]
    for i in reversed(ids):
        typ, msg_data = M.fetch(i, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subj = msg.get("Subject","")
                from_ = msg.get("From","")
                date_ = msg.get("Date","")
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        if ctype == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore") if msg.get_content_charset() else msg.get_payload()
                mails.append({
                    "from": from_,
                    "subject": subj,
                    "body": body,
                    "date": date_ if date_ else datetime.utcnow().isoformat(sep=" ")
                })
    M.logout()
    return mails

def send_email(to_addr: str, subject: str, body: str):
    host = _env("SMTP_HOST")
    port = int(_env("SMTP_PORT","587") or "587")
    user = _env("SMTP_USER")
    pw = _env("SMTP_PASSWORD")
    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP(host, port) as server:
        server.starttls(context=context)
        server.login(user, pw)
        server.send_message(msg)
