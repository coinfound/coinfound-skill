# RWA Probe Workflow

## 前置顺序

先看共享数据，再决定是否探测：

- `../../shared/coinfound_rwa/data/endpoint_catalog.json`
- `../../shared/coinfound_rwa/data/schema_snapshots/`

若 catalog 标记为 `probe_required`，或 snapshot 缺失/过期，再执行探测。

## 标准步骤

1. 选定 `endpoint_key`。
2. 通过 `discover_entities.py` 获取可用 path/query 样本值。
3. 运行 `probe_schema.py` 做样本请求与结构推断。
4. 校验输出 shape family 与字段类型是否稳定。
5. 需要沉淀时写入 `schema_snapshots`。

## 命令示例

```bash
python ../../shared/coinfound_rwa/scripts/discover_entities.py \
  --endpoint-key x-stock.dataset
```

```bash
python ../../shared/coinfound_rwa/scripts/probe_schema.py \
  --endpoint-key x-stock.dataset \
  --path-params '{"ticker":"NVDA"}'
```
