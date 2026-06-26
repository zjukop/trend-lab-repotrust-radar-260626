"""RepoTrust Radar CLI."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from typing import Iterable

SUSPICIOUS_PATTERNS = {
    "crypto_lure": ["flash", "usdt", "wallet", "seed", "balance", "exodus"],
    "credential_risk": ["bruteforce", "recovery", "generator", "private-key"],
    "game_executor": ["executor", "execut", "roblox", "cheat"],
}


@dataclass(frozen=True)
class TrustCard:
    repo: str
    score: int
    grade: str
    signals: list[str]


def normalize_repo(value: str) -> str:
    """Return owner/repo from a GitHub URL or owner/repo string."""
    cleaned = value.strip().removesuffix(".git")
    match = re.search(r"github\.com[:/](?P<repo>[^/\s]+/[^/\s#?]+)", cleaned)
    repo = match.group("repo") if match else cleaned
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise ValueError("expected a GitHub URL or owner/repo")
    return repo


def find_signals(repo: str, patterns: dict[str, Iterable[str]] = SUSPICIOUS_PATTERNS) -> list[str]:
    haystack = repo.lower().replace("-", " ").replace("_", " ")
    signals: list[str] = []
    for category, words in patterns.items():
        hits = sorted({word for word in words if word in haystack})
        if hits:
            signals.append(f"{category}: {', '.join(hits)}")
    return signals


def grade_for(score: int) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 50:
        return "C"
    return "D"


def analyze(value: str) -> TrustCard:
    repo = normalize_repo(value)
    signals = find_signals(repo)
    score = max(0, 100 - 20 * len(signals))
    return TrustCard(repo=repo, score=score, grade=grade_for(score), signals=signals)


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a RepoTrust trust card.")
    parser.add_argument("repo", help="GitHub URL or owner/repo")
    args = parser.parse_args(argv)

    try:
        card = analyze(args.repo)
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(asdict(card), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
