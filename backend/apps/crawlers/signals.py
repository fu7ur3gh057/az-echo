from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from apps.crawlers.models import Echo, Driller
from apps.customers.models import Repository
from utils.task_util import TaskStatus, get_time_interval


# ECHO
@receiver(post_save, sender=Repository)
def create_echo(sender, instance, created, **kwargs):
    if created:
        echo = Echo.objects.create(repository=instance, status=TaskStatus.disabled)
        echo.save()


@receiver(post_save, sender=Echo)
def create_or_update_echo_tasks(sender, instance, created, **kwargs):
    if created:
        instance.setup_tasks()
    else:
        if instance.discover_task is not None:
            instance.discover_task.enabled = instance.status == TaskStatus.active
            instance.discover_task.interval = get_time_interval(time=instance.discover_interval)
            instance.discover_task.save()
        if instance.extract_task is not None:
            instance.extract_task.enabled = instance.status == TaskStatus.active
            instance.extract_task.interval = get_time_interval(time=instance.extract_interval)
            instance.extract_task.save()


@receiver(post_delete, sender=Echo)
def delete_echo_task(sender, instance, *args, **kwargs):
    if instance.discover_task is not None:
        print(f'Deleting Discover Task')
        instance.discover_task.delete()
    if instance.extract_task is not None:
        print('Deleting Extract Task')
        instance.extract_task.delete()


# DRILLER
@receiver(post_save, sender=Driller)
def create_or_update_driller_task(sender, instance, created, **kwargs):
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == TaskStatus.active
            instance.task.interval = get_time_interval(time=instance.interval)
            instance.task.save()
