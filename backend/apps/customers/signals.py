from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.customers.models import Customer, Repository
from client.redis_client import RedisClient


@receiver(post_save, sender=Customer)
def create_repository(sender, instance, created, **kwargs):
    if created:
        repository = Repository.objects.create(customer=instance, blacklist=[])
        repository.save()


# Delete Customer's blacklist from Redis
@receiver(post_delete, sender=Repository)
def delete_repository(sender, instance, *args, **kwargs):
    blacklist_id = f'blacklist_{instance.pkid}'
    RedisClient().flush_keys(key=blacklist_id)
