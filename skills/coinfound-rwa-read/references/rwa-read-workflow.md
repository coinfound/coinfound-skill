# RWA Read Workflow

本文件定义 read skill 的标准执行顺序，避免绕过共享 catalog 与快照。

## 前置检查

优先读取以下共享数据：

- `../../shared/coinfound_rwa/data/endpoint_catalog.json`
- `../../shared/coinfound_rwa/data/schema_snapshots/`

若两者都无法提供目标 endpoint 的稳定结构，再考虑转交 `$coinfound-rwa-schema-probe`。

## 标准步骤

1. 根据用户意图确定 `asset_class`、`family`、`metric`。
2. 在 `endpoint_catalog.json` 中找到唯一 `endpoint_key`。
3. 通过 `fetch_rwa.py` 执行请求。
4. 返回 envelope 与归一化结果，附带 `schema_source`。

## 命令示例

```bash
python ../../shared/coinfound_rwa/scripts/fetch_rwa.py \
  --endpoint-key commodity.market-cap.pie
```

```bash
python ../../shared/coinfound_rwa/scripts/fetch_rwa.py \
  --asset-class market-overview \
  --family list \
  --metric asset-classes
```
