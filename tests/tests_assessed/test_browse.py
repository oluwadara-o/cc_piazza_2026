"TC07	Tech browsing returns three posts with no initial reactions or comments"
from test_auth import all_four_login, all_four_register
from test_create_post import add_tech_posts

def test_tc07(client_db, add_tech_posts, all_four_login):
    client, db_gen_func = client_db
    olga_post_r, nick_post_r, mary_post_r = add_tech_posts
    olga_token, nick_token, mary_token, nest_token = [login.json()["access_token"] for login in all_four_login]
    tech_browse = client.get("piazza_posts/post/topic/tech",
                              headers={"Authorization": f"Bearer {olga_token}"}
                              )
    print(tech_browse)
    print(tech_browse.status_code)
    print(tech_browse.text)
    print(tech_browse.json())

    assert tech_browse.status_code == 200
