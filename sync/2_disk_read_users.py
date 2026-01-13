import sys  
root = '/root/udemy/websocket_from_scratch/system_design_concepts/cache/'
sys.path.append(root) 

from sqlalchemy.orm import Session
import time
from sqlalchemy import select
from utils.connection import Connections
from utils.model import User
from utils.constants import USER_POPULATION
from utils.helpers import display_statistics

start               = time.perf_counter()
all_users           = []

engine = Connections.get_db_connection()

for uid in range(1,USER_POPULATION+1):
    with Session(engine) as session:
        stmt = select(User).where(User.id == str(uid))
        db_user = (session.execute(stmt)).scalars().one_or_none()
        all_users.append({
            'id': db_user.id,
            'name': db_user.name,
            'age': db_user.age
        })  
        
end     = time.perf_counter()
display_statistics(start,end,len(all_users))