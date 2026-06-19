---
name: uvicore-services-events-jobs
description: "Extending a Uvicore app with your own logic layer — binding custom services into the IoC container (@uvicore.service / uvicore.ioc.make), defining and listening to events (@uvicore.event, Event.listen, app lifecycle events, reacting to ORM model events), and defining/dispatching background jobs (@uvicore.job). Use when adding reusable services, event listeners, or jobs to a Uvicore application."
user-invocable: true
---

# Uvicore Services, Events & Jobs (App Logic Layer)

When app logic doesn't fit in a route/command/model, reach for these three patterns. All are
decorator-based and resolved through the IoC container.

## 1. Custom services (IoC)

Put reusable logic in a service class, bind it to the container, resolve it anywhere.

```python
# acme/appstub/services/billing.py
import uvicore

@uvicore.service('acme.appstub.services.billing.Billing', aliases=['Billing'], singleton=True)
class Billing:
    async def charge(self, user, amount): ...
```
Resolve it:
```python
billing = uvicore.ioc.make('Billing')          # by alias
billing = uvicore.ioc.make('acme.appstub.services.billing.Billing')   # by full name
await billing.charge(user, 1000)
```
- `@uvicore.service(name=None, *, singleton=False, aliases=[], factory=None, kwargs=None)`. Default
  name is `{module}.{Class}`. `singleton=True` → one shared instance; otherwise resolved fresh.
- The class's module must be **imported** for the decorator to register it. If it isn't imported by
  normal use, bind it explicitly in your provider `register()`:
  `self.bind('Billing', 'acme.appstub.services.billing.Billing', singleton=True)`, or import it from
  a module the provider already loads.
- For a documented contract, define an ABC and have the service implement it (mirrors the framework's
  `uvicore/contracts/` pattern) — optional but nice for swappable services.
- `uvicore.ioc.make(name, default=None, **kwargs)` also accepts a default + kwargs for lazy binding.

## 2. Events

Define an event, listen with handlers, dispatch when something happens. Great for decoupling.

```python
# acme/appstub/events/post.py
import uvicore
from uvicore.events import Event

@uvicore.event()
class PostCreated(Event):
    """Fired after a post is created"""
    is_async = True                      # True = supports async handlers / codispatch()
    def __init__(self, post):
        self.post = post
```
Listen (register listeners in your provider's `register()` — early is fine for listeners):
```python
# provider.py register()
from acme.appstub.events.post import PostCreated
PostCreated.listen('acme.appstub.listeners.notify.Notify')   # module path or callable
# priority: lower runs first (default 50) -> PostCreated.listen(handler, priority=10)
```
A listener is a callable or a class with `__call__(self, event)`:
```python
# acme/appstub/listeners/notify.py
class Notify:
    async def __call__(self, event):     # event.post is available
        ...
```
Dispatch:
```python
await PostCreated(post).codispatch()     # async (== dispatch_async)
PostCreated(post).dispatch()             # sync
```
- `Event.listen / listener / handle / handler / call` are all the same registration method.
- Wildcard string listeners are supported: `uvicore.events.listen('acme.appstub.events.*', handler)`.

### React to app lifecycle & framework events
```python
# Run code after ALL packages have booted (e.g. cross-package setup):
from uvicore.foundation.events import app as AppEvents
AppEvents.Booted.listen('acme.appstub.listeners.ready.Ready')

# React to ORM model writes (fired by the framework per model):
uvicore.events.listen('acme.appstub.models.post.Post-AfterSave', my_handler)
# Event name pattern: {model.modelfqn}-BeforeInsert|AfterInsert|BeforeSave|AfterSave|BeforeDelete|AfterDelete
```
> Prefer overriding the model's `_before_save()` / `_after_save()` hooks for per-model logic (see
> `uvicore-database`); use event listeners for cross-cutting reactions.

## 3. Jobs

A job is a unit of work with an async `handle()` — dispatch it from routes, commands, or listeners.

```python
# acme/appstub/jobs/rebuild_index.py
import uvicore

@uvicore.job()
class RebuildIndex:
    """Rebuild the search index"""
    def __init__(self, scope: str):
        self.scope = scope
    async def handle(self):
        ...                              # do the work; return a result (optionally a JobResults model)
        return {'rebuilt': self.scope}
```
Dispatch:
```python
result = await RebuildIndex('posts').codispatch()    # async (== dispatch_async)
result = RebuildIndex('posts').dispatch()             # sync
```
The job dispatcher simply runs `handle()`. For richer return values, subclass
`uvicore.jobs.results.JobResults` (a Pydantic model) for clean printing.

## Where files go (and the `paths` config)
Conventional folders (override in `config/package.py` `paths`): `services/`, `events/`,
`listeners/`, `jobs/`. Keep one concern per module.

## Checklist
- [ ] Service: `@uvicore.service(...)`, resolve with `uvicore.ioc.make(...)`; ensure it gets imported
      (bind in provider if needed).
- [ ] Event: `@uvicore.event()` subclass of `Event`, set `is_async`; register listeners in provider
      `register()`; dispatch with `await ....codispatch()`.
- [ ] Job: `@uvicore.job()` class with async `handle()`; dispatch with `await ....codispatch()`.
- [ ] Test the behavior with the `appstub` fixture — see `uvicore-testing`.
