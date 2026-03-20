---
name: coinfound-rwa-read
description: Read-only CoinFound RWA data skill for third-party integrations. Supports GET endpoints across the CoinFound RWA catalog.
---

# CoinFound RWA Read

用于第三方只读获取 CoinFound 的 RWA 数据。该 skill 只处理 `GET` 数据接口。

## 使用边界

- 支持：`v1/c/rwa/*` 下的 `aggregates`、`timeseries`、`pie`、`list`、`dataset`。
- 不负责 schema 探测与快照刷新；此类任务交给 `$coinfound-rwa-schema-probe`。

## 执行流程

1. 先读取共享目录中的接口与 schema 快照，再决定调用参数。
2. 按 `asset_class + family + metric` 或 `endpoint_key` 解析路由。
3. 通过共享脚本发起请求并归一化返回。
4. 若接口结构缺失或冲突，转交 `$coinfound-rwa-schema-probe`。

## 共享资源（优先顺序）

优先读取：

- `../../shared/coinfound_rwa/data/endpoint_catalog.json`
- `../../shared/coinfound_rwa/data/schema_snapshots/`

再使用：

- `../../shared/coinfound_rwa/scripts/fetch_rwa.py`

## 最小调用示例

```bash
python ../../shared/coinfound_rwa/scripts/fetch_rwa.py \
  --endpoint-key stable-coin.market-cap.timeseries \
  --query '{"groupBy":"network"}'
```

```bash
python ../../shared/coinfound_rwa/scripts/fetch_rwa.py \
  --asset-class private-credit \
  --family aggregates
```

## 结果约定

默认输出应包含：

- `request`
- `response_envelope`
- `normalized_data`
- `display_data`
- `shape_family`
- `schema_source`

## 参考文档

- `references/rwa-read-workflow.md`
- `references/rwa-read-capabilities.md`
- `references/rwa-read-integration-notes.md`
