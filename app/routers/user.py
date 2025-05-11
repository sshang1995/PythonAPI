from .. import models
from ..database import SessionDep
from sqlmodel import Session, select
from ..schemas import UserCreate, UserResponse
from ..util import hash
from fastapi import FastAPI, HTTPException, Response, status, APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, session: SessionDep): 
    # hash password 
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserResponse)
def get_user(id:int, session: SessionDep):
    user = session.get(models.Users, id)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Did not find user with id = {id}")
    return user 