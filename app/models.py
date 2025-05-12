from typing import Annotated, Optional
from sqlalchemy import Column, Boolean, DateTime, text
from sqlalchemy.orm import relationship
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, ForeignKey, Integer, Session, SQLModel, create_engine, select, Relationship
from datetime import datetime

class Users(SQLModel, table=True):
    id:int = Field(nullable=False, primary_key=True)
    email:str = Field(nullable=False, unique=True)
    password:str = Field(nullable=False, unique=True)
    created_at:datetime = Field(sa_column=Column(DateTime, server_default=text("now()"), nullable=False))
    # user links to user field in Posts Model
    posts: list["Posts"] = Relationship(back_populates="user")
    phone_number: str= Field(nullable=True)

class Posts(SQLModel, table=True): 
    id: int = Field(nullable=False, primary_key=True)
    title:str = Field(index=True, nullable=False)
    content:str = Field(index= True, nullable=False)
    published:bool = Field( sa_column=Column(Boolean, server_default=text("true"), nullable=False))
    created_at:datetime = Field(sa_column=Column(DateTime, server_default=text("now()"), nullable=False))
    user_id: int = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False))
    # posts links to posts filed in Users Model
    user:Optional[Users] = Relationship(back_populates="posts")

class Votes(SQLModel, table=True):
    user_id: int = Field(sa_column = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False,primary_key=True))
    post_id: int = Field(sa_column=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False,primary_key=True))