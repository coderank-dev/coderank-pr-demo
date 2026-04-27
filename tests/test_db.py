from __future__ import annotations

from sqlalchemy.orm import Session

from src.db import PostRow, UserRow, get_user_by_email, make_engine


def test_user_post_round_trip_uses_typed_orm() -> None:
    engine = make_engine()
    with Session(engine) as session:
        alice = UserRow(email="alice@example.com", display_name="Alice")
        session.add(alice)
        session.commit()
        session.refresh(alice)

        post = PostRow(title="Hello", body="world", author_id=alice.id)
        session.add(post)
        session.commit()
        session.refresh(post)

        loaded = get_user_by_email(session, "alice@example.com")
        assert loaded is not None
        assert loaded.id == alice.id
        assert [p.title for p in loaded.posts] == ["Hello"]


def test_get_user_by_email_returns_none_for_missing() -> None:
    engine = make_engine()
    with Session(engine) as session:
        assert get_user_by_email(session, "nobody@example.com") is None
