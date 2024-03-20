from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from core.database import Base
from sqlalchemy.orm import relationship

class SignUp(Base):
    __tablename__="SignUp"
    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    name=Column(String)
    surname=Column(String)
    number=Column(Integer)
    token=Column(String)
    password=Column(String)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
class Files(Base):
    __tablename__="file"
    id=Column(Integer,primary_key=True)
    image_url=Column(String)
    user_id=Column(Integer)
    size=Column(Integer)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    file_name=Column(String)
    file_format=Column(String)
    is_liked=Column(Boolean,default=False)
    creator = relationship("Shared", back_populates="blogs")
class Folder(Base):
    __tablename__="folders"
    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    name=Column(String)
    url=Column(String)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    
class Shared(Base):
    __tablename__='shared'
    id=Column(Integer,primary_key=True,index=True, autoincrement=True)
    number=Column(Integer)
    can_edit=Column(Boolean)
    message=Column(String)
    user_id = Column(Integer, ForeignKey('file.id'))
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)
    blogs = relationship('Files', back_populates="creator")
