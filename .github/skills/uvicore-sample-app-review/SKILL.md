---
name: uvicore-sample-app-review
description: 'Review sample-app changes to check whether the example app still reflects current Uvicore framework best practices. Use for auditing provider wiring, config layout, routes, commands, models, tests, and whether the sample remains a good canonical example for users.'
argument-hint: 'Describe the sample-app change or review target'
user-invocable: true
---

# Uvicore Sample App Review

Use this skill when reviewing changes in the sample app and the main question is whether the example app still matches current Uvicore conventions and teaches the right patterns.

## When To Use

- Review a sample-app PR before merge.
- Audit whether a sample-app change drifted away from current framework best practices.
- Check whether the sample still demonstrates the recommended provider, config, CLI, HTTP, and database patterns.
- Review whether sample-app tests and docs implications were updated alongside the code.

## Outcome

Produce a review that checks whether the sample app:

- still reflects current framework best practices
- keeps provider/config/runtime wiring coherent
- remains a good example for users reading the repo or docs
- includes the right tests for changed example behavior

## Procedure

1. Inspect the changed sample-app files and identify which app surface changed: provider, bootstrap, config, CLI, HTTP, database, views, public assets, or tests.
2. Compare the changed structure against current Uvicore app conventions using [review checklist](./references/review-checklist.md).
3. Check that the sample still uses the expected register vs boot responsibilities.
4. Check that config remains split cleanly and that new behavior is driven through config when appropriate.
5. Check that commands, routes, models, tables, seeders, views, public assets, and HTTP entrypoints are registered in the provider and placed in the expected folders.
6. Check whether tests were updated to cover the changed example behavior.
7. Flag any places where the sample now teaches a weaker or non-recommended pattern compared to the framework conventions.

## Review Rules

- Prefer findings that explain how the sample diverges from recommended Uvicore practice.
- Treat the sample app as teaching material, not only as working code.
- Flag changes that technically work but demonstrate a less preferred pattern than the framework expects.
- Call out missing provider wiring, config drift, route drift, or test drift explicitly.

## Required Checks

- Does `package/provider.py` still follow Uvicore best practices?
- Are `register()` and `boot()` responsibilities still respected?
- Does `config/app.py` still aggregate concern-specific config cleanly?
- Are new routes, commands, models, tables, or seeders registered in the provider?
- Do new sample-app features include tests?
- Should related docs in the docs repo be updated because the sample changed what it demonstrates?

## References

- [review checklist](./references/review-checklist.md)
- [example drift signals](./references/example-drift-signals.md)
