# RepoTrust Radar

A tiny Python starter for scoring GitHub repository URLs with safe, metadata/text-only heuristics.

## Install

```bash
pip install -e .
```

## Usage

```bash
repotrust https://github.com/owner/repo
# or
python -m repotrust_radar.main owner/repo
```

Outputs a JSON trust card with a letter grade and risk signals.

## Development

```bash
pip install -e .[dev]
pytest
```

This starter does not call the GitHub API yet; it analyzes the provided URL/name only and is safe by design.
