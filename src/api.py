"""FastAPI surface for the demo service.

Uses the modern ``lifespan`` context manager pattern (introduced in
FastAPI 0.93 and recommended ever since); the legacy ``on_event`` startup
hook is avoided.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session, sessionmaker

from .db import PostRow, UserRow, make_engine
from .models import Post, PostCreate, User, UserCreate


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = make_engine()
    app.state.session_factory = sessionmaker(engine, expire_on_commit=False)
    try:
        yield
    finally:
        engine.dispose()


def get_session(app_state) -> Session:
    return app_state.session_factory()


app = FastAPI(title="coderank-pr-demo", lifespan=lifespan)


def _session_dep() -> Session:
    raise RuntimeError("session dependency must be overridden by the app")


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, session: Session = Depends(_session_dep)) -> UserRow:
    row = UserRow(email=payload.email, display_name=payload.display_name)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


@app.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, session: Session = Depends(_session_dep)) -> PostRow:
    author = session.get(UserRow, payload.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="author not found")
    row = PostRow(title=payload.title, body=payload.body, author_id=payload.author_id)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row
