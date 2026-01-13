import sys  
root = '/root/udemy/websocket_from_scratch/system_design_concepts/cache/'
sys.path.append(root) 

import asyncio
from sqlalchemy import text
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import uvloop

from utils.connection import Connections
from utils.constants import USER_POPULATION
from utils.helpers import display_statistics

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async_engine = Connections.get_async_db_connection()
AsyncSessionLocal   = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def fetch_user(uid : int) -> dict:
    async with async_engine.connect() as connection:
        stmt        = text("SELECT id, name, age FROM users WHERE id = :uid")
        result      = await connection.execute(stmt, {"uid": uid})
        db_user_row = result.fetchone()
        if db_user_row is None:
            raise Exception(f"User with ID {uid} not found.")
        return {
            "id": db_user_row.id, 
            "name": db_user_row.name,
            "age": db_user_row.age
        }

async def main() -> None:
    start       = time.perf_counter()
    all_users   = []
    for uid in range(1, USER_POPULATION+1):
        db_user = await fetch_user(uid)
        all_users.append(db_user)

    end     = time.perf_counter()
    display_statistics(start,end,len(all_users))
    
if __name__ == "__main__":
    asyncio.run(main())