import json
import redis
from typing import Any, Optional

from app.core.config import settings


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            username=settings.redis_username,
            password=settings.redis_password,
            ssl=settings.redis_ssl,
            decode_responses=True,
        )

    def get(self, key: str) -> Optional[Any]:
        value = self.client.get(key)
        if value is None:
            if key not in {"cache:hits", "cache:misses"}:
                self.client.incr("cache:misses")
            return None
        if key not in {"cache:hits", "cache:misses"}:
            self.client.incr("cache:hits")
        return json.loads(value)

    def set(self, key: str, value: Any, ttl: int):
        self.client.setex(
            key,
            ttl,
            json.dumps(value)
        )

    def delete(self, key: str):
        self.client.delete(key)

    def ping(self) -> bool:
        try:
            return self.client.ping()
        except Exception:
            return False

    def get_metrics(self) -> dict:
        hits = int(self.client.get("cache:hits") or 0)
        misses = int(self.client.get("cache:misses") or 0)

        total_requests = hits + misses
        hit_rate = (
            (hits / total_requests) * 100
            if total_requests > 0
            else 0.0
        )

        return {
            "hits": hits,
            "misses": misses,
            "total_requests": total_requests,
            "hit_rate": round(hit_rate, 2),
        }


redis_client = RedisClient()