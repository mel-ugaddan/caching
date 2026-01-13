import sys  
root = '/root/udemy/websocket_from_scratch/system_design_concepts/cache/'
sys.path.append(root) 

from sqlalchemy.orm import Session
import time
from utils.connection import Connections
from utils.constants import USER_POPULATION
from utils.helpers import display_statistics
from sqlalchemy import text

start               = time.perf_counter()
all_users           = []

engine = Connections.get_db_connection()
for uid in range(1,USER_POPULATION+1):
    with Session(engine) as session:
        stmt = text("SELECT id, name, age FROM users WHERE id = :uid")
        result = session.execute(stmt, {"uid": uid}).mappings().one_or_none()
        all_users.append({
            "id": result["id"],
            "name": result["name"],
            "age": result["age"],
        })

    
end     = time.perf_counter()
display_statistics(start,end,len(all_users))
