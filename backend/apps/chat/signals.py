from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.chat.models import Room

User = get_user_model()


@receiver(post_save, sender=User)
def create_room(sender, instance, created, **kwargs):
    if created:
        room = Room.objects.create(user=instance)
        room.save()
