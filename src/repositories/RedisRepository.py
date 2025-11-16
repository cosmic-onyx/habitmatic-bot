import redis
import json

from settings.config import env_settings as settings


class RedisRepository:
    def get_redis_client(self):
        return redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )

    def set_data(self, key, value):
        redis_client = self.get_redis_client()
        redis_client.set(key, json.dumps(value))

        redis_client.close()

    def get_data(self, key):
        redis_client = self.get_redis_client()
        value = redis_client.get(key)

        redis_client.close()
        return json.loads(value)