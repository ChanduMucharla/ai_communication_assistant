
import os, sys, json
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)

import streamlit as st
import pandas as pd
from datetime import datetime
from backend import utils
from backend.utils import contains_support_term, detect_priority, extract_contacts, extract_product, parse_date
from backend.nlp import sentiment_label
from backend.rag import SimpleRAG
from backend.responder import generate_reply
from backend.db import init_db, SessionLocal, Email, Response
from backend.email_client import can_use_live, fetch_demo_emails, fetch_imap, send_email

st.set_page_config(page_title="AI Communication Assistant", layout="wide")

# Init DB and RAG
init_db()
rag = SimpleRAG(kb_dir=os.path.join(os.path.dirname(__file__), "kb"))
session = SessionLocal()

# Sidebar
st.sidebar.title("Settings")
mode = "Live IMAP" if can_use_live() else "Demo Mode"
st.sidebar.write(f"Mode: **{mode}**")
if st.sidebar.button("Fetch Emails Now"):
    if can_use_live():
        try:
            emails = fetch_imap(max_count=50)
        except Exception as e:
            st.sidebar.error(f"IMAP failed: {e}. Using Demo.")
            emails = fetch_demo_emails(os.path.join(os.path.dirname(__file__), "data", "sample_emails.json"))
    else:
        emails = fetch_demo_emails(os.path.join(os.path.dirname(__file__), "data", "sample_emails.json"))

    # Filter by subject terms
    filtered = [m for m in emails if contains_support_term(m.get("subject","").lower())]
    # Persist to DB (avoid duplicates by subject+from+date hash)
    for m in filtered:
        body = m.get("body","")
        phones, alts = extract_contacts(body)
        sentiment = sentiment_label(body)
        priority = detect_priority(m.get("subject","") + " " + body)
        product = extract_product(body)
        rec_at = parse_date(m.get("date",""))
        # Save
        e = Email(
            sender=m.get("from",""),
            subject=m.get("subject",""),
            body=body,
            received_at=rec_at,
            sentiment=sentiment,
            priority=priority,
            phone=", ".join(phones),
            alt_email=", ".join(alts),
            product=product or ""
        )
        session.add(e)
    session.commit()
    st.sidebar.success(f"Fetched & stored {len(filtered)} support emails.")

st.title("📧 AI-Powered Communication Assistant")

# KPIs
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    total_24 = session.query(Email).count()
    resolved = session.query(Email).filter(Email.resolved==True).count()
    pending = total_24 - resolved
    urgent_cnt = session.query(Email).filter(Email.priority=="Urgent").count()
    col1.metric("Total Emails", total_24)
    col2.metric("Resolved", resolved)
    col3.metric("Pending", pending)
    col4.metric("Urgent", urgent_cnt)

# Charts
df = pd.read_sql("SELECT * FROM emails", session.bind)
if not df.empty:
    colA, colB = st.columns(2)
    with colA:
        st.subheader("Sentiment Distribution")
        pie_df = df.groupby("sentiment").size().reset_index(name="count")
        st.plotly_chart({
            "data": [{
                "type": "pie",
                "labels": pie_df["sentiment"],
                "values": pie_df["count"]
            }],
            "layout": {"height": 350}
        }, use_container_width=True)
    with colB:
        st.subheader("Priority (Bar)")
        bar_df = df.groupby("priority").size().reset_index(name="count")
        st.plotly_chart({
            "data": [{
                "type": "bar",
                "x": bar_df["priority"],
                "y": bar_df["count"]
            }],
            "layout": {"height": 350}
        }, use_container_width=True)

st.subheader("Filtered Support Emails")
# Priority queue ordering: urgent first, then newest
df = pd.read_sql("SELECT * FROM emails ORDER BY CASE WHEN priority='Urgent' THEN 0 ELSE 1 END, received_at DESC", session.bind)
st.dataframe(df[["id","sender","subject","received_at","sentiment","priority","phone","alt_email","product"]], use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("Process & Respond")

selected_id = st.selectbox("Choose an email ID to draft a response:", options=df["id"].tolist() if not df.empty else [])
if selected_id:
    e = session.query(Email).filter(Email.id==int(selected_id)).first()
    if e:
        st.write(f"**From:** {e.sender}  \n**Subject:** {e.subject}  \n**Received:** {e.received_at}")
        with st.expander("Show Email Body"):
            st.code(e.body or "", language="markdown")
        with st.expander("Extracted Info"):
            st.write({
                "Phone(s)": e.phone,
                "Alternate Email(s)": e.alt_email,
                "Product": e.product,
                "Sentiment": e.sentiment,
                "Priority": e.priority
            })

        if st.button("Generate AI Draft (Urgent first)"):
            # No background queue; we simply generate immediately.
            draft = generate_reply(
                {
                    "from": e.sender, "subject": e.subject, "body": e.body
                },
                rag
            )
            r = Response(email_id=e.id, draft=draft, sent=False)
            session.add(r)
            session.commit()
            st.success("Draft generated and saved.")

        # Show latest draft if any
        r = session.query(Response).filter(Response.email_id==e.id).order_by(Response.id.desc()).first()
        if r:
            new_draft = st.text_area("AI Draft (editable)", value=r.draft, height=220)
            colx, coly, colz = st.columns(3)
            with colx:
                if st.button("Save Draft"):
                    r.draft = new_draft
                    session.commit()
                    st.success("Draft saved.")
            with coly:
                if st.button("Mark as Resolved"):
                    e.resolved = True
                    session.commit()
                    st.success("Email marked as resolved.")
            with colz:
                if st.button("Send Email Now"):
                    try:
                        if e.sender and "@" in e.sender:
                            send_email(e.sender, f"Re: {e.subject}", new_draft)
                            r.sent = True
                            r.sent_at = datetime.utcnow()
                            e.resolved = True
                            session.commit()
                            st.success("Email sent via SMTP.")
                        else:
                            st.error("Invalid recipient email address.")
                    except Exception as ex:
                        st.error(f"Failed to send: {ex}")
else:
    st.info("Use the sidebar to fetch emails, then select one above to generate a draft.")
