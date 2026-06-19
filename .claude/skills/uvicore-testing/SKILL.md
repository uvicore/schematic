---
name: uvicore-testing
description: "Writing and running tests for a Uvicore application — the pytest layout in tests/, the appstub fixture in tests/conftest.py that boots the app, enabling DB drop/create/seed, async test patterns, testing HTTP routes with a client, and running via poetry run ./bin/test.sh. Use when adding or running tests in a Uvicore application."
user-invocable: true
---

# Uvicore Application Testing

Tests live in `tests/`. They boot the real app via the `appstub` fixture (your installer renamed it
from `appstub` to your app's short name) in `tests/conftest.py`, using pytest + pytest-asyncio.

## Running
This is a **Poetry** project — run through `poetry run`:
- All tests: `poetry run ./bin/test.sh`
- Coverage: `poetry run ./bin/test-cov.sh` (HTML: `poetry run ./bin/test-cov-html.sh`)
- A subset: `poetry run ./bin/test.sh tests/test_example.py`

## The `appstub` fixture (`tests/conftest.py`)
Session-scoped, async. It:
1. `from acme.appstub.package import bootstrap; bootstrap.Application(is_console=True)()` — boots the
   full app (providers register + boot).
2. dispatches `console.events.command.PytestStartup` → the DB layer connects all databases.
3. (optionally) drops/creates/seeds the DB — **commented out by default**; enable once you have
   tables/seeders:
   ```python
   from uvicore.database.commands import db
   await db.drop_tables('appstub')
   await db.create_tables('appstub')
   await db.seed_tables('appstub')
   ```
4. yields, then dispatches `PytestShutdown` on teardown (disconnect).

**Every test that touches the app takes the `appstub` fixture.** Import models/services *inside* the
test (after boot):

```python
import pytest

@pytest.mark.asyncio
async def test_posts_query(appstub):
    from acme.appstub.models.post import Post
    posts = await Post.query().get()
    assert isinstance(posts, list)
```

## Testing HTTP routes
Add an async HTTP client fixture (httpx) bound to the booted ASGI app, mirroring the framework's
pattern:
```python
# conftest.py
import pytest_asyncio
from httpx import AsyncClient

@pytest_asyncio.fixture(scope="session")
async def client():
    import uvicore
    async with AsyncClient(app=uvicore.app.http, base_url="http://testserver") as c:
        yield c
```
```python
@pytest.mark.asyncio
async def test_welcome(appstub, client):
    res = await client.get('/api/welcome')
    assert res.status_code == 200
    assert res.json()['data']['hello'] == 'World!'
```
> `testserver` is already in the API `TrustedHost` allow-list in `config/http.py`.

## Testing CLI commands
Boot the app (the `appstub` fixture) and either call the command's async function directly or use
AsyncClick's test runner. Assert on output / side effects (e.g. rows created).

## What to test in an app
- **Routes**: status code + body for web/API endpoints (use the `client`).
- **Models**: queries, relations, writes return expected data (enable DB seeding).
- **Commands**: registered and produce expected output/side effects.
- **Guards**: protected routes reject unauthenticated/under-scoped requests and allow authorized.
- **Config**: behavior that depends on prefixes/connections/toggles.
- Add a regression test for every bug you fix.

## Conventions
- `@pytest.mark.asyncio` on async tests; reuse the session `appstub`/`client` fixtures; keep setup
  minimal.
- Name tests for the behavior being verified.
- Prefer asserting real outcomes (HTTP responses, query rows) over import-only checks.
- Put tests in `tests/`, grouped by feature as the app grows.
