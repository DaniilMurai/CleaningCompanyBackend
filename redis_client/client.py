from redis import asyncio as aioredis

from config import settings

redis = aioredis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
)
