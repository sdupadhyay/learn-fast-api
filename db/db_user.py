from utils.token import create_token
from fastapi import status
from fastapi import HTTPException
from models.user import DbUser
from schemas.user import UserBase
from sqlalchemy.orm import Session
from hash import Hash


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    users = db.query(DbUser).all()
    return users


def get_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        return "User Not present in DB"
    else:
        return user


def update_user(db: Session, id: int, request: UserBase):
    user = get_user(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found"
        )
    user.username = request.username
    user.email = request.email
    user.password = request.password
    db.commit()
    db.refresh(user)
    return user


def update_user_partially(db: Session, id: int, request: UserBase):
    user = get_user(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found"
        )
    if request.username is not None:
        user.username = request.username
    if request.email is not None:
        user.email = request.email
    if request.password is not None:
        user.password = request.password
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, id: int):
    user = get_user(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found"
        )
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


def login_user(db: Session, username: str, password: str):
    user = db.query(DbUser).filter((DbUser.username == username) | (DbUser.email == username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username or email '{username}' not found"
        )
    else:
        if Hash.verify_password(password, user.password):
            token = create_token(data={"sub": user.username})
            return {
                "access_token": token,
                "token_type": "bearer",
                "userName": user.username,
                "message": "Login Successful",
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password"
            )
