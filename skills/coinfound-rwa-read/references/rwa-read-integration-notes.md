# RWA Read Integration Notes

## 输入建议

推荐优先使用 `endpoint_key`，其次再使用 `asset_class + family + metric` 组合。

```json
{
  "endpoint_key": "stable-coin.aggregates",
  "query": {},
  "raw": false
}
```

## 输出建议

```json
{
  "request": {"method": "GET", "path": "/v1/c/rwa/stable-coin/aggregates"},
  "response_envelope": {"code": 0, "message": "success", "data": {}},
  "normalized_data": {},
  "display_data": {},
  "shape_family": "envelope_object",
  "schema_source": "snapshot"
}
```

## 兼容性注意事项

- 存在 `code=0` 且缺失 `data` 的成功响应，需要保留 `empty_success` 语义。
- `dataset` 可能存在深层嵌套数组，不要默认拍平。
- `display_data` 是展示层格式化输出，`normalized_data` 仍然保留原始数值。
- 大数默认格式化为 `T/B/M/K`，时间戳字段会转为 ISO UTC 字符串。
- 若快照与实时返回冲突，优先保留实时响应并提交 probe 刷新任务。

## 共享资源提醒

集成时先读：

- `../../shared/coinfound_rwa/data/endpoint_catalog.json`
- `../../shared/coinfound_rwa/data/schema_snapshots/`
