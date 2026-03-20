# RWA Snapshot Policy

## 目标

让 `schema_snapshots` 作为 read skill 的第一数据源，减少每次实时探测开销。

## 写入规则

- 仅在以下情况写入或更新 snapshot：
  - endpoint 首次探测成功
  - 现有 snapshot 缺失关键字段
  - 实时响应与现有 snapshot 明显冲突
- 写入时保留：
  - `endpoint_key`
  - `shape_family`
  - `inferred_schema`
  - `sample_response`
  - `updated_at`

## 质量门槛

- 至少通过两次独立请求得到一致 shape 才标记为稳定。
- `empty_success` 需要单独记录，不可与 `data: null` 混淆。
- 深层数组结构（如 `dataset` 下 `networks`）必须完整保留。

## 与 read skill 的衔接

`$coinfound-rwa-read` 应优先消费快照，不应默认触发 probe。只有在缺失或冲突时才转交 probe。

## 共享数据提醒

优先查看以下目录：

- `../../shared/coinfound_rwa/data/endpoint_catalog.json`
- `../../shared/coinfound_rwa/data/schema_snapshots/`
