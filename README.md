🚀 AI Communication Assistant (Streamlit Version)

The AI Communication Assistant is a smart platform that helps organizations manage support-related emails end-to-end.
It retrieves incoming emails, analyzes them for sentiment and urgency, generates context-aware draft replies, and presents everything on a Streamlit-powered dashboard.

✨ This project improves:

⚡ Efficiency → automatic prioritization

💬 Response quality → empathetic, professional AI replies

😊 Customer satisfaction → faster, accurate support

🎯 Core Features
📩 1. Email Retrieval & Filtering

✔️ Connects to your inbox via IMAP (Gmail/Outlook)
✔️ Filters only support-related emails (subjects containing: Support, Query, Request, Help)
✔️ Extracts:

Sender

Subject

Body

Date/Time

🧠 2. Categorization & Prioritization

✔️ Sentiment Analysis → Positive / Negative / Neutral
✔️ Priority Detection → Urgent / Not Urgent (keyword-based)
✔️ Urgent emails appear first in dashboard

🤖 3. Context-Aware AI Replies

✔️ Uses OpenAI GPT (if API key provided)
✔️ Draft replies are:

Polite & professional

Context-aware (mentions products/issues)

Empathetic (acknowledges frustration)
✔️ Fallback template used if no API key

🔍 4. Information Extraction

✔️ Pulls contact details (phone, alt. email)
✔️ Detects requirements/requests
✔️ Extracts sentiment indicators
✔️ Highlights products/services mentioned

📤 5. Email Sending

✔️ Draft replies can be reviewed & edited
✔️ Sending via SMTP (Gmail, Outlook, custom)
✔️ Secure with App Passwords

📊 6. Interactive Dashboard (Streamlit)

✔️ Cards → Total, Resolved, Pending, Urgent
✔️ Pie Chart → Sentiment distribution
✔️ Bar Chart → Urgent vs Not Urgent
✔️ Email Table → All emails, details, draft, and send

🛠 Tech Stack

🖥 UI → Streamlit

🔎 NLP → NLTK VADER (sentiment)

🤖 AI → OpenAI GPT API (optional)

🗄 Database → SQLite (SQLAlchemy ORM)

📊 Charts → Plotly

📧 Email → IMAP + SMTP

⚡ Quickstart Guide
1️⃣ Setup Environment
cd app
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt

2️⃣ Configure Environment

Create a .env file in app/:

IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=your_email@gmail.com
IMAP_PASSWORD=your_app_password

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

OPENAI_API_KEY=sk-xxxxxx   # optional


⚠️ Use App Passwords for Gmail/Outlook instead of normal passwords.

3️⃣ Run the App
streamlit run app.py
