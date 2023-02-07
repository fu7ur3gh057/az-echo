from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.synthesis.models import Generator
from utils.task_util import TaskStatus, get_time_interval


@receiver(post_save, sender=Generator)
def create_or_update_generator_task(sender, instance, created, **kwargs):
    if created:
        instance.setup_task()
    if not created:
        if instance.task is not None:
            print('UPDATE GENERATOR TASK')
            instance.task.enabled = instance.status == TaskStatus.active
            instance.task.interval = get_time_interval(time=instance.time_interval)
            instance.task.save()


@receiver(post_delete, sender=Generator)
def delete_generator_task(sender, instance, *args, **kwargs):
    instance.task.delete()
