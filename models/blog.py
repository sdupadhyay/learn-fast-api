from db.database import Base
from sqlalchemy import Column,ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class DbBlog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer,ForeignKey('users.id'))

    user = relationship("DbUser",back_populates="blogs")