from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.models import PostCreate, UserCreate


def test_user_create_strips_whitespace_and_validates_email() -> None:
    user = UserCreate(email="  alice@example.com  ", display_name="  Alice  ")
    assert user.email == "alice@example.com"
    assert user.display_name == "Alice"


def test_user_create_rejects_at_sign_in_display_name() -> None:
    with pytest.raises(ValidationError) as exc:
        UserCreate(email="bob@example.com", display_name="bo@b")
    assert "display_name must not contain '@'" in str(exc.value)


def test_post_create_requires_non_empty_title_and_body() -> None:
    with pytest.raises(ValidationError):
        PostCreate(title="", body="hi", author_id=1)
    with pytest.raises(ValidationError):
        PostCreate(title="hi", body="", author_id=1)
