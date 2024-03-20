from fastapi import Depends
from core.database import SessionLocal, get_db
from sqlalchemy.orm import Session

from models.models import Files
from models.schemas import Shared_Models
from models import Shared

async def shared_add(requset:Shared_Models,id:int,db: Session = Depends(get_db)):
    new_add = Shared(
      number=requset.number,
      can_edit=requset.can_edit,
      message=requset.message,
      user_id=id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return {
        "number":new_add.number,
        "can_edit":new_add.can_edit,
        "message":new_add.message,
        "user_id":new_add.user_id
    }
async def shared_get(userId:int,db: Session = Depends(get_db)):
    blog = db.query(Shared).all()
    print(blog)
    # blog.append()
    return blog