# Uvicore Sample App Review Checklist

## Provider And Bootstrap

- `package/bootstrap.py` still handles base path, `.env`, app config import, and `uvicore.bootstrap(...)` cleanly.
- `package/provider.py` keeps `register()` limited to config merges and early wiring.
- `boot()` still owns routes, commands, views, assets, public paths, redis/db connections, models, tables, and seeders.

## Config

- `config/app.py` still aggregates app-level config modules clearly.
- New behavior uses concern-specific config files when appropriate.
- Runtime choices such as prefixes, connections, drivers, and toggles are not hardcoded in random modules.

## CLI, HTTP, And Database

- Commands remain in `commands/` and are registered through the provider.
- Web and API routes stay separate and are registered through provider helpers.
- Models, tables, and seeders stay in their expected folders and are registered through the provider.
- Views, public files, and assets remain in the standard HTTP structure.

## Tests

- Changed example behavior has tests.
- Tests cover runtime and wiring behavior when the sample demonstrates framework integration.

## Docs Impact

- If the sample app changes what users should copy or learn, related docs should be reviewed for updates.
