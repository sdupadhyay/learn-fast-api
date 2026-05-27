from fastapi import FastAPI;
from enum import Enum
app = FastAPI()

@app.get("/")
def get_started():
    return {"Message":"Hello World"}
@app.get("/user/all")
def get_all_user():
    return {"message":"All Users"}
    
# Dynamic Route
@app.get("/user/{userName}")
def get_userName(userName:str):
    return {"message":f"The user name is {userName}"}

class UserRole(str,Enum):
     admin = "admin"
     editor = "editor"
     viewer = "viewer"

@app.get("/user/role/{role}")
def get_user(role:UserRole):
    return {"message":f"The user role is {role.value}"}

class SubscriptionPlan(str,Enum):
    free = "free"
    pro = "pro"
    basic = "basic"
    premium = "premium"
    enterprise = "enterprise"
@app.get("/user/subscription/{plan}")
def get_subscription(plan:SubscriptionPlan):
    return {"message":f"The subscription plan is {plan.value}"}
