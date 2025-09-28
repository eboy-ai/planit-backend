from pydantic_settings import BaseSettings
from pydantic import Field

class Setting(BaseSettings):
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_host: str = Field("localhost", alias="DB_HOST")
    db_port: str = Field("3306", alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")

    # JWT settings
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"
        populate_by_name = True
    
    @property
    def db_url(self) -> str:
        return f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property  # 비동기 DB URL
    def async_db_url(self) -> str:
        return f"mysql+asyncmy://{self.db_url}"

    @property  # 동기 DB URL
    def sync_db_url(self) -> str:
        return f"mysql+pymysql://{self.db_url}"


settings = Setting()