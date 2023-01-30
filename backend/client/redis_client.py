import redis
from contextlib import contextmanager
from redis.client import Redis
from django.conf import settings


class RedisClient:
    def __init__(self):
        self._redis_client = redis.StrictRedis(host=f"{settings.REDIS_HOST}",
                                               port=settings.REDIS_PORT,
                                               db=1,
                                               decode_responses=True)

    @contextmanager
    def locker(self, lock_id: str):
        try:
            acquired = self._redis_client.get(lock_id)
            yield acquired
        finally:
            return 'done'

    def set_key(self, key: str, value: str):
        self._redis_client.set(key, value)

    def delete_key(self, key: str):
        self._redis_client.delete(key)

    def key_exists(self, key: str):
        does_exist = self._redis_client.exists(key)
        if does_exist == 0:
            return False
        else:
            return True

    def populate_list(self, key: str, value_list: list):
        if not self.key_exists(key=key) and len(value_list) != 0:
            for value in value_list:
                self._redis_client.lpush(key, value)

    # Push to list
    def push(self, key: str, value):
        self._redis_client.lpush(key, value)

    def flush_keys(self, key):
        if self.key_exists(key=key):
            self._redis_client.delete(*key)

    def flush_all(self):
        self._redis_client.flushall()

# redis_client = redis.StrictRedis(host=f"{settings.REDIS_HOST}", port=settings.REDIS_PORT, db=1, decode_responses=True)


# @contextmanager
# def redis_locker(lock_id):
#     try:
#         acquired = redis_client.get(lock_id)
#         yield acquired
#     finally:
#         return 'done'
#
#
# def set_redis_key(key, value):
#     redis_client.set(key, value)
#
#
# def delete_redis_key(key):
#     redis_client.delete(key)
#
#
# # Key exists
# def key_exists(key: str):
#     does_exist = redis_client.exists(key)
#     if does_exist == 0:
#         return False
#     else:
#         return True
#
#
# # Populate blacklist
# def populate_blacklist(key: str, blacklist: list):
#     if not key_exists(key=key):
#         for value in blacklist:
#             redis_client.lpush(key, value)
#
#
# # Remove blacklist
# def flush_keys(key: str):
#     if key_exists(key=key):
#         redis_client.delete(*key)
