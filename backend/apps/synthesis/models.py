from apps.common.models import TimeStampedUUIDModel
from uuid import uuid4
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask
from apps.common.models import TimeStampedUUIDModel
from django_enum_choices.fields import EnumChoiceField

from apps.customers.models import Repository
from utils.task_util import TimeInterval, TaskStatus, get_time_interval
from django.core.validators import MinValueValidator, MaxValueValidator


class Synthesis(TimeStampedUUIDModel):
    repository = models.ForeignKey(Repository, related_name="synthesis_list", on_delete=models.CASCADE)
    # Voicen given Job ID
    job_id = models.IntegerField(null=True, blank=True)
    link = models.CharField(max_length=512, blank=False)
    # Text extracted from link
    text = models.TextField(blank=True)
    # Customer language
    lang = models.CharField(max_length=20, blank=False)
    crawled_status = models.BooleanField(default=False)
    error_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Synthesis'
        verbose_name_plural = 'Synthesis List'

    def __str__(self):
        return str(self.pkid)


# Task Class for Generating Synthesis for all customers
class Generator(models.Model):
    task = models.ForeignKey(PeriodicTask, related_name="generator_task", on_delete=models.CASCADE,
                             null=True, blank=True, verbose_name=_("Synthesis Generator Task"))
    generation_count = models.IntegerField(default=1,
                                           help_text="Maximum count of generations, min value = 1, max value = 5",
                                           validators=[MinValueValidator(1),
                                                       MaxValueValidator(5)])
    generation_timeout = models.IntegerField(default=3,
                                             help_text="Generation timeout in sec, min value = 3, max value = 10",
                                             validators=[MinValueValidator(3),
                                                         MaxValueValidator(10)])
    interval = EnumChoiceField(TimeInterval, default=TimeInterval.one_min)
    status = EnumChoiceField(TaskStatus, default=TaskStatus.active)

    class Meta:
        verbose_name = "Generator"
        verbose_name_plural = "Generators"

    @transaction.atomic
    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name="Synthesis Generator Task",
            task="generator_task",
            interval=get_time_interval(time=self.interval),
            start_time=timezone.now()
        )

    def save(self, *args, **kwargs):
        # check if this instance already exists
        if self.id:
            super().save()
        elif Generator.objects.all().count() > 0:
            return  # no save will be processed
        else:
            super().save()

    def __str__(self):
        return f'Generator'
