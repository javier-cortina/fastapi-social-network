import pytest
from jose import jwt
from app import schemas
# from .database import client, session  # not needed anymore, because they are defined in the conftest.py file
from app.config import settings

# def test_root(client):
#     res = client.get("/")
#     assert res.json().get('message') == 'Welcome to my API!!'
#     assert res.status_code == 200

def test_create_user(client):
    resp = client.post("/users/", json={"email": "hello@gmail.com", "password": "password"})
    assert resp.status_code == 201
    new_user = schemas.UserOut(**resp.json())  # this also does a validation, not the actual values, but that it has the properties
    assert new_user.email == "hello@gmail.com"
    
def test_login_user(client, test_user):
    resp = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})  # in this case instead of sending it as a json, we send it as data
    assert resp.status_code == 200  # validate response code
    login_resp = schemas.Token(**resp.json())  # verify schema
    assert login_resp.token_type == 'bearer'
    payload = jwt.decode(login_resp.access_token, settings.secret_key, algorithms=[settings.algorithm])  # decode jwt token
    id = payload.get("user_id")  # extract id
    assert id == test_user['id']

@pytest.mark.parametrize("email, password, status_code",[
    ("wrongemail@gmail.com", "password", 403),
    ("javi@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    (None, "password", 422),  # schema validation failure, from pydantic, missing validation errors
    ("wrongemail@gmail.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    resp = client.post("/login", data={"username": email, "password": password})
    assert resp.status_code == status_code
    # assert resp.json().get('detail') == "Invalid Credentials"