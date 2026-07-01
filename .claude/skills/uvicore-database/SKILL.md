---
name: uvicore-database
description: "Working with data in a Uvicore app — defining database tables (database/tables/), ORM models (models/) with fields and relations, seeders (database/seeders/), querying with the async ORM query builder, configuring connections (config/database.py), and the ./uvicore db CLI commands. Use when adding or querying models/tables/seeders in a Uvicore application. Requires the 'database' extra."
user-invocable: true
---

# Uvicore Database (Models, Tables, Seeders, Queries)

Requires the `database` extra (and `uvicore.database`+`uvicore.orm` in `config/dependencies.py` —
the installer adds these if you chose database support). The stub ships empty `models/`,
`database/tables/`, `database/seeders/`; the provider already registers those folders in `boot()`:

```python
self.register_db_connections(connections=self.package.config.database.connections,
                             default=self.package.config.database.default)
self.register_db_models(['acme.appstub.models'])
self.register_db_tables(['acme.appstub.database.tables'])
self.register_db_seeders(['acme.appstub.database.seeders.seed'])
```
Use `['acme.appstub.models']` if you keep a `models/__init__.py` index, or
`['acme.appstub.models.*']` for wildcard import. Order doesn't matter — tables are sorted
topologically for foreign keys.

## 1. Define a table (`database/tables/post.py`)
Tables are plain SQLAlchemy column definitions wrapped in a Uvicore `Table`.

```python
import sqlalchemy as sa
import uvicore
from uvicore.database import Table

@uvicore.table()
class Posts(Table):
    name = 'posts'                 # table name WITHOUT prefix (prefix comes from connection config)
    connection = 'appstub'         # a connection name from config/database.py
    schema = [
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('slug', sa.String(255), unique=True),
        sa.Column('title', sa.String(255)),
        sa.Column('creator_id', sa.Integer, sa.ForeignKey('users.id')),
    ]
    schema_kwargs = {}
```
Generate one with `./uvicore gen table post`.

## 2. Define a model (`models/post.py`)
Models are Pydantic-v2-backed (use v2 idioms; pipe typing `X | None`, not `Optional[...]`) and link
to a table via `__tableclass__`.

```python
from __future__ import annotations
from typing import List
import uvicore
from uvicore.orm import Model, ModelMetaclass, Field, BelongsTo, HasMany, BelongsToMany
from acme.appstub.database.tables import post as table

@uvicore.model()
class Post(Model['Post'], metaclass=ModelMetaclass):
    """App Posts"""
    __tableclass__ = table.Posts

    id: int | None    = Field('id', primary=True, read_only=True)
    slug: str          = Field('slug', max_length=255, description='URL slug')
    title: str         = Field('title')
    creator_id: int    = Field('creator_id')

    # Relations (field name is yours; the string is the related model's module path):
    creator: User | None = Field(None, relation=BelongsTo('uvicore.auth.models.user.User'))
    comments: List[Comment] | None = Field(None,
        relation=HasMany('acme.appstub.models.comment.Comment', foreign_key='post_id'))
    tags: List[Tag] | None = Field(None,
        relation=BelongsToMany('acme.appstub.models.tag.Tag',
                               join_tablename='post_tags', left_key='post_id', right_key='tag_id'))

# If relations use forward refs (quoted/late types), import them at the bottom of the file
# (keep `from __future__ import annotations` at the top). No model_rebuild()/update_forward_refs()
# call needed — Uvicore rebuilds every registered model centrally at boot (Pydantic v2):
from acme.appstub.models.comment import Comment   # isort:skip
```

`Field(column, *, primary, description, default, sortable, searchable, read_only, write_only,
callback, relation, max_length, example, ...)`. The field name can differ from the DB column.
`read_only` fields are excluded from writes; `write_only` from reads. Generate with
`./uvicore gen model post`.

### Relation types (`from uvicore.orm import ...`)
- `BelongsTo(model, foreign_key='id', local_key='{field}_id')` — FK is on THIS table.
- `HasOne(model, foreign_key=...)` / `HasMany(model, foreign_key=...)` — FK on the RELATED table.
- `BelongsToMany(model, join_tablename=, left_key=, right_key=)` — pivot table.
- `MorphOne`/`MorphMany`/`MorphToMany(..., polyfix='taggable')` — polymorphic.

## 3. Query — async ORM query builder
```python
from acme.appstub.models.post import Post

posts = await Post.query().get()                                  # all
post  = await Post.query().find(1)                                # by primary key
posts = await Post.query().where('title', 'like', '%hello%').get()
posts = await (Post.query()
    .include('creator', 'comments', 'tags')                       # eager-load relations (dot-nested ok)
    .where('creator_id', 5)
    .order_by('id', 'DESC')
    .limit(25).offset(0)
    .get())
count = await Post.query().count()
```
Chainable: `where(col, op='=', val)`, `or_where([...])`, `include(*rels)`, `filter()/or_filter()`
(filter related rows of a *Many), `sort()`, `order_by()`, `limit()`, `offset()`, `key_by(field)`,
`show_writeonly()`, `cache(key, seconds=)`. Terminal (await): `get()`, `find(pk)`, `count()`,
`update(**kwargs)`, `delete()`. Operators: `= != > < >= <= in !in like !like`.

### Writes
```python
post = Post(slug='hello', title='Hello', creator_id=1)
await post.save()                          # insert or update by PK
await Post.insert([{...}, {...}])           # bulk insert
await post.create('tags', [tag1, tag2])     # insert children + link (alias .add)
await post.link('tags', [tag3])             # link existing (pivot only) / .unlink(...)
await post.delete()
```
Lifecycle hooks you can override on a model (async): `_before_save`, `_after_save`,
`_before_insert`, `_after_insert`, `_before_delete`, `_after_delete` (call `await super()...`).

## 4. Seeders (`database/seeders/`)
A seeder is an async fn that uses your models. The provider registers
`acme.appstub.database.seeders.seed`, so create a `seed.py` (or `__init__.py` exposing `seed`) that
runs your individual seeders:

```python
# database/seeders/posts.py
import uvicore
from acme.appstub.models.post import Post

@uvicore.seeder()
async def seed():
    uvicore.log.item('Seeding posts')
    await Post(slug='first', title='First', creator_id=1).save()
```
Generate with `./uvicore gen seeder posts`.

## 5. Connections (`config/database.py`)
Multiple named connections; pick the default. SQLite/MySQL/Postgres/Snowflake. Use `env(...)`:
```python
database = {
  'default': env('DATABASE_DEFAULT', 'appstub'),
  'connections': {
    'appstub': {'backend': 'sqlalchemy', 'dialect': 'sqlite',
                'driver': 'aiosqlite', 'database': ':memory:', 'prefix': None},
  },
}
```
A model's `connection` attribute (via its table) names which connection it uses.

## 6. `./uvicore db` CLI commands
`./uvicore db create <conn>` (build tables), `db drop <conn>`, `db recreate <conn>`,
`db seed <conn>`, `db reseed <conn>` (drop+create+seed), `db connections`. Comma-separate multiple
connections.

## Checklist
- [ ] Table in `database/tables/`, decorated `@uvicore.table()`, `name`/`connection`/`schema` set.
- [ ] Model in `models/`, `@uvicore.model()` + `metaclass=ModelMetaclass`, `__tableclass__` linked.
- [ ] Forward-ref relation types imported at the bottom of the file (no `update_forward_refs()`/`model_rebuild()` call — Uvicore rebuilds models centrally at boot).
- [ ] Models/tables/seeders folders registered in the provider (stub already does this).
- [ ] Want CRUD endpoints for free? Register the model → it appears in the auto-API (`uvicore-api`).
- [ ] Test queries with the `appstub` fixture (enable DB drop/create/seed in conftest) — see `uvicore-testing`.
