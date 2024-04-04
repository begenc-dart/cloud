from typing import List
from fastapi import APIRouter, Depends, Request,status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from core.database import get_db
import crud
from crud.auth import authenticate_admin, get_current_user
from crud.folders import folder
from models.schemas import Folder_Models, Show_folers


folder_api = APIRouter(
    prefix='/folders',
    # dependencies=[Depends(HTTPBearer())],
    tags=['folders']
)
@folder_api.post('/folder_add', dependencies=[Depends(HTTPBearer())])
async def folder_add(req:Folder_Models,header_param: Request, db: Session = Depends(get_db)):
    print(id)
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    result = await crud.folder_add(req=req,user_id=user.id,db=db)
    if not result:
        return "error"
    else:
        return JSONResponse(content=result,status_code=status.HTTP_201_CREATED)
@folder_api.get("/folder_get", dependencies=[Depends(HTTPBearer())],response_model=List[Show_folers])
async def folder_get(header_param: Request, db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    data=await folder(userId=user.id,db=db)
    if not data:
        return JSONResponse(content={
            "status":"You dont have file"
        },status_code=status.HTTP_404_NOT_FOUND)
    else:
        return data