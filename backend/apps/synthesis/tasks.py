import time
from contextlib import contextmanager

import redis
from celery import shared_task
from django.db.models import Q
from django.utils import timezone

from apps.synthesis.api import voicen_api
from apps.synthesis.models import Synthesis, Generator
from celery.utils.log import get_task_logger
from django.conf import settings
from constants import GENERATOR_PRIORITY
from client.redis_client import RedisClient

logger = get_task_logger(__name__)

redis_client = RedisClient()


@shared_task(name='generator_task', priority=GENERATOR_PRIORITY)
def generator_task():
    lock_id = 'lock_generator'
    current_time = timezone.now().isoformat()
    with redis_client.locker(lock_id=lock_id) as acquired:
        if acquired is None or acquired is False:
            redis_client.set_key(key=lock_id, value=current_time)
            generator = Generator.objects.all().first()
            timeout = generator.generation_timeout
            synthesis_list = Synthesis.objects.all().filter(
                Q(job_id=None) & Q(crawled_status=True) & Q(error_status=False)
            ).all()[0:generator.generation_count]
            if len(synthesis_list) == 0:
                return f'There are no synthesis jobs'
            for synthesis in synthesis_list:
                try:
                    done_status = False
                    logger.info(f'send text to synthesis {synthesis.link}')
                    job_id = voicen_api.post_synthesis(text=synthesis.text, lang=synthesis.lang)
                    synthesis.job_id = job_id
                    # Wait until status is True
                    while done_status is False:
                        logger.info(f'waiting success status, sleep {timeout}...')
                        time.sleep(timeout)
                        # Get job status
                        response = voicen_api.check_synthesis_status(job_id=job_id)
                        done_status = response
                except Exception as ex:
                    logger.info(ex)
                finally:
                    synthesis.save()
            redis_client.delete_key(lock_id)
            return f'Synthesis Generator Task: complete'
