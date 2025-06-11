import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import json
import unittest
from unittest.mock import patch

from threat_aggregator.aggregator import aggregate_urls


class MockResponse:
    def __init__(self, data: str):
        self._data = data.encode("utf-8")

    def read(self) -> bytes:
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class TestAggregator(unittest.TestCase):
    @patch("threat_aggregator.aggregator.urlopen")
    def test_aggregate_urls(self, mock_urlopen):
        mock_urlopen.side_effect = [
            MockResponse(json.dumps([
                {"id": "1", "threat": "A"},
                {"id": "2", "threat": "B"},
            ])),
            MockResponse(json.dumps([
                {"id": "2", "threat": "B"},
                {"id": "3", "threat": "C"},
            ])),
        ]

        results = aggregate_urls(["http://feed1", "http://feed2"])
        ids = {r["id"] for r in results}
        self.assertEqual(ids, {"1", "2", "3"})
        self.assertEqual(len(results), 3)


if __name__ == "__main__":
    unittest.main()
