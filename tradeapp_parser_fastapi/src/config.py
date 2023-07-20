from pydantic.v1.env_settings import BaseSettings


class MongoSettings(BaseSettings):
    MONGO_INITDB_DATABASE: str
    DATABASE_URL: str

    class Config:
        env_file = '.env'


mongo_settings = MongoSettings()
