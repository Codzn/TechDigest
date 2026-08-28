import smtplib
import os
import dotenv

dotenv.load_dotenv()

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

server.login(os.getenv("EMAIL_USER"), os.getenv("MDP_EMAIL"))

server.sendmail(
    os.getenv("EMAIL_FROM"),
    os.getenv("EMAIL_USER"),
    "Subject: Test\n\nThis is a test email sent from Python.")

server.quit()