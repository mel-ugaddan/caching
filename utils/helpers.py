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

async def generate_redis_cache_async(engine : Engine, cache_redis : redis.Redis) -> None:
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
            cache_redis.set(cache_key, orjson.dumps(data), ex=REDIS_TTL)

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
