from sqlalchemy.orm import Session
import random
from utils.connection import engine
from utils.model import Base, User, Post
from utils.constants import USER_POPULATION,NO_OF_POSTS

Base.metadata.drop_all(engine) 
Base.metadata.create_all(engine)

with Session(engine) as session:
    users = [User(name=f"User {index}",age=random.randint(20, 40)) for index in range(USER_POPULATION)]
    session.add_all(users)
    session.flush() 
    
    posts = []
    for index in range(NO_OF_POSTS):
        rand_number = random.randint(0, USER_POPULATION-1)
        user_object = users[rand_number]
        posts.append(Post(title=f"Title {index}", text=f"Post Content {index}", user=user_object))
        
    session.add_all(posts)
    session.commit()
    