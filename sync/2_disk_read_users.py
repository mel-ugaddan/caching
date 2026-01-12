import sys  
root = '/root/udemy/websocket_from_scratch/system_design_concepts/cache/'
sys.path.append(root) 

from sqlalchemy.orm import Session
import time
from sqlalchemy import select
from utils.connection import engine
from utils.model import User
from utils.constants import USER_POPULATION

start               = time.perf_counter()
all_users           = []

for uid in range(1,USER_POPULATION+1):
    with Session(engine) as session:
        stmt    = select(User).where(User.id == str(uid))
        db_user = session.execute(stmt).scalar_one()
        all_users.append({
            'id': db_user.id,
            'name': db_user.name,
            'age': db_user.age
        })  
        
end     = time.perf_counter()
elapsed = end - start
rps     = len(all_users) / elapsed

print(f"")
print(f"Direct disk read    :")
print(f"Total time          : {elapsed/len(all_users):.10f} s")
print(f"Throughput          : {rps:.0f} req/s")
