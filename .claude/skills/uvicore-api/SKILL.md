---
name: uvicore-api
description: "Building REST API features in a Uvicore app — API routes (http/routes/api.py), API controllers (http/api/), the APIResponse envelope, returning ORM models, the automatic model CRUD API (ModelRouter / auto_api), OpenAPI/Swagger docs, route guards/scopes, and HTTP exceptions. Use when adding JSON/REST endpoints to a Uvicore application."
user-invocable: true
---

# Uvicore API (Routes, Controllers, Auto-API)

API endpoints live under `acme/appstub/http/api/` and are registered by the provider via
`register_http_api_routes(module='acme.appstub.http.routes.api.Api', prefix=...)`. The API runs on
its own FastAPI sub-server (default prefix `/api`) with full OpenAPI docs at `/api/docs`.

## 1. The api routes file (`http/routes/api.py`)

```python
import uvicore
from uvicore.http.routing import Routes, ApiRouter, ModelRouter

@uvicore.routes()
class Api(Routes):
    # Class-level scopes/auth/middleware apply to all child routes (see uvicore-config-and-auth).
    def register(self, route: ApiRouter):
        route.controllers = 'acme.appstub.http.api'
        route.controller('welcome')                                   # → http/api/welcome.py

        # Automatic CRUD API for all registered ORM models:
        route.include(ModelRouter, options=uvicore.config.app.api.auto_api)
        return route                                                  # ALWAYS return the router
```

## 2. An API controller (`http/api/welcome.py`)

```python
import uvicore
from uvicore.http import Request
from uvicore.http.response import APIResponse
from typing import List
from uvicore.typing import Dict
from uvicore.http.exceptions import HTTPException
from uvicore.http.routing import ApiRouter, Controller

@uvicore.controller()
class Welcome(Controller):
    def register(self, route: ApiRouter):

        @route.get('/welcome', tags=['Welcome'])
        async def welcome(request: Request) -> APIResponse[dict]:
            response = APIResponse.begin()          # starts the response timer
            user = request.scope['user']            # current (possibly anonymous) user
            data = {'hello': 'World!', 'welcome': user.email}
            return response(data)                   # standard envelope

        return route
```

API route methods accept extra OpenAPI kwargs vs web: `tags=[...]`, `summary`, `description`,
`response_model=`, `response_class=`, `responses={...}`, plus the common `name/scopes/auth/
middleware/autoprefix`. The handler's `-> Type` return hint also drives the OpenAPI schema.

## 3. Returning data — three idioms
- **APIResponse envelope** (adds api_version/timing/paging metadata):
  ```python
  async def list(request: Request) -> APIResponse[List[Dict]]:
      response = APIResponse.begin()
      return response(data)                                   # non-paged
      return response(data, total_count=2, page=1, page_size=25)  # paged
  ```
- **Return ORM models directly** (FastAPI/Pydantic serializes them):
  ```python
  async def show(id: int) -> models.Post:
      return await models.Post.query().find(id)
  # or @route.get('/posts', response_model=List[models.Post]) and return the list
  ```
- The docstring of an endpoint shows up in OpenAPI.

## 4. The automatic model CRUD API (`ModelRouter`)
`route.include(ModelRouter, options=uvicore.config.app.api.auto_api)` auto-generates REST endpoints
for **every registered ORM model**: `GET /` (list, with query-param filtering/sorting/paging),
`GET /{id}`, `POST /`, `POST /with_relations`, `PUT /{id}`, `PATCH /{id}`, `DELETE /{id}`.

Configured in `config/app.py` under `api.auto_api`:
- `scopes`: override the default per-model CRUD scopes (`{tablename}.{create|read|update|delete}`).
  `[]` makes the auto-API public (no permissions). Or a per-verb dict
  `{'create': '...', 'read': '...', ...}`.
- `include` / `exclude`: wildcard model lists, e.g. `'acme.appstub.models.*'`, `'uvicore.auth.*'`.

List endpoint query params are JSON: `?include=["creator","tags"]`,
`?where=["field","op","value"]`, `?order_by=...`, `?page=2&page_size=50`.

## 5. Guards / scopes / current user (summary — see `uvicore-config-and-auth`)
- Per-route shorthand: `@route.get('/x', scopes=['authenticated', 'post.read'])`.
- Or `auth=Guard(['authenticated'])`, or `middleware=[Guard([...])]`.
- Inject the user: `async def x(..., user: UserInfo = Guard(['authenticated'])):` or read
  `request.scope['user']`. User must have **ALL** listed scopes (AND); superadmin bypasses.
- OAuth2 for the OpenAPI docs is toggled by `config/app.py` `api.openapi.oauth2_enabled` (auth
  middleware must be enabled in `api.middleware` for guards to populate a real user).

## 6. Errors
```python
from uvicore.http.exceptions import HTTPException
raise HTTPException(404, 'Not found')
raise HTTPException(500, message='Friendly title', detail='...', exception=e)  # exception shown only if app.debug
```
The API exception handler (`config/app.py` `api.exception.handler`) renders the standard
`APIErrorResponse`.

## Checklist
- [ ] API controller under `http/api/`, decorated `@uvicore.controller()`, `register()` returns the router.
- [ ] Mounted from `http/routes/api.py` (`route.controller('...')`).
- [ ] Use `APIResponse.begin()` / `return response(data)` or a typed model return for serialization.
- [ ] `tags=` set so it groups nicely in `/api/docs`.
- [ ] Auto-API: register your models (see `uvicore-database`); set `auto_api` scopes/include/exclude.
- [ ] Guard sensitive endpoints with scopes; raise `HTTPException` for errors.
- [ ] Test via the `appstub` fixture + HTTP client — see `uvicore-testing`.
