"""Core aggregation logic for threat feeds.

This module fetches threat intelligence from remote feeds provided by
open source threat intelligence platforms and merges them into a single
deduplicated list. Each feed URL is expected to return JSON data in the
same format: a list of objects with at least an ``id`` field.
"""

from __future__ import annotations

import json
from typing import Iterable, Dict, List

from urllib.request import urlopen


def load_feed_from_url(url: str) -> List[Dict[str, object]]:
    """Fetch a threat feed from ``url`` and return its entries."""
    with urlopen(url, timeout=30) as resp:
        data = resp.read()
    return json.loads(data)


def aggregate_urls(urls: Iterable[str]) -> List[Dict[str, object]]:
    """Aggregate multiple threat feeds provided as URLs.

    Entries are deduplicated by their ``id`` field.
    """
    aggregated: Dict[str, Dict[str, object]] = {}
    for url in urls:
        for entry in load_feed_from_url(url):
            entry_id = str(entry.get("id"))
            aggregated[entry_id] = entry
    return list(aggregated.values())
