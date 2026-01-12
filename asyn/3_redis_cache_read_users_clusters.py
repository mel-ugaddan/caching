from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Mapped
from typing import List
from sqlalchemy import select
import asyncio
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
import uvloop
import redis.asyncio as redis
import time
from redis.asyncio.cluster import RedisCluster
from redis.cluster import ClusterNode
import redis
import orjson
from utils.model import User
import os
from utils.model import User
from utils.constants import USER_POPULATION

serializer_fn   = orjson.dumps
deserializer_fn = orjson.loads

# Libuv Event loop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


DB_USER     = str(os.getenv("DB_USER"))
DB_PW       = str(os.getenv("DB_PW"))
DB_HOST     = str(os.getenv("DB_HOST"))
DB_PORT     = str(os.getenv("DB_PORT"))
DB_NAME     = str(os.getenv("DB_NAME"))
REDIS_HOST  = str(os.getenv("REDIS_HOST"))
REDIS_PORT  = str(os.getenv("REDIS_PORT"))

db_url      = f"postgresql+asyncpg://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine      = create_async_engine(
    db_url
)

AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base    = declarative_base()


nodes           = [
    ClusterNode(REDIS_HOST, 7001),
    ClusterNode(REDIS_HOST, 7002),
    ClusterNode(REDIS_HOST, 7003)
]
cache_redis = RedisCluster(
    startup_nodes=nodes,
    decode_responses=True
)

async def generate_cache(cache_redis : redis.Redis) -> None:
    async with AsyncSessionLocal() as session:
        query_result = await session.execute(select(User))
        users = query_result.scalars().all()
        for user in users:
            if user.id > 10:
                break
            cache_key ="user:{"+str(user.id)+"}"
            data = {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "posts": [ 
                    {"id": post.id, "title": post.title, "text": post.text } for post in user.posts
                ]
            }

            await cache_redis.set(cache_key, serializer_fn(data), ex=240)

async def fetch_user(uid: int) -> dict:
    cache_key ="user:{"+str(uid)+"}"
    cache_data  = await cache_redis.get(cache_key)
    if cache_data is None:
        async with AsyncSessionLocal() as session:
            result  = await session.execute(select(User).where(User.id == uid))
            db_user = result.scalar_one()
        return {
            'id': db_user.id,
            'name': db_user.name,
            'age': db_user.age,
            'posts' : [
                {'id' : post.id, "title": post.title, "text": post.text } for post in db_user.posts
            ]
        }
    else:
        user_data = deserializer_fn(cache_data)
        return {
            'id'    : user_data['id'],
            'name'  : user_data['name'],
            'age'   : user_data['age'],
            'posts' : user_data['posts']
        }
        
async def main() -> None:
    await generate_cache(cache_redis)
    start       = time.perf_counter()
    all_users   = []
    # # Create a list of coroutines
    tasks = [fetch_user(uid) for uid in range(1, USER_POPULATION + 1)]
    all_users = await asyncio.gather(*tasks)
    # pipe = cache_redis.pipeline()
    # for uid in range(1, USER_POPULATION + 1):
    #     key ="user:{"+str(uid)+"}"
    #     pipe.get(key)  # redis-py routes by slot
    # all_users = await pipe.execute()

    end     = time.perf_counter()
    elapsed = end - start
    rps     = len(all_users) / elapsed
    print(f"")
    print(f"Redis read          :")
    print(f"Total time          : {elapsed/len(all_users):.10f} s")
    print(f"Throughput          : {rps:.0f} req/s")
    await cache_redis.aclose()
if __name__ == "__main__":
    asyncio.run(main())


