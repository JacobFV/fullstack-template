from datetime import datetime
from enum import Enum
import functools
from pathlib import Path
import secrets
import warnings
from typing import Annotated, Any, Literal

import semver
from pydantic import (
    AnyUrl,
    BeforeValidator,
    Field,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
    AliasChoices,
    AmqpDsn,
    BaseModel,
    ImportString,
    RedisDsn,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    version_major: int
    version_minor: int
    version_patch: int

    @property
    def version(self) -> str:
        return f"{self.version_major}.{self.version_minor}.{self.version_patch}"

    @version.setter
    def version(self, value: str) -> None:
        try:
            version_info = semver.VersionInfo.parse(value)
            self.version_major = version_info.major
            self.version_minor = version_info.minor
            self.version_patch = version_info.patch
        except ValueError:
            raise ValueError(
                f"Invalid version format: {value}. Must be in the format '<major>.<minor>.<patch>'"
            )

    seeded_on: datetime | None = Field(env=False)
    start_time: datetime = Field(default_factory=datetime.utcnow, env=False)
    maintenance_mode: bool = Field(default=False)

    @property
    def duration_since_seed(self):
        return datetime.utcnow() - self.seeded_on

    @property
    def uptime(self):
        return datetime.utcnow() - self.start_time

    class Environment(Enum):
        dev = "dev"
        staging = "staging"
        production = "production"

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Environment = Environment.dev

    REDIS_DSN: RedisDsn = Field(
        "redis://user:pass@localhost:6379/1",
        validation_alias=AliasChoices("SERVICE_REDIS_DSN", "REDIS_URL"),
    )

    code_dir_override: str | None = Field(
        default=None, validation_alias=AliasChoices("CODE_DIR_OVERRIDE")
    )

    @computed_field  # type: ignore[misc]
    @property
    def code_dir(self) -> Path:
        import typer

        return typer.get_app_dir(app_name=self.app_name)

    app_name: str = Field("Gotcha", validation_alias=AliasChoices("APP_NAME"))

    LOG_FILE: str = "./logs/debug.log"
    LOG_FORMAT: str = r"{time} {level} {message}"
    LOG_LEVEL: str = "DEBUG"
    LOG_ROTATION: str = "10 MB"
    LOG_COMPRESSION: str = "zip"

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    PROJECT_NAME: str = "targets"
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # TODO: update type to EmailStr when sqlmodel supports it
    EMAIL_TEST_USER: str = "test@example.com"
    # TODO: update type to EmailStr when sqlmodel supports it
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @functools.wraps(super().__setattr__)
        def new_setattr_fn(name: str, value: Any) -> None:
            super(Settings, self).__setattr__(name, value)
            asyncio.create_task(store_settings(self))

        self.__setattr__ = new_setattr_fn


from app.core.shared_resources import get_redis_connection, settings

settings: Settings | None = None  # Global settings variable


async def store_settings(settings: Settings):
    redis = await get_redis_connection()
    await redis.set("app_settings", settings.to_json())
    await redis.publish("settings_channel", "updated")


async def get_settings() -> Settings:
    redis = await get_redis_connection()
    settings_json = await redis.get("app_settings")
    if settings_json:
        return Settings.from_json(settings_json)
    return Settings()  # Return default settings if not found in Redis


async def listen_for_settings_changes():
    redis = await get_redis_connection()
    pubsub = redis.pubsub()
    await pubsub.subscribe("settings_channel")
    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message and message["data"] == "updated":
            global settings  # Reference to the global settings object
            settings = await get_settings()


import asyncio


# Called start of application
async def init_settings():
    global settings
    settings = await get_settings()
    asyncio.create_task(listen_for_settings_changes())
