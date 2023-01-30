import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.payments.models import SubscriptionChecker, Subscription
from utils.task_util import TaskStatus, get_time_interval


@receiver(post_save, sender=Subscription)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        create_date = instance.created_at
        year = create_date.year
        month = create_date.month + 1
        day = create_date.day
        if month > 12:
            month = 1
            year += 1
        instance.expire_date = datetime.date(year=year, month=month, day=25)
        instance.save()


@receiver(post_save, sender=SubscriptionChecker)
def create_or_update_subscription_task(sender, instance, created, **kwargs):
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == TaskStatus.active
            instance.task.interval = get_time_interval(time=instance.interval)
            instance.task.save()
