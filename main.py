from fastapi import FastAPI;
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

