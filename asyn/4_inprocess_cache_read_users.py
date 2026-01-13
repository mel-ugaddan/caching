import sys  
root = '/root/udemy/websocket_from_scratch/system_design_concepts/cache/'
sys.path.append(root)

from cachetools import TTLCache
import time
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio

from utils.connection import Connections
from utils.model import User
from utils.constants import USER_POPULATION
from utils.helpers import display_statistics
from utils.helpers import generate_inprocess_cache_async

async_engine = Connections.get_async_db_connection()
cache_inprocess = Connections.get_inprocess_cache()

AsyncSessionLocal = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def generate_cache(cache_inprocess : TTLCache) -> None:
    async with AsyncSessionLocal() as session:
        query_result    = await session.execute(select(User))
        users           = query_result.scalars().all()
        for user in users:
            cache_key = f"user-{user.id}"
            data = {
                "id": user.id,
                "name": user.name,
                "age": user.age
            }
            cache_inprocess[cache_key] = data
          

async def get_user_data(uid : int):
    cache_key = f"user-{uid}"
    cache_data = cache_inprocess.get(cache_key)
    if cache_data is None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.id == uid))  
            db_user = result.scalar_one()              
            user_data = {
                'id': db_user.id,
                'name': db_user.name,
                'age': db_user.age
            }
    else:
        user_data = cache_data
    return user_data  
        
async def main()-> None:  
    await generate_inprocess_cache_async(cache_inprocess)
    start               = time.perf_counter()
    all_users           = []
    for uid in range(1, USER_POPULATION+1):
        user_data = await get_user_data(uid)
        all_users.append(user_data)

    end     = time.perf_counter()
    display_statistics(start,end,len(all_users))
    
if __name__ == "__main__":
    asyncio.run(main())