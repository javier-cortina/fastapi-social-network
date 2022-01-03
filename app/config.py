from pydantic import BaseSettings

# Environment variables. If they exist they are used, otherwise the default is used.
# Their name must match the environment variable's name, case insensitive
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # here we can specify where to look for them instead of in the environment variables
    class Config:
        env_file = ".env"

settings = Settings()