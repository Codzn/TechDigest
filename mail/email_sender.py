import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dotenv
import logging

dotenv.load_dotenv()

def envoyer_veille_technologique(contenu_html: str):
    """
    Takes the AI-generated text and sends it via email to the address specified in the RECIPIENT_EMAIL environment variable.   
    """
    # Retrieving environment variables for email sending
    email_sender = os.getenv("EMAIL_SENDER", "")
    pass_email = os.getenv("PASS_EMAIL", "")
    recipient_email = os.getenv("RECIPIENT_EMAIL", email_sender)  # If RECIPIENT_EMAIL is not defined, the email is sent to the sender's address.

    # 2. Creating the email message
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = recipient_email
    msg['Subject'] = "Actualité TechDigest de la veille"

    msg.attach(MIMEText(contenu_html, 'html', 'utf-8'))

    try:
        # 3. Connecting to the SMTP server and sending the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_sender, pass_email)
            server.sendmail(email_sender, recipient_email, msg.as_string())
        logging.info(f"E-mail envoyé avec succès à {recipient_email}.")
    except Exception as e:
        logging.error(f"Erreur lors de l'envoi de l'e-mail : {e}")