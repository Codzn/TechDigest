import smtplib
import os
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dotenv

dotenv.load_dotenv()

def envoyer_veille_technologique(contenu_texte: str):
    """
    Prend le texte généré par l'IA et l'envoie par e-mail à l'adresse spécifiée dans la variable d'environnement EMAIL_DESTINATAIRE.
    """
    # Récupération des variables d'environnement pour l'envoi de l'e-mail
    email_user = os.getenv("EMAIL_USER", "")
    mdp_email = os.getenv("MDP_EMAIL", "")
    email_to = os.getenv("EMAIL_DESTINATAIRE", email_user)  # Si EMAIL_DESTINATAIRE n'est pas défini, on envoie à l'adresse de l'expéditeur

    # 2. Création du message e-mail
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_to
    msg['Subject'] = "Actualité TechDigest de la veille"

    msg.attach(MIMEText(contenu_texte, 'plain', 'utf-8'))

    try:
        # 3. Connexion au serveur SMTP et envoi de l'e-mail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_user, mdp_email)
        server.sendmail(email_user, email_to, msg.as_string())
        server.quit()
        print(f"E-mail envoyé avec succès à {email_to}.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")