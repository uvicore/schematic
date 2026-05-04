# Uvicore Sample App Drift Signals

Flag review findings when the sample app starts doing things users should not copy.

## Common Drift Signals

- Heavy work moved into `register()`.
- New runtime behavior added without provider registration.
- Config split abandoned in favor of hardcoded values.
- New routes or commands added in nonstandard locations.
- New models, tables, or seeders added without consistent provider registration.
- Tests missing for new example behavior.
- The sample demonstrates a shortcut that conflicts with the framework's preferred best practice.

## Review Framing

- Explain not only that something changed, but why it weakens the sample as canonical guidance.
- Prefer findings that say what pattern the sample should demonstrate instead.
