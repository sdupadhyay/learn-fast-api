from db.database import engine
from fastapi import FastAPI
from routers import user_get_routes, product_routes, product_post, user_post_routes
from routers import user as user_router
from routers import blog as blog_router
from routers import auth as auth_router
from models import user as user_model
from models import blog as blog_model

app = FastAPI()

app.include_router(user_get_routes.router)
app.include_router(product_routes.router)
app.include_router(product_post.router)
app.include_router(user_post_routes.router)
app.include_router(user_router.router)
app.include_router(blog_router.router)
app.include_router(auth_router.router)

@app.get("/")
def get_started():
    return {"Message": "Hello World"}

user_model.Base.metadata.create_all(engine)
blog_model.Base.metadata.create_all(engine)