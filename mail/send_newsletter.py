import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dotenv
import logging

dotenv.load_dotenv()

def send_newsletter(contenu_html: str):
    """
    Takes the AI-generated text and sends it via email to the address specified in the RECIPIENT_EMAIL environment variable.   
    """
    # Retrieving environment variables for email sending
    email_sender = os.getenv("EMAIL_SENDER", "")
    pass_email = os.getenv("PASS_EMAIL")
    recipient_email = os.getenv("RECIPIENT_EMAIL", email_sender)  # If RECIPIENT_EMAIL is not defined, the email is sent to the sender's address.

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = recipient_email
    msg['Subject'] = "TechDigest : votre veille tech de la semaine"

    msg.attach(MIMEText(contenu_html, 'html', 'utf-8'))

    if not email_sender or not pass_email or not recipient_email:
        logging.error("Error: Missing email configuration in environment variables.")
        raise ValueError ("Missing email configuration: check the required environment variables")
    
    try:
        logging.info("Connecting to the SMTP server...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) as server:
            logging.info("SMTP connection established.")
            logging.info("Authentification SMTP...")
            server.login(email_sender, pass_email)
            logging.info("Authentification successfull.")
            logging.info("Sending the mail...")
            server.sendmail(email_sender, recipient_email, msg.as_string())
        logging.info(f"E-mail successfully send to {recipient_email}.")
    except smtplib.SMTPAuthenticationError as e:
            logging.exception(e)
            raise
    except Exception:
        logging.error("Error while connecting to the server.")
        raise # Re-raise the exception to be handled by the calling function
