from routers import authentication
from routers import booking
from time import time
from fastapi import Request
from routers import handle_file
from db.database import engine
from fastapi import FastAPI
from routers import user_get_routes, product_routes, product_post, user_post_routes, food_order_api
from routers import user as user_router
from routers import blog as blog_router
from routers import auth as auth_router
from models import user as user_model
from models import blog as blog_model
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def log_request(request:Request,call_next):
     start = time()
     response = await call_next(request)
     duration = time() - start
     print(f"Request: {request.url} | Time Taken: {duration}")
     return response

app.mount("/files", StaticFiles(directory="uploaded_files"), name="files")
app.include_router(user_get_routes.router)
app.include_router(product_routes.router)
app.include_router(product_post.router)
app.include_router(user_post_routes.router)
app.include_router(user_router.router)
app.include_router(blog_router.router)
app.include_router(auth_router.router)
app.include_router(handle_file.router)
# Assignemnt Routes 
app.include_router(food_order_api.router)
app.include_router(booking.router)
app.include_router(authentication.router)
@app.get("/")
def get_started():
    return {"Message": "Hello World"}

user_model.Base.metadata.create_all(engine)
blog_model.Base.metadata.create_all(engine)