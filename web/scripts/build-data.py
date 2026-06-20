#!/usr/bin/env python3
"""Build browser-readable knowledge-base data from Markdown and JSON files."""

from __future__ import annotations

import json
import re
import sys
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
DATA = ROOT / "data"
OUT = ROOT / "web" / "assets" / "kb-data.json"
OUT_JS = ROOT / "web" / "assets" / "kb-data.js"
FUNCTION_DATA = ROOT / "netlify" / "functions" / "_shared" / "kb-data.mjs"


DOC_ORDER = [
    "00-learning-map.md",
    "01-foundations.md",
    "02-casting-and-installing.md",
    "03-judgment-framework.md",
    "04-topic-playbooks.md",
    "05-case-template.md",
    "06-classics-reading-index.md",
    "07-rule-cards.md",
    "08-research-and-deployment-log.md",
    "09-bushi-zhengzong-notes.md",
    "10-zengshan-case-index.md",
    "11-external-project-benchmark.md",
    "12-najia-engine-notes.md",
    "13-accuracy-evaluation.md",
    "14-github-versioning.md",
    "15-multi-system-roadmap.md",
    "16-ziwei-foundation.md",
    "17-qimen-foundation.md",
    "18-liuren-foundation.md",
    "sources.md",
    "website-plan.md",
]


def load_json(name: str):
    with (DATA / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def doc_title(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def doc_summary(text: str) -> str:
    cleaned = re.sub(r"```[\s\S]*?```", "", text)
    cleaned = re.sub(r"^#+\s+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:180]


def load_docs():
    docs = []
    for name in DOC_ORDER:
        path = DOCS / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        slug = path.stem
        docs.append(
            {
                "id": slug,
                "title": doc_title(text, path.stem),
                "path": f"docs/{name}",
                "summary": doc_summary(text),
                "markdown": text,
            }
        )
    return docs


def content_hash(payload: dict) -> str:
    stable = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    payload = {
        "docs": load_docs(),
        "terms": load_json("terms.json"),
        "ziwei_terms": load_json("ziwei_terms.json"),
        "ziwei_structures": load_json("ziwei_structures.json"),
        "qimen_terms": load_json("qimen_terms.json"),
        "qimen_structures": load_json("qimen_structures.json"),
        "liuren_terms": load_json("liuren_terms.json"),
        "liuren_structures": load_json("liuren_structures.json"),
        "sources": load_json("sources.json"),
        "systems": load_json("systems.json"),
        "rules": load_json("rules.json"),
        "classics": load_json("classics_index.json"),
        "classic_notes": load_json("classic_notes.json"),
        "case_index": load_json("case_index.json"),
        "accuracy_cases": load_json("accuracy_cases.json"),
        "external_projects": load_json("external_projects.json"),
        "case_schema": load_json("case_schema.json"),
    }
    payload["built_at"] = f"content-{content_hash(payload)}"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    FUNCTION_DATA.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, ensure_ascii=False, indent=2)
    OUT.write_text(data, encoding="utf-8")
    OUT_JS.write_text(f"window.LIUYAO_KB_DATA = {data};\n", encoding="utf-8")
    FUNCTION_DATA.write_text(f"export default {data};\n", encoding="utf-8")
    print(
        "Built web data: "
        f"{len(payload['docs'])} docs, {len(payload['terms'])} terms, "
        f"{len(payload['ziwei_terms'])} ziwei terms, "
        f"{len(payload['qimen_terms'])} qimen terms, "
        f"{len(payload['liuren_terms'])} liuren terms, "
        f"{len(payload['systems'])} systems, "
        f"{len(payload['rules'])} rules, {len(payload['classic_notes'])} notes, "
        f"{len(payload['case_index'])} case slots, "
        f"{len(payload['accuracy_cases'])} accuracy cases, "
        f"{len(payload['external_projects'])} external projects "
        f"-> {OUT}, {OUT_JS}, and {FUNCTION_DATA}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
