import os
import shutil
import sys
import uuid
from fastapi import Depends, File, UploadFile
from sqlalchemy import and_
from sqlalchemy.orm import Session
from core.database import get_db
# from crud.folders import one_folder
from models import File_Models,Files
from models.models import Folder
from models.schemas import Create_folder, Update_name



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
def create_folder(directory,userid:int):
    path_const = f"/uploads/{userid}/{directory}/"
    path = sys.path[0] + path_const
    if not os.path.exists(path):
        os.makedirs(path)
    return Create_folder(path=path, path_const=path_const)
#---------------------------------------------------------------------------------
def upload_image(directory:str, userid:int, file:UploadFile = File(...)):
    print(directory)
    path=create_folder(directory=directory,userid= userid)
    
    extension = file.filename.split(".")[-1]
    unique_id = str(uuid.uuid4())
    new_name = unique_id + "." + extension
    upload_file_path_for_save_static = path.path + f"{new_name}"
    upload_file_path_for_db = path.path_const + f"{new_name}"
        
    with open(upload_file_path_for_save_static, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
    if upload_file_path_for_db:
        return upload_file_path_for_db
    

def delete_uploaded_image(image_name):
    path_for_remove = sys.path[0] + image_name
    print(path_for_remove)
    if os.path.exists(path_for_remove):
        os.remove(path_for_remove)

    if path_for_remove:
        return True
    
    
#----------------------------------------------------------------------------   
async def create(user_name:str,folders_id:int,userid:int, files:UploadFile = File(...),db: Session = Depends(get_db)):
    # print(blog.id)
    if folders_id == -1:
        print(blog,"Creating")
        uploaded_image = upload_image(directory=user_name,userid=userid, file=files)
    else:
        blog = db.query(Folder).filter(folders_id==Folder.id).first()
        if not blog:
            return False
        else:
            print(blog.name)
            uploaded_image = upload_image(directory=blog.name,userid=userid, file=files)
    format=files.filename.split(".")[-1]
    new_add = Files(
        image_url = uploaded_image,
        user_id = userid,
        size=files.size,
        file_name=files.filename,
        file_format=format,
        folder_id=folders_id
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
#--------------------------------------------------------------------------
async def file_get(userId:int,db: Session = Depends(get_db)):
    
    blog = db.query(Files).filter(userId==Files.user_id).all()
    print(blog[0].folder_id)
    # blog.append()
    return blog
#--------------------------------------------------------------------------
async def one_file(userId:int,file_id:int,db: Session = Depends(get_db)):
    print(file_id)
    blog = db.query(Files).filter(and_(userId==Files.user_id , file_id==Files.id)).first()
    print(blog)
    # blog.append()
    return blog
#--------------------------------------------------------------------------
async def change_name(req:Update_name,db: Session = Depends(get_db)):
    blog=db.query(Files).filter(req.id==Files.id).update({
            Files.file_name:req.name+"."+Files.file_format
            })
    print(blog)
    db.commit()
    db.close()
    return blog
#--------------------------------------------------------------------------
async def delete(file_id:int,user_id:int,db: Session=Depends(get_db)):
    db_get = db.query(Files)\
        .filter(file_id==Files.id and user_id==Files.user_id)
    
    if not db_get.first():
        return False
    else:
        delete_data=delete_uploaded_image(image_name=db_get.first().image_url)
        print(delete_data)
        succes_delete=db_get.delete(synchronize_session=False)
        db.commit()
        db.close()
        return True