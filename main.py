from fastapi import FastAPI
from routers import user_get_routes, product_routes, product_post, user_post_routes

app = FastAPI()

app.include_router(user_get_routes.router)
app.include_router(product_routes.router)
app.include_router(product_post.router)
app.include_router(user_post_routes.router)

@app.get("/")
def get_started():
    return {"Message": "Hello World"}
