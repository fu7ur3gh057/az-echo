from django.core.management.base import BaseCommand

from client.redis_client import RedisClient


class Command(BaseCommand):
    help = 'Deletes all lock keys from Redis'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Flushing all Redis Locker keys...'))
            RedisClient().flush_keys('lock_')
            self.stdout.write(self.style.SUCCESS('Redis lockers successfully delete'))
        except Exception as ex:
            self.stdout.write(self.style.ERROR(f'{ex}'))
