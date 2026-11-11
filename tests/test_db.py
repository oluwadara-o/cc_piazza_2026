import datetime
from email import message

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from application import create_app
from database import get_db, models


@pytest.fixture
def helper_db(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'piazza-test.db'}",
        connect_args={"check_same_thread": False},
    )
    sessions = sessionmaker(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    with sessions() as session:
        return session

def test_users(helper_db):
    db = helper_db


    db_user = models.User(
        username="Lisa",
        email="Lisa@Blackpink.com",
        hashed_password="hashednonsense"
    )

    # Save the new user and reload it so the generated ID is available.
    db.add(db_user)
    db.commit()

    db_entry = db.query(models.User).first()
    assert db_entry.email == db_user.email
    assert db_entry.username == "Lisa"
    assert db_entry.hashed_password == db_user.hashed_password

    db_user_duplicate_username = models.User(
        username="Lisa",
        email="Lisa1@Blackpink.com",
        hashed_password="hashednonsense")

    with pytest.raises(IntegrityError):
        db.add(db_user_duplicate_username)
        db.commit()

def test_post_complete(helper_db):
    """Mostly been added to test how to query the database"""
    db_user = models.User(
        username="Lisa",
        email="Lisa@Blackpink.com",
        hashed_password="hashednonsense"
    )
    helper_db.add(db_user)
    helper_db.commit()

    db_post = models.Post(
        title="Concert",
        message="The concert will be on Jume 1st!!",
        username="Lisa",
        creation_ts=datetime.datetime.now(),
        expiration_ts=datetime.datetime.now() + datetime.timedelta(days=1),
    )
    helper_db.add(db_post)
    helper_db.commit()
    helper_db.refresh(db_post)

    db_comment = models.Comment(
        post_id=db_post.post_id,
        username=db_user.username,
        comment_text="Get Ready for DEADLINE",
        comment_ts=datetime.datetime.now()
    )
    helper_db.add(db_comment)
    helper_db.commit()

    db_user2 = models.User(
        username="Fan",
        email="Manon@FanEvents.com",
        hashed_password="hashednonsense"
    )
    helper_db.add(db_user2)
    helper_db.commit()

    db_comment = models.Comment(
        post_id=db_post.post_id,
        username=db_user2.username,
        comment_text="So Excited!!!",
        comment_ts=datetime.datetime.now()
    )
    helper_db.add(db_comment)
    helper_db.commit()

    db_comment = models.Comment(
        post_id=db_post.post_id,
        username=db_user2.username,
        comment_text="Just Bought my ticket!!!",
        comment_ts=datetime.datetime.now()
    )
    helper_db.add(db_comment)
    helper_db.commit()

    db_reaction = models.Reaction(
        post_id=db_post.post_id,
        username=db_user2.username,
        reaction_type="Like",
    )
    helper_db.add(db_reaction)
    helper_db.commit()

    comments_query = (helper_db.query(models.Comment.comment_text)
          .join(models.Post, models.Comment.post_id == models.Post.post_id))
    assert comments_query.count() == 3
    comments_text = [comment.comment_text for comment in comments_query.all()]
    assert comments_text == ["Get Ready for DEADLINE", "So Excited!!!", "Just Bought my ticket!!!"]

    reactions_query = (helper_db.query(models.Reaction.reaction_type)
                      .join(models.Post, models.Reaction.post_id == models.Post.post_id))
    assert reactions_query.count() == 1
    reactions_text = [reaction.reaction_type for reaction in reactions_query.all()]
    assert reactions_text == ["Like"]
    # print(helper_db.query(models.Comment)
    #       .join(models.Post, models.Comment.post_id == models.Post.post_id).all())
    # print(comments_query.count())
    for comment in comments_query.all():
        print(comment.comment_text)

