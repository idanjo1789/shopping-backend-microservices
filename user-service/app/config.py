from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "user-service"

    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root"
    MYSQL_DATABASE: str = "user_db"
    MYSQL_HOST: str = "mysql-user"
    MYSQL_PORT: str = "3306"

    DATABASE_URL: str = (
        f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )

    SECRET_KEY: str = "idan-josifov"
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRY_TIME: int = 60

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()