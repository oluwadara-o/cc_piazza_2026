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

@router.post("/post", status_code=201)
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
    print(db_post.post_id)
    db.flush()
    for topic in post.topics:
        print(topic)
        db_topics = models.Topic(
            topic_name=topic,
            post_id=db_post.post_id,
        )
        db.add(db_topics)
    db.commit()

    # try:
    #     db.flush()
    #     for topic in post.topics:
    #         print(topic)
    #         db_topics = models.Topic(
    #             topic_name=topic,
    #             post_id=db_post.post_id,
    #         )
    #         db.add(db_topics)
    #     db.commit()
    # except Exception as e:
    #     db.rollback()

    print("done")
    print(db.query(models.Topic).first().topic_name)
    # TODO add to topics
    # try:
    #     db.commit()
    # except IntegrityError as e:
    #     print(e)
    #     db.rollback()
    #     raise HTTPException(status_code=409, detail="Issue adding post")
    db.commit()
    db.refresh(db_post)
    return db_post