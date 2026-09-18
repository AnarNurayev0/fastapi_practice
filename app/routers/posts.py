from fastapi import status, HTTPException, Depends, APIRouter, Response
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func
from typing import List


router = APIRouter(prefix="/posts",tags=["posts"])

"""
    POSTS
"""

# GET ALL POSTS
@router.get("/",status_code=status.HTTP_202_ACCEPTED, response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # posts = db.query(models.Post).all()

    # print(current_user)

    # posts = db.query(models.Post, func(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    posts = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .all()
    )

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return posts


# GET POST BY ID
@router.get("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.PostOut)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    # print(current_user.email)
    post = (
            db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
            .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
            .group_by(models.Post.id).filter(models.Post.id == id).first()
    )

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post you want to get is not found!")

    return post


# CREATE POST
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    if not post:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="The post you want to create is empty!")

    # print(current_user)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# DELETE POST
@router.delete("/{id}",status_code=status.HTTP_202_ACCEPTED)
def delete_post_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    delete_post = db.query(models.Post).filter(models.Post.id == id)

    if not delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The post you delete is not found!")

    delete_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE POST
@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.Post)
def fully_change_post_by_id(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()

    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The post you want to update is not found!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()