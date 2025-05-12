from fastapi import FastAPI, HTTPException, Response, status, APIRouter, Depends
from ..schemas import Vote
from .. import models
from ..database import SessionDep
from .oauth2 import get_curr_user
from sqlmodel import select
router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.get("/", )
async def get():
    pass

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:Vote, session: SessionDep, user: str = Depends(get_curr_user)):
    post = session.exec(select(models.Posts).where(models.Posts.id == vote.post_id)).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post does not exist")
    found_vote = session.exec(select(models.Votes).where(models.Votes.post_id == vote.post_id, models.Votes.user_id == user.user_id)).first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user.username} has already voted on post {vote.post_id}")
        new_vote = models.Votes(post_id=vote.post_id, user_id=user.user_id)
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
        return {"message": "added new vote"}
    else:
        if found_vote:
            session.delete(found_vote)
            session.commit()
            return {"message": "deleted vote"}
        else: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")

