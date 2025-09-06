
import os
from textwrap import dedent
from .rag import SimpleRAG
from .nlp import sentiment_label

USE_OPENAI = False
_openai_client = None

def _maybe_openai():
    global USE_OPENAI, _openai_client
    try:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if api_key:
            _openai_client = OpenAI(api_key=api_key)
            USE_OPENAI = True
    except Exception:
        USE_OPENAI = False
    return USE_OPENAI

def build_prompt(email, kb_snippets):
    base = f"""
    You are an empathetic customer support assistant. Write a professional, concise reply.
    Email From: {email.get('from')}
    Subject: {email.get('subject')}
    Body:
    {email.get('body')}

    Detected sentiment: {sentiment_label(email.get('body',''))}

    Use the knowledge base below if relevant. If user is frustrated, acknowledge it gently.
    Knowledge Base:
    """
    for i, snip in enumerate(kb_snippets, 1):
        base += f"\n[{i}] {snip['chunk'][:800]}"
    base += "\n\nWrite a reply that references any relevant policy/product in a friendly tone. Keep it under 160 words."
    return base

def generate_reply(email, rag: SimpleRAG):
    _maybe_openai()
    snippets = rag.top_k(email.get("body","") + " " + (email.get("subject","") or ""), k=2)
    prompt = build_prompt(email, snippets)
    if USE_OPENAI and _openai_client:
        try:
            resp = _openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"system","content":"You are a helpful support assistant."},
                          {"role":"user","content":prompt}],
                temperature=0.4,
                max_tokens=220
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            # fall through to template
            pass
    # Template fallback
    kb_summary = "; ".join([s["chunk"].splitlines()[0] for s in snippets])
    body = email.get("body","")
    sentiment = sentiment_label(body)
    sal = "Hi there"
    if email.get("from"):
        sal = f"Hi {email['from'].split('@')[0].split('.')[0].title()}"
    reply = dedent(f"""
    {sal},

    Thanks for reaching out. I understand you're facing an issue related to "{email.get('subject','')}".
    {"I’m sorry for the frustration this has caused. " if sentiment=="Negative" else ""}
    Here's how we can proceed:
    • {kb_summary or "We'll review your request and assist you promptly."}
    • If this involves account access, please try the password reset again and check spam/junk folders.
    • If billing is involved, we can review the charge and initiate a refund within 14 days if eligible.

    Could you confirm any error messages or screenshots? I’ll prioritize this and keep you updated.

    Best regards,
    Support Team
    """).strip()
    return reply
