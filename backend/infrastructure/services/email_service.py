import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from application.interfaces.email_sender import EmailSender

class MailtrapEmailSender(EmailSender):
    def __init__(self, host: str, port: int, username: str, password: str, from_email: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.FRONTEND_URL = os.getenv('FRONTEND_URL')

    def send_verification_email(self, to_email: str, verification_token: str) -> None: 
        verification_link = f"{self.FRONTEND_URL}/auth/verify-account/{verification_token}"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Verifica tu cuenta en Chambeapp"
        message["From"] = self.from_email
        message["To"] = to_email

        text = f"Hola,\n\nPara activar tu cuenta en Chambeapp, haz clic en el siguiente enlace:\n{verification_link}\n\nSi no creaste esta cuenta, ignora este correo."
        html = f"""\
        <html>
          <body>
            <h2>¡Bienvenido a Chambeapp!</h2>
            <p>Para activar tu cuenta y empezar a gestionar tus tableros, haz clic en el siguiente botón:</p>
            <a href="{verification_link}" style="padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Verificar mi cuenta</a>
          </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(
                    self.from_email, 
                    to_email, 
                    message.as_string()
                )
        except Exception as e:
            print(f"Error enviando correo a {to_email}: {str(e)}")


    def send_password_reset_email(self, to_email: str, verification_token: str) -> None:
            verification_link = f"{self.FRONTEND_URL}/auth/reset-password/{verification_token}"
            
            message = MIMEMultipart("alternative")
            message["Subject"] = "Restablecer contraseña en Chambeapp"
            message["From"] = self.from_email
            message["To"] = to_email
    
            text = f"Hola,\n\nPara restablecer tu cuenta en Chambeapp, haz clic en el siguiente enlace:\n{verification_link}\n\nSi no creaste esta cuenta, ignora este correo."
            html = f"""\
            <html>
              <body>
                <h2>¡Bienvenido a Chambeapp!</h2>
                <p>Para restablecer tu contraseña y recuperar tu acceso, haz clic en el siguiente botón:</p>
                <a href="{verification_link}" style="padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Restablcer mi contraseña</a>
              </body>
            </html>
            """
    
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
    
            try:
                with smtplib.SMTP(self.host, self.port) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    server.sendmail(
                        self.from_email, 
                        to_email, 
                        message.as_string()
                    )
            except Exception as e:
                print(f"Error enviando correo a {to_email}: {str(e)}")

    
