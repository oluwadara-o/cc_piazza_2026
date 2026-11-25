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
            topic_name=topic.lower(),
            post_id=db_post.post_id,
        )
        db.add(db_topics)
        topic_list.append(db_topics.topic_name)

    db.commit()
    db.refresh(db_post)
    return {"post_id": db_post.post_id,
            "title": db_post.title,
             "topics": topic_list,
             "expires_at": db_post.expiration_ts,
             "username": current_user.username
             }

#TODO debug/define response model PostBrowseResponse
@router.get("/post/topic/{topic}")
def browse_post(topic: str,
                current_user: models.User = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    # Create a database user.
    # The password is hashed before it is stored.
    if topic:
        print(db.query(models.Topic).first().topic_name)
        print(topic)
        posts = db.query(models.Topic).filter(models.Topic.topic_name == topic).all()
        posts_to_return = []
        for post in posts:
            print(post.post_id)
            post_query = db.query(models.Post).filter(models.Post.post_id == post.post_id).first()
            print(post_query)
            reactions_query = (db.query(models.Reaction.reaction_type)
                               .join(models.Post, models.Reaction.post_id == models.Post.post_id))
            likes_count = reactions_query.filter(models.Reaction.reaction_type == "like").count()
            dislikes_count = reactions_query.filter(models.Reaction.reaction_type == "dislike").count()
            posts_to_return.append({
                "title": post_query.title,
                "body": post_query.body,
                "expiration_ts": post_query.expiration_ts,
                "like_count": likes_count,
                "dislike_count": dislikes_count,
            })
    else:
        posts = db.query(models.Post).all()

    return posts_to_return


