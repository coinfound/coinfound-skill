# RWA Read Capabilities

## 支持能力

- `get_rwa_aggregates`
- `get_rwa_timeseries`
- `get_rwa_pie`
- `get_rwa_list`
- `get_rwa_dataset`

## 支持的资产域

- `private-credit`
- `commodity`
- `institutional-fund`
- `government-bond`
- `corporate-bond`
- `stable-coin`
- `us-treasuries`
- `market-overview`
- `x-stock`
- `platforms`

## 共享数据优先级

调用前优先查看：

- `../../shared/coinfound_rwa/data/endpoint_catalog.json`
- `../../shared/coinfound_rwa/data/schema_snapshots/`
