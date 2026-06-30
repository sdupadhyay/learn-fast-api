from fastapi import status
from fastapi import HTTPException
from models.user import DbUser
from schemas.user import UserBase
from sqlalchemy.orm import Session
from hash import Hash
def create_user(db:Session,request:UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db:Session):
    users = db.query(DbUser).all()
    return users

def get_user(db:Session,id:int):
    user = db.query(DbUser).filter(DbUser.id==id).first()
    if not user:
       return "User Not present in DB"
    else :
       return user
def update_user(db:Session,id:int,request:UserBase):
    user = get_user(db,id)
    if not user:
        return "User Not present in DB"
    user.username = request.username
    user.email = request.email
    user.password = request.password
    db.commit()
    db.refresh(user)
    return user
def update_user_partially(db:Session,id:int,request:UserBase):
    user = get_user(db,id)
    if not user:
        return None
    if request.username is not None:
        user.username = request.username
    if request.email is not None:
        user.email = request.email
    if request.password is not None:
        user.password = request.password
    db.commit()
    db.refresh(user)
    return user
    
def delete_user(db:Session,id:int):
    user = get_user(db,id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
    

def login_user(db:Session,email:str,password:str):
    user = db.query(DbUser).filter(DbUser.email == email).first()
    if not user:
        return "User Not present in DB"
    else:
        if Hash.verify_password(password, user.password):
            return {"userName":user.username,"message":"Login Sucessfull"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Password")