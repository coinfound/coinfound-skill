from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from shared.coinfound_rwa.catalog import DEFAULT_CATALOG_PATH, build_catalog, load_catalog, write_catalog
from shared.coinfound_rwa.fetch import resolve_entry


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load_catalog(DEFAULT_CATALOG_PATH)
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.catalog_path = Path(cls.tempdir.name) / "endpoint_catalog.json"
        write_catalog(cls.catalog, cls.catalog_path)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tempdir.cleanup()

    def test_catalog_contains_core_keys(self) -> None:
        keys = {entry["key"] for entry in self.catalog}
        self.assertIn("private-credit.aggregates", keys)
        self.assertIn("stable-coin.market-cap.timeseries", keys)
        self.assertIn("commodity.market-cap.pie", keys)
        self.assertIn("market-overview.asset-classes.list", keys)
        self.assertIn("platforms.detail.asset.dataset", keys)
        self.assertIn("x-stock.dataset", keys)

    def test_doc_status_for_known_gaps(self) -> None:
        status = {entry["key"]: entry["doc_status"] for entry in self.catalog}
        self.assertEqual(status["private-credit.aggregates"], "partial")
        self.assertEqual(status["commodity.aggregates"], "probe_required")
        self.assertEqual(status["stable-coin.dataset"], "probe_required")
        self.assertEqual(status["stable-coin.weekly-report"], "unsupported_by_design")
        self.assertEqual(status["stable-coin.weekly-report.create"], "unsupported_by_design")
        self.assertEqual(status["stable-coin.recently-report.list"], "unsupported_by_design")

    def test_build_catalog_from_sample_markdown(self) -> None:
        sample = """
# 默认模块

# v1/rwa/rwa-私人信贷

## GET 私人信贷数据概览

GET /v1/c/rwa/private-credit/aggregates

> 返回示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "activeLoansValue": 1.0
  }
}
```

### 返回数据结构

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» message|string|true|none||none|
|» data|object|true|none||none|

# v1/rwa/rwa-稳定币

## GET 稳定币数据集

GET /v1/c/rwa/stable-coin/dataset/{ticker}

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ticker|path|string| 是 |none|

> 返回示例

```json
{}
```
"""
        catalog = build_catalog(sample)
        by_key = {entry["key"]: entry for entry in catalog}
        self.assertEqual(by_key["private-credit.aggregates"]["doc_status"], "partial")
        self.assertEqual(by_key["stable-coin.dataset"]["doc_status"], "probe_required")
        self.assertEqual(by_key["stable-coin.dataset"]["path_params"], ["ticker"])

    def test_resolve_entry_from_dimensions(self) -> None:
        entry = resolve_entry(
            asset_class="private-credit",
            family="aggregates",
            catalog_path=self.catalog_path,
        )
        self.assertEqual(entry["key"], "private-credit.aggregates")

    def test_resolve_platform_detail_asset_dataset(self) -> None:
        entry = resolve_entry(
            asset_class="platforms",
            family="dataset",
            metric="asset",
            path_params={"platform": "tether-holdings"},
            catalog_path=self.catalog_path,
        )
        self.assertEqual(entry["key"], "platforms.detail.asset.dataset")


if __name__ == "__main__":
    unittest.main()
