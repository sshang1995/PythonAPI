from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from ..database import SessionDep
from ..models import Users
from ..util import hash, verify
from ..schemas import UserResponse, UserLogin, Token
from sqlmodel import select
from .oauth2 import create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session:SessionDep): 
    found_user = session.exec(select(Users).where(Users.email == form_data.username)).first()
    if not found_user: 
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Did not find user with email = {form_data.username}")
    result = verify(form_data.password, found_user.password)
    if result: 
        access_token = create_access_token(data ={"user_id" : found_user.id, "email": found_user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

