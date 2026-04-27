"""SQLAlchemy 2.0 typed ORM layer.

Uses the modern ``DeclarativeBase`` + ``Mapped`` / ``mapped_column`` style
introduced in SQLAlchemy 2.0. Avoids the legacy ``declarative_base()`` and
``Column(...)`` helpers, which are still importable but discouraged.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)

from .models import utcnow


class Base(DeclarativeBase):
    pass


class UserRow(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    display_name: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    posts: Mapped[list["PostRow"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )


class PostRow(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    author: Mapped[UserRow] = relationship(back_populates="posts")


def make_engine(url: str = "sqlite:///:memory:"):
    engine = create_engine(url, echo=False, future=True)
    Base.metadata.create_all(engine)
    return engine


def get_user_by_email(session: Session, email: str) -> Optional[UserRow]:
    stmt = select(UserRow).where(UserRow.email == email)
    return session.scalars(stmt).one_or_none()
