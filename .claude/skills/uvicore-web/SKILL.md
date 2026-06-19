---
name: uvicore-web
description: "Building server-rendered web features in a Uvicore app — web routes (http/routes/web.py), web controllers (http/controllers/), Jinja2 views/templates (http/views/), public files and static assets, the response.View/HTML/Text/Redirect helpers, route naming, and route groups. Use when adding browser-facing HTML pages to a Uvicore application."
user-invocable: true
---

# Uvicore Web (Routes, Controllers, Views)

Server-rendered HTML lives under `acme/appstub/http/`. Web routes are registered by the provider via
`register_http_web_routes(module='acme.appstub.http.routes.web.Web', prefix=...)` (already wired in
the stub's `register_routes()`).

## 1. The web routes file (`http/routes/web.py`)

A `Routes` class whose `register()` mounts controllers. It's the root of your web router.

```python
import uvicore
from uvicore.http.routing import Routes, WebRouter

@uvicore.routes()
class Web(Routes):
    # Class-level guards apply to ALL routes/children (see uvicore-config-and-auth):
    # scopes = ['authenticated']            # simplest
    # auth = Guard(['authenticated'])       # equivalent
    # middleware = [Guard([...]), ...]      # full control

    def register(self, route: WebRouter):
        route.controllers = 'acme.appstub.http.controllers'   # base path for relative names
        route.controller('welcome')                           # → controllers/welcome.py Welcome
        return route                                          # ALWAYS return the router
```

Controller path resolution from `route.controller('x')` / `.include('x')` (aliases):
- `'welcome'` → `{route.controllers}.welcome.Welcome`
- `'.sub.Other'` (leading dot) → append to `route.controllers` → `...controllers.sub.Other`
- `'full.module.path.Class'` (dots, no leading dot) → used as-is

## 2. A web controller (`http/controllers/welcome.py`)

```python
import uvicore
from uvicore.http import Request, response
from uvicore.http.routing import WebRouter, Controller

@uvicore.controller()
class Welcome(Controller):
    # Same class-level scopes/auth/middleware options as a Routes class.
    def register(self, route: WebRouter):

        @route.get('/', name='welcome')
        async def welcome(request: Request):
            me = uvicore.app.package(main=True)
            return await response.View('appstub/welcome.j2', {
                'request': request,                # REQUIRED for any View
                'app_name': me.name,
                'app_version': me.version,
            })

        return route                               # ALWAYS return the router
```

Route methods: `route.get/post/put/patch/delete(path, endpoint=None, *, name=None, autoprefix=True,
middleware=None, auth=None, scopes=None)`. Usable as a decorator (above) or directly
(`route.get('/x', my_fn)`). Every handler that renders a view takes `request: Request`.

## 3. Responses (`from uvicore.http import response`)
- `await response.View('appstub/template.j2', {'request': request, ...})` — render Jinja (async).
- `response.HTML('<b>hi</b>')`, `response.Text('hi')`, `response.JSON({...})`,
  `response.Redirect('/somewhere')`, `response.File(...)`, `response.Stream(...)`.
- GET query params: add typed params to the handler — `async def x(request: Request, name: str):`.
- POST form: `async def x(request: Request, name: str = Form(...)):` (`from uvicore.http.params
  import Form`).
- Errors: `from uvicore.http.exceptions import HTTPException; raise HTTPException(404, 'not found')`.

## 4. Views / templates (`http/views/appstub/*.j2`)
Jinja2 templates. The provider registers the view path with `register_http_views(['acme.appstub.
http.views'])`, so reference templates as `'appstub/welcome.j2'`. In templates:
- **Link by route name, not path**: `{{ url('acme.appstub.welcome') }}` — paths change when the app
  is mounted under a prefix; names are stable.
- **Static assets**: `{{ asset('appstub/images/uvicore.jpg') }}` and `{{ public('...') }}`.
- View composers (shared context for matching views) are registered with
  `register_http_view_composers(...)`; generate one with `./uvicore gen composer <name>`.

## 5. Public files & assets (`http/public/`, `http/public/assets/`)
- `register_http_public(['acme.appstub.http.public'])` — browser-served files (favicon, robots.txt)
  mounted at `/`.
- `register_http_assets(['acme.appstub.http.public.assets'])` — static assets mounted at `/assets`
  (configurable via `config/app.py` `web.asset.path`/`host`). Use `{{ asset('appstub/...') }}` to
  reference them.

## 6. Route naming & groups
- **Autoprefix**: a route named `welcome` becomes `acme.appstub.welcome` automatically; the URL path
  gets the package's `web.prefix`. To set a fully custom name, pass `autoprefix=False`.
- **Groups** (shared prefix/scopes/tags):
  ```python
  @route.group('/admin', scopes=['authenticated'])
  def admin():
      route.controller('dashboard')        # nested; scopes merge with parent
  ```
  `group()` works as a decorator or method (with `routes=[...]`). Nesting merges scopes and prefixes.

## Web web vs api
There is **no technical difference** between `http/routes/web.py`, `http/routes/api.py`, and
controllers — they're all one recursively-nested router, split only for clarity. Web routes render
HTML/templates; API routes return data + OpenAPI (see `uvicore-api`). The web FastAPI sub-server has
OpenAPI disabled.

## Checklist
- [ ] Controller created under `http/controllers/`, decorated `@uvicore.controller()`.
- [ ] Mounted from `http/routes/web.py` (`route.controller('...')`).
- [ ] Every `register()` **returns** the router.
- [ ] View handlers pipe `request` into the context; templates use `url()`/`asset()` not raw paths.
- [ ] Auth via class-level `scopes`/`auth` or per-route — see `uvicore-config-and-auth`.
- [ ] Test with the `appstub` fixture + an HTTP client — see `uvicore-testing`.
