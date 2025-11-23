# AI Lead Finder & Email Outreach Agent

An end-to-end Streamlit app that finds journalist/contact details and drafts outreach emails using web search (Serper/Google), simple parsing, and an LLM for social extraction & email drafting.

**Features**
- Input: Journalist/lead name + outlet
- Web search (Serper Google API) to gather result snippets
- Email extraction from text
- LLM-based extraction of social links and outreach email drafting
- Streamlit UI with table and CSV export

**Files**
- `app.py` — main Streamlit app
- `utils.py` — helper functions for search, parsing, and LLM calls
- `requirements.txt` — Python dependencies
- `.env.example` — environment variables example
- `Procfile` — for Heroku deploy (optional)
- `.gitignore` — ignored files
- `LICENSE` — MIT
- `.github/workflows/python-app.yml` — CI template

## Quickstart (local)

1. Clone repo or create new folder and copy files.
2. Create virtual env and install:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt

Enter your own api keys.