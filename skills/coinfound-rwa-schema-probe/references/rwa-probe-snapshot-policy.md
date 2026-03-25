# RWA Snapshot Policy

## Goal

Treat `schema_snapshots` as the first schema source for the read skill so live probing stays exceptional.

## Write Rules

- Write or refresh a snapshot only when:
  - an endpoint is successfully probed for the first time
  - the existing snapshot is missing critical fields
  - the live response clearly conflicts with the existing snapshot
- Keep these fields in the stored snapshot:
  - `endpoint_key`
  - `shape_family`
  - `inferred_schema`
  - `sample_response`
  - `updated_at`

## Quality Bar

- Mark a snapshot as stable only after at least two independent requests agree on the shape.
- Record `empty_success` explicitly and do not merge it with `data: null`.
- Preserve deep nested arrays such as `dataset[*].networks` without flattening.

## Handoff To The Read Skill

`$coinfound-rwa-read` should consume snapshots first and should not trigger probing by default. Hand off to probe only when data is missing or conflicting.

## Bundled Data Reminder

Read these directories first:

- `shared/coinfound_rwa/data/endpoint_catalog.json`
- `shared/coinfound_rwa/data/schema_snapshots/`
