---
name: coinfound-rwa-schema-probe
description: Probe CoinFound RWA endpoint schemas and refresh bundled schema snapshots when documentation is incomplete.
version: 0.1.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
---

# CoinFound RWA Schema Probe

Self-contained schema probing for CoinFound RWA endpoints.

## Scope

- Primary responsibilities:
  - infer endpoint schemas
  - discover sample entity values such as `ticker`, `platform`, `issuer`, or `network`
  - classify the response `shape_family`
  - refresh `schema_snapshots`
- Does not serve as the default read path for integrations. Normal reads belong to `$coinfound-rwa-read`.

## Workflow

1. Read the bundled catalog and existing snapshots first to confirm the gap.
2. Run entity discovery and sample probing only for uncovered or conflicting endpoints.
3. Infer field types, nullability, nested array structure, and `shape_family`.
4. Write or refresh the bundled snapshot when the live response is stable enough to keep.

## Bundled Resources

Read first:

- `shared/coinfound_rwa/data/endpoint_catalog.json`
- `shared/coinfound_rwa/data/schema_snapshots/`

Run:

- `shared/coinfound_rwa/scripts/discover_entities.py`
- `shared/coinfound_rwa/scripts/probe_schema.py`

## Minimal Examples

```bash
python3 shared/coinfound_rwa/scripts/discover_entities.py \
  --asset-class platforms
```

```bash
python3 shared/coinfound_rwa/scripts/probe_schema.py \
  --endpoint-key stable-coin.dataset \
  --path-params '{"ticker":"USDT"}'
```

```bash
python3 shared/coinfound_rwa/scripts/probe_schema.py \
  --endpoint-key platforms.detail.asset.dataset \
  --path-params '{"platform":"tether-holdings"}' \
  --write-snapshot
```

## Expected Output

Suggested output:

- `sample_request`
- `sample_response`
- `inferred_schema`
- `shape_family`
- `notes`
- `snapshot_path` when a write occurs

## References

- `references/rwa-probe-workflow.md`
- `references/rwa-probe-strategy.md`
- `references/rwa-probe-snapshot-policy.md`
