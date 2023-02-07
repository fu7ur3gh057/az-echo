from celery import shared_task
from django.db.models import Q
from django.utils import timezone
from celery.utils.log import get_task_logger
from django.conf import settings

from apps.crawlers.models import Echo, Driller
from apps.synthesis.models import Synthesis
from constants import DISCOVER_PRIORITY, EXTRACT_PRIORITY, DRILLER_PRIORITY
from services.discover_service import DiscoverService
from services.drill_service import DrillerService
from services.extract_service import ExtractService
from client.redis_client import RedisClient
from utils.text_util import text_is_empty

logger = get_task_logger(__name__)

redis_client = RedisClient()


@shared_task(bind=True, priority=DISCOVER_PRIORITY, name="discover_task")
def discover_task(self, echo_id):
    lock_id = f'lock_discover_{echo_id}'
    current_time = timezone.now().isoformat()
    with redis_client.locker(lock_id=lock_id) as acquired:
        if acquired is None or acquired is False:
            # set Redis lock key
            redis_client.set_key(key=lock_id, value=current_time)
            echo = Echo.objects.get(pkid=echo_id)
            repo = echo.repository
            customer = repo.customer
            lang = customer.lang
            blacklist_id = f'blacklist_{repo.pkid}'
            blacklist = repo.blacklist
            # populate blacklist to redis
            redis_client.populate_list(key=blacklist_id, value_list=blacklist)
            service = DiscoverService(domain=customer.domain, search_url=customer.search_url,
                                      negative_tags=customer.negative_path_tag, blacklist=blacklist, lang=lang)
            # start discover service
            logger.info('start service')
            data = service.start()
            to_blacklist = data['blacklist']
            new_links = data['new_links']
            # create synthesis objects
            if new_links is not None and len(new_links) != 0:
                for link in new_links:
                    Synthesis.objects.create(repository=repo, link=link, lang=lang)
            # save to Database and Redis
            if to_blacklist is not None:
                for link in to_blacklist:
                    if link not in blacklist:
                        blacklist.append(link)
                        redis_client.push(key=blacklist_id, value=link)
            repo.blacklist = blacklist
            repo.save()
            # delete Redis lock key
            redis_client.delete_key(key=lock_id)
            return f'DISCOVER TASK :: {customer.domain} to blacklist - {len(to_blacklist)}, to crawl - {len(new_links)}'


@shared_task(bind=True, priority=EXTRACT_PRIORITY, name="extract_task")
def extract_task(self, echo_id):
    lock_id = f"lock_extract_{echo_id}"
    current_time = timezone.now().isoformat()
    with redis_client.locker(lock_id=lock_id) as acquired:
        if acquired is None or acquired is False:
            # set Redis lock key
            redis_client.set_key(key=lock_id, value=current_time)
            echo = Echo.objects.get(pkid=echo_id)
            repo = echo.repository
            customer = repo.customer
            lang = customer.lang
            synthesis_list = Synthesis.objects.filter(Q(repository=repo) & Q(crawled_status=False)).all()
            counter = 0
            for data in synthesis_list:
                service = ExtractService(url=data.link, lang=lang, negative_words=customer.negative_words)
                text = service.start()
                data.crawled_status = True
                if text_is_empty(text):
                    data.error_status = True
                    data.save()
                else:
                    counter += 1
                    data.text = text
                    data.error_status = False
                    data.save()
            redis_client.delete_key(key=lock_id)
            return f"EXTRACT TASK :: text - {counter}"


@shared_task(bind=True, priority=DRILLER_PRIORITY, name="driller_task")
def driller_task(self, driller_id):
    lock_id = f"lock_extract_{driller_id}"
    current_time = timezone.now().isoformat()
    with redis_client.locker(lock_id=lock_id) as acquired:
        if acquired is None or acquired is False:
            # set Redis lock key
            redis_client.set_key(key=lock_id, value=current_time)
            driller = Driller.objects.get(pkid=driller_id)
            repo = driller.repository
            customer = repo.customer
            lang = customer.lang
            blacklist_id = f'blacklist_{repo.pkid}'
            blacklist = repo.blacklist
            redis_client.populate_list(key=blacklist_id, value_list=blacklist)
            service = DrillerService(domain=customer.domain, url_pattern=driller.url_pattern,
                                     page_count=driller.page_count, negative_tags=repo.negative_path_tag,
                                     blacklist=blacklist)
            data = service.start(step_number=driller.step_number)
            links = data['links']
            driller.step_number = data['step_number']
            last_page = data['last_page']
            driller.last_page = last_page
            driller.save()
            if len(links) == 0:
                return f"DRILLER TASK :: No new links at page {last_page}"
            for link in links:
                blacklist.append(link)
                redis_client.push(key=blacklist_id, value=link)
                Synthesis.objects.create(repository=repo, link=link, lang=lang)
            redis_client.delete_key(key=lock_id)
            return f"DRILLER TASK :: {last_page}, founded links - {len(links)}"
