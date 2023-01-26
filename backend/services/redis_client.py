import redis

from redis.client import Redis
from django.conf import settings

redis_client = redis.StrictRedis(host=f"{settings.REDIS_HOST}", port=settings.REDIS_PORT, db=1, decode_responses=True)


# Key exists
def key_exists(key: str):
    does_exist = redis_client.exists(key)
    if does_exist == 0:
        return False
    else:
        return True


# Populate blacklist
def populate_blacklist(key: str, blacklist: list):
    if not key_exists(key=key):
        for value in blacklist:
            redis_client.lpush(key, value)


# Remove blacklist
def flush_keys(key: str):
    if key_exists(key=key):
        redis_client.delete(*key)
