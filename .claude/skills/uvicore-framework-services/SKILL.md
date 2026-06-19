---
name: uvicore-framework-services
description: "Using the built-in Uvicore framework services from app code — caching (uvicore.cache), email (Mail), the Templates engine (render a Jinja .j2 to a string, e.g. for email bodies or CLI output), Redis (uvicore.ioc.make('redis')), the colored logger (uvicore.log), and the shared aiohttp HTTP client. Covers their async APIs and the matching config files. Use when an app needs to cache, send mail, render a template to a string, talk to Redis, log, or make outbound HTTP calls."
user-invocable: true
---

# Uvicore Built-in Services (Cache, Mail, Templating, Redis, Log, HTTP Client)

These ship with the framework and are configured in your app's concern config files. All I/O is
async.

## Cache — `uvicore.cache` (config/cache.py)
Stores: `array` (in-memory, default) and `redis` (ties to a `config/database.py` redis connection).
```python
import uvicore

await uvicore.cache.put('key', value, seconds=600)     # store (0 = forever)
await uvicore.cache.get('key', default=None)           # fetch
await uvicore.cache.has('key')                          # bool
await uvicore.cache.add('key', value, seconds=60)       # put only if absent -> bool
await uvicore.cache.pull('key')                         # get + forget
await uvicore.cache.forget('key')                       # delete one
await uvicore.cache.flush()                             # clear store
await uvicore.cache.increment('hits', 1)                # / decrement('hits', 1)
await uvicore.cache.touch('key', seconds=120)

# remember = get-or-compute-and-store:
val = await uvicore.cache.remember('expensive', my_async_callback, seconds=300)

# pick a non-default store:
await uvicore.cache.store('redis').put('k', v, seconds=60)
```
Config: `config/cache.py` sets `default` store and per-store `driver`/`connection`/`prefix`/
`seconds`. Redis caching needs the `redis` extra + a `cache` redis connection in `config/database.py`.

## Mail — `Mail` (config/mail.py)
Fluent, chainable builder; send is async.
```python
from uvicore.mail import Mail        # or: uvicore.ioc.make('Mail')

await (Mail()
    .to(['user@example.com'])
    .cc([]).bcc([])
    .from_name('Acme').from_address('no-reply@acme.test')
    .subject('Welcome')
    .html('<h1>Hi</h1>')
    .text('Hi')
    .send())
```
Also `.mailer('name')` / `.mailer_options({...})` / `.attachments([...])`. Defaults (default mailer,
from name/address, driver) come from `config/mail.py` (`app.mail.*`). Backends are driver-based
(e.g. mailgun in `uvicore/mail/backends/`). For an HTML email body, render a template to a string
first (below) and pass it to `.html(...)`.

## Templating — render a `.j2` to a string (`Templates` service)
Web routes return `await response.View('appstub/page.j2', {...})` (see `uvicore-web`). For NON-web
rendering — an email body, a CLI report, a generated file — use the `Templates` service to render a
template to a **string**:
```python
import uvicore
templates = uvicore.ioc.make('templates')          # aliases: 'Templates', 'templates'
html = templates.render('appstub/emails/welcome.j2', {'name': user.first_name})
await Mail().to([user.email]).subject('Welcome').html(html).send()
```
- `render(template_name, data={}) -> str` is synchronous and returns the rendered string.
- It resolves templates from the paths your provider registered. Your web view path
  (`register_http_views(['acme.appstub.http.views'])`) is available; to register a separate
  non-web templates directory, add the `Templating` provider mixin and call
  `self.register_templating_paths(['acme.appstub.templates'])` in `boot()`.
- The same `url()` / `asset()` context functions and any view composers apply.

## Redis — `uvicore.ioc.make('redis')` (config/database.py → redis)
Requires the `redis` extra.
```python
import uvicore

redis = await uvicore.ioc.make('redis').connect('appstub')   # connection name; omit for default
await redis.set('key', 'value')
val = await redis.get('key')
# full aioredis async command surface: hset/hget, lpush, zadd, expire, etc.
```
`uvicore.ioc.make('redis').connection('appstub')` returns the connection config; `.connect()` returns
a pooled `redis.asyncio.Redis`. Connections are defined in `config/database.py` under `redis`.

## Logger — `uvicore.log`
Colored, structured console logging. Standard levels plus layout helpers:
```python
uvicore.log.info('message');   uvicore.log.notice('heads up')
uvicore.log.warning('careful'); uvicore.log.error('bad'); uvicore.log.debug('detail')
uvicore.log.header('Section');  uvicore.log.header2('Sub'); uvicore.log.header3('...')
uvicore.log.item('bullet');     uvicore.log.item2('nested')      # indented bullets
uvicore.log.line();  uvicore.log.nl();  uvicore.log.separator()
uvicore.log.name('mylogger').info('scoped')                       # named sub-logger
```
Great inside CLI commands and seeders. Configured in `config/logger.py` (handlers, levels, filters).

## HTTP client — shared aiohttp session
The `uvicore.http_client` package (a default dependency) opens one shared `aiohttp.ClientSession`
on startup, bound to the IoC as `aiohttp` / `http_client`.
```python
import uvicore

session = uvicore.ioc.make('aiohttp')          # shared aiohttp.ClientSession (alias 'http_client')
async with session.get('https://api.example.com/things') as resp:
    data = await resp.json()
```
Don't create/close your own session for normal calls — reuse this one (the framework closes it on
shutdown). Use it from routes, commands, jobs, services.

## Enabling / configuring
Each service is active only if its package is a dependency (`config/dependencies.py`) and its extra
is installed (`database`, `redis`, `web`). The installer wired these based on the extras you chose.
Cache, mail and logging come with the foundation; Redis needs the `redis` extra; the `Templates`
service is registered by `uvicore.templating` (included with the `web` extra) — a CLI-only app
without web won't have it unless you add `uvicore.templating` to `config/dependencies.py`. Tune
behavior in the matching concern config file (`cache.py`, `mail.py`, `logger.py`, `database.py`)
using `env(...)` — never hardcode hosts/keys.

## Checklist
- [ ] Service's package/extra is installed and listed in `config/dependencies.py`.
- [ ] Connection/store/mailer configured in the right concern config file via `env()`.
- [ ] All calls `await`ed; reuse the shared aiohttp session rather than making new ones.
- [ ] Test side effects with the `appstub` fixture — see `uvicore-testing`.
