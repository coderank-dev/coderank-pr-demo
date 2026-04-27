# coderank-pr-demo

Fixture repository used as the **review target** for [CodeRank Reviewer](https://github.com/coderank-dev/coderank-pr).
Pull requests opened here are picked up by the reviewer agent during local
development, integration tests, and the demo video.

The code intentionally looks like a tiny but realistic Python service:

- `src/models.py` - Pydantic v2 models
- `src/db.py` - SQLAlchemy 2.0 typed ORM
- `src/api.py` - FastAPI surface with the modern `lifespan` context

The `main` branch is always a **clean, idiomatic baseline**. PRs introduce
specific misuse patterns (often paired with one correct usage as a control)
to exercise the reviewer's citation-grounded checks.

## Stack

| Library     | Pin           |
|-------------|---------------|
| Python      | >=3.11,<3.14  |
| Pydantic    | >=2.9,<2.10   |
| FastAPI     | >=0.115       |
| SQLAlchemy  | >=2.0,<2.1    |

## Running tests

```bash
uv run --extra dev pytest -q
```

## Why this exists

CodeRank Reviewer cites every comment it posts back to the official docs of
the symbol it touched. To test that grounding works in practice we need a
small repo with PRs that mix:

1. Patterns LLMs nearly always get right (controls)
2. Patterns LLMs frequently hallucinate (hard cases)
3. Patterns where being right requires *current* documentation, not training data

This repo is that fixture.

## License

Apache-2.0. See [LICENSE](LICENSE).
