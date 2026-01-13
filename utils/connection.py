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

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.engine import Engine


load_dotenv(override=True)

class Connections:
    def __init__(
        self,
        db_user=None,
        db_pw=None,
        db_host=None,
        db_port=None,
        db_name=None,
        redis_host=None,
        redis_port=None,
        in_process_maxsize=1000,
        in_process_ttl=300
    ):
        # Load from environment variables if not provided
        self.db_user = db_user or str(os.getenv("DB_USER"))
        self.db_pw = db_pw or str(os.getenv("DB_PW"))
        self.db_host = db_host or str(os.getenv("DB_HOST"))
        self.db_port = db_port or str(os.getenv("DB_PORT"))
        self.db_name = db_name or str(os.getenv("DB_NAME"))
        self.redis_host = redis_host or str(os.getenv("REDIS_HOST"))
        self.redis_port = redis_port or str(os.getenv("REDIS_PORT"))
        
        # Initialize connections as None (lazy loading)
        self._engine = None
        self._async_engine = None
        self._cache_redis = None
        self._async_cache_redis = None
        self._cache_inprocess = TTLCache(maxsize=in_process_maxsize, ttl=in_process_ttl)
    
    def get_db_connection(self) -> Engine:
        """Get synchronous database engine"""
        if self._engine is None:
            db_url = f"postgresql+psycopg2://{self.db_user}:{self.db_pw}@{self.db_host}:{self.db_port}/{self.db_name}"
            self._engine = create_engine(db_url)
        return self._engine
    
    def get_async_db_connection(self) -> AsyncEngine:
        """Get asynchronous database engine"""
        if self._async_engine is None:
            async_db_url = f"postgresql+asyncpg://{self.db_user}:{self.db_pw}@{self.db_host}:{self.db_port}/{self.db_name}"
            self._async_engine = create_async_engine(async_db_url)
        return self._async_engine
    
    def get_redis_connection(self) -> redis.Redis:
        """Get synchronous Redis connection"""
        if self._cache_redis is None:
            self._cache_redis = redis.Redis(host=self.redis_host, port=self.redis_port)
        return self._cache_redis
    
    def get_async_redis_connection(self) -> redis.asyncio.Redis:
        """Get asynchronous Redis connection"""
        if self._async_cache_redis is None:
            self._async_cache_redis = redis.asyncio.Redis(host=self.redis_host, port=self.redis_port)
        return self._async_cache_redis
    
    def get_inprocess_cache(self) -> TTLCache:
        """Get in-process TTL cache"""
        return self._cache_inprocess
    
    def close(self):
        """Close all synchronous connections"""
        if self._engine:
            self._engine.dispose()
        if self._cache_redis:
            self._cache_redis.close()
    
    async def aclose(self):
        """Close all asynchronous connections"""
        if self._async_engine:
            await self._async_engine.dispose()
        if self._async_cache_redis:
            await self._async_cache_redis.close()
