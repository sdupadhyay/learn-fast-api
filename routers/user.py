from fastapi import Response
from typing import Optional
from schemas.user import UserPartial
from typing import List
from schemas.user import UserBase
from schemas.user import UserDisplay
from db.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header
from db import db_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/header")
def get_header(custom_header: Optional[List[str]] = Header(None)):
    return custom_header


@router.get("/response-header")
def get_header(response: Response):
    response.headers["Toke"] = "sample-token"
    return {"message": "Header added"}


@router.post("/", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    return db_user.get_user(db, id)


@router.put("/{id}", response_model=UserDisplay)
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    return db_user.update_user(db, id, request)


@router.patch("/{id}", response_model=UserDisplay)
def update_user_partially(id: int, request: UserPartial, db: Session = Depends(get_db)):
    return db_user.update_user_partially(db, id, request)


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete_user(db, id)
