from functools import cache
import aio_pika
from app.core.config import settings


@cache
async def get_aoimq_connection() -> aio_pika.Connection:
    return await aio_pika.connect_robust(settings.RABBITMQ_URL, durable=True)


@cache
async def get_aoimq_channel() -> aio_pika.Channel:
    return await get_aoimq_connection().channel()
