import streamlit as st
import os
import subprocess
from pdf_processor import extract_text_from_pdf, process_pdf_with_openai
from matcher import find_matches_in_db
from database import SessionLocal, Inmate, Match
import re

st.set_page_config(page_title="Inmate Matcher", layout="wide")

st.title("Inmate Roster Matcher Pipeline")

with st.sidebar:
    st.header("Actions")
    if st.button("Run Scrapers (Live)"):
        with st.spinner("Scraping Madison County..."):
            subprocess.run(["python3", "scraper_madison.py"])
        with st.spinner("Scraping Limestone County..."):
            subprocess.run(["python3", "scraper_limestone.py"])
        st.success("Scraping completed (Check terminal logs for Cloudflare issues)")
        
    if st.button("Seed Mock Data (Fallback)"):
        with st.spinner("Seeding database..."):
            subprocess.run(["python3", "seed_mock_data.py"])
        st.success("Test dataset injected!")
        
    st.markdown("---")
    st.subheader("Database Stats")
    session = SessionLocal()
    inmates_count = session.query(Inmate).count()
    matches_count = session.query(Match).count()
    st.write(f"Inmates currently in DB: **{inmates_count}**")
    st.write(f"Matches logged: **{matches_count}**")

uploaded_file = st.file_uploader("Upload Legal Document (PDF) here", type=['pdf'])

if uploaded_file is not None:
    # Save uploaded file temporarily
    temp_pdf = f"temp_{uploaded_file.name}"
    with open(temp_pdf, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.subheader("1. Extracting Text from PDF")
    raw_text = extract_text_from_pdf(temp_pdf)
    
    with st.expander("View Raw PDF Text"):
        st.text(raw_text)
        
    st.subheader("2. AI Document Classification & NLP Extraction")
    with st.spinner("Running OpenAI Inference..."):
        ai_result = process_pdf_with_openai(raw_text)
        
    st.write(f"**Document Type:** {ai_result.document_type}")
    st.write(f"**Confidence:** {ai_result.confidence_score}%")
    st.write(f"**Extracted Names:** {', '.join(ai_result.names)}")
    
    st.subheader("3. Matching against Inmate Database")
    with st.spinner("Comparing against scraped rosters..."):
        matches = find_matches_in_db(ai_result.names, uploaded_file.name, context=raw_text)
        
    if matches:
        st.success(f"Found {len(matches)} match(es)!")
        for match in matches:
            st.markdown("---")
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"### Roster Profile")
                inmate = match.inmate
                st.write(f"**Name:** {inmate.full_name}")
                st.write(f"**County:** {inmate.county}")
                if inmate.photo_url and "http" in inmate.photo_url:
                    st.image(inmate.photo_url, caption=inmate.full_name, width=200)
                else:
                    st.info("No photo available")
                st.metric("Fuzzy Match Score", f"{match.confidence_score:.1f}%")
                
                st.caption("✅ Email Alert Dispatched to configured GMAIL_USER")
                
            with col2:
                st.markdown(f"### Document Evidence")
                escaped_name = re.escape(match.extracted_name)
                highlighted_text = re.sub(
                    f"({escaped_name})", 
                    r"<mark style='background-color: yellow; color: black; font-weight: bold;'>\1</mark>", 
                    raw_text, 
                    flags=re.IGNORECASE
                )
                
                st.markdown(
                    f"<div style='height: 400px; overflow-y: scroll; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #2b2b2b; color: #FFF; white-space: pre-wrap; font-family: monospace;'>{highlighted_text}</div>", 
                    unsafe_allow_html=True
                )
    else:
        st.info("No corresponding inmates found in the roster database.")
        
    if os.path.exists(temp_pdf):
        os.remove(temp_pdf)
