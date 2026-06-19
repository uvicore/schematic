---
name: uvicore-app-structure
description: "Orientation for developing a Uvicore application — the folder layout, the package-vs-app config split, config/dependencies.py, the provider register()/boot() lifecycle and its register_* helpers, the console + HTTP entrypoints, and the ./uvicore gen schematic generators. Read this first before adding any feature to a Uvicore app."
user-invocable: true
---

# Uvicore Application Structure

A Uvicore app (`acme.appstub` — your real `vendor.package`) is a Python package that uses the
`uvicore` library. You build features in standard folders and **wire each one into the package
provider** so it loads. This skill is the map; the per-feature skills (`uvicore-web`, `uvicore-api`,
`uvicore-database`, `uvicore-commands`, `uvicore-config-and-auth`) have the details.

## The provider is your hub (`acme/appstub/package/provider.py`)

```python
@uvicore.provider()
class Appstub(Provider, Cli, Db, Redis, Http, Templating):   # mixins depend on installed extras
    def register(self) -> None:
        # CONFIG MERGES + light IoC binds + early event listeners ONLY.
        # Config is NOT fully merged yet; self.package is NOT available here.
        self.configs([{'key': self.name, 'value': self.package_config}])

    def boot(self) -> None:
        # REAL WIRING — config is fully merged now; self.package is available.
        self.registers(self.package.config.registers)
        # (DB block present only if you installed the 'database' extra:)
        self.register_db_connections(connections=..., default=...)
        self.register_db_models(['acme.appstub.models'])
        self.register_db_tables(['acme.appstub.database.tables'])
        self.register_db_seeders(['acme.appstub.database.seeders.seed'])
        self.register_views()        # views/public/assets   → uvicore-web
        self.register_routes()       # web + api routes      → uvicore-web / uvicore-api
        self.register_commands()     # CLI commands          → uvicore-commands
```

**The cardinal rule:** `register()` does config only; `boot()` does everything else. Anything you
add (route file, command, model) only takes effect once it's referenced from a `boot()` helper. The
`register_*` helper methods come from the framework mixins your provider inherits (`Cli`, `Db`,
`Http`, `Redis`, `Templating`).

## Two configs, two scopes

| File | Loaded when | Holds | Accessed via |
|---|---|---|---|
| `config/package.py` | ALWAYS (as app **or** imported as a library) | `version`, `web`/`api` prefixes, `registers` gate, generator `paths`, `database`, `redis`, `dependencies` | `uvicore.config['acme.appstub']` / `self.package.config` |
| `config/app.py` | ONLY when this package is the running app | `name`, `debug`, `main.{package,provider}`, and `server`/`web`/`api`/`auth`/`mail`/`cache`/`logger`/`overrides` | `uvicore.config.app.*` |

`config/app.py` and `config/package.py` each import smaller concern files (`http.py`,
`database.py`, `auth.py`, `dependencies.py`, ...). Keep that split — see `uvicore-config-and-auth`.

### `config/dependencies.py` — what framework features load
An `OrderedDict` of the **package providers** your app depends on. Always includes
`uvicore.foundation`; the installer added `uvicore.database`+`uvicore.orm`, `uvicore.redis`,
`uvicore.http`+`uvicore.templating` based on the extras you chose. Add a dependency here (and the
matching mixin/import to the provider) to pull in another Uvicore package.

### `registers` gate (`config/package.py`)
A dict like `{'web_routes': True, 'models': True, 'commands': True, ...}`. When your package is used
as a library inside another app, this lets the host app disable parts of your registration. The
`register_*` helpers respect it.

## Entrypoints

- **Console** — `./uvicore` (the repo-root script): bootstraps `is_console=True`, makes `Console`
  from the IoC, runs the AsyncClick group. `./uvicore` lists commands; `./uvicore appstub welcome`
  runs one; `./uvicore http serve` starts the dev server.
- **HTTP** — `acme/appstub/http/server.py`: bootstraps `is_console=False` and exposes `http` for
  `uvicorn`/`gunicorn` (`serve-uvicorn`/`serve-gunicorn` scripts).
- **Bootstrap** — `acme/appstub/package/bootstrap.py` is shared by both: finds base path, loads
  `.env`, imports `config/app.py`, calls `uvicore.bootstrap(app_config, base_path, is_console)`.

## Schematic generators (`./uvicore gen ...`)
The framework ships generators that scaffold files into the folders defined by `config/package.py`
`paths`:
- `./uvicore gen command <name>` → `commands/<name>.py`
- `./uvicore gen model <name>` → `models/<name>.py`
- `./uvicore gen table <name>` → `database/tables/<name>.py`
- `./uvicore gen seeder <name>` → `database/seeders/<name>.py`
- `./uvicore gen controller <name>` / `gen api-controller <name>` → `http/controllers|api/<name>.py`
- `./uvicore gen composer <name>` → view composer
Generated files still need to be **registered/included in the provider or a routes file**.

## Adding a feature — the universal recipe
1. Decide the type (web / api / model / command / service) and pick the right folder + skill.
2. Create the file using the namespace `acme.appstub.*` for any module paths.
3. **Register it** in the provider's `boot()` (or include it from a routes file / models index).
4. Add config to the right concern file if behavior is config-driven (prefixes, connections,
   toggles) — never hardcode.
5. Add a test (`uvicore-testing`).
6. Run it: `./uvicore ...` or `./uvicore http serve`.

## Gotchas
- Heavy work in `register()` reads stale/empty config — move it to `boot()`.
- `self.package` is `None` in `register()`.
- A file that's never registered/imported never runs (its decorators never fire).
- Keep web vs api concerns separate; keep files in their standard folders so generators and other
  developers find them.
