---
name: uvicore-commands
description: "Adding CLI commands to a Uvicore app — async command modules in commands/, the @command/@argument/@option decorators (AsyncClick), registering commands/groups in the provider via register_cli_commands, running them with ./uvicore <group> <command>, and the ./uvicore gen generators. Use when adding console commands to a Uvicore application."
user-invocable: true
---

# Uvicore CLI Commands

Commands live in `acme/appstub/commands/` and are **async**. They run through the `./uvicore`
console entrypoint. The stub ships `commands/welcome.py`, registered under the `appstub` group.

## 1. Write a command (`commands/welcome.py`)

```python
import uvicore
from uvicore.support.dumper import dump, dd
from uvicore.exceptions import SmartException
from uvicore.console import command, argument, option

@command()
async def cli():
    """Help text shown by ./uvicore appstub welcome --help"""
    try:
        print('Welcome to Uvicore!')
    except SmartException as e:
        exit(e.detail)        # non-empty exit() == error exit code in bash
```

With arguments/options:
```python
@command(help="Optional help override")
@argument('id_or_name')
@option('--tenant', help='Tenant')
@option('--coin', default='BTC', help='Coin with default')
@option('--json', is_flag=True, help='Output as JSON')
async def cli(id_or_name: str, tenant: str, coin: str, json: bool):
    """Shown as the command help"""
    ...
# Run: ./uvicore appstub get widget1 --tenant bob --json
```
`command`, `group`, `argument`, `option` come from `uvicore.console` (a colored AsyncClick wrapper).
The decorated function is **async** — you can `await` ORM queries, services, etc. By convention each
command module exposes a function named `cli` (the registration string points at it).

## 2. Register it in the provider (`package/provider.py` → `register_commands()`)

```python
def register_commands(self) -> None:
    self.register_cli_commands(
        group='appstub',
        help='Appstub Commands',
        commands={
            'welcome': 'acme.appstub.commands.welcome.cli',   # group cmd -> module path
        },
    )
```
- Pass `group=`/`help=`/`commands=` as kwargs (multiple calls append), **or** a full dict:
  `self.register_cli_commands({'appstub': {'help': '...', 'commands': {...}}})`.
- The value is a **module path string** to the command function — don't import it inline.
- Nested groups use `parent:child` as the group key.
- A command only appears once it's registered here (gated by the `registers.commands` flag).

Run it: `./uvicore` (lists groups/commands) → `./uvicore appstub welcome`.

## 3. Generators
- `./uvicore gen command <name>` scaffolds `commands/<name>.py` from the framework stub. You still
  add it to `register_commands()`.
- Other generators: `gen model`, `gen table`, `gen seeder`, `gen controller`, `gen api-controller`,
  `gen composer`. Destinations follow `config/package.py` `paths`.

## 4. Using services inside commands
Commands run inside the fully-booted app, so you have everything:
```python
@command()
async def cli():
    from acme.appstub.models.post import Post
    posts = await Post.query().get()
    uvicore.log.header('Posts'); [uvicore.log.item(p.title) for p in posts]
```
`uvicore.log` (colored logger with `.header/.item/.notice/...`), `uvicore.config`, `uvicore.db`,
`uvicore.ioc.make('Name')` are all available. `uvicore.console.command_is('migrate')` checks the
running command.

## Gotchas
- Commands are **async** — define `async def`, and `await` your I/O.
- Register the module path in the provider; an unregistered command won't show in `./uvicore`.
- `exit(value)` with a non-empty value signals an error exit code; catch `SmartException` and
  `exit(e.detail)` for clean error reporting.
- Test command behavior with the `appstub` fixture (and AsyncClick's test runner) — see
  `uvicore-testing`.
