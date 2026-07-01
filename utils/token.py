
from models.user import DbUser
from jose import JWTError
from fastapi import HTTPException
from fastapi import status
from db.database import get_db
from sqlalchemy.orm.session import Session
from fastapi import Depends
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6cd2e3cf2add0d0c1b1562"
JWT_ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def create_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expire_delta if expire_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
    try:
       payload = jwt.decode(token,JWT_SECRET,algorithms=JWT_ALGORITHM)
       username : str = payload.get("sub")
       if not username:
           raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
    return user
