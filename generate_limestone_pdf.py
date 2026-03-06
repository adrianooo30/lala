import os
import io
import base64
from fpdf import FPDF
from datetime import datetime

data_json = [{"id":"1","county":"Limestone","full_name":"ADAMS, BOBBY EUGENE","first_name":"BOBBY EUGENE","last_name":"ADAMS","photo_url":"data:image/png;base64,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","details":"ADAMS, BOBBY EUGENE\tWhite\tMale\t\n02/23/1985\n\t12/07/2025\tAthens PD\t\n\nWarrant: Capias/Failure to Pay warrant 93-MC-2024-214.00 issued by Limestone, AL; Arrest Date 12/07/2025; Bond - Cash, $500.00; Set By Warrant;\nWarrant: Alias warrant 93-MC-2025-360.00 issued by Limestone, AL; Arrest Date 12/07/2025; Bond - Cash, $500.00; Set By Warrant;","scraped_at":"2026-03-06 04:19:18.095286"}]

class PDF(FPDF):
    def header(self):
        # Title
        self.set_font("helvetica", "B", 18)
        self.cell(0, 10, "Booking Summary (Template A)", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("helvetica", "", 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, "Filled example using Limestone County inmate roster information.", align="L", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_draw_color(220, 220, 220)
        self.set_line_width(0.2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

inmate = data_json[0]
base64_img = inmate["photo_url"].split(",")[1]
img_path = "temp_mugshot.jpg"
with open(img_path, "wb") as f:
    f.write(base64.b64decode(base64_img))

pdf = PDF()
pdf.add_page()
pdf.set_text_color(0, 0, 0)
pdf.set_font("helvetica", "B", 10)

def draw_row(label, value, y_pos):
    pdf.set_y(y_pos)
    pdf.set_x(10)
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(50, 6, label, border=0)
    pdf.set_font("helvetica", "", 10)
    pdf.cell(80, 6, value, border=0)
    # thin border line below row
    pdf.set_line_width(0.1)
    pdf.set_draw_color(230, 230, 230)
    pdf.line(10, pdf.get_y() + 6, 140, pdf.get_y() + 6)
    pdf.set_draw_color(0, 0, 0)

y = pdf.get_y()
# Section 1: Agency details
draw_row("Agency", "Athens PD", y)
draw_row("Facility", "Limestone County Detention Center", y+8)
draw_row("Booking #", "93-MC-2024-214", y+16)
draw_row("Booking Time", "12/07/2025 10:48 AM", y+24)
draw_row("Case #", "93-MC-2024-214.00", y+32)
draw_row("Arresting Agency", "Athens PD", y+40)
draw_row("Court", "CIRC", y+48)
draw_row("Disposition", "ACT", y+56)
draw_row("Holds", "None", y+64)

# Place image on the right hand side next to the table
pdf.image(img_path, x=145, y=y, w=50)

# Subject Information
pdf.ln(18)
pdf.set_font("helvetica", "B", 14)
pdf.cell(0, 10, "Subject Information", new_x="LMARGIN", new_y="NEXT")

y = pdf.get_y()
draw_row("Subject Name", inmate["full_name"], y)
draw_row("Age", "39", y+8)
draw_row("Sex", "M", y+16)
draw_row("Race", "W", y+24)
draw_row("DOB", "02/23/1985", y+32)
draw_row("Aliases", "N/A", y+40)
draw_row("Address", "N/A", y+48)

# Charges table
pdf.ln(15)
pdf.set_font("helvetica", "B", 14)
pdf.cell(0, 10, "Charges", new_x="LMARGIN", new_y="NEXT")

pdf.set_draw_color(220, 220, 220)
pdf.set_fill_color(245, 245, 245)
pdf.set_font("helvetica", "B", 10)
pdf.cell(100, 8, "Charge", border=1, fill=True)
pdf.cell(50, 8, "Statute", border=1, fill=True)
pdf.cell(40, 8, "Bond Amount", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

pdf.set_font("helvetica", "", 10)
# Use MultiCell trick to avoid overflow, or just truncate
pdf.cell(100, 8, "Capias/Failure to Pay warrant 93-MC-2024-214.00", border=1)
pdf.cell(50, 8, "N/A", border=1)
pdf.cell(40, 8, "$500.00", border=1, new_x="LMARGIN", new_y="NEXT")

pdf.cell(100, 8, "Alias warrant 93-MC-2025-360.00", border=1)
pdf.cell(50, 8, "N/A", border=1)
pdf.cell(40, 8, "$500.00", border=1, new_x="LMARGIN", new_y="NEXT")

# Narrative
pdf.ln(10)
pdf.set_font("helvetica", "B", 14)
pdf.cell(0, 10, "Narrative", new_x="LMARGIN", new_y="NEXT")

pdf.set_font("helvetica", "", 10)
narrative = f"Subject {inmate['full_name']} was booked on 12/07/2025 under booking number 93-MC-2024-214. Listed charge: Capias/Failure to Pay warrant (Statute N/A). Arresting Agency: Athens PD; Court: CIRC; Disposition: ACT; Holds: None. Bond amounts may change after court appearances."
pdf.multi_cell(0, 5, narrative)

pdf.ln(15)
pdf.set_font("helvetica", "", 9)
pdf.cell(0, 4, "Template A", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 4, f"Generated {datetime.now().strftime('%Y-%m-%d')}", new_x="LMARGIN", new_y="NEXT")

output_file = "Booking_Summary_Template_A_Limestone.pdf"
pdf.output(output_file)

if os.path.exists(img_path):
    os.remove(img_path)

print(f"Successfully generated {output_file}")
