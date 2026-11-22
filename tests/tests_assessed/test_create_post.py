"""
TC03	Olga’s request without a token is rejected
TC04	Olga creates a Tech post with an expiry timestamp
TC05	Nick creates another Tech post
TC06	Mary creates another Tech post
"""

from datetime import datetime, timedelta

import database.models as models
from database import get_db
from test_auth import all_four_login, all_four_register, OLGA, NICK, MARY

olga_post = {"title": "The Importance of AI",
             "body": "AvecVou",
             "topics": ["Tech"],
             "expires_at": datetime.strftime(datetime.now() + timedelta(hours=24), "%Y-%m-%d %H:%M:%S"),
             }

nick_post = {"title": "HPC Moredenisation",
             "body": "AvecVou",
             "topics": ["Tech"],
             "expires_at": datetime.strftime(datetime.now() + timedelta(hours=24), "%Y-%m-%d %H:%M:%S"),
             }

mary_post = {"title": "BDT optiomisations at the LHC",
             "body": "AvecVou",
             "topics": ["Tech", "Physics"],
             "expires_at": datetime.strftime(datetime.now() + timedelta(hours=24), "%Y-%m-%d %H:%M:%S"),
             }


def test_tc03(client, all_four_login):
    olga_login, nick_login, mary_login, nest_login = all_four_login
    profile = client.post("piazza_posts/post",
                          json={"title": "Hello Calgary",
                                "body": "AvecVou",
                                "topics": ["Poetry"],
                                "expires_at": datetime.strftime(datetime.now() + timedelta(hours=24),
                                                                "%Y-%m-%d %H:%M:%S"),
                                "username": OLGA["username"]}
                          )
    print(profile.text)
    assert profile.status_code == 401


def test_tc04(client_db, all_four_login):
    client, db = client_db

    olga_login, nick_login, mary_login, nest_login = all_four_login
    token = olga_login.json()["access_token"]
    profile = client.post("piazza_posts/post",
                          headers={"Authorization": f"Bearer {token}"},
                          json=olga_post
                          )
    print(profile.text)
    assert profile.status_code == 201

    # db = next(get_db())
    db = db()
    db = next(db)
    print(db)
    print(type(db))

    print(db.query(models.Topic).first().topic_name)
    assert db.query(models.Topic).first().topic_name == "Tech"

def test_tc05_06(client_db, all_four_login):
    client, db_gen_func = client_db

    olga_token, nick_token, mary_token, nest_token = [login.json()["access_token"] for login  in all_four_login]
    olga_post_r = client.post("piazza_posts/post",
                          headers={"Authorization": f"Bearer {olga_token}"},
                          json=olga_post
                          )
    nick_post_r = client.post("piazza_posts/post",
                          headers={"Authorization": f"Bearer {nick_token}"},
                          json=nick_post
                          )
    mary_post_r = client.post("piazza_posts/post",
                          headers={"Authorization": f"Bearer {mary_token}"},
                          json=mary_post
                          )

    assert nick_post_r.status_code == 201
    assert mary_post_r.status_code == 201
    assert olga_post_r.status_code == 201
    assert nick_post_r.json()["username"] == NICK["username"]
    assert mary_post_r.json()["username"] == MARY["username"]

    db = next(db_gen_func())

    # print(db.query(models.Topic).first().topic_name)
    # posts = db.query(models.Topic).filter(models.Topic.topic_name == "Tech").all()
    # for post in posts:
    #     print(post.post_id)
    #     print(db.query(models.Post).filter(models.Post.post_id == post.post_id).first().title)