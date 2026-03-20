---
name: coinfound-rwa-schema-probe
description: Probe CoinFound RWA endpoint schemas when docs are missing, and refresh schema snapshots in shared data.
---

# CoinFound RWA Schema Probe

用于在文档缺失或结构冲突时，探测 CoinFound RWA endpoint 的请求/响应结构，并刷新共享 schema 快照。

## 使用边界

- 主要职责：
  - 探测 endpoint schema
  - 发现可用实体参数（ticker/platform/issuer/network）
  - 归类 shape family
  - 刷新 `schema_snapshots`
- 不负责第三方常规读数聚合输出；常规读数交给 `$coinfound-rwa-read`。

## 执行流程

1. 优先读取共享 catalog 与已有快照，确认是否已覆盖。
2. 对缺口 endpoint 执行实体发现与样本探测。
3. 推断字段类型、可空性、数组元素结构与 shape family。
4. 将结果写入或更新 `schema_snapshots`。

## 共享资源（优先顺序）

优先读取：

- `../../shared/coinfound_rwa/data/endpoint_catalog.json`
- `../../shared/coinfound_rwa/data/schema_snapshots/`

再使用：

- `../../shared/coinfound_rwa/scripts/discover_entities.py`
- `../../shared/coinfound_rwa/scripts/probe_schema.py`

## 最小调用示例

```bash
python ../../shared/coinfound_rwa/scripts/discover_entities.py \
  --asset-class platforms
```

```bash
python ../../shared/coinfound_rwa/scripts/probe_schema.py \
  --endpoint-key stable-coin.dataset \
  --path-params '{"ticker":"USDT"}'
```

```bash
python ../../shared/coinfound_rwa/scripts/probe_schema.py \
  --endpoint-key platforms.detail.asset.dataset \
  --path-params '{"platform":"tether-holdings"}' \
  --write-snapshot
```

## 输出约定

建议输出：

- `sample_request`
- `sample_response`
- `inferred_schema`
- `shape_family`
- `notes`
- `snapshot_path`（当执行写入时）

## 参考文档

- `references/rwa-probe-workflow.md`
- `references/rwa-probe-strategy.md`
- `references/rwa-probe-snapshot-policy.md`
