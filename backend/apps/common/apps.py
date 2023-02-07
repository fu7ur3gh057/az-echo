from django.apps import AppConfig

from client.redis_client import RedisClient


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.common'

    def ready(self):
        RedisClient().flush_keys('lock_')
