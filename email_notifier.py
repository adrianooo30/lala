import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_match_alert(inmate_name: str, pdf_filename: str):
    user = os.getenv("GMAIL_USER", "")
    password = os.getenv("GMAIL_APP_PASSWORD", "")
    
    if not user or not password:
        print("Warning: GMAIL_USER or GMAIL_APP_PASSWORD not set. Email not sent.")
        return False
        
    msg = EmailMessage()
    msg.set_content(f"A match was found for {inmate_name} in the document: {pdf_filename}.")
    msg['Subject'] = f"New Inmate Match Alert: {inmate_name}"
    msg['From'] = user
    msg['To'] = user # Sending alert to self
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(user, password)
        server.send_message(msg)
        server.quit()
        print(f"Alert email sent to {user} for {inmate_name}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
        
if __name__ == "__main__":
    # Test
    # send_match_alert("John Doe", "test.pdf")
    pass
