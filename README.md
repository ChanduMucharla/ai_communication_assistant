📧 AI Communication Assistant (Streamlit Version)

The AI Communication Assistant is a smart platform that helps organizations manage support-related emails end-to-end.
It retrieves incoming emails, analyzes them for sentiment and urgency, generates context-aware draft replies, and presents everything on a Streamlit-powered dashboard.

This improves:

⚡ Efficiency (automatic prioritization)

💬 Response quality (empathetic, professional AI replies)

😊 Customer satisfaction

🚀 Features
1. Email Retrieval & Filtering

Connects to your email inbox (via IMAP/Gmail/Outlook APIs).

Filters only support-related emails (subjects containing: Support, Query, Request, Help).

Extracts key details:

Sender email

Subject

Body

Date/time received

2. Categorization & Prioritization

Sentiment Analysis using NLTK VADER:

Positive / Negative / Neutral

Priority Detection based on keywords:

Urgent (e.g., "immediately", "critical", "cannot access")

Not Urgent

Urgent emails appear first in the dashboard (priority queue).

3. Context-Aware AI Replies

Uses OpenAI GPT models (if API key provided) to generate draft responses.

Draft replies are:

Professional & empathetic

Context-aware (mentions products, acknowledges frustration, etc.)

If OpenAI key is missing → fallback template-based reply.

Drafts are shown in the dashboard before sending.

4. Information Extraction

From each email, the assistant extracts:

Contact details (phone numbers, alternate emails)

Customer requirements or requests

Sentiment indicators (positive / negative words)

Product or service mentioned

This structured info is displayed alongside raw emails.

5. Email Sending

Draft replies can be edited before sending.

Sending uses SMTP with secure login.

Supports Gmail, Outlook, and custom SMTP servers.

6. Dashboard (Streamlit)

A clean, interactive dashboard showing:

📊 Cards: Total emails, Resolved, Pending, Urgent

🥧 Pie Chart: Sentiment distribution

📊 Bar Chart: Urgent vs Not Urgent

📋 Email Table: Each email with details, draft reply button, and send option

🛠️ Tech Stack

UI: Streamlit

ML/NLP: NLTK (sentiment), keyword-based priority detection

AI: OpenAI GPT API (optional)

DB: SQLite (via SQLAlchemy)

Charts: Plotly (integrated in Streamlit)

Email: IMAP for reading, SMTP for sending
