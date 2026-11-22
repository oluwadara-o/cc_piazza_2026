"""
TC01	Olga, Nick, Mary and Nestor register successfully
TC02	All four users log in and receive tokens
"""
import pytest

OLGA = {"username": "olga@", "email": "olga@example.com", "password": "secret123"}
NICK = {"username": "nick", "email": "nick@example.com", "password": "apples"}
MARY = {"username": "mary", "email": "mary@example.com", "password": "bananas"}
NESTOR = {"username": "nestor1", "email": "nestor@example.com", "password": "pears!"}



@pytest.fixture
def all_four_register(client):
    olga_reg = client.post("/auth/register", json=OLGA)
    nick_reg = client.post("/auth/register", json=NICK)
    mary_reg = client.post("/auth/register", json=MARY)
    nest_reg = client.post("/auth/register", json=NESTOR)
    yield olga_reg, nick_reg, mary_reg, nest_reg

@pytest.fixture
def all_four_login(client, all_four_register):
    olga_login = client.post("/auth/login", json={"username":OLGA["username"], "password":OLGA["password"]})
    nick_login = client.post("/auth/login", json={"username":NICK["username"], "password":NICK["password"]})
    mary_login = client.post("/auth/login", json={"username":MARY["username"], "password":MARY["password"]})
    nestor_login = client.post("/auth/login", json = {"username": NESTOR["username"], "password": NESTOR["password"]})
    return olga_login, nick_login, mary_login, nestor_login


def test_tc01(client, all_four_register):
    all_reg = all_four_register
    for reg in all_reg:
        print(reg.json())
        assert reg.status_code == 201

    all_reg_json = (reg.json() for reg in all_reg)
    olga_username, nick_username, mary_username, nest_username = (_json["username"] for _json in all_reg_json)
    print(all_reg_json)
    print(olga_username, nick_username, mary_username, nest_username)
    assert olga_username == OLGA["username"]
    assert nick_username == NICK["username"]
    assert mary_username == MARY["username"]
    assert nest_username == "nestor1"

def test_tc02(all_four_login):
    all_reg = all_four_login
    for reg in all_reg:
        print(reg.json())
        assert reg.status_code == 200
        print(reg.json())
        # TODO check token exists