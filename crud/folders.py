from fastapi import Depends
from core.database import get_db
from crud.file_md import create_folder, upload_image
from models.models import Folder
from sqlalchemy.orm import Session

from models.schemas import Folder_Models

async def folder_add(req:Folder_Models,user_id:int,db: Session = Depends(get_db)):
    path=create_folder(directory=req.name,userid=user_id)
    new_add = Folder(
        user_id=user_id,
        name=req.name,
        url=path.path_const
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return {
        "name":new_add.name,
        "user_id":new_add.user_id,
        "url":path.path_const,
        "id":new_add.id
    }
async def folder(userId:int,db: Session = Depends(get_db)):
    blog = db.query(Folder).filter(userId==Folder.user_id).all()
    print(blog)
    # blog.append()
    return blog
async def one_folder(folder_id:int,db: Session = Depends(get_db)):
    blog = db.query(Folder).filter(folder_id==Folder.id).first()
    print(blog)
    # blog.append()
    return blog