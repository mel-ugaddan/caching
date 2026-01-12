import sys  
root = '/root/udemy/websocket_from_scratch/system_design_concepts/cache/'
sys.path.append(root) 
from utils.constants import IN_PROCESS_MAXSIZE,IN_PROCESS_TTL

from sqlalchemy import create_engine
import redis
from cachetools import TTLCache
from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv

load_dotenv(override=True)

DB_USER     = str(os.getenv("DB_USER"))
DB_PW       = str(os.getenv("DB_PW"))
DB_HOST     = str(os.getenv("DB_HOST"))
DB_PORT     = str(os.getenv("DB_PORT"))
DB_NAME     = str(os.getenv("DB_NAME"))
REDIS_HOST  = str(os.getenv("REDIS_HOST"))
REDIS_PORT  = str(os.getenv("REDIS_PORT"))

db_url      = f"postgresql+psycopg2://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(
    db_url
)

cache_redis         = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
async_cache_redis   = redis.asyncio.Redis(host=REDIS_HOST,port=REDIS_PORT)
cache_inprocess     = TTLCache(maxsize=IN_PROCESS_MAXSIZE, ttl=IN_PROCESS_TTL) 

async_db_url    = f"postgresql+asyncpg://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
async_engine    = create_async_engine(
    async_db_url
)

