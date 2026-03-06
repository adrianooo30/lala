import os
from database import SessionLocal, Inmate
from fpdf import FPDF

def create_sample_pdf():
    # 1. Fetch an inmate from the database
    session = SessionLocal()
    inmate = session.query(Inmate).first()
    
    if not inmate:
        print("No inmates found in the database. Please run seed_mock_data.py or scraper_limestone.py first.")
        return
    
    print(f"Selected inmate: {inmate.full_name} ({inmate.county})")
    print(f"Creating a sample Booking Summary PDF for {inmate.full_name}...")
    
    # 2. Create PDF with the inmate's name explicitly
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    
    pdf.cell(200, 10, txt="BOOKING SUMMARY", ln=1, align='C')
    pdf.cell(200, 10, txt="=================", ln=1, align='C')
    pdf.cell(200, 10, txt="", ln=1)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: 2026-03-06", ln=1)
    pdf.cell(200, 10, txt=f"Facility: {inmate.county} County Jail", ln=1)
    pdf.cell(200, 10, txt=f"Subject Name: {inmate.full_name}", ln=1)
    
    if inmate.first_name and inmate.last_name:
        pdf.cell(200, 10, txt=f"First Name: {inmate.first_name}", ln=1)
        pdf.cell(200, 10, txt=f"Last Name: {inmate.last_name}", ln=1)
        
    pdf.cell(200, 10, txt="", ln=1)
    pdf.cell(200, 10, txt="Charges:", ln=1)
    pdf.cell(200, 10, txt="- SAMPLE CHARGE 1", ln=1)
    pdf.cell(200, 10, txt="- SAMPLE CHARGE 2", ln=1)
    
    pdf_filename = "sample_booking_summary.pdf"
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), pdf_filename)
    pdf.output(output_path)
    
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    create_sample_pdf()
