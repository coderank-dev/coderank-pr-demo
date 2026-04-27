"""Pydantic models for the demo API.

Uses Pydantic v2 patterns throughout: ``model_config`` instead of an inner
``Config`` class, and ``field_validator`` instead of the v1 ``validator``.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    display_name: str = Field(min_length=1, max_length=64)

    @field_validator("display_name")
    @classmethod
    def _no_at_sign(cls, value: str) -> str:
        if "@" in value:
            raise ValueError("display_name must not contain '@'")
        return value


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    display_name: str
    created_at: datetime


class PostCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)
    author_id: int


class Post(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str
    author_id: int
    created_at: datetime


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
