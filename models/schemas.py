
from typing import Optional,List
from pydantic import BaseModel

from models.models import Shared
class Shared_Models(BaseModel):
    number:int
    can_edit:bool
    message:Optional[str]=None
class Share(Shared_Models):
    class Config:
        orm_mode = True
class File_Models(BaseModel):
    image_url:str
    user_id:int
    size:int
    file_name:str
class Files(File_Models):
    class Config:
        orm_mode = True
class Folder_Models(BaseModel):
    name:str
class Show_folers(BaseModel):
    url:str
    name:str
    files:List[Files]=[]
    class Config:
        orm_mode = True  
class Show_File(BaseModel):
    id:int
    image_url:str
    user_id:int
    size:int
    file_name:str
    is_liked:bool
    class Config:
        orm_mode = True  
class One_file_Model(Show_File):
    creator:List[Share]=[]
    class Config:
        orm_mode = True 
class Show_Shared(BaseModel):
    number:int
    can_edit:bool
    message:Optional[str]=None
    blogs:Show_File
    class Config:
        orm_mode = True
class Sign_Up_Model(BaseModel):
    name:str
    last_Name:str
    number:int
    password:str
class Sigin(BaseModel):
    number:int
    password:str
class Update_name(BaseModel):
    id:int
    name:str
class Create_folder(BaseModel):
    path:str
    path_const:str