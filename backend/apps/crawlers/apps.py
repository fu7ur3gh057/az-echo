from django.apps import AppConfig

from client.redis_client import RedisClient


class CrawlersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.crawlers'

    def ready(self):
        import apps.crawlers.signals
        RedisClient().flush_all()
