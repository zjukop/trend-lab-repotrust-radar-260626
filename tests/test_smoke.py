import json
import subprocess
import sys

from repotrust_radar.main import analyze, normalize_repo


def test_normalize_repo_url():
    assert normalize_repo("https://github.com/owner/repo.git") == "owner/repo"


def test_analyze_flags_suspicious_name():
    card = analyze("deniszhukov965/Flash-USDT-Sender")
    assert card.grade in {"C", "D"}
    assert card.signals


def test_cli_outputs_json():
    result = subprocess.run(
        [sys.executable, "-m", "repotrust_radar.main", "owner/repo"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["repo"] == "owner/repo"
    assert payload["grade"] == "A"
