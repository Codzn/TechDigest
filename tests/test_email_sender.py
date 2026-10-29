from unittest.mock import patch
import pytest

from mail.send_newsletter import send_newsletter

def test_send_newsletter(monkeypatch):
    # Configuration fictive, uniquement pour le test
    monkeypatch.setenv("EMAIL_SENDER", "expediteur@example.com")
    monkeypatch.setenv("PASS_EMAIL", "mot-de-passe-fictif")
    monkeypatch.setenv("RECIPIENT_EMAIL", "destinataire@example.com")

    contenu_html = "<h1>Actualité IA</h1>"

    with patch("mail.email_sender.smtplib.SMTP_SSL") as mock_smtp:

        # Récupère le faux serveur utilisé par le bloc with
        mock_server = mock_smtp.return_value.__enter__.return_value

        # Exécute la fonction à tester
        send_newsletter(contenu_html)

    
        print("Appels SMTP :", mock_smtp.call_args_list)

        # Vérifie la connexion au serveur
        mock_smtp.assert_called_once_with("smtp.gmail.com", 465, timeout= 30)

        # Vérifie l'authentification
        mock_server.login.assert_called_once_with(
            "expediteur@example.com",
            "mot-de-passe-fictif",
        )

        # Vérifie l'envoi du message
        mock_server.sendmail.assert_called_once()

        # Récupère les arguments transmis à sendmail()
        args = mock_server.sendmail.call_args.args


        assert args[0] == "expediteur@example.com"
        assert args[1] == "destinataire@example.com"

def test_missing_email_configuration_raises_value_error(monkeypatch):
    monkeypatch.delenv("EMAIL_SENDER", raising=False)
    monkeypatch.delenv("PASS_EMAIL", raising=False)
    monkeypatch.delenv("RECIPIENT_EMAIL", raising=False)

    contenu_html = "<h1>Actualité IA</h1>"

    with pytest.raises(ValueError, match="Missing email configuration: check the required environment variables"):
        send_newsletter(contenu_html)




    