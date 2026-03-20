from __future__ import annotations

import unittest

from shared.coinfound_rwa.formatter import format_display_data, format_number
from shared.coinfound_rwa.fetch import fill_path_template, normalize_data
from shared.coinfound_rwa.schema import infer_schema, infer_shape_family


class FetchAndSchemaTests(unittest.TestCase):
    def test_fill_path_template(self) -> None:
        resolved = fill_path_template(
            "/v1/c/rwa/platforms/{platform}/asset/dataset",
            {"platform": "tether-holdings"},
        )
        self.assertEqual(resolved, "/v1/c/rwa/platforms/tether-holdings/asset/dataset")

    def test_infer_timeseries_shape(self) -> None:
        response = {
            "code": 0,
            "message": "success",
            "data": [{"time": 1, "aggregates": [{"name": "Ethereum", "value": 1.0}]}],
        }
        self.assertEqual(infer_shape_family(response, None), "timeseries_aggregate")
        normalized = normalize_data(response, "timeseries_aggregate")
        self.assertEqual(normalized[0]["time"], 1)

    def test_infer_pie_shape(self) -> None:
        response = {
            "code": 0,
            "message": "success",
            "data": [{"name": "Ethereum", "value": 10}],
        }
        self.assertEqual(infer_shape_family(response, None), "pie_name_value")

    def test_infer_dataset_nested_networks_shape(self) -> None:
        response = {
            "code": 0,
            "message": "success",
            "data": {
                "list": [
                    {
                        "name": "Tether USDt",
                        "ticker": "USDT",
                        "networks": [{"networkName": "Ethereum", "contractAddress": "0x1"}],
                    }
                ]
            },
        }
        self.assertEqual(infer_shape_family(response, "dataset_wrapped_list"), "dataset_nested_networks")
        schema = infer_schema(response["data"])
        self.assertEqual(schema["type"], "object")
        self.assertIn("list", schema["properties"])

    def test_infer_empty_success_shape(self) -> None:
        response = {"code": 0, "message": "success"}
        self.assertEqual(infer_shape_family(response, None), "empty_success")
        self.assertIsNone(normalize_data(response, "empty_success"))

    def test_format_number_compact(self) -> None:
        self.assertEqual(format_number(323_841_339_847.1784), "323.84B")
        self.assertEqual(format_number(278_208_962), "278.21M")
        self.assertEqual(format_number(2_990), "2.99K")
        self.assertEqual(format_number(0.0231), "0.0231")

    def test_format_display_data_preserves_time_semantics(self) -> None:
        payload = {
            "time": 1773763200000,
            "latest_time": 1773763200000,
            "marketCapSum": 323_841_339_847.1784,
            "holdersSum": 278_208_962,
            "ratio": 0.0231,
        }
        display = format_display_data(payload)
        self.assertEqual(display["time"], "2026-03-17T16:00:00+00:00")
        self.assertEqual(display["latest_time"], "2026-03-17T16:00:00+00:00")
        self.assertEqual(display["marketCapSum"], "323.84B")
        self.assertEqual(display["holdersSum"], "278.21M")
        self.assertEqual(display["ratio"], "0.0231")


if __name__ == "__main__":
    unittest.main()
