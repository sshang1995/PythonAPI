from .. import models
from ..database import SessionDep
from sqlmodel import select
from ..schemas import Post
from ..util import hash
from .oauth2 import get_curr_user
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response, status, APIRouter, Depends

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[Post])
async def get(session: SessionDep, user: str = Depends(get_curr_user)):
    posts = session.exec(select(models.Posts)).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: models.Posts,session: SessionDep, user: str = Depends(get_curr_user)):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.get("/{id}", response_model=Post)
def get_post(id:int, session: SessionDep, user: str = Depends(get_curr_user)):
    post = session.get(models.Posts, id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Did not find post with id = {id}")
    return post 

    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, session: SessionDep, user: str = Depends(get_curr_user)):
    post = session.get(models.Posts, id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    session.delete(post)
    session.commit()
    return {"ok": True}


@router.put("/{id}", response_model=Post)
def update_post(id:int, post: models.Posts, session: SessionDep, user: str = Depends(get_curr_user)): 
    exist_post = session.get(models.Posts, id)
    if not exist_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    exist_post.title = post.title
    exist_post.content = post.content
    exist_post.published = post.published

    session.add(exist_post)
    session.commit()
    session.refresh(exist_post)
    return exist_post
