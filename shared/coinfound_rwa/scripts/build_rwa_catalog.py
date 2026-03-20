#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.coinfound_rwa.catalog import DEFAULT_CATALOG_PATH, DEFAULT_DOC_PATH, build_catalog_from_file, write_catalog


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the CoinFound RWA endpoint catalog from 默认模块.md.")
    parser.add_argument("--source", type=Path, default=DEFAULT_DOC_PATH, help="Path to 默认模块.md")
    parser.add_argument("--output", type=Path, default=DEFAULT_CATALOG_PATH, help="Where to write endpoint_catalog.json")
    args = parser.parse_args()

    try:
        entries = build_catalog_from_file(args.source)
        output_path = write_catalog(entries, args.output)
        summary = {
            "entries_written": len(entries),
            "output": str(output_path),
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:  # pragma: no cover - CLI guard
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
