import os
import fitz # PyMuPDF
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ExtractedNamesResponse(BaseModel):
    document_type: str = Field(description="The type of document, e.g., 'Booking Summary', 'Court Docket Notice', 'Crash Report'")
    confidence_score: float = Field(description="Confidence score in the extraction from 0.0 to 100.0")
    names: list[str] = Field(description="List of standardized full names of the primary subjects found in the document")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract raw text from a PDF file using PyMuPDF."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def process_pdf_with_openai(text: str) -> ExtractedNamesResponse:
    """Use OpenAI to classify document type and extract structured names."""
    prompt = f"""
You are an expert legal document parser. 
I have extracted text from a document.
Please identify what kind of document this is (e.g. 'Booking Summary', 'Court Docket Notice', or 'Crash Report') 
and extract the name(s) of the primary subjects (e.g. the person being booked, the defendant, or the driver).
Standardize the names into a clean "FIRST LAST" format. If multiple names are present, return them all.
If you are unsure or fields are missing, assign a lower confidence_score.

Document Text:
{text}
"""
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a precise document parser."},
                {"role": "user", "content": prompt}
            ],
            response_format=ExtractedNamesResponse,
            temperature=0.0
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return ExtractedNamesResponse(document_type="Unknown", confidence_score=0.0, names=[])

if __name__ == "__main__":
    test_pdf = "PDF_Template_A_Booking_Summary_FILLED.pdf"
    if os.path.exists(test_pdf):
        txt = extract_text_from_pdf(test_pdf)
        print(f"Extracted {len(txt)} chars from {test_pdf}")
        # Requires valid api key
        # res = process_pdf_with_openai(txt)
        # print(res.model_dump_json(indent=2))
