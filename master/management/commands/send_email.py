# myapp/management/commands/send_email.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send an email with the given parameters'

    def add_arguments(self, parser):
        parser.add_argument('to_email', type=str, help='The email address of the receiver')
        parser.add_argument('message', type=str, help='The message to be sent')

    def handle(self, *args, **kwargs):
        to_email = kwargs['to_email']
        message = kwargs['message']
        
        subject = 'Custom Email from Django Command'
        self.stdout.write(f'Sending email from to {to_email} with message: "{message}"')

        try:
            send_mail(subject, message, None, [to_email])
            self.stdout.write(self.style.SUCCESS(f'Email sent successfully to {to_email}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {e}'))

# example command: python3 manage.py send_email nandanramdani608@gmail.com "Hello, this is a test email."