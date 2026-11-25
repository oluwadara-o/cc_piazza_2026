from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api import schemas
from database import get_db, models
# from models import topics
from security import get_current_user

router = APIRouter()

@router.post("/post/{post_id}/reaction", response_model=schemas.ReactResponse)
def post_reaction(post_id, react_type:schemas.ReactPost,
                current_user: models.User = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    # Create a database user.
    returned_post = db.query(models.Post).filter(models.Post.post_id == post_id).first()
    if not returned_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if returned_post.username == current_user.username:
        raise HTTPException(status_code=403, detail="You can't like your own post!")

    returned_reaction = (db.query(models.Reaction).filter(models.Reaction.post_id == post_id)
                         .filter(models.Reaction.username == current_user.username).first())
    if returned_reaction:
        db.delete(returned_reaction)
        db.flush()

    db_react = models.Reaction(
        username=current_user.username,
        post_id=post_id,
        reaction_type=react_type.reaction_type
    )
    db.add(db_react)
    #
    # db.execute(update(models.Reaction), db_react)
    #
    db.commit()
    db.refresh(db_react)
    return {"post_id": db_react.post_id,
             "reaction_type": db_react.reaction_type,
             }