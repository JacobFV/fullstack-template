from redis import Redis
# from app.core.config import settings
from app.core.shared_resources import get_redis_connection, settings


def get_redis_connection() -> Redis:
    return Redis.from_url(settings.REDIS_URL)
