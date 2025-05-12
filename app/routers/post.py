from .. import models
from ..database import SessionDep
from sqlmodel import func, select
from ..schemas import Post, PostResponse
from ..util import hash
from .oauth2 import get_curr_user
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response, status, APIRouter, Depends

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[PostResponse])
async def get(session: SessionDep, user: str = Depends(get_curr_user), limit:int = 10, skip:int = 0, search:Optional[str]=""):
    #posts = session.exec(select(models.Posts).where(models.Posts.title.contains(search)).offset(skip).limit(limit)).all()
    posts = session.exec(select(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).where(models.Posts.title.contains(search)).offset(skip).limit(limit).group_by(models.Posts.id)).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: models.Posts,session: SessionDep, user: str = Depends(get_curr_user)):
    post.user_id = user.user_id
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.get("/{id}", response_model=PostResponse)
def get_post(id:int, session: SessionDep, user: str = Depends(get_curr_user)):
    #post = session.get(models.Posts, id)
    post = session.exec(select(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).where(models.Posts.id == id).group_by(models.Posts.id)).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Did not find post with id = {id}")
    if post.Posts.user_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to get this post")
    return post 

    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, session: SessionDep, user: str = Depends(get_curr_user)):
    post = session.get(models.Posts, id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post.Posts.user_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform delete post")
    session.delete(post)
    session.commit()
    return {"ok": True}


@router.put("/{id}", response_model=Post)
def update_post(id:int, post: models.Posts, session: SessionDep, user: str = Depends(get_curr_user)): 
    exist_post = session.get(models.Posts, id)
    if not exist_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if exist_post.user_id != user.user_id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform update post")
    exist_post.title = post.title
    exist_post.content = post.content
    exist_post.published = post.published

    session.add(exist_post)
    session.commit()
    session.refresh(exist_post)
    return exist_post
