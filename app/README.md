# AI-Powered Communication Assistant (Streamlit)

A fully working Streamlit app that fetches support emails (IMAP demo or live), prioritizes them,
extracts key info, generates AI responses (OpenAI optional), and displays a clean dashboard with
cards and charts (pie + bar).

## Quick Start

```bash
# 1) Create & activate a virtual environment (recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install requirements
pip install -r app/requirements.txt

# 3) (Optional) Configure live email + OpenAI
cp app/.env.example app/.env
# Edit app/.env with your IMAP/SMTP + OPENAI_API_KEY

# 4) Run the app
streamlit run app/app.py
```

The app will default to **Demo Mode** (using sample emails) unless valid IMAP/SMTP credentials are provided.

## Features
- Email Retrieval (IMAP) + Demo Mode
- Filtering by Subject: Support, Query, Request, Help
- Sentiment Analysis (VADER) + Priority (keyword-based + heuristics)
- Information Extraction: phone, alt email, product, sentiment keywords
- Priority queue (urgent first) in processing and display
- RAG-lite using TF-IDF over local `/app/kb/*.md`
- AI Responses via OpenAI (if API key present) or smart template fallback
- Dashboard with KPIs + pie & bar charts
- Review/edit AI drafts and send via SMTP

## Tech
- Streamlit, SQLAlchemy (SQLite), scikit-learn (TF-IDF), NLTK VADER, OpenAI (optional)

## Notes
- On first run, VADER lexicon is downloaded automatically.
- If IMAP login fails, the app switches to Demo Mode.
- Demo emails: `app/data/sample_emails.json`
- Knowledge base: `app/kb/*.md` – add your docs here to improve answers.

## Security
- Use an app-specific password for Gmail/IMAP/SMTP.
- `.env` is optional and read by `python-dotenv`. Do **not** commit secrets.

## License
MIT
