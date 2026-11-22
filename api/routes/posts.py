from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api import schemas
from database import get_db, models
# from models import topics
from security import get_current_user

router = APIRouter()

# def get_profile(current_user: models.User = Depends(get_current_user)):

@router.post("/post", response_model=schemas.PostCreateResponse, status_code=201)
def create_post(post: schemas.PostCreate,
                current_user: models.User = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    # Create a database user.
    # The password is hashed before it is stored.
    db_post = models.Post(
        title=post.title,
        body=post.body,
        creation_ts=datetime.now(),
        expiration_ts=post.expires_at,
        username=current_user.username,
    )
    db.add(db_post)

    db.flush()
    topic_list = []
    for topic in post.topics:
        db_topics = models.Topic(
            topic_name=topic,
            post_id=db_post.post_id,
        )
        db.add(db_topics)
        topic_list.append(db_topics.topic_name)

    db.commit()
    db.refresh(db_post)
    return {"title": db_post.title,
             "topics": topic_list,
             "expires_at": db_post.expiration_ts,
             "username": current_user.username
             }