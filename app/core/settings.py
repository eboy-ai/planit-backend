from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_host: str = Field("localhost", alias="DB_HOST")
    db_port: str = Field("3306", alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")

    # JWT settings
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    #weather apikey
    weather_key: str = Field(alias="openweather_api_key")


    class Config:
        env_file = ".env"
        extra = "allow"
        populate_by_name = True
        case_sensitive = True

    @property
    def tmp_db(self) -> str:
        return f'{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
    
    @property
    def database_url(self) -> str:
        return f'mysql+aiomysql://{self.tmp_db}'

settings = Settings()