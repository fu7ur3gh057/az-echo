from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.customers.models import Customer, Repository
from services.redis_client import flush_keys


@receiver(post_save, sender=Customer)
def create_repository(sender, instance, created, **kwargs):
    if created:
        repository = Repository.objects.create(customer=instance, black_list=[])
        repository.save()


# Delete Customer's blacklist from Redis
@receiver(post_delete, sender=Repository)
def delete_repository(sender, instance, *args, **kwargs):
    blacklist_lock = f'blacklist_lock_{instance.pkid}'
    flush_keys(key=blacklist_lock)
