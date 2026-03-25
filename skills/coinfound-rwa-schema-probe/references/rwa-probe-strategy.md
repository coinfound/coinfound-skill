# RWA Probe Strategy

## Probe Priority

1. Use `list` and `aggregates` routes to collect candidate entity values first.
2. Use `dataset` and detail routes to confirm deep nested structures.
3. Use `timeseries` and `pie` routes to verify the stable response shape.

## Important Shape Families

- `envelope_object`
- `envelope_list`
- `timeseries_aggregate`
- `pie_name_value`
- `dataset_wrapped_list`
- `dataset_nested_networks`
- `empty_success`

## Parameter Strategy

- Prefer slug values for `platforms/{platform}`.
- For `dataset/{ticker}`, discover candidate values first instead of hard-coding a symbol.
- Probe the same endpoint with at least two parameter sets when possible to reduce single-sample bias.

## Bundled Data Reminder

Read these files before every probe:

- `shared/coinfound_rwa/data/endpoint_catalog.json`
- `shared/coinfound_rwa/data/schema_snapshots/`
