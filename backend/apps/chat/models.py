from django.db import models
from django.contrib.auth import get_user_model
from apps.common.models import TimeStampedUUIDModel, TimeStampedModel

User = get_user_model()


class Room(models.Model):
    user = models.ForeignKey(User, related_name="rooms", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    # superusers = models.ManyToManyField(User, verbose_name="superusers", related_name="rooms")

    # def save(self, *args, **kwargs):
    #     superusers = User.objects.all().filter(is_superuser=True)
    #     for superuser in superusers:
    #         superuser.rooms.append(self)
    #         superuser.save()


class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE, null=True)
    text = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
