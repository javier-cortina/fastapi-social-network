## this file is completely useless now, because we have moved it to conftest.py


from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base

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