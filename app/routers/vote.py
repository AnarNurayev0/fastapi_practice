from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/vote",tags=["vote"])
"""
    VOTES
"""

# VOTE POST
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post does not exist!")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    vote_found = vote_query.first()

    if vote.direction == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="This post has alredy liked!")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Post liked successfully!"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist!")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Post like deleted successfully!"}
