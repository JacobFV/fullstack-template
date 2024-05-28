from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlmodel import Session
from app.schema.user.user import User


class Context(BaseModel):
    """
    In the future, we'll pass this around instead of user and session objects independently
    """

    app: FastAPI
    api_route: str
    user: "User" | None
    roles: list[str]
    db_session: Optional[Session]

    created_at: datetime = Field(default_factory=datetime.utcnow)
    entered_at: datetime
    exited_at: datetime

    def __enter__(self):
        self.entered_at = datetime.utcnow()

    def __exit__(self, exc_type, exc_value, traceback):
        self.exited_at = datetime.utcnow()
