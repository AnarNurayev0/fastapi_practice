from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/users",tags=["users"])

"""
    USERS
"""

# CREATE USER
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    if not user:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Login was unsuccessful!")

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# # GET ALL USERS
# @router.get("/",status_code=status.HTTP_202_ACCEPTED,response_model=list[schemas.UserOut])
# def get_all_users(db: Session = Depends(get_db)):

#     users = db.query(models.User).all()

#     if not users:
#          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Users are not found!")

#     return users


# GET USER BY ID
@router.get("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User are not found!")

    return user