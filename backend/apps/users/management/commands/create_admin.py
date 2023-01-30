from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates AzEcho application super user.'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Started super user creation process...'))
            if User.objects.all().count() != 0:
                self.stdout.write(self.style.SUCCESS('Database has already a user.'))
                return
            user = User(email='funt@gmail.com', username='funt', is_staff=True, is_superuser=True,
                        first_name='Future', last_name='Ghost')
            user.save()
            user.set_password('lol123lol')
            self.stdout.write(self.style.SUCCESS('Successfully created the super user.'))
        except Exception as ex:
            self.stdout.write(self.style.ERROR(f'{ex}'))