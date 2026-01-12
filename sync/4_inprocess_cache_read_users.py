import sys  
root = '/root/udemy/websocket_from_scratch/system_design_concepts/cache/'
sys.path.append(root) 

from sqlalchemy.orm import Session
import time
from sqlalchemy import select
from utils.connection import engine,cache_inprocess
from utils.model import User
from utils.helpers import generate_inprocess_cache
from utils.constants import USER_POPULATION

generate_inprocess_cache(engine, cache_inprocess)
start = time.perf_counter()
all_users = []

for uid in range(1, USER_POPULATION+1):
    cache_key = f"user-{uid}"
    cache_data = cache_inprocess.get(cache_key)
    if cache_data is None:
        with Session(engine) as session:
            stmt    = select(User).where(User.id == uid)
            db_user = session.execute(stmt).scalar_one()
        user_data = {
            'id': db_user.id,
            'name': db_user.name,
            'age': db_user.age
        }
    else:
        user_data = cache_data
    all_users.append(user_data)

end     = time.perf_counter()
elapsed = end - start
rps = len(all_users) / elapsed
print(f"")
print(f"In-process          :")
print(f"Total time          : {elapsed/len(all_users):.10f} s")
print(f"Throughput          : {rps:.0f} req/s")

