from typing import Dict
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter

router = APIRouter(prefix="/user",tags=["user"])
class Address(BaseModel):
    city: str
    state: str
    pincode: int

class UserCreate(BaseModel):
      name:str
      email: EmailStr
      is_active: Optional[bool] = None
      roles: List[str]
      settings: Dict[str,str]
      address: Optional[Address] = None
      
@router.post("/create")
def create_user(user:UserCreate):
    return {"message":"User created successfully","user":user}