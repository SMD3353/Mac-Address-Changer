"""Command line interface for threat aggregator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from .aggregator import aggregate_urls


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate threat feeds from open source URLs"
    )
    parser.add_argument("output", help="Output file path for aggregated feed")
    parser.add_argument(
        "urls",
        nargs="+",
        help="One or more threat feed URLs returning JSON lists",
    )
    args = parser.parse_args(argv)

    aggregated = aggregate_urls(args.urls)

    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(aggregated, fh, indent=2)
    print(f"Wrote {len(aggregated)} entries to {output_path}")


if __name__ == "__main__":
    main()
