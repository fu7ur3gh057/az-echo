from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.synthesis.models import Generator
from utils.task_util import TaskStatus, get_time_interval


@receiver(post_save, sender=Generator)
def update_generator_task(sender, instance, created, **kwargs):
    if not created:
        if instance.task is not None:
            instance.task.enabled = instance.status == TaskStatus.active
            instance.task.interval = get_time_interval(time=instance.time_interval)
            instance.task.save()
