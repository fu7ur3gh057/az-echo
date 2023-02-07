from django.core.management.base import BaseCommand

from apps.payments.models import SubscriptionChecker
from apps.synthesis.models import Generator


class Command(BaseCommand):
    help = 'Initializing General Singleton Tasks'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Initializing general singleton tasks...'))
            Generator.objects.create(generation_count=1, generation_timeout=3)
            SubscriptionChecker.objects.create()
            self.stdout.write(self.style.SUCCESS('General singleton tasks successful created'))
        except Exception as ex:
            self.stdout.write(self.style.ERROR(f'{ex}'))
