from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()