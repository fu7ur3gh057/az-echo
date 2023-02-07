import datetime

from django.db.models import Q
from django.utils import timezone
from celery import shared_task

from apps.payments.models import Subscription
from client.redis_client import RedisClient
from celery.utils.log import get_task_logger
from django.conf import settings

from constants import SUBSCRIPTION_CHECKER_PRIORITY

logger = get_task_logger(__name__)

redis_client = RedisClient()


@shared_task(priority=SUBSCRIPTION_CHECKER_PRIORITY, name="subscription_checker_task")
def subscription_checker_task():
    lock_id = f'lock_subscription'
    current_time = timezone.now().isoformat()
    with redis_client.locker(lock_id=lock_id) as acquired:
        if acquired is None or acquired is False:
            redis_client.set_key(key=lock_id, value=current_time)
            today = datetime.date.today()
            # Active subscriptions
            subscriptions = Subscription.objects.all().filter(Q(type=1) & Q(expire_date__lt=today))
            for subscription in subscriptions:
                # Subscription expire date ended and this object not canceled
                subscription.type = 2
                subscription.save()
            redis_client.delete_key(key=lock_id)
