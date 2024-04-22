
from pstats import Stats
import statistics
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from core.database import  get_db
from sqlalchemy.orm import Session
from models.models import SignUp
from models.schemas import Sign_Up_Model


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)
#----------------------------------------------------------
def create_access_token(username: str, password: str, user_id: int):
    encode = {'username': username, 'password': password, 'id': user_id}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

#-------------------------------------------------------------
def authenticate_admin(number: str, password: str, db):
   
    user = db.query(SignUp).filter(SignUp.number == number).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user
#-------------------------------------------------------------
async def get_current_user(header_params: Request):
    
    token = header_params.headers.get('Authorization').split('Bearer ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        password: str = payload.get('password')
        user_id: int = payload.get('id')
        
        
        if username is None or user_id is None or password is None:
            raise HTTPException(status_code=statistics.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return  {
                    'username': username, 
                    'password': password, 
                    'id': user_id}
    except JWTError:
        raise HTTPException(status_code=Stats.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
def post_sign_up(req: Sign_Up_Model,db: Session = Depends(get_db)):
    create_user_model = SignUp(
        # student_id=req.student_id,
        name=req.name,
        surname=req.last_Name,
        number = req.number,
        password = bcrypt_context.hash(req.password),
        # group_id=req.group_id
    )
    user = db.query(SignUp).filter(SignUp.number == create_user_model.number).first()
    if not user:
        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model)
        access_token = create_access_token(
            req.number, 
            req.password, 
            create_user_model.id)
        update_user_model = db.query(SignUp)\
            .filter(SignUp.id == create_user_model.id)\
        .update({SignUp.token: access_token}, synchronize_session=False)
        db.commit()
        return access_token
    else:
        return False
