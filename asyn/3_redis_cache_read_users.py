import sys  
root = '/root/udemy/websocket_from_scratch/system_design_concepts/cache/'
sys.path.append(root)

from sqlalchemy import select
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uvloop
import time
from utils.connection import async_engine,async_cache_redis
from utils.model import User
from utils.helpers import generate_redis_cache_async
from utils.constants import USER_POPULATION
from utils.helpers import display_statistics

import orjson
serializer_fn   = orjson.dumps
deserializer_fn = orjson.loads

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def fetch_user(uid: int, async_engine ) -> dict:
    cache_key   = f"user-{uid}"
    cache_data  = await async_cache_redis.get(cache_key)
    if cache_data is None:
        async with AsyncSession(async_engine) as session:
            result  = await session.execute(select(User).where(User.id == uid))
            db_user = result.scalar_one()
        return {
            'id': db_user.id,
            'name': db_user.name,
            'age': db_user.age
        }
    else:
        user_data = deserializer_fn(cache_data)
        return {
            'id'    : user_data['id'],
            'name'  : user_data['name'],
            'age'   : user_data['age']
        }

async def main() -> None:
    await generate_redis_cache_async(async_engine,async_cache_redis)
    start           = time.perf_counter()
    all_users       = []
    
    for uid in range(1, USER_POPULATION + 1):
        user = await fetch_user(uid, async_engine)
        all_users.append(user)
        
    end     = time.perf_counter()
    display_statistics(start,end,len(all_users))
    
if __name__ == "__main__":
    asyncio.run(main())


