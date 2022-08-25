from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendEmailService:
    def __init__(self):
        apikey = config("SENDGRID_API_KEY")
        self.sg = SendGridAPIClient(apikey)
        self.from_email = config("FROM_EMAIL")

    def send_email(self, to_email, subject, body):
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=f"<strong>{body}</strong>",
        )
        try:
            response = self.sg.send(message)
            return response.status_code
        except Exception as ex:
            raise Exception(ex)
