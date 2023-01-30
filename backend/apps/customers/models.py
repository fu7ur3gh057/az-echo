import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Customer(TimeStampedUUIDModel):
    LANGUAGE_CHOICES = (
        (None, _('Choose language')),
        ('az', 'Azərbaycan'),
        ('tr', 'Türkçe'),
        ('ru', 'Русский'),
        ('en', 'English'),
    )
    user = models.OneToOneField(User, related_name='customer', on_delete=models.CASCADE, null=True)
    # Company name: Report
    name = models.CharField(max_length=70, blank=False)
    # Domain name : https://www.report.az/
    domain = models.CharField(verbose_name=_("Domain Url"), max_length=512, blank=False)
    # Search Url : https://www.report.az/sonxeberler/
    search_url = models.CharField(verbose_name=_("Search Url"), max_length=512, blank=False)
    lang = models.CharField(verbose_name=_("Language"), max_length=3, blank=False, choices=LANGUAGE_CHOICES)
    # negative URL Path that will ignore, like email-verification314121dgs13
    negative_path_tag = ArrayField(models.CharField(max_length=512, blank=True),
                                   verbose_name=_("Negative Path TAG"),
                                   null=True)
    # negative words in text, like Yuxari or -FOTO
    negative_words = ArrayField(models.CharField(max_length=512, blank=True, null=True),
                                verbose_name=_("Negative Words"),
                                null=True)
    # For Javascript Widget, and Rest API
    api_token = models.UUIDField(blank=False, null=True, max_length=50, default=uuid.uuid4)

    def __str__(self):
        return self.name


class Repository(TimeStampedUUIDModel):
    customer = models.OneToOneField(Customer, related_name='repository', on_delete=models.CASCADE)
    # All founded links, no matter error status or no
    blacklist = ArrayField(models.CharField(max_length=512), verbose_name=_("Black List"), null=True, blank=True)

    class Meta:
        verbose_name = 'Repository'
        verbose_name_plural = 'Repositories'

    def customer_name(self):
        return self.customer.name

    def __str__(self):
        return f'{self.customer.name} Repository'
