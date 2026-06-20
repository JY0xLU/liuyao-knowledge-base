#!/usr/bin/env python3
"""Query structured Liuyao knowledge-base data."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name: str):
    with (DATA / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def contains(value, needle: str) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return needle.lower() in value.lower()
    if isinstance(value, list):
        return any(contains(item, needle) for item in value)
    if isinstance(value, dict):
        return any(contains(item, needle) for item in value.values())
    return needle.lower() in str(value).lower()


def print_json(items) -> None:
    print(json.dumps(items, ensure_ascii=False, indent=2))


def query_terms(keyword: str, as_json: bool) -> int:
    terms = load("terms.json")
    matches = [item for item in terms if contains(item, keyword)]
    if as_json:
        print_json(matches)
        return 0 if matches else 1
    for item in matches:
        aliases = ", ".join(item.get("aliases", []))
        print(f"- {item['term']} ({item.get('category', '-')})")
        if aliases:
            print(f"  aliases: {aliases}")
        print(f"  {item.get('definition', '')}")
        refs = ", ".join(item.get("source_refs", []))
        if refs:
            print(f"  sources: {refs}")
    return 0 if matches else 1


def query_ziwei_terms(keyword: str, as_json: bool) -> int:
    terms = load("ziwei_terms.json")
    matches = [item for item in terms if contains(item, keyword)]
    if as_json:
        print_json(matches)
        return 0 if matches else 1
    for item in matches:
        aliases = ", ".join(item.get("aliases", []))
        print(f"- {item['term']} ({item.get('category', '-')}/{item.get('group', '-')})")
        if aliases:
            print(f"  aliases: {aliases}")
        print(f"  {item.get('definition', '')}")
        refs = ", ".join(item.get("source_refs", []))
        if refs:
            print(f"  sources: {refs}")
        if item.get("boundary_notes"):
            print(f"  boundary: {item['boundary_notes']}")
    return 0 if matches else 1


def query_qimen_terms(keyword: str, as_json: bool) -> int:
    terms = load("qimen_terms.json")
    matches = [item for item in terms if contains(item, keyword)]
    if as_json:
        print_json(matches)
        return 0 if matches else 1
    for item in matches:
        aliases = ", ".join(item.get("aliases", []))
        print(f"- {item['term']} ({item.get('category', '-')}/{item.get('group', '-')})")
        if aliases:
            print(f"  aliases: {aliases}")
        print(f"  {item.get('definition', '')}")
        refs = ", ".join(item.get("source_refs", []))
        if refs:
            print(f"  sources: {refs}")
        if item.get("boundary_notes"):
            print(f"  boundary: {item['boundary_notes']}")
    return 0 if matches else 1


def query_liuren_terms(keyword: str, as_json: bool) -> int:
    terms = load("liuren_terms.json")
    matches = [item for item in terms if contains(item, keyword)]
    if as_json:
        print_json(matches)
        return 0 if matches else 1
    for item in matches:
        aliases = ", ".join(item.get("aliases", []))
        print(f"- {item['term']} ({item.get('category', '-')}/{item.get('group', '-')})")
        if aliases:
            print(f"  aliases: {aliases}")
        print(f"  {item.get('definition', '')}")
        refs = ", ".join(item.get("source_refs", []))
        if refs:
            print(f"  sources: {refs}")
        if item.get("boundary_notes"):
            print(f"  boundary: {item['boundary_notes']}")
    return 0 if matches else 1


def query_rules(keyword: str, layer: str | None, as_json: bool) -> int:
    rules = load("rules.json")
    matches = []
    for item in rules:
        if layer and item.get("layer") != layer:
            continue
        if contains(item, keyword):
            matches.append(item)
    if as_json:
        print_json(matches)
        return 0 if matches else 1
    for item in matches:
        print(f"- {item['id']} [{item.get('layer', '-')}] {item.get('title', '')}")
        print(f"  {item.get('statement', '')}")
        refs = ", ".join(item.get("source_refs", []))
        print(f"  confidence: {item.get('confidence', '-')}  sources: {refs}")
    return 0 if matches else 1


def query_sources(keyword: str, class_filter: str | None, as_json: bool) -> int:
    sources = load("sources.json")
    matches = []
    for item in sources:
        if class_filter and item.get("class") != class_filter:
            continue
        if contains(item, keyword):
            matches.append(item)
    if as_json:
        print_json(matches)
        return 0 if matches else 1
    for item in matches:
        print(f"- {item['id']} [{item.get('class', '-')}/{item.get('type', '-')}] {item.get('title', '')}")
        print(f"  {item.get('url', '')}")
        print(f"  {item.get('notes', '')}")
    return 0 if matches else 1


def query_classics(keyword: str, as_json: bool) -> int:
    classics = load("classics_index.json")
    matches = [item for item in classics if contains(item, keyword)]
    if as_json:
        print_json(matches)
        return 0 if matches else 1
    for item in matches:
        print(f"- {item['title']} ({item.get('role', '-')}, priority {item.get('priority', '-')})")
        print(f"  read first: {', '.join(item.get('read_first', []))}")
        print(f"  tasks: {'; '.join(item.get('knowledge_tasks', []))}")
    return 0 if matches else 1


def query_notes(keyword: str, group: str | None, as_json: bool) -> int:
    notes = load("classic_notes.json")
    matches = []
    for item in notes:
        if group and item.get("section_group") != group:
            continue
        if contains(item, keyword):
            matches.append(item)
    if as_json:
        print_json(matches)
        return 0 if matches else 1
    for item in matches:
        print(
            f"- {item['id']} [{item.get('section_group', '-')}] "
            f"{item.get('order', '-')}. {item.get('topic', '')}"
        )
        print(f"  problem: {item.get('problem', '')}")
        print(f"  focus: {'; '.join(item.get('rule_focus', []))}")
        print(f"  fields: {', '.join(item.get('extraction_fields', []))}")
        rules = ", ".join(item.get("linked_rule_ids", []))
        if rules:
            print(f"  linked rules: {rules}")
    return 0 if matches else 1


def query_cases(keyword: str, topic: str | None, as_json: bool) -> int:
    cases = load("case_index.json")
    matches = []
    for item in cases:
        if topic and item.get("topic") != topic:
            continue
        if contains(item, keyword):
            matches.append(item)
    if as_json:
        print_json(matches)
        return 0 if matches else 1
    for item in matches:
        print(f"- {item['id']} [{item.get('topic', '-')}] {item.get('case_type', '')}")
        print(f"  pattern: {item.get('question_pattern', '')}")
        print(f"  main god: {item.get('main_god', '')}")
        print(f"  must record: {', '.join(item.get('must_record', []))}")
        rules = ", ".join(item.get("linked_rule_ids", []))
        if rules:
            print(f"  linked rules: {rules}")
    return 0 if matches else 1


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Query structured Liuyao data")
    sub = parser.add_subparsers(dest="kind", required=True)

    terms = sub.add_parser("terms")
    terms.add_argument("keyword")
    terms.add_argument("--json", action="store_true")

    ziwei_terms = sub.add_parser("ziwei_terms")
    ziwei_terms.add_argument("keyword")
    ziwei_terms.add_argument("--json", action="store_true")

    qimen_terms = sub.add_parser("qimen_terms")
    qimen_terms.add_argument("keyword")
    qimen_terms.add_argument("--json", action="store_true")

    liuren_terms = sub.add_parser("liuren_terms")
    liuren_terms.add_argument("keyword")
    liuren_terms.add_argument("--json", action="store_true")

    rules = sub.add_parser("rules")
    rules.add_argument("keyword")
    rules.add_argument("--layer")
    rules.add_argument("--json", action="store_true")

    sources = sub.add_parser("sources")
    sources.add_argument("keyword")
    sources.add_argument("--class", dest="class_filter")
    sources.add_argument("--json", action="store_true")

    classics = sub.add_parser("classics")
    classics.add_argument("keyword")
    classics.add_argument("--json", action="store_true")

    notes = sub.add_parser("notes")
    notes.add_argument("keyword")
    notes.add_argument("--group", choices=["十八论", "十八问答"])
    notes.add_argument("--json", action="store_true")

    cases = sub.add_parser("cases")
    cases.add_argument("keyword")
    cases.add_argument("--topic")
    cases.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if args.kind == "terms":
        return query_terms(args.keyword, args.json)
    if args.kind == "ziwei_terms":
        return query_ziwei_terms(args.keyword, args.json)
    if args.kind == "qimen_terms":
        return query_qimen_terms(args.keyword, args.json)
    if args.kind == "liuren_terms":
        return query_liuren_terms(args.keyword, args.json)
    if args.kind == "rules":
        return query_rules(args.keyword, args.layer, args.json)
    if args.kind == "sources":
        return query_sources(args.keyword, args.class_filter, args.json)
    if args.kind == "classics":
        return query_classics(args.keyword, args.json)
    if args.kind == "notes":
        return query_notes(args.keyword, args.group, args.json)
    if args.kind == "cases":
        return query_cases(args.keyword, args.topic, args.json)
    raise AssertionError(args.kind)


if __name__ == "__main__":
    raise SystemExit(main())
