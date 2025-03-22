
from django.conf import settings
from django.core.mail import EmailMessage

class EmailUtil():
    
    @staticmethod
    def send(to_email, subject, body):
        email = EmailMessage(
            subject = subject,
            body=body,
            from_email = settings.EMAIL_HOST_USER,
            to = [to_email]
        )
        email.content_subtype = "html"
        email.send()