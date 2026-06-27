from fastapi import APIRouter, Response,status
from enum import Enum
router = APIRouter(prefix="/user",tags=["user"])

@router.get("/all")
def get_all_user():
    return {"message":"All Users"}

# Dynamic Route
@router.get("/{userName}")
# Adding Response status code
def get_userName(userName:str,response:Response):
    if userName == "sdupadhyay":
        response.status_code = status.HTTP_200_OK
        return {"message":f"The user name is {userName}"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":f"The user name is is not Found"}

class UserRole(str,Enum):
     admin = "admin"
     editor = "editor"
     viewer = "viewer"

@router.get("/role/{role}")
def get_user(role:UserRole):
    return {"message":f"The user role is {role.value}"}

class SubscriptionPlan(str,Enum):
    free = "free"
    pro = "pro"
    basic = "basic"
    premium = "premium"
    enterprise = "enterprise"
@router.get("/subscription/{plan}")
def get_subscription(plan:SubscriptionPlan):
    return {"message":f"The subscription plan is {plan.value}"}