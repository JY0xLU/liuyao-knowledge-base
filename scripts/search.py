#!/usr/bin/env python3
"""Simple local search for the Liuyao knowledge base."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {".md", ".txt", ".json"}
DEFAULT_EXCLUDED_PARTS = {
    ".git",
    ".netlify",
    ".pnpm-runtime",
    ".pytest_cache",
    ".tools",
    "__pycache__",
    "node_modules",
}
DEFAULT_EXCLUDED_PREFIXES = (".deploy-netlify-clean-",)
DEFAULT_EXCLUDED_FILES = {".last-deploy-dir.txt"}
DEFAULT_EXCLUDED_PATHS = {
    ("web", "assets"),
    ("netlify", "functions", "_shared"),
}


def normalize(text: str) -> str:
    return text.lower()


def iter_files(root: Path):
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        relative_parts = current_path.relative_to(root).parts
        dirs[:] = [
            item
            for item in dirs
            if item not in DEFAULT_EXCLUDED_PARTS and not item.startswith(DEFAULT_EXCLUDED_PREFIXES)
        ]
        if any(part in DEFAULT_EXCLUDED_PARTS for part in relative_parts):
            continue
        if any(part.startswith(DEFAULT_EXCLUDED_PREFIXES) for part in relative_parts):
            continue
        if any(relative_parts[: len(excluded)] == excluded for excluded in DEFAULT_EXCLUDED_PATHS):
            dirs[:] = []
            continue
        for name in files:
            path = current_path / name
            if name in DEFAULT_EXCLUDED_FILES or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            yield path


def snippets(text: str, terms: list[str], width: int = 72) -> list[str]:
    compact = re.sub(r"\s+", " ", text)
    lowered = normalize(compact)
    found: list[str] = []

    for term in terms:
        needle = normalize(term)
        if not needle:
            continue
        pos = lowered.find(needle)
        if pos == -1:
            continue
        start = max(0, pos - width)
        end = min(len(compact), pos + len(term) + width)
        snippet = compact[start:end].strip()
        for raw in sorted(terms, key=len, reverse=True):
            if raw:
                snippet = re.sub(re.escape(raw), f"[{raw}]", snippet, flags=re.IGNORECASE)
        found.append(snippet)
    return found[:3]


def score_text(text: str, terms: list[str]) -> int:
    lowered = normalize(text)
    score = 0
    for term in terms:
        needle = normalize(term)
        if not needle:
            continue
        count = lowered.count(needle)
        score += count * (10 + min(len(term), 8))
    return score


def search(root: Path, query: str) -> list[dict]:
    terms = [part.strip() for part in re.split(r"\s+", query) if part.strip()]
    if not terms:
        return []

    results = []
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")
        score = score_text(text, terms)
        if score <= 0:
            continue
        results.append(
            {
                "path": str(path.relative_to(root)),
                "score": score,
                "snippets": snippets(text, terms),
            }
        )

    return sorted(results, key=lambda item: (-item["score"], item["path"]))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Search local Liuyao knowledge base")
    parser.add_argument("query", help="Search query, e.g. 用神 or '月建 日辰'")
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    root = args.root.resolve()
    results = search(root, args.query)[: args.limit]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    if not results:
        print(f"No results for: {args.query}")
        return 1

    for index, item in enumerate(results, 1):
        print(f"{index}. {item['path']}  score={item['score']}")
        for snippet in item["snippets"]:
            print(f"   - {snippet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
