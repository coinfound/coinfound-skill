# RWA Probe Strategy

## 探测优先级

1. `list` / `aggregates`：先拿候选实体。
2. `dataset` / detail：确认深层结构。
3. `timeseries` / `pie`：确认稳定 shape。

## 重点 shape family

- `envelope_object`
- `envelope_list`
- `timeseries_aggregate`
- `pie_name_value`
- `dataset_wrapped_list`
- `dataset_nested_networks`
- `empty_success`

## 参数策略

- `platforms/{platform}` 优先使用 slug 值。
- `dataset/{ticker}` 需要先通过 discovery 拿候选值，不要硬编码 symbol。
- 同一 endpoint 至少使用两组参数探测，避免单样本偏差。

## 共享数据提醒

每次探测前先读：

- `../../shared/coinfound_rwa/data/endpoint_catalog.json`
- `../../shared/coinfound_rwa/data/schema_snapshots/`
