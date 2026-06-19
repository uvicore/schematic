---
name: uvicore-config-and-auth
description: "Configuration and authentication for a Uvicore app — the package-vs-app config split, env() variables, concern config files, accessing config at runtime, overriding other packages' config/IoC bindings, HTTP middleware, and auth (Guards, scopes/permissions, the current user, the Authentication middleware). Use when working with config, middleware, permissions, or login in a Uvicore application."
user-invocable: true
---

# Uvicore Config & Auth

## Configuration

### The two-file split
- **`config/package.py`** — ALWAYS loaded (whether your package is the running app or imported as a
  library). Holds `version`, `web`/`api` prefixes, the `registers` gate, generator `paths`, and the
  `database`/`redis`/`dependencies` modules. Read at `uvicore.config['acme.appstub']` or, inside the
  provider, `self.package.config`.
- **`config/app.py`** — ONLY when this package is the running app. Holds `name`, `debug`,
  `main.{package,provider}`, and the `server`/`web`/`api`/`auth`/`mail`/`cache`/`logger`/`overrides`
  modules. Read at `uvicore.config.app.*`.

Both aggregate smaller **concern files** (`http.py`, `database.py`, `auth.py`, `mail.py`,
`cache.py`, `logger.py`, `overrides.py`, `dependencies.py`). Keep the split — put new settings in the
matching concern file, not inline in code.

### env() — environment values
```python
from uvicore.configuration import env
env('APP_NAME', 'Appstub App')        # str
env.bool('DEBUG', False)               # bool
env.int('SERVER_PORT', 5000)           # int
env.list('CORS_ALLOW_ORIGINS', [...])  # list
```
Edit `.env` (copied from `.env-example` at install) for machine-specific values. **Never hardcode**
environment-specific values — wrap them in `env()` in a config file.

### Reading config at runtime
```python
uvicore.config.app.name                       # app.py values
uvicore.config.app.api.auto_api               # nested
uvicore.config['acme.appstub'].version        # package.py values
uvicore.config.dotget('app.web.prefix')       # dot-path access
self.package.config.web.prefix                # inside the provider (package config)
```
Config is a deep-merged `Dict` (SuperDict) — use `.dotget()`/attribute access; missing keys return
empty, not errors.

### Overriding ANOTHER package's config or classes
This is a superpower of Uvicore — your app can reshape framework/3rd-party packages.
- **Config override** (deep-merge into another package's config) in your provider `register()`:
  ```python
  self.configs([
      {'key': self.name, 'value': self.package_config},
      {'key': 'uvicore.auth', 'module': 'acme.appstub.config.packages.auth.config'},  # override auth
  ])
  ```
- **IoC binding / provider overrides** in `config/app.py` `overrides`:
  ```python
  overrides = {
      'providers': { ... },          # replace an entire package's provider
      'ioc_bindings': {              # swap an individual class (Table, Model, etc.)
          'uvicore.auth.models.user.User': 'acme.appstub.models.user.User',
      },
  }
  ```
  Your override class can subclass the original (the framework binds the original under a `_BASE`
  name to avoid circular imports). See `config/overrides.py`.

## Authentication & Authorization

### The model
- An **Authentication middleware** runs per request, tries configured authenticators (e.g. Basic,
  JWT), and populates `request.user` / `request.scope['user']` with a `UserInfo` (anonymous if not
  logged in). Enable it per route-type in `config/app.py` `web.middleware` / `api.middleware`
  (commented out by default) and configure mechanisms in `config/auth.py`.
- **Guards/scopes** enforce permissions on routes. A user must have **ALL** listed scopes (AND
  logic); a superadmin bypasses every check.

### Applying guards (4 equivalent levels)
1. **Class-level** on a Routes/Controller class (applies to all its routes + children — preferred
   for whole sections):
   ```python
   class Admin(Controller):
       scopes = ['authenticated', 'admin']        # simplest
       # auth = Guard(['authenticated', 'admin'])  # equivalent
       # middleware = [Guard([...]), OtherMiddleware()]  # full stack
   ```
2. **Per-route shorthand**: `@route.get('/x', scopes=['post.read'])`.
3. **Per-route auth**: `@route.get('/x', auth=Guard(['post.read']))`.
4. **Per-route middleware**: `@route.get('/x', middleware=[Guard(['post.read'])])`.

### Getting the current user
```python
from uvicore.auth import UserInfo
from uvicore.http.routing import Guard

# Inject + guard in one step (also enforces the scopes):
@route.get('/me')
async def me(request: Request, user: UserInfo = Guard(['authenticated'])):
    return response.JSON({'email': user.email})

# Or read it from the request (guard separately via decorator scopes):
@route.get('/me2', scopes=['authenticated'])
async def me2(request: Request):
    user: UserInfo = request.scope['user']
```
`UserInfo` exposes `id, uuid, username, email, first_name, last_name, groups, roles, permissions,
superadmin, authenticated`, helpers like `is_admin`/`is_authenticated`, and `user.can(perms)`.

### Route groups with scopes
```python
@route.group('/admin', scopes=['authenticated'])
def admin():
    route.controller('dashboard')      # scopes merge with any nested groups/controllers
```

### Auto-API permissions
The automatic model CRUD API (see `uvicore-api`) defaults to `{tablename}.{create|read|update|
delete}` scopes per model. Tune via `config/app.py` `api.auto_api.scopes` (List, per-verb dict, or
`[]` for public) and `include`/`exclude`.

## Checklist
- [ ] New settings live in the right concern config file, wrapped in `env()` when environment-specific.
- [ ] Decide package-config (`package.py`) vs app-config (`app.py`) by whether it applies when used
      as a library.
- [ ] To protect routes, add class-level `scopes`/`auth` or per-route guards; enable the
      Authentication middleware so `request.user` is real.
- [ ] Overriding another package? Use `self.configs([...])` (config) or `overrides` (classes/providers).
- [ ] Test config effects and guard enforcement — see `uvicore-testing`.
