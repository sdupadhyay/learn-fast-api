from db import db_user
from schemas.user import Login
from db.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(request: Login, db: Session = Depends(get_db)):
    return db_user.login_user(db, request.email, request.password)
