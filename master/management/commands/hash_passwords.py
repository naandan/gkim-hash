# myapp/management/commands/hash_passwords.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Hash all plain text passwords for users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if not user.password.startswith('pbkdf2_'):  # Check if the password is already hashed
                self.stdout.write(f'Hashing password for user: {user.username}')
                user.password = make_password(user.password)
                user.save()
                self.stdout.write(f'Password for user {user.username} hashed successfully.')
            else:
                self.stdout.write(f'Password for user {user.username} is already hashed.')

        self.stdout.write(self.style.SUCCESS('Successfully hashed all user passwords'))
