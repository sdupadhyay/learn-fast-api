from utils.token import get_current_user
from utils.token import oauth2_scheme
from typing import List
from db import db_blog
from db.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from schemas.blog import Blog


router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/", response_model=Blog)
def create_blog(
    request: Blog, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    user = get_current_user(token,db)

    return db_blog.create_blog(db, request, user.id)


@router.get("/", response_model=List[Blog])
def all_blogs(db: Session = Depends(get_db)):
    return db_blog.get_all_blogs(db)
