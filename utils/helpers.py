import redis
from sqlalchemy.orm import Session
from utils.model import User
import orjson
from cachetools import TTLCache
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import orjson
from utils.constants import REDIS_TTL

serializer_fn   = orjson.dumps
deserializer_fn = orjson.loads

def generate_redis_cache(engine : Engine, cache_redis : redis.Redis) -> None:
    with Session(engine) as session:
        users = session.query(User)
        for user in users:
            cache_key = f"user-{user.id}"
            data = {
                "id": user.id,
                "name": user.name,
                "age": user.age
            }
            cache_redis.set(cache_key, orjson.dumps(data), ex=REDIS_TTL)
            
def generate_inprocess_cache(engine : Engine, cache_inprocess : TTLCache ) -> None:
    with Session(engine) as session:
        users = session.query(User)
        for user in users:
            cache_key = f"user-{user.id}"
            data = {
                "id": user.id,
                "name": user.name,
                "age": user.age
            }
            cache_inprocess[cache_key] = data

async def generate_redis_cache_async(engine: Engine, cache_redis: redis.asyncio.Redis) -> None:
    async with AsyncSession(engine) as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all() 
        for user in users:
            cache_key = f"user-{user.id}"
            data = {
                "id": user.id,
                "name": user.name,
                "age": user.age
            }
            await cache_redis.set(cache_key, orjson.dumps(data), ex=REDIS_TTL) 
            
async def generate_aredis_cache_async(engine : Engine, cache_redis : redis.asyncio.Redis) -> None:
    async with AsyncSession(engine) as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        for user in users:
            cache_key = f"user-{user.id}"
            data = {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "posts": [ 
                    {"id": post.id, "title": post.title, "text": post.text } for post in user.posts
                ]
            }
            await cache_redis.set(cache_key, orjson.dumps(data), ex=REDIS_TTL)
            
def display_statistics(start : float, end : float, no_of_items : int ) -> None:
    elapsed = end - start
    rps     = len(no_of_items) / elapsed
    time_per_request_us = (elapsed / len(no_of_items)) * 1_000_000 

    print(f"Direct disk read    :")
    print(f"Total time          : {elapsed:.10f} s")
    print(f"Time per request    : {time_per_request_us:.2f} µs")
    print(f"Throughput          : {rps:.0f} req/s")
    
