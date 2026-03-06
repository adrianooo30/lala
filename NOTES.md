Materials (use these as your initial inputs)
1) Madison County Jail inmate roster:
https://www.madisoncountysheriffal.org/inmate-roster
2) Limestone County Jail inmate roster:
https://limestone-al-911.zuercherportal.com/#/inmates
3) Attached PDF templates to test your extraction + document-type detection:
- PDF_Template_A_Booking_Summary_FILLED.pdf
- PDF_Template_B_Court_Docket_Notice_FILLED.pdf
- PDF_Template_C_Crash_Report_FILLED.pdf

Note: During review we may utilize additional PDFs to ensure your pipeline handles multiple document formats.

What you'll build
1) Scrape the provided rosters
- Scrape the sites above.
- Extract inmate names and the associated photo(s) (and any helpful identifiers available).
- Store results in a structured format for matching later.

2) Parse PDFs and isolate names
- Extract text from the PDFs.
- Identify and normalize the names found in each document.

3) Match PDF names to scraped roster entries
- Compare names found in PDFs to names from the scraped rosters.
- If a match is found, flag it for review.

4) Web app for review
- Display extracted PDF text (or relevant sections).
- Highlight matched names in the document view.
- Show the matched roster photos) next to the matching name(s).

5) Email notification (Google/Gmail configuration)
- Add an email notification feature.
- Your app should support a Google/Gmail configuration (document your approach clearly).
- When a match is found, send an alert email with the match details.

6) Document type detection + template identification (OpenAl)
- Assume we will send different document types/templates.
- Use an OpenAl API key to classify the document type/template.
- Include your prompting approach and how you handle uncertainty (e.g., low confidence, missing fields).
 
Implementation notes (recommended)
- These roster pages may be dynamic. We recommend using Playwright.
- Feel free to use Cursor, Claude Code, Codex, or any other agentic/dev tooling you prefer-just document what you used and why.

Secure handling of API keys & secrets (required)
- Do not hardcode secrets or commit them to the repo.
- Use environment variables (preferred) and include a .env.example with placeholder values.
- Avoid logging sensitive values (AP| keys, Auth tokens, refresh tokens).
- Your README should list required environment variables and setup steps.

What to submit
- A repo link or zipped project folder
- A README that covers:
- How to run the scraper + matching pipeline
- How to run the web app
- How to configure email notifications (Google/Gmail)
- How to set environment variables (including OpenAl key) securely
- Assumptions, limitations, and what you'd improve with more time (Optional) A short screen recording showing the end-to-end flow.