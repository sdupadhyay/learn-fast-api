from db import db_user
from schemas.user import Login
from db.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return db_user.login_user(db, request.username, request.password)
