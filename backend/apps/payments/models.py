from django.db import models, transaction
import datetime
from django.utils import timezone

from django_celery_beat.models import PeriodicTask
from django_enum_choices.fields import EnumChoiceField
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel
from apps.customers.models import Customer
from utils.task_util import TaskStatus, TimeInterval, get_time_interval


# class Transaction(TimeStampedUUIDModel):
#     pass


class Subscription(TimeStampedUUIDModel):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Expired'),
        (3, 'Canceled'),
    )
    customer = models.ForeignKey(Customer, related_name="subscriptions", on_delete=models.CASCADE)
    type = models.IntegerField(choices=STATUS_CHOICES, default=1)
    expire_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    canceled = models.BooleanField(default=False)

    # учесть в феврале нет 29 числа
    # def save(self, *args, **kwargs):
    #     super().save()
    #     if not self.pkid:
    #         create_date = self.created_at
    #         year = create_date.year
    #         month = create_date.month + 1
    #         day = create_date.day
    #         if month > 12:
    #             month = 1
    #             year += 1
    #         self.expire_date = datetime.date(year=year, month=month, day=25)
    #         super().save()


class SubscriptionChecker(models.Model):
    task = models.OneToOneField(PeriodicTask, related_name='subscription_checker', on_delete=models.CASCADE,
                                null=True, blank=True, verbose_name=_("Subscription Checker Task"))
    interval = EnumChoiceField(TimeInterval, default=TimeInterval.one_day)
    status = EnumChoiceField(TaskStatus, default=TaskStatus.active)

    class Meta:
        verbose_name = "Subscription Checker"
        verbose_name_plural = "Subscription Checker"

    @transaction.atomic
    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name="Subscription Checker Task",
            task="subscription_checker_task",
            interval=get_time_interval(time=self.interval),
            start_time=timezone.now()
        )

    def save(self, *args, **kwargs):
        # check if this instance already exists
        if self.id:
            super().save()
        elif SubscriptionChecker.objects.all().count() > 0:
            return  # no save will be processed
        else:
            super().save()

    def delete(self, *args, **kwargs):
        task = self.task
        super().delete()
        task.delete()

    def __str__(self):
        return 'Subscription Checker'
