from typing import List
from fastapi import APIRouter, Depends, HTTPException,status, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from core.database import get_db
from sqlalchemy.orm import Session
import crud
from crud.auth import authenticate_admin, get_current_user
from crud.shared_md import shared_get
from models import Shared_Models
from models.schemas import Show_Shared, Show_folers

shared_router = APIRouter(
    prefix='/shared',
    # dependencies=[Depends(HTTPBearer())],
    tags=['shared']
)
@shared_router.post("/shared_file/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(HTTPBearer())])
async def shared_file(requset:Shared_Models,id:int,header_param: Request,db: Session = Depends(get_db)):

    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    try:
        data= await crud.shared_add(requset=requset,id=id,db=db)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File with id {id} not found")
        else:
            return JSONResponse(content={"url":data}, status_code=status.HTTP_201_CREATED)
    except Exception as error:
        print(error)
        return error 
@shared_router.get("/get-shared/",  dependencies=[Depends(HTTPBearer())])
async def get_file(header_param: Request, db: Session = Depends(get_db)):
    print(id)
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    data=await shared_get(userId=user.id,db=db)
    if not data:
        return JSONResponse(content={
            "status":"You dont have file"
        },status_code=status.HTTP_404_NOT_FOUND)
    else:
        return data
