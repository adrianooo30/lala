# Inmate Roster Matching System

## Overview

This application scrapes county jail rosters, parses legal PDFs using OpenAI to classify document types and extract subjective names, and matches them against the scraped database. It provides a Streamlit web interface for review and sends an email alert when a fuzzy match is detected.

## Prerequisites

- **Python 3.9+**
- **Google Account** (for Gmail SMTP app password)
- **OpenAI API Key**

## Installation & Setup

1. **Clone or Download the Project Folder** (where this README resides).
2. **Create a Virtual Environment & Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   playwright install
   ```
3. **Initialize the SQLite Database**:
   ```bash
   python database.py
   ```

## Configuring Environment Variables

Do **not** hardcode secrets. This project uses python-dotenv to load environment variables.

1. Copy the example `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and configure your credentials:
   - `OPENAI_API_KEY`: Your key starting with `sk-...`
   - `GMAIL_USER`: The sender/recipient email address (e.g., `youremail@gmail.com`)
   - `GMAIL_APP_PASSWORD`: Since Google disabled basic auth, you must generate an [App Password](https://myaccount.google.com/apppasswords) and paste the 16-character code here.

## How to Run the Pipeline

### 1. Web Scrapers

To populate the database with live roster data:
```bash
python scraper_madison.py
python scraper_limestone.py
```

*Note on Scrapers*: Both Madison and Limestone county portals may utilize dynamic anti-bot protections (like Cloudflare or SPA dynamic rendering). If the scrapers fail to extract data on your network (e.g. returning 403 or empty elements), the pipeline includes a fallback seed script to inject the names from the provided PDF templates into the database so you can still test the matching logic.

**Fallback:**
```bash
python seed_mock_data.py
```

### 2. Review Web App

To launch the interactive dashboard:
```bash
streamlit run app.py
```
This will open a browser window typically at `http://localhost:8501`.

### 3. Usage Flow
- **Sidebar**: You can trigger the scrapers or inject the mock data directly from the UI.
- **Main View**: Upload a PDF (e.g. `PDF_Template_C_Crash_Report_FILLED.pdf`).
- The app will extract the full text using PyMuPDF.
- It will ping OpenAI to identify the document type *without regarding file extension* (e.g. determining it is a "Crash Report") and extract standard normalized names.
- It will then perform fuzzy matching against the SQLite database using `thefuzz`.
- If a match is found, it will automatically send an email alert via your Gmail settings and display the match side-by-side with the highlighted PDF text context.

## Assumptions & Limitations
- **Scraping Protections**: The scraper heuristic relies on standard `.inmate-card` and table row (`tr`) structures. If Cloudflare outright blocks the request (common for AWS IPs or certain regions), the scraper will fail gracefully. The fallback script mitigates this for testing.
- **OpenAI Extraction**: Strict JSON structured output via Pydantic is utilized using `<gpt-4o>`, assuring robust and unified naming conventions (FIRST LAST) even when names are unstructured in the PDF template.
- **Matching Quality**: Fuzzy name matching is used with a threshold of 75/100 to handle minor misspellings. Highly common names ("John Doe") might require secondary identifier matching (e.g. DOB) which is extracted if present but relies on consistent scraper availability. With more time, secondary key matching (DOB, Age) should be implemented uniformly.
