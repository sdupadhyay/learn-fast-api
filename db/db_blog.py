from sqlalchemy.orm import Session
from models.blog import DbBlog
from schemas.blog import Blog
from uuid import uuid4

def create_blog(db:Session,request:Blog,user_id):
    new_blog=DbBlog(
        # id=uuid4(),
        title=request.title,
        content=request.content,
        user_id=user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_all_blogs(db:Session):
    return db.query(DbBlog).all()