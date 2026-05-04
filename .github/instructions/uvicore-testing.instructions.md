---
description: "Use when adding or modifying Uvicore app tests, or when generating new Uvicore app features that should include framework-style tests. Covers pytest structure, async patterns, fixture usage, test placement, and expectations for provider/config wiring tests."
name: "Uvicore Testing Conventions"
---
# Uvicore Testing Conventions

Use these rules when generating tests for a Uvicore app.

## General Style

- Follow the existing pytest style used in this workspace and in the Uvicore framework tests.
- Prefer focused tests by feature area instead of one large mixed integration file.
- Use `@pytest.mark.asyncio` for async behavior.
- Reuse app bootstrap fixtures and shared setup patterns instead of inventing a second bootstrap path.
- Keep test names explicit about the behavior being validated.

## Placement

- Put app tests under the app `tests/` folder.
- Group tests by feature area such as CLI, HTTP, database, or unit-level utilities.
- Keep test files near the concern they validate in naming and structure.

## What New Features Must Test

- Provider wiring so new features are actually registered.
- Config-driven behavior when prefixes, connections, drivers, or bindings are added.
- CLI command registration and execution behavior for new commands.
- API or web routing behavior for new HTTP features.
- Database tables, models, relationships, and seed data behavior for new data features.
- Integration with cache, events, auth, redis, mail, or db when the feature depends on them.

## Preferred Test Shape

- Prefer testing real app behavior over shallow import-only assertions when practical.
- Assert outcomes that matter to users, such as route responses, query results, registered commands, or rendered behavior.
- Keep setup minimal and rely on shared fixtures when possible.
- Add regression tests for bugs that were fixed.

## Expectations For Generated Code

- New Uvicore app features should include tests unless the user explicitly says not to add them.
- If a feature adds provider changes, config changes, and runtime behavior, tests should cover all three layers where reasonable.
- If a feature cannot be tested end to end, add the highest-value focused tests closest to the changed behavior.
