# Threat Aggregator

A simple Python application to aggregate threat intelligence from open source platforms. The tool fetches JSON feeds from one or more URLs, merges the entries by unique `id`, and writes the combined feed to an output file.

## Usage

```
python -m threat_aggregator <output_file> <feed_url1> [feed_url2 ...]
```

## Running Tests

```
python -m unittest discover -s tests
```
