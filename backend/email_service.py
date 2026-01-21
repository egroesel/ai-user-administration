import resend
from config import settings

resend.api_key = settings.RESEND_API_KEY


def send_password_reset_email(email: str, reset_token: str, user_name: str = None):
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                margin: 20px 0;
            }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Passwort zurücksetzen</h2>
            <p>Hallo{f" {user_name}" if user_name else ""},</p>
            <p>Du hast eine Anfrage zum Zurücksetzen deines Passworts erhalten.</p>
            <p>Klicke auf den folgenden Button, um dein Passwort zurückzusetzen:</p>
            <a href="{reset_url}" class="button">Passwort zurücksetzen</a>
            <p>Oder kopiere diesen Link in deinen Browser:</p>
            <p style="word-break: break-all;">{reset_url}</p>
            <p>Dieser Link ist 1 Stunde lang gültig.</p>
            <p>Wenn du diese Anfrage nicht gestellt hast, kannst du diese E-Mail ignorieren.</p>
            <div class="footer">
                <p>Diese E-Mail wurde automatisch generiert. Bitte antworte nicht darauf.</p>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        params = {
            "from": settings.FROM_EMAIL,
            "to": [email],
            "subject": "Passwort zurücksetzen",
            "html": html_content,
        }
        resend.Emails.send(params)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_welcome_email(email: str, user_name: str = None):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Willkommen!</h2>
            <p>Hallo{f" {user_name}" if user_name else ""},</p>
            <p>Dein Account wurde erfolgreich erstellt.</p>
            <p>Du kannst dich jetzt mit deiner E-Mail-Adresse und deinem Passwort anmelden.</p>
            <p><a href="{settings.FRONTEND_URL}/login">Zum Login</a></p>
            <div class="footer">
                <p>Diese E-Mail wurde automatisch generiert. Bitte antworte nicht darauf.</p>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        params = {
            "from": settings.FROM_EMAIL,
            "to": [email],
            "subject": "Willkommen bei der Nutzerverwaltung",
            "html": html_content,
        }
        resend.Emails.send(params)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_test_email(email: str, email_type: str, user_name: str = None):
    """
    Send test emails for admin testing

    email_type options:
    - 'welcome': Welcome email
    - 'password_reset': Password reset email
    - 'account_activated': Account activated notification
    - 'account_deactivated': Account deactivated notification
    - 'test_simple': Simple test email
    """

    if email_type == "welcome":
        return send_welcome_email(email, user_name)

    elif email_type == "password_reset":
        test_token = "TEST_TOKEN_123456"
        return send_password_reset_email(email, test_token, user_name)

    elif email_type == "account_activated":
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Account aktiviert</h2>
                <p>Hallo{f" {user_name}" if user_name else ""},</p>
                <p>Dein Account wurde von einem Administrator aktiviert.</p>
                <p>Du kannst dich jetzt wieder anmelden.</p>
                <p><a href="{settings.FRONTEND_URL}/login">Zum Login</a></p>
                <div class="footer">
                    <p>Diese E-Mail wurde automatisch generiert. Bitte antworte nicht darauf.</p>
                </div>
            </div>
        </body>
        </html>
        """

        try:
            params = {
                "from": settings.FROM_EMAIL,
                "to": [email],
                "subject": "Dein Account wurde aktiviert",
                "html": html_content,
            }
            resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    elif email_type == "account_deactivated":
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Account deaktiviert</h2>
                <p>Hallo{f" {user_name}" if user_name else ""},</p>
                <p>Dein Account wurde von einem Administrator deaktiviert.</p>
                <p>Bei Fragen wende dich bitte an den Support.</p>
                <div class="footer">
                    <p>Diese E-Mail wurde automatisch generiert. Bitte antworte nicht darauf.</p>
                </div>
            </div>
        </body>
        </html>
        """

        try:
            params = {
                "from": settings.FROM_EMAIL,
                "to": [email],
                "subject": "Dein Account wurde deaktiviert",
                "html": html_content,
            }
            resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    elif email_type == "test_simple":
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Test-E-Mail</h2>
                <p>Hallo{f" {user_name}" if user_name else ""},</p>
                <p>Dies ist eine Test-E-Mail aus der Nutzerverwaltung.</p>
                <p>Wenn du diese E-Mail erhältst, funktioniert der E-Mail-Versand korrekt.</p>
                <div class="footer">
                    <p>Diese E-Mail wurde automatisch generiert. Bitte antworte nicht darauf.</p>
                </div>
            </div>
        </body>
        </html>
        """

        try:
            params = {
                "from": settings.FROM_EMAIL,
                "to": [email],
                "subject": "Test-E-Mail von der Nutzerverwaltung",
                "html": html_content,
            }
            resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    else:
        return False
