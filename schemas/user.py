from schemas.blog import Blog
from typing import Optional
from typing import List
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserPartial(BaseModel):
    username: Optional[str]=None
    email: Optional[str]=None
    password: Optional[str]=None
    
class UserDisplay(BaseModel):
    username: str
    email: str
    blogs: List[Blog] = []

    class Config:
        orm_mode = True

class Login(BaseModel):
    email:str
    password:str