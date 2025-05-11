from typing import Annotated
from sqlalchemy import Column, Boolean, DateTime, text
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

class Posts(SQLModel, table=True): 
    id: int = Field(nullable=False, primary_key=True)
    title:str = Field(index=True, nullable=False)
    content:str = Field(index= True, nullable=False)
    published:bool = Field( sa_column=Column(Boolean, server_default=text("true"), nullable=False))
    created_at:datetime = Field(sa_column=Column(DateTime, server_default=text("now()"), nullable=False))


class Users(SQLModel, table=True):
    id:int = Field(nullable=False, primary_key=True)
    email:str = Field(nullable=False, unique=True)
    password:str = Field(nullable=False, unique=True)
    created_at:datetime = Field(sa_column=Column(DateTime, server_default=text("now()"), nullable=False))

