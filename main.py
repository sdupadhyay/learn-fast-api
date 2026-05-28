from fastapi import FastAPI, Response,status;
from enum import Enum
from typing import Optional
app = FastAPI()

@app.get("/")
def get_started():
    return {"Message":"Hello World"}
@app.get("/user/all")
def get_all_user():
    return {"message":"All Users"}
    
# Dynamic Route
@app.get("/user/{userName}")
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


# Query Paramers 
@app.get("/products")
def get_products(
    page: int = 1,
    category: Optional[str] = None,
    in_stock: Optional[bool] = True
):
    return {
        "message": f"Fetching products in category '{category}', in stock: {in_stock} on page {page}"
    }

@app.get("/products/search")
def search_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = "price",
    order: Optional[str] = "asc",
    page: Optional[int] = 1,
    page_size: Optional[int] = 10
):
    return {
        "message": f"Fetching products in category '{category}' with price between {min_price}-{max_price}, sorted by {sort_by} in {order} order, page {page} with {page_size} items per page"
    }