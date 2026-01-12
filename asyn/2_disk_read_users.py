import sys  
root = '/root/udemy/websocket_from_scratch/system_design_concepts/cache/'
sys.path.append(root) 
from sqlalchemy import select
import asyncio

import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from utils.connection import async_engine
from utils.model import User
from utils.constants import USER_POPULATION

import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

AsyncSessionLocal   = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def fetch_user(uid : int ) -> dict:
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.id == uid)
        result = await session.execute(stmt)
        db_user = result.scalar_one()
        return {"id": db_user.id, "name": db_user.name, "age": db_user.age}

async def main() -> None:
    start       = time.perf_counter()
    all_users   = []
    for uid in range(1, USER_POPULATION+1):
        db_user = await fetch_user(uid)
        all_users.append(db_user)
    end     = time.perf_counter()
    elapsed = end - start
    rps     = len(all_users) / elapsed

    print(f"Direct disk read    :")
    print(f"Total time          : {elapsed/len(all_users):.10f} s")
    print(f"Throughput          : {rps:.0f} req/s")

if __name__ == "__main__":
    asyncio.run(main())