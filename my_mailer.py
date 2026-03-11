import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

# 1. Load Environment
env_path = r"C:\Users\user\.env"
load_dotenv(dotenv_path=env_path)

email_address = os.getenv('EMAIL_ADDRESS')
password = os.getenv('PASSWORD')
recipient_email = "recipient_email@email.com
# 2. Setup the Email Content
msg = EmailMessage()
msg['Subject'] = '🚨 SOC Alert: Ticket SOC-022FEEBF'
msg['From'] = email_address
msg['To'] = recipient_email
msg.set_content("SOC Incident Report\n-------------------\nTarget IP identified. Review required.")

# 3. Send via SMTP
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls() # Secure the connection
        smtp.ehlo()
        smtp.login(email_address, password)
        smtp.send_message(msg)
        print(f"Ticket sent successfully to {recipient_email}!")
except smtplib.SMTPAuthenticationError:
    print("Error: App Password incorrect. Check line 3 of your .env file.")
except Exception as e:

    print(f"An unexpected error occurred: {e}")
