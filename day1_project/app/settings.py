import sys
from enum import Enum 
from functools import lru_cache
from typing import Literal
from pydantic import Field,PostgresDsn,SecretStr, field_validator
from pydantic_settings import BaseSettings,SettingsConfigDict

class Environment(str,Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class Settings(BaseSettings):
    ENV: Environment = Field(
        default=Environment.DEV,
        description="Target runtime environment(dev,staging,or prod)",
    )
    APP_NAME: str = Field(default="MyBackendService")
    DEBUG:bool = Field(default=False)
    PORT:int = Field(default=8000,ge=1024,le=65535)
    DATABASE_URL: PostgresDsn
    API_KEY: SecretStr

    @field_validator("DEBUG",mode="after")
    @classmethod
    def enforce_no_debug_in_prod(cls,v:bool,info)->bool:
        """Safety guard to prevent DEBUG mode in production environment"""
        env = info.data.get("ENV")
        if env == Environment.PROD and v:
            raise ValueError("DEBUG mode is not allowed in production environment")
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings()-> Settings:
    """"
    Creates and caches a the settings instance
    """
    print("---> [I/O INTENSIVE] Reading environment and instantiating settings")
    return Settings()

