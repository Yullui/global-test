import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

# 1. Load Environment (Point to your Agentic folder)
env_path = r"C:\Users\[USERNAME]\Agentic\.env"
load_dotenv(dotenv_path=env_path)

email_address = os.getenv('EMAIL_ADDRESS')
password = os.getenv('PASSWORD')
recipient_email = "[YOUR_PROTON_EMAIL]@proton.me"

# 2. Setup the Email Content
msg = EmailMessage()
msg['Subject'] = '🚨 SOC Connectivity Test'
msg['From'] = email_address
msg['To'] = recipient_email
msg.set_content("Connection successful. The SOC Mailer is ready for dispatch.")

# 3. Send via SMTP
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(email_address, password)
        smtp.send_message(msg)
        print(f"Test email sent successfully to {recipient_email}!")
except Exception as e:
    print(f"Connection failed: {e}")
