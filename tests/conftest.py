from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

# override database with testing database for testing
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"  # modify string SQLALCHEMY_DATABASE_URL with '_test' in the end

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define testing client before each test
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)  # delete all of our tables for us
    Base.metadata.create_all(bind=engine)  # create all of our tables for us
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# fixture to create a new user
@pytest.fixture()
def test_user(client):
    user_data = {"email": "javi@gmail.com", "password": "password"}
    resp = client.post("/users/", json=user_data)
    assert resp.status_code == 201
    new_user = resp.json()
    new_user['password'] = user_data['password']
    return new_user

# fixture to create a second new user
@pytest.fixture()
def test_user2(client):
    user_data = {"email": "ines@gmail.com", "password": "password2"}
    resp = client.post("/users/", json=user_data)
    assert resp.status_code == 201
    new_user = resp.json()
    new_user['password'] = user_data['password']
    return new_user

# fixture to login and get a new token. We will use the get_access_token function from oauth2.py
@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

# fixture to get a new client which is also authorized
@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

# fixture to create a few testing posts as a base
@pytest.fixture()
def test_posts(test_user, test_user2, session):
    # define the testing data
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "4rd title",
            "content": "4rd content",
            "owner_id": test_user2['id']
        }
    ]

    # convert data for the proper format with the map function
    def create_post_model(post):
        return models.Post(**post)

    posts_mapped = map(create_post_model, posts_data)
    posts = list(posts_mapped)

    # insert data
    session.add_all(posts)
    session.commit()

    # retrieve inserted data
    return session.query(models.Post).all()
