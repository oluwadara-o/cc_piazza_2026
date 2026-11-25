"""TC08	Nick and Olga like Mary’s post
TC09	Nestor likes Nick’s post and dislikes Mary’s post
TC10	Counts show Mary with two likes and one dislike, and Nick with one like
TC11	Mary’s attempt to like her own post is rejected
"""
from test_auth import all_four_login, all_four_register
from test_create_post import add_tech_posts

def test_tc08(client_db, add_tech_posts, all_four_login):
    client, db_gen_func = client_db
    olga_post_r, nick_post_r, mary_post_r = add_tech_posts
    olga_token, nick_token, mary_token, nest_token = [login.json()["access_token"] for login in all_four_login]
    mary_post_id = mary_post_r.json()['post_id']

    nick_react = client.post(f"piazza_posts/post/{mary_post_id}/reaction",
                             headers={"Authorization": f"Bearer {nick_token}"},
                             json={"reaction_type": "like"}
                             )
    olga_react = client.post(f"piazza_posts/post/{mary_post_id}/reaction",
                             headers={"Authorization": f"Bearer {olga_token}"},
                             json={"reaction_type": "like"}
                             )
    assert nick_react.status_code == 200
    assert olga_react.status_code == 200

def test_tc09(client_db, add_tech_posts, all_four_login):
    client, db_gen_func = client_db
    olga_post_r, nick_post_r, mary_post_r = add_tech_posts
    olga_token, nick_token, mary_token, nest_token = [login.json()["access_token"] for login in all_four_login]
    mary_post_id = mary_post_r.json()['post_id']
    nick_post_id = nick_post_r.json()['post_id']

    nestor_like = client.post(f"piazza_posts/post/{nick_post_id}/reaction",
                              headers={"Authorization": f"Bearer {nest_token}"},
                              json={"reaction_type": "like"}
                              )
    nestor_dislike = client.post(f"piazza_posts/post/{mary_post_id}/reaction",
                                 headers={"Authorization": f"Bearer {nest_token}"},
                                 json={"reaction_type": "dislike"}
                                 )
    assert nestor_like.status_code == 200
    assert nestor_dislike.status_code == 200

def test_tc10(client_db, add_tech_posts, all_four_login):
    client, db_gen_func = client_db
    olga_post_r, nick_post_r, mary_post_r = add_tech_posts
    olga_token, nick_token, mary_token, nest_token = [login.json()["access_token"] for login in all_four_login]
    mary_post_id = mary_post_r.json()['post_id']
    nick_post_id = nick_post_r.json()['post_id']

    nick_react = client.post(f"piazza_posts/post/{mary_post_id}/reaction",
                             headers={"Authorization": f"Bearer {nick_token}"},
                       json={"reaction_type": "like"}
                             )
    olga_react = client.post(f"piazza_posts/post/{mary_post_id}/reaction",
                            headers={"Authorization": f"Bearer {olga_token}"},
                            json={"reaction_type": "like"}
                            )
    assert nick_react.status_code == 200
    assert olga_react.status_code == 200
    nestor_like = client.post(f"piazza_posts/post/{nick_post_id}/reaction",
                             headers={"Authorization": f"Bearer {nest_token}"},
                             json={"reaction_type": "like"}
                             )
    nestor_dislike = client.post(f"piazza_posts/post/{mary_post_id}/reaction",
                                headers={"Authorization": f"Bearer {nest_token}"},
                                json={"reaction_type": "dislike"}
                                )
    assert nestor_like.status_code == 200
    assert nestor_dislike.status_code == 200

    tech_browse = client.get("piazza_posts/post/topic/tech",
                              headers={"Authorization": f"Bearer {olga_token}"}
                              )
    print(tech_browse)
    print(tech_browse.status_code)
    print(tech_browse.text)
    print(tech_browse.json())
    assert False


def test_tc11(client_db, add_tech_posts, all_four_login):
    client, db_gen_func = client_db
    olga_post_r, nick_post_r, mary_post_r = add_tech_posts
    olga_token, nick_token, mary_token, nest_token = [login.json()["access_token"] for login in all_four_login]
    mary_post_id = mary_post_r.json()['post_id']

    mary_react = client.post(f"piazza_posts/post/{mary_post_id}/reaction",
                             headers={"Authorization": f"Bearer {mary_token}"},
                             json={"reaction_type": "like"}
                             )

    assert mary_react.status_code == 403