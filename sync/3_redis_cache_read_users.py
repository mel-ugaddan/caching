import sys  
root = '/root/udemy/websocket_from_scratch/system_design_concepts/cache/'
sys.path.append(root) 

from sqlalchemy.orm import Session
import orjson
import time
from sqlalchemy import select
from utils.connection import engine,cache_redis
from utils.model import User
from utils.helpers import generate_redis_cache
from utils.constants import USER_POPULATION
from utils.helpers import display_statistics

generate_redis_cache(engine, cache_redis)

start = time.perf_counter()
all_users = []
for uid in range(1,USER_POPULATION+1):
    cache_key = f"user-{uid}"
    cache_data = cache_redis.get(cache_key)
    if cache_data is None:
        with Session(engine) as session:
            stmt    = select(User).where(User.id == str(uid))
            db_user = session.execute(stmt).scalar_one()
        all_users.append({
            'id': db_user.id,
            'name': db_user.name,
            'age': db_user.age
        })
    else:
        user_data = orjson.loads(cache_data)
        all_users.append({
            'id': user_data['id'],
            'name': user_data['name'],
            'age': user_data['age']
        })
        
end     = time.perf_counter()
display_statistics(start,end,len(all_users))
