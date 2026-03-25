# RWA Probe Workflow

## Preflight Order

Check the bundled data before probing:

- `shared/coinfound_rwa/data/endpoint_catalog.json`
- `shared/coinfound_rwa/data/schema_snapshots/`

Probe only when the catalog says `probe_required`, or when the snapshot is missing or outdated.

## Standard Steps

1. Select the target `endpoint_key`.
2. Use `discover_entities.py` to gather sample path values when the endpoint needs them.
3. Run `probe_schema.py` to execute a live sample request and infer the structure.
4. Verify that the `shape_family` and field types are stable.
5. Write to `schema_snapshots` only when the result is stable enough to keep.

## Command Examples

```bash
python3 shared/coinfound_rwa/scripts/discover_entities.py \
  --asset-class x-stock
```

```bash
python3 shared/coinfound_rwa/scripts/probe_schema.py \
  --endpoint-key x-stock.dataset \
  --path-params '{"ticker":"NVDA"}'
```
