
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
class Sign_Up_Model(BaseModel):
    name:str
    last_Name:str
    number:int
    password:str
class Sigin(BaseModel):
    number:int
    password:str
class File_Models(BaseModel):
    image_url:str
    user_id:int
    size:int
    file_name:str


class Show_File(BaseModel):
    id:int
    image_url:str
    user_id:int
    size:int
    file_name:str
    creator:List[Share]=[]
    class Config:
        orm_mode = True
class Update_name(BaseModel):
    id:int
    name:str
    
class Show_Shared(BaseModel):
    number:int
    can_edit:bool
    message:Optional[str]=None
    blogs:Show_File
    class Config:
        orm_mode = True
        
