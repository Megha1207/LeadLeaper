# LeadLeaper - AI Lead Finder & Email Outreach Agent

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

<img width="1916" height="663" alt="image" src="https://github.com/user-attachments/assets/9c3ddc33-f051-40b8-82c9-e3a4008cb79f" />
<img width="1895" height="833" alt="image" src="https://github.com/user-attachments/assets/863733f7-1293-4fbd-a312-4e353e0b32a4" />
<img width="1856" height="618" alt="image" src="https://github.com/user-attachments/assets/cd4db5a8-8835-4204-95b6-d7a221c23f9a" />
<img width="1806" height="662" alt="image" src="https://github.com/user-attachments/assets/5df9361b-5068-49fa-9c9c-69b1e2d62cf7" />



