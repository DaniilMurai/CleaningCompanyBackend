import asyncio

from redis import asyncio as aioredis

from config import settings

redis = aioredis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
)


async def listen_to_redis():
    print("hello")
    pubsub = redis.pubsub()
    await pubsub.subscribe("export_report")
    async for message in pubsub.listen():
        print(message)
        if message['type'] == 'message':
            break


async def test_redis():
    listener_task = asyncio.create_task(listen_to_redis())

    await asyncio.sleep(0.1)

    await redis.publish("export_report", "status_updated")
    await listener_task

    await redis.aclose()

    # redis_set = await redis.set("myKey", "Hello Redis")
    # print("redis_set: ", redis_set)
    #
    # redis_get = await redis.get("myKey")
    # print("redis_get: ", redis_get)
    #
    # redis_delete = await redis.delete("myKey")
    # print("redis_delete: ", redis_delete)
    #
    # redis_close = await redis.aclose()
    #
    # print("redis_close: ", redis_close)


if __name__ == '__main__':
    asyncio.run(test_redis())
