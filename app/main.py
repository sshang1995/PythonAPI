from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor # this will give you column name when fetch data from DB
import time 
from . import models
from .database import  create_db_and_tables
from .routers import post, user, auth, vote
from . import config
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Changeme04!', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB connect successfully!")
#         break
#     except Exception as err: 
#         print(f"DB connect failed! {err}")
#         time.sleep(3)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# @app.get("/posts", response_model=List[Post])
# async def get(session: SessionDep):
#     # cursor.execute("""Select * from post""")
#     # posts = cursor.fetchall()
#     # if not posts: 
#     #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Did not find any post")
#     # return {"message":posts}
#     posts = session.exec(select(models.Posts)).all()
#     return posts

# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
# def create_posts(post: models.Posts,session: SessionDep):
#     # # sanitize the variables by passing %s
#     # cursor.execute("""Insert into post(title, content, published) Values(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
#     # new_post = cursor.fetchone()
#     # # need to commit to save to DB
#     # conn.commit()
#     # return {"message":new_post}
#     session.add(post)
#     session.commit()
#     session.refresh(post)
#     return post


# @app.get("/posts/{id}", response_model=Post)
# def get_post(id:int, session: SessionDep):
#     # cursor.execute("""Select * from post where id = %s""", (str(id)))
#     # post = cursor.fetchone()
#     # if not post: 
#     #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Did not find post with id = {id}")
#     # return {"post_detail":post}
#     post = session.get(models.Posts, id)
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Did not find post with id = {id}")
#     return post 

    

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int, session: SessionDep):
#     # cursor.execute("""Delete from post where id = %s returning *""", (str(id)))
#     # deleted = cursor.fetchone()
#     # conn.commit()
#     # if deleted is None: 
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

#     # return Response(status_code = status.HTTP_204_NO_CONTENT)
#     post = session.get(models.Posts, id)
#     if not post: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#     session.delete(post)
#     session.commit()
#     return {"ok": True}


# @app.put("/posts/{id}", response_model=Post)
# def update_post(id:int, post: models.Posts, session: SessionDep): 
#     # cursor.execute("""Update post SET title = %s, content=%s, published=%s Where id=%s RETURNING *""", (post.title, post.content, post.published, id))
#     # updated = cursor.fetchone()
#     # conn.commit()
#     # if not updated:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#     # return {"data":updated}
#     exist_post = session.get(models.Posts, id)
#     if not exist_post: 
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#     exist_post.title = post.title
#     exist_post.content = post.content
#     exist_post.published = post.published

#     session.add(exist_post)
#     session.commit()
#     session.refresh(exist_post)
#     return exist_post

# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
# def create_user(user: UserCreate, session: SessionDep): 
#     # hash password 
#     hashed_password = hash(user.password)
#     user.password = hashed_password
#     new_user = models.Users(**user.dict())
#     session.add(new_user)
#     session.commit()
#     session.refresh(new_user)
#     return new_user


# @app.get("/users/{id}", response_model=UserResponse)
# def get_post(id:int, session: SessionDep):
#     user = session.get(models.Users, id)
#     if not user:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Did not find user with id = {id}")
#     return user 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)