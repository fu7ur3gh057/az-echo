from django.db import models, transaction
import json
from django.utils import timezone
from apps.common.models import TimeStampedUUIDModel
from apps.customers.models import Repository
from utils.task_util import TimeInterval, TaskStatus, get_time_interval
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.utils.translation import gettext_lazy as _


# Task Class for finding links & extracting text for each customer
class Echo(TimeStampedUUIDModel):
    repository = models.OneToOneField(Repository, related_name='crawler', on_delete=models.CASCADE)
    # for searching new fresh links
    discover_task = models.ForeignKey(PeriodicTask, related_name='discover_task', on_delete=models.CASCADE,
                                      null=True, blank=True, verbose_name=_("Discover Task"))
    # discover links task time interval
    discover_interval = EnumChoiceField(TimeInterval, default=TimeInterval.three_min)
    # for extracting text from founded links in repository
    extract_task = models.ForeignKey(PeriodicTask, related_name="extract_task", on_delete=models.CASCADE,
                                     null=True, blank=True, verbose_name=_("Extract Task"))
    # extract text task time interval
    extract_interval = EnumChoiceField(TimeInterval, default=TimeInterval.five_min)
    status = EnumChoiceField(TaskStatus, default=TaskStatus.active)
    title_included = models.BooleanField(default=False, verbose_name=_("Title Included"))

    @property
    def customer_name(self):
        return self.repository.customer_name()

    class Meta:
        verbose_name = 'Echo'
        verbose_name_plural = 'Echoes'

    @transaction.atomic
    def setup_tasks(self):
        # Discover Task
        self.discover_task = PeriodicTask.objects.create(
            name=f'{self.customer_name} Discover Task',
            task='discover_task',
            interval=get_time_interval(time=self.discover_interval),
            args=json.dumps([self.pkid]),
            start_time=timezone.now()
        )
        # Extract Task
        self.extract_task = PeriodicTask.objects.create(
            name=f'{self.customer_name} Extract Task',
            task='extract_task',
            interval=get_time_interval(time=self.extract_interval),
            args=json.dumps([self.pkid]),
            start_time=timezone.now(),
        )

    def __str__(self):
        return f'{self.customer_name} Echo'


# Task Class for deep finding links for each customer
class Driller(TimeStampedUUIDModel):
    repository = models.OneToOneField(Repository, related_name="driller", on_delete=models.CASCADE)
    task = models.ForeignKey(PeriodicTask, related_name="driller_task", on_delete=models.CASCADE,
                             null=True, blank=True, verbose_name=_("Driller Task"))
    interval = EnumChoiceField(TimeInterval, default=TimeInterval.one_min)
    status = EnumChoiceField(TaskStatus, default=TaskStatus.active)
    url_pattern = models.CharField(max_length=512, help_text='add replace part of search url with $182next_page281$',
                                   blank=True, verbose_name=_('URL Pattern'))
    last_page = models.CharField(max_length=512, blank=True, help_text="Last Crawled Page")
    next_page = models.CharField(max_length=512, blank=True, help_text="Next Crawl Page")
    page_count = models.IntegerField(default=0, help_text="Total Page Count")
    step_number = models.IntegerField(default=0, help_text="Current Page Number")
    title_included = models.BooleanField(default=False, verbose_name=_("Title Included"))

    @property
    def customer_name(self):
        return self.repository.customer_name()

    class Meta:
        verbose_name = "Driller"
        verbose_name_plural = "Drillers"

    @transaction.atomic
    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=f'{self.customer_name} Driller Task',
            task='driller_task',
            interval=get_time_interval(time=self.interval),
            args=json.dumps([self.pkid]),
            start_time=timezone.now(),
            # one_off=True,
        )

    def __str__(self):
        return f'{self.customer_name} Driller'
