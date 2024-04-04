

from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile,status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from sqlalchemy import ReturnsRows

from sqlalchemy.orm import Session


from core.database import get_db
import crud
from crud.file_md import change_name, file_get, one_file
from crud.auth import authenticate_admin, get_current_user
from models import Show_File
from models.schemas import One_file_Model, Update_name
banner_router = APIRouter(
    prefix='/upload',
    # dependencies=[Depends(HTTPBearer())],
    tags=['upload']
)
#-----------------------------------------------------------------------------------------
@banner_router.post("/update-file/{folders_id}", dependencies=[Depends(HTTPBearer())])
async def update_image(folders_id:int,header_param: Request,  files: UploadFile = File(...),db: Session = Depends(get_db)):
    print(id)
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    # result = await crud.update_post_image(db=db, id=id, file=files)
    try:
        print(files.filename)
        result = await crud.create(user_name=user.name,folders_id=folders_id,userid=user.id,db=db,files=files)
        
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File with id {folders_id} not found")
        else:
            return JSONResponse(content={"url":result}, status_code=status.HTTP_201_CREATED)
    except Exception as error:
        print(error)
        return error

#---------------------------------------------------------------------
@banner_router.post("/update-file/", dependencies=[Depends(HTTPBearer())])
async def update_image(header_param: Request,  files: UploadFile = File(...),db: Session = Depends(get_db)):
    print(id)
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    # result = await crud.update_post_image(db=db, id=id, file=files)
    try:
        # print(files.filename)
        result = await crud.create(user_name=user.name,folders_id=-1,userid=user.id,db=db,files=files)
        
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File with id  not found")
        else:
            return JSONResponse(content={"url":result}, status_code=status.HTTP_201_CREATED)
    except Exception as error:
        print(error)
        return error
#---------------------------------------------------------------------
@banner_router.get("/get-file/", dependencies=[Depends(HTTPBearer())], response_model=List[Show_File])
async def get_file(header_param: Request, db: Session = Depends(get_db)):
    print(id)
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    data=await file_get(userId=user.id,db=db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File with id {id} not found")
       
    else:
        return data

#---------------------------------------------------------------------
@banner_router.get("/one-file/{id}",status_code=status.HTTP_200_OK, dependencies=[Depends(HTTPBearer())],response_model=One_file_Model )
async def get_one_file(id:int,header_param: Request, db :Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    data=await one_file(userId=user.id,file_id=id,db=db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File with id {id} not found")
    else:
        return data
#---------------------------------------------------------------------
@banner_router.put("/update-name/", dependencies=[Depends(HTTPBearer())],)
async def update_name(request:Update_name,header_param: Request, db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    data=await change_name(req=request,db=db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="You dont have file")
    else:
        return JSONResponse(content={
            "status":"success"
        },status_code=status.HTTP_200_OK)
#--------------------------------------------------------------------------------
@banner_router.delete("/delete/{file_id}", dependencies=[Depends(HTTPBearer())],)
async def delete_file(file_id,header_param:Request, db: Session = Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    data=await crud.delete(file_id=file_id,user_id=user.id,db=db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File with id {file_id} not found")
    else:
        return JSONResponse(content={
            "status":"success"
        },status_code=status.HTTP_200_OK)

#---------------------------------------------------------------------


    