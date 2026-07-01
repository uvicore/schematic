---
name: uvicore-framework-reference
description: "Quick reference for the Uvicore framework that an app developer needs but cannot see (the framework is installed as a library in the uv virtualenv, not in this repo). Covers the import cheatsheet (where to import everything from), the uvicore.* globals, debugging with dump/dd, useful ./uvicore inspection commands, and how to read the installed framework source when a skill doesn't cover something."
user-invocable: true
---

# Uvicore Framework Reference (for App Developers)

The `uvicore` framework is a PyPI library installed into your uv virtualenv (`.venv/`) — its source is
**not** in this app repo and not in your editor by default. This skill is the cheatsheet so you
rarely need to go looking, plus how to look when you must.

## Import cheatsheet — where things come from

```python
import uvicore                       # the framework + globals + decorators

# Globals (available after bootstrap):
uvicore.app        # Application (app.name, app.version, app.package(main=True), app.http, app.debug)
uvicore.config     # merged config Dict  (uvicore.config.app.*, uvicore.config['acme.appstub'])
uvicore.log        # colored logger
uvicore.db         # database service (needs 'database' extra)
uvicore.cache      # cache service
uvicore.events     # event dispatcher
uvicore.jobs       # job dispatcher
uvicore.ioc        # IoC container (ioc.make('Name'))

# Decorators (all from `uvicore`):
@uvicore.provider()  @uvicore.service()  @uvicore.controller()  @uvicore.routes()
@uvicore.model()     @uvicore.table()    @uvicore.seeder()      @uvicore.event()
@uvicore.job()       @uvicore.composer()

# HTTP
from uvicore.http import Request, response          # response.View/HTML/JSON/Text/Redirect/File/Stream/UJSON/ORJSON
from uvicore.http.response import APIResponse
from uvicore.http.routing import (Routes, Controller, WebRouter, ApiRouter,
                                   WebRoute, ApiRoute, Router, Guard, ModelRouter, AutoApi)
from uvicore.http.params import Path, Query, Header, Cookie, Body, Form, File, Depends, Security
from uvicore.http.exceptions import (HTTPException, NotFound, PermissionDenied,
                                      NotAuthenticated, InvalidCredentials, BadParameter)
from uvicore.http import status                     # status.HTTP_200_OK, HTTP_404_NOT_FOUND, ...

# ORM / Database
from uvicore.orm import (Model, ModelMetaclass, Field,
                         BelongsTo, HasOne, HasMany, BelongsToMany, MorphOne, MorphMany, MorphToMany)
from uvicore.database import Table

# Console
from uvicore.console import command, group, argument, option
from uvicore.exceptions import SmartException

# Auth
from uvicore.auth import UserInfo

# Config / typing / debug
from uvicore.configuration import env, Env
from typing import List, Any                    # stdlib typing — use `X | Y` / `X | None` (not Union/Optional)
from uvicore.typing import Dict, OrderedDict     # SuperDict
from uvicore.support.dumper import dump, dd                                 # debugging
```

## The uvicore.* globals — common calls
- `uvicore.app.package(main=True).name` / `.version` — the running app's name/version.
- `uvicore.app.version` — the framework version. `uvicore.app.debug` — debug flag.
- `uvicore.config.app.api.prefix`, `uvicore.config.dotget('app.web.prefix')`,
  `uvicore.config['acme.appstub'].version` — config is a deep-merged `Dict`.
- `uvicore.ioc.make('Name')` — resolve any bound service/model by name or alias.
- `uvicore.log.info/header/item/notice/error(...)` — see `uvicore-framework-services`.

## Debugging: `dump` and `dd`
```python
from uvicore.support.dumper import dump, dd
dump(some_var, another)     # pretty-print (prettyprinter), keep going
dd(some_var)                # dump-and-die: print then stop execution
```
Use these liberally while developing routes/commands — `dd()` in a handler shows you exactly what a
request/query produced.

## Inspect the running app from the CLI
- `./uvicore` — list all command groups/commands.
- `./uvicore package list` — list loaded packages.
- `./uvicore http routes` — list all registered web/api routes with their **names** and paths
  (use the names in `url('...')` and tests).
- `./uvicore db connections` — list database connections (with the `database` extra).

## When the skills don't cover something — read the installed framework
The framework source is in your virtualenv. Find and grep it:
```bash
# Where is uvicore installed?
uv run python -c "import uvicore, os; print(os.path.dirname(uvicore.__file__))"

# Then read/grep that path, e.g. the public API of a service:
UVICORE=$(uv run python -c "import uvicore, os; print(os.path.dirname(uvicore.__file__))")
grep -rn "def " $UVICORE/orm/query.py            # ORM query builder methods
ls $UVICORE/contracts/                            # ABC interfaces = the documented public API
```
`uvicore/contracts/*.py` are the interface definitions for every service (Application, Database,
Cache, Logger, Router, Model, etc.) — the best place to confirm a public method signature. Major
modules: `orm/`, `database/`, `http/`, `console/`, `events/`, `jobs/`, `cache/`, `mail/`, `redis/`,
`auth/`, `templating/`, `configuration/`, `typing/`.

> Treat installed framework code as **read-only reference**. To customize framework behavior, use
> config overrides / IoC binding overrides from your app (see `uvicore-config-and-auth`), never edit
> files in the virtualenv.

## Don't guess
If you can't confirm an API from this cheatsheet, the other skills, or the stub examples, **inspect
the installed source** (above) rather than inventing a method name. The framework uses **Pydantic
v2** — use v2 idioms in models (and pipe-style typing `X | None`, not `Optional[...]`).
