from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    # class config:
    #     orm_mode = True

    class Config:
        from_attributes = True



class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    owner: UserOut
    # class Config:
    #     orm_mode = True

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int


    class Config:
        from_attributes = True


    

class UserCreate(BaseModel):
    email: EmailStr
    password: str






class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    id: Optional[str] = None

   
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0 ,le=1)
