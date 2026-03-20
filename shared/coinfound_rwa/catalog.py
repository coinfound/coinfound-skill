from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parent
SHARED_ROOT = PACKAGE_ROOT.parent
REPO_ROOT = SHARED_ROOT.parent
DEFAULT_DOC_PATH = REPO_ROOT / "默认模块.md"
DATA_DIR = PACKAGE_ROOT / "data"
DEFAULT_CATALOG_PATH = DATA_DIR / "endpoint_catalog.json"
SNAPSHOT_DIR = DATA_DIR / "schema_snapshots"
BASE_URL = "https://api.coinfound.org/api/kakyoin"

KNOWN_PARTIAL_ENDPOINTS: dict[str, str] = {
    "private-credit.aggregates": "Field table omits currentAvgAPR and totalLoans.",
    "stable-coin.weekly-report": "Report endpoint is intentionally excluded from read skill coverage.",
}

KNOWN_PROBE_REQUIRED_ENDPOINTS: dict[str, str] = {
    "stable-coin.aggregates": "Document example is empty, but live response contains data.",
    "stable-coin.market-cap.timeseries": "Document example is empty, but live response contains data.",
    "stable-coin.dataset": "Document example is empty, but live response contains nested dataset fields.",
    "commodity.aggregates": "Document example is empty, but live response contains data.",
    "commodity.market-cap.pie": "Document example is empty, but live response contains data.",
    "market-overview.asset-classes.list": "Document example is empty, but live response contains data.",
    "market-overview.main-asset-classes.summary": "Document example is empty, but live response contains data.",
    "platforms.aggregates": "Document example is empty, but live response contains data.",
    "platforms.dataset": "Document example is empty, but live response contains nested dataset fields.",
    "platforms.detail.asset.dataset": "Document example is empty, but live response contains nested dataset fields.",
    "x-stock.aggregates": "Document example is empty, but live response contains data.",
    "x-stock.total-value.pie": "Document example is empty, but live response contains data.",
    "x-stock.dataset": "Dataset route may return code=0 without data for some candidate tickers.",
}


def load_catalog(path: Path | None = None) -> list[dict[str, Any]]:
    catalog_path = path or DEFAULT_CATALOG_PATH
    with catalog_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_catalog(entries: list[dict[str, Any]], path: Path | None = None) -> Path:
    catalog_path = path or DEFAULT_CATALOG_PATH
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    with catalog_path.open("w", encoding="utf-8") as handle:
        json.dump(entries, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return catalog_path


def build_catalog_from_file(doc_path: Path | None = None) -> list[dict[str, Any]]:
    source_path = doc_path or DEFAULT_DOC_PATH
    content = source_path.read_text(encoding="utf-8")
    return build_catalog(content)


def build_catalog(markdown: str) -> list[dict[str, Any]]:
    lines = markdown.splitlines()
    entries: list[dict[str, Any]] = []
    current_section: str | None = None
    current_endpoint_title: str | None = None
    current_endpoint_lines: list[str] = []

    def flush_endpoint() -> None:
        nonlocal current_endpoint_title, current_endpoint_lines
        if not current_endpoint_title:
            return
        block = "\n".join(current_endpoint_lines)
        entry = build_entry(current_section, current_endpoint_title, block)
        if entry:
            entries.append(entry)
        current_endpoint_title = None
        current_endpoint_lines = []

    for line in lines:
        if line.startswith("# "):
            flush_endpoint()
            current_section = line[2:].strip() if line.startswith("# v1/rwa/") else None
            continue
        if line.startswith("## GET ") or line.startswith("## POST "):
            flush_endpoint()
            current_endpoint_title = line[3:].strip()
            current_endpoint_lines = [line]
            continue
        if current_endpoint_title is not None:
            current_endpoint_lines.append(line)

    flush_endpoint()
    return entries


def build_entry(section: str | None, title: str, block: str) -> dict[str, Any] | None:
    route_match = re.search(r"^(GET|POST)\s+(/v1/c/rwa/[^\s]+)\s*$", block, re.MULTILINE)
    if not route_match:
        return None

    method, path_template = route_match.groups()
    path_parts = path_template.strip("/").split("/")
    if len(path_parts) < 4 or path_parts[:3] != ["v1", "c", "rwa"]:
        return None

    asset_class = path_parts[3]
    key = build_endpoint_key(path_template)
    family, metric = classify_family_and_metric(path_template)
    path_params = extract_path_params(path_template)
    query_params = extract_request_parameters(block)
    field_count = len(re.findall(r"^\|»", block, re.MULTILINE))
    json_examples = extract_json_examples(block)
    empty_example = any(example.strip() == "{}" for example in json_examples)
    non_empty_example = any(example.strip() and example.strip() != "{}" for example in json_examples)
    doc_status = classify_doc_status(
        key=key,
        family=family,
        empty_example=empty_example,
        non_empty_example=non_empty_example,
        field_count=field_count,
    )
    notes = build_notes(key, family, empty_example, field_count)

    return {
        "asset_class": asset_class,
        "doc_status": doc_status,
        "family": family,
        "field_count": field_count,
        "key": key,
        "method": method,
        "metric": metric,
        "notes": notes,
        "path_params": path_params,
        "path_template": path_template,
        "query_params": query_params,
        "section": section,
        "shape_family": default_shape_family(path_template, family),
        "title": title,
        "unsupported_by_design": family.startswith("report"),
    }


def classify_doc_status(
    *,
    key: str,
    family: str,
    empty_example: bool,
    non_empty_example: bool,
    field_count: int,
) -> str:
    if family.startswith("report"):
        return "unsupported_by_design"
    if key in KNOWN_PROBE_REQUIRED_ENDPOINTS:
        return "probe_required"
    if key in KNOWN_PARTIAL_ENDPOINTS:
        return "partial"
    if empty_example and field_count == 0:
        return "probe_required"
    if empty_example and field_count > 0:
        return "partial"
    if non_empty_example and field_count == 0:
        return "partial"
    if field_count > 0:
        return "documented"
    return "partial"


def build_notes(key: str, family: str, empty_example: bool, field_count: int) -> list[str]:
    notes: list[str] = []
    if key in KNOWN_PARTIAL_ENDPOINTS:
        notes.append(KNOWN_PARTIAL_ENDPOINTS[key])
    if key in KNOWN_PROBE_REQUIRED_ENDPOINTS:
        notes.append(KNOWN_PROBE_REQUIRED_ENDPOINTS[key])
    if family.startswith("report"):
        notes.append("Excluded from the read skill by product decision.")
    if empty_example and field_count == 0:
        notes.append("Documentation contains an empty JSON example and no field table.")
    return notes


def build_endpoint_key(path_template: str) -> str:
    parts = path_template.strip("/").split("/")[3:]
    key_parts: list[str] = []
    for index, part in enumerate(parts):
        if index == 0:
            key_parts.append(part)
            continue
        if part.startswith("{") and part.endswith("}"):
            if index != len(parts) - 1 and key_parts[-1] != "detail":
                key_parts.append("detail")
            continue
        key_parts.append(part)
    return ".".join(key_parts)


def classify_family_and_metric(path_template: str) -> tuple[str, str | None]:
    parts = path_template.strip("/").split("/")[3:]
    if path_template.endswith("/weekly-report/create"):
        return "report-create", "weekly-report"
    if path_template.endswith("/recently-report/list"):
        return "report-list", "recently-report"
    if path_template.endswith("/weekly-report"):
        return "report", "weekly-report"
    if path_template.endswith("/timeseries"):
        return "timeseries", previous_literal(parts, "timeseries")
    if path_template.endswith("/pie"):
        return "pie", previous_literal(parts, "pie")
    if path_template.endswith("/list"):
        return "list", previous_literal(parts, "list")
    if "/dataset/" in path_template or path_template.endswith("/dataset"):
        dataset_metric = previous_literal(parts, "dataset")
        return "dataset", None if dataset_metric == parts[0] else dataset_metric
    if path_template.endswith("/aggregates"):
        return "aggregates", None
    if path_template.endswith("/summary"):
        return "summary", previous_literal(parts, "summary")
    return "unknown", None


def default_shape_family(path_template: str, family: str) -> str:
    if family == "timeseries":
        return "timeseries_aggregate"
    if family == "pie":
        return "pie_name_value"
    if family in {"aggregates", "summary"}:
        return "envelope_object"
    if family == "list":
        return "envelope_list"
    if family == "dataset":
        if path_template.endswith("/platforms/{platform}/asset/dataset"):
            return "dataset_nested_networks"
        if "/stable-coin/dataset/" in path_template:
            return "dataset_nested_networks"
        return "dataset_wrapped_list"
    if family.startswith("report"):
        return "unsupported"
    return "unknown"


def extract_path_params(path_template: str) -> list[str]:
    return re.findall(r"\{([^}]+)\}", path_template)


def extract_request_parameters(block: str) -> list[dict[str, Any]]:
    params: list[dict[str, Any]] = []
    lines = block.splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip() != "### 请求参数":
            index += 1
            continue
        index += 1
        table_lines: list[str] = []
        while index < len(lines):
            stripped = lines[index].strip()
            if not stripped:
                index += 1
                continue
            if not stripped.startswith("|"):
                break
            table_lines.append(stripped)
            index += 1
        if len(table_lines) < 3:
            continue
        for row in table_lines[2:]:
            columns = split_markdown_row(row)
            if len(columns) < 5:
                continue
            params.append(
                {
                    "description": columns[4],
                    "in": columns[1],
                    "name": columns[0],
                    "required": "是" in columns[3] or columns[3].strip().lower() == "true",
                    "type": columns[2],
                }
            )
        break
    return params


def split_markdown_row(row: str) -> list[str]:
    return [column.strip() for column in row.strip().strip("|").split("|")]


def extract_json_examples(block: str) -> list[str]:
    return re.findall(r"```json\s*(.*?)\s*```", block, re.DOTALL)


def previous_literal(parts: list[str], target: str) -> str | None:
    try:
        index = parts.index(target)
    except ValueError:
        return None
    for part in reversed(parts[:index]):
        if part.startswith("{") and part.endswith("}"):
            continue
        return part
    return None
