from fastapi import status, Response, Cookie
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
import uuid

router = APIRouter(prefix="/authentication" , tags=["authentication"])


class User_details(BaseModel):
    username: str
    password: str

@router.post("/login")
def auth_user(user:User_details, response: Response):
    if user.username == "admin" and user.password == "secret":
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id)
        response.headers["X-Login-Status"] = "Success"
        return "Authentication successful"
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials"
    )
@router.get("/profile")
def get_profile(session_id: str | None = Cookie(default=None)):
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in"
        )
    return {"message": "Session active", "session_id": session_id}

@router.get("/logout")
def logout_user(response: Response):
    response.delete_cookie(key="session_id")
    return "You have been logged out."