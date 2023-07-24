from pydantic.v1.env_settings import BaseSettings


class MongoSettings(BaseSettings):
    MONGO_COLLECTION: str
    DATABASE_URL: str

    class Config:
        env_file = '.env'


mongo_settings = MongoSettings()
