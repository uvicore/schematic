# Uvicore Application — Developer Guide (CLAUDE.md)

This is a **Uvicore application/package** (namespace `acme.appstub` — your installer replaces this
with your real `vendor.package`, e.g. `mreschke.wiki`). It is built **on top of** the
[Uvicore framework](https://github.com/uvicore/framework), which is installed as a PyPI library
(`uvicore` with the `database`/`redis`/`web` extras). You write *application* code here — routes,
controllers, models, commands — not framework internals.

> If you are reading this in the freshly-installed app, `acme`/`appstub`/`Appstub` below were
> rewritten to your chosen names during install.

> **The framework source is NOT in this repo** — `uvicore` lives in the Poetry virtualenv's
> site-packages. These skills carry the framework knowledge you need; when you need an API that
> isn't here, use the `uvicore-framework-reference` skill (cheatsheet + how to read the installed
> source) instead of guessing.

## Skills — load the right one for the task

Specialized skills live in `.claude/skills/`. **Read the matching skill before building that kind
of feature** — each has the real patterns, the exact registration step, and the gotchas.

| Skill | Use when you want to… |
|---|---|
| `uvicore-app-structure` | understand the app layout, package-vs-app config, `dependencies.py`, the provider `register()`/`boot()` lifecycle, entrypoints, and the `./uvicore gen` generators. **Read this first.** |
| `uvicore-web` | add web routes, web controllers, Jinja views, templates, public files, and assets. |
| `uvicore-api` | add API routes, API controllers, `APIResponse`, the automatic model CRUD API (ModelRouter), and OpenAPI docs. |
| `uvicore-database` | add ORM models, database tables, seeders; query data; run `./uvicore db` commands. |
| `uvicore-commands` | add CLI commands and groups; use the schematic generators. |
| `uvicore-config-and-auth` | work with config (env, concern files, overriding other packages), middleware, and auth — Guards, scopes/permissions, the current user. |
| `uvicore-services-events-jobs` | add your own IoC services, event listeners (incl. app lifecycle & model events), and background jobs. |
| `uvicore-framework-services` | use built-in services: caching, email, rendering a template to a string (Templates), Redis, the logger, and the shared HTTP client. |
| `uvicore-framework-reference` | the framework import cheatsheet, `uvicore.*` globals, `dump`/`dd` debugging, `./uvicore` inspection commands, and how to read the framework source in the venv. **The framework isn't in this repo — start here when you need an API you can't recall.** |
| `uvicore-testing` | write and run tests for the app (`poetry run ./bin/test.sh`, the `appstub` fixture, DB seeding). |

There are also legacy GitHub Copilot files in `.github/` (app conventions + a sample-app-review
skill). They're good background; the `.claude/` skills above are the primary guide.

## What a Uvicore app is

A Uvicore app is a normal Python package (`acme/appstub/`) that depends on the `uvicore` library and
runs through one of two entrypoints:

- **Console**: `./uvicore` (bootstraps with `is_console=True`, runs the AsyncClick CLI). Try
  `./uvicore`, `./uvicore appstub welcome`, `./uvicore http serve`.
- **HTTP**: `acme/appstub/http/server.py` exposes `http` for `uvicorn`/`gunicorn` (see
  `serve-uvicorn`, `serve-gunicorn`, or `./uvicore http serve` for dev).

Everything is wired through the **package provider** (`acme/appstub/package/provider.py`). Adding a
feature is almost always: create the file in the right folder → **register it in the provider** so
it actually loads.

## The mental model (provider lifecycle)

`package/bootstrap.py` finds the base path, loads `.env`, imports `config/app.py`, and calls
`uvicore.bootstrap(...)`. The framework then runs every package provider's:
- **`register()`** — merge configs (`self.configs([...])`), light IoC binds, early event listeners
  ONLY. No real work; config isn't fully merged yet; `self.package` is unavailable here.
- **`boot()`** — the real wiring: `register_db_connections/models/tables/seeders`,
  `register_views()`, `register_routes()`, `register_commands()`. All config is merged now.

The stub provider already calls helper methods (`register_views`, `register_routes`,
`register_commands`, and a DB block if you installed the `database` extra). Extend those.

## Config: two files, two scopes
- **`config/package.py`** — ALWAYS loaded, whether your package runs as the app or is imported as a
  library by another app. Holds `version`, `web`/`api` prefixes, the `registers` gate, generator
  `paths`, and `database`/`redis`/`dependencies`. Reached at `uvicore.config['acme.appstub']` /
  `self.package.config`.
- **`config/app.py`** — ONLY used when THIS package is the running app. Holds `name`, `debug`,
  `main.package`/`main.provider`, and the `server`/`web`/`api`/`auth`/`mail`/`cache`/`logger`/
  `overrides` modules. Reached at `uvicore.config.app.*`. (If your package is library-only you can
  delete `app.py` and its imports.)

`config/dependencies.py` lists the **package providers** your app depends on (always
`uvicore.foundation`; plus `uvicore.database`/`uvicore.orm`/`uvicore.redis`/`uvicore.http`/
`uvicore.templating` depending on the extras you chose). This drives what framework features load.

All config values use `env('KEY', default)` / `env.int(...)` / `env.bool(...)` / `env.list(...)`
from `uvicore.configuration`. Edit `.env` (copied from `.env-example`) for environment-specific
values.

## Dev workflow
- **Poetry** project. Install: `poetry install`. The `uvicore` dep is a local path dep to
  `../framework` with `database,redis,web` extras during development.
- **Run the app**: `./uvicore` (CLI), `./uvicore http serve` (dev web server at
  http://127.0.0.1:5000, API docs at `/api/docs`).
- **Tests**: `poetry run ./bin/test.sh` (and `poetry run ./bin/test-cov.sh`). See `uvicore-testing`.
- **Generators**: `./uvicore gen <type> <name>` scaffolds commands/models/controllers/etc. into the
  folders defined by `config/package.py` `paths`.
- **DB**: `./uvicore db create|seed|reseed <connection>` (needs the `database` extra + a connection
  in `config/database.py`).

## App directory map (`acme/appstub/`)
```
package/      bootstrap.py (entry) + provider.py (wires everything — your hub)
config/       app.py, package.py, http.py, database.py, auth.py, cache.py, mail.py,
              logger.py, overrides.py, dependencies.py
commands/     CLI command modules (welcome.py)              → uvicore-commands
http/
  routes/     web.py (Web Routes), api.py (Api Routes)      → uvicore-web / uvicore-api
  controllers/ web controllers (welcome.py)                 → uvicore-web
  api/        api controllers (welcome.py)                  → uvicore-api
  views/appstub/   Jinja2 .j2 templates                     → uvicore-web
  public/     browser-served files; public/assets/ static   → uvicore-web
  server.py   ASGI entrypoint (exposes `http`)
models/       ORM models (empty until you add them)         → uvicore-database
database/
  tables/     SQLAlchemy table definitions                  → uvicore-database
  seeders/    data seeders                                  → uvicore-database
```
The `welcome` route/controller/command/view are working examples — copy their shape. Every stub
file is heavily commented with more patterns.

## Golden rules
1. **Wire it in the provider.** A model/route/command that isn't registered does nothing.
2. **`register()` = config only; `boot()` = real work.**
3. **Routes/controllers must `return route`** — the whole router is one recursive nested structure.
4. **Web views need `request` piped through** the context dict; reference routes by **name**
   (`{{ url('acme.appstub.welcome') }}`) and assets via `{{ asset('appstub/...') }}`, never raw
   paths (paths change; names don't).
5. Use `env()` for anything environment-specific; keep it in the right concern config file.
6. Use your package namespace (`acme.appstub`) consistently in module paths.
