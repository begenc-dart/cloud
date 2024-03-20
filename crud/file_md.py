import os
import shutil
import sys
import uuid
from fastapi import Depends, File, UploadFile
from sqlalchemy.orm import Session
from core.database import get_db
from models import File_Models,Files
from models.schemas import Update_name



# async def update_post_image( id:int, file,db: Session = Depends(get_db)):
#     # print(str(id)+"dsadsa")
#     # get_image = db.query(Subcategories).filter(Subcategories.id == id).first()
    
#     # db.close()
#     # print(get_image.answer)
#     # if get_image.file is not None:
#     #     try:
#     #         delete_uploaded_image(image_name=get_image.file)
#     #     except Exception as e:
#     #         print(e)
#     uploaded_img = upload_image(directory="posts", file=file)
    
#     new_update = db.query(Subcategories).filter(Subcategories.id == id).\
#         update({
#             Subcategories.file : uploaded_img
#         }, synchronize_session=False)
    
#     data=get_image.file
#     print(data)
#     db.commit()
#     db.close()
#     if new_update:
#         return data
#     else:
#         return None
    
    
#-----------------------------------------------------------------------

def upload_image(directory, file):
    path_const = f"/uploads/{directory}/"
    path = sys.path[0] + path_const
    print(directory+"sadsa")
    print(str(file)+"fdsfsd")
    if not os.path.exists(path):
        os.makedirs(path)
    extension = file.filename.split(".")[-1]
    unique_id = str(uuid.uuid4())
    new_name = unique_id + "." + extension
    upload_file_path_for_save_static = path + f"{new_name}"
    upload_file_path_for_db = path_const + f"{new_name}"
        
    with open(upload_file_path_for_save_static, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
    if upload_file_path_for_db:
        return upload_file_path_for_db
    

def delete_uploaded_image(image_name):
    path_for_remove = sys.path[0] + image_name
    if os.path.exists(path_for_remove):
        os.remove(path_for_remove)

    if path_for_remove:
        return True
    
    
#----------------------------------------------------------------------------   
async def create(userid:int, files:UploadFile = File(...),db: Session = Depends(get_db)):
    print(files.size)
    uploaded_image = upload_image('images', files)
    format=files.filename.split(".")[-1]
    new_add = Files(
        image_url = uploaded_image,
        user_id = userid,
        size=files.size,
        file_name=files.filename,
        file_format=format
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return {
        "image_url":new_add.image_url,
        "user_id":new_add.user_id,
        "size":new_add.size,
        "file_name":new_add.file_name
    }
#---------------------------------------------------
async def file_get(userId:int,db: Session = Depends(get_db)):
    blog = db.query(Files).filter(userId==Files.user_id).all()
    print(blog)
    # blog.append()
    return blog
async def change_name(req:Update_name,db: Session = Depends(get_db)):
    blog=db.query(Files).filter(req.id==Files.id).update({
            Files.file_name:req.name+"."+Files.file_format
            })
    print(blog)
    db.commit()
    db.close()
    return blog