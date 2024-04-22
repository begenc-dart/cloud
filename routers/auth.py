
from pstats import Stats
import statistics
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jose import JWTError,jwt
from passlib.context import CryptContext
from core.database import SessionLocal, get_db
from starlette import status
from crud.auth import authenticate_admin, create_access_token, get_current_user, post_sign_up
from models.models import SignUp
from models.schemas import Sigin, Sign_Up_Model
from sqlalchemy.orm import Session
auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@auth_router.post('/sign_up', status_code=status.HTTP_201_CREATED)
async def create_user(req: Sign_Up_Model, db: Session = Depends(get_db),):
    data=post_sign_up(req=req,db=db)
    if not data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='This number is already in use')
    return JSONResponse(content={'token': data,}, 
                        status_code=status.HTTP_201_CREATED)

@auth_router.get('/get-me', dependencies=[Depends(HTTPBearer())])
async def getme(header_param: Request, db:Session=Depends(get_db)):
    dec_token = await get_current_user(header_param)
    user = authenticate_admin(dec_token['username'], dec_token['password'], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    print(user.name)
    return db.query(SignUp).filter(SignUp.id==user.id).first()
@auth_router.post('/logIn', status_code=status.HTTP_200_OK)
def  logIn(req:Sigin,session:Session=Depends(get_db),db: Session = Depends(get_db)):
    user = authenticate_admin(req.number, req.password, session)
    print(req.password)
    print(req.number)
    if not user:
        return JSONResponse(content={"data":"You are not Login"}, 
                        status_code=status.HTTP_400_BAD_REQUEST) 
    else:
        return {"data":user,}





