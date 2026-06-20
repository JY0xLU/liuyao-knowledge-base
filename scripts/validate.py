#!/usr/bin/env python3
"""Validate structured Liuyao knowledge-base data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_json(name: str):
    path = DATA / name
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require_unique(items, key: str, label: str) -> list[str]:
    errors: list[str] = []
    seen = set()
    for item in items:
        value = item.get(key)
        if not value:
            errors.append(f"{label} item missing {key}: {item}")
            continue
        if value in seen:
            errors.append(f"{label} duplicate {key}: {value}")
        seen.add(value)
    return errors


def check_refs(items, source_ids: set[str], label: str) -> list[str]:
    errors: list[str] = []
    for item in items:
        item_id = item.get("id") or item.get("term") or item.get("title")
        for ref in item.get("source_refs", []):
            if ref not in source_ids:
                errors.append(f"{label} {item_id} references missing source {ref}")
    return errors


def iter_ziwei_structure_items(structures):
    for key, value in structures.items():
        if isinstance(value, list):
            for item in value:
                yield key, item


def check_ziwei_terms(terms, source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    errors += require_unique(terms, "id", "ziwei_terms")
    seen_terms: set[str] = set()
    for item in terms:
        term = item.get("term")
        if not term:
            errors.append(f"ziwei_term missing term: {item}")
            continue
        if term in seen_terms:
            errors.append(f"ziwei_term duplicate term: {term}")
        seen_terms.add(term)
        for key in ["category", "definition", "group", "boundary_notes"]:
            if not item.get(key):
                errors.append(f"ziwei_term {term} missing {key}")
    required = {"紫微斗数", "命盘", "命宫", "十二宫", "十四主星", "四化", "三方四正"}
    missing = required - seen_terms
    if missing:
        errors.append(f"ziwei_terms missing required terms: {', '.join(sorted(missing))}")
    errors += check_refs(terms, source_ids, "ziwei_term")
    return errors


def check_ziwei_structures(structures, source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if structures.get("system") != "ziwei":
        errors.append("ziwei_structures system must be ziwei")
    if not structures.get("boundary"):
        errors.append("ziwei_structures missing boundary")

    required_counts = {
        "palaces": 12,
        "major_stars": 14,
        "transformations": 4,
        "chart_fields": 6,
    }
    for key, minimum in required_counts.items():
        value = structures.get(key)
        if not isinstance(value, list) or len(value) < minimum:
            errors.append(f"ziwei_structures {key} must have at least {minimum} items")

    ids: set[str] = set()
    for group, item in iter_ziwei_structure_items(structures):
        item_id = item.get("id")
        if not item_id:
            errors.append(f"ziwei_structure {group} item missing id: {item}")
            continue
        if item_id in ids:
            errors.append(f"ziwei_structure duplicate id: {item_id}")
        ids.add(item_id)
        if not item.get("name"):
            errors.append(f"ziwei_structure {item_id} missing name")
        if not (item.get("focus") or item.get("core_focus") or item.get("description")):
            errors.append(f"ziwei_structure {item_id} missing focus/core_focus/description")
        for ref in item.get("source_refs", []):
            if ref not in source_ids:
                errors.append(f"ziwei_structure {item_id} references missing source {ref}")
    return errors


def check_rule_ids(case_schema, rule_ids: set[str]) -> list[str]:
    errors: list[str] = []
    judgment = case_schema.get("properties", {}).get("judgment", {})
    props = judgment.get("properties", {})
    if "rule_refs" not in props:
        errors.append("case_schema missing judgment.rule_refs")
    if not rule_ids:
        errors.append("rules.json has no rules")
    return errors


def check_note_refs(notes, source_ids: set[str], rule_ids: set[str]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for item in notes:
        note_id = item.get("id")
        if not note_id:
            errors.append(f"classic_note missing id: {item}")
            continue
        if note_id in seen:
            errors.append(f"classic_note duplicate id: {note_id}")
        seen.add(note_id)
        for key in ["classic_id", "classic_title", "section_group", "topic", "problem"]:
            if not item.get(key):
                errors.append(f"classic_note {note_id} missing {key}")
        if not item.get("rule_focus"):
            errors.append(f"classic_note {note_id} missing rule_focus")
        if not item.get("extraction_fields"):
            errors.append(f"classic_note {note_id} missing extraction_fields")
        if not item.get("practice_tasks"):
            errors.append(f"classic_note {note_id} missing practice_tasks")
        for ref in item.get("source_refs", []):
            if ref not in source_ids:
                errors.append(f"classic_note {note_id} references missing source {ref}")
        for rule_id in item.get("linked_rule_ids", []):
            if rule_id not in rule_ids:
                errors.append(f"classic_note {note_id} references missing rule {rule_id}")
    return errors


def check_case_index_refs(case_index, source_ids: set[str], rule_ids: set[str]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for item in case_index:
        case_id = item.get("id")
        if not case_id:
            errors.append(f"case_index missing id: {item}")
            continue
        if case_id in seen:
            errors.append(f"case_index duplicate id: {case_id}")
        seen.add(case_id)
        for key in ["source_ref", "topic", "case_type", "question_pattern", "main_god", "status"]:
            if not item.get(key):
                errors.append(f"case_index {case_id} missing {key}")
        if item.get("source_ref") not in source_ids:
            errors.append(f"case_index {case_id} references missing source {item.get('source_ref')}")
        if not item.get("must_record"):
            errors.append(f"case_index {case_id} missing must_record")
        for rule_id in item.get("linked_rule_ids", []):
            if rule_id not in rule_ids:
                errors.append(f"case_index {case_id} references missing rule {rule_id}")
    return errors


def check_external_projects(projects) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for item in projects:
        project_id = item.get("id")
        if not project_id:
            errors.append(f"external_project missing id: {item}")
            continue
        if project_id in seen:
            errors.append(f"external_project duplicate id: {project_id}")
        seen.add(project_id)
        for key in ["name", "owner", "url", "platform", "project_type", "scope", "adoption"]:
            if not item.get(key):
                errors.append(f"external_project {project_id} missing {key}")
        if not str(item.get("url", "")).startswith("https://github.com/"):
            errors.append(f"external_project {project_id} has non-GitHub url {item.get('url')}")
        for list_key in ["evidence", "useful_patterns", "risks"]:
            if not item.get(list_key):
                errors.append(f"external_project {project_id} missing {list_key}")
    return errors


def check_systems(systems) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for item in systems:
        system_id = item.get("id")
        if not system_id:
            errors.append(f"system missing id: {item}")
            continue
        if system_id in seen:
            errors.append(f"system duplicate id: {system_id}")
        seen.add(system_id)
        for key in ["name", "status", "scope", "source_strategy", "risk_notes"]:
            if not item.get(key):
                errors.append(f"system {system_id} missing {key}")
        for list_key in ["core_objects", "product_modules", "next_steps"]:
            if not item.get(list_key):
                errors.append(f"system {system_id} missing {list_key}")
    required = {"liuyao", "ziwei", "qimen", "liuren"}
    missing = required - seen
    if missing:
        errors.append(f"systems missing required ids: {', '.join(sorted(missing))}")
    return errors


def check_accuracy_cases(cases, source_ids: set[str], rule_ids: set[str]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for item in cases:
        case_id = item.get("id")
        if not case_id:
            errors.append(f"accuracy_case missing id: {item}")
            continue
        if case_id in seen:
            errors.append(f"accuracy_case duplicate id: {case_id}")
        seen.add(case_id)
        for key in ["title", "event_type", "event_date", "prediction", "actual_result", "score"]:
            if not item.get(key):
                errors.append(f"accuracy_case {case_id} missing {key}")
        prediction = item.get("prediction", {})
        if not prediction.get("summary"):
            errors.append(f"accuracy_case {case_id} missing prediction.summary")
        actual_result = item.get("actual_result", {})
        if not actual_result.get("summary"):
            errors.append(f"accuracy_case {case_id} missing actual_result.summary")
        score = item.get("score", {})
        total = score.get("total")
        if not isinstance(total, (int, float)) or total < 0 or total > 100:
            errors.append(f"accuracy_case {case_id} score.total must be 0-100")
        if not score.get("dimensions"):
            errors.append(f"accuracy_case {case_id} missing score.dimensions")
        if item.get("status") == "retrospective-calibration":
            if prediction.get("made_at") != "retrospective-not-precommitted":
                errors.append(f"accuracy_case {case_id} retrospective case must not look precommitted")
            if score.get("mode") != "retrospective_calibration_not_accuracy" or total != 0:
                errors.append(f"accuracy_case {case_id} retrospective case must not count toward accuracy")
        for ref in item.get("source_refs", []):
            if ref not in source_ids:
                errors.append(f"accuracy_case {case_id} references missing source {ref}")
        for rule_id in item.get("linked_rule_ids", []):
            if rule_id not in rule_ids:
                errors.append(f"accuracy_case {case_id} references missing rule {rule_id}")
    return errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    sources = load_json("sources.json")
    systems = load_json("systems.json")
    terms = load_json("terms.json")
    ziwei_terms = load_json("ziwei_terms.json")
    ziwei_structures = load_json("ziwei_structures.json")
    rules = load_json("rules.json")
    classics = load_json("classics_index.json")
    classic_notes = load_json("classic_notes.json")
    case_index = load_json("case_index.json")
    accuracy_cases = load_json("accuracy_cases.json")
    external_projects = load_json("external_projects.json")
    case_schema = load_json("case_schema.json")

    errors: list[str] = []
    errors += require_unique(sources, "id", "sources")
    errors += require_unique(systems, "id", "systems")
    errors += require_unique(rules, "id", "rules")
    errors += require_unique(classics, "id", "classics")

    source_ids = {item["id"] for item in sources if "id" in item}
    rule_ids = {item["id"] for item in rules if "id" in item}

    errors += check_refs(terms, source_ids, "term")
    errors += check_ziwei_terms(ziwei_terms, source_ids)
    errors += check_ziwei_structures(ziwei_structures, source_ids)
    errors += check_refs(rules, source_ids, "rule")
    errors += check_refs(classics, source_ids, "classic")
    errors += check_rule_ids(case_schema, rule_ids)
    errors += check_note_refs(classic_notes, source_ids, rule_ids)
    errors += check_case_index_refs(case_index, source_ids, rule_ids)
    errors += check_accuracy_cases(accuracy_cases, source_ids, rule_ids)
    errors += check_external_projects(external_projects)
    errors += check_systems(systems)

    required_docs = [
        "docs/00-learning-map.md",
        "docs/01-foundations.md",
        "docs/02-casting-and-installing.md",
        "docs/03-judgment-framework.md",
        "docs/04-topic-playbooks.md",
        "docs/05-case-template.md",
        "docs/06-classics-reading-index.md",
        "docs/07-rule-cards.md",
        "docs/08-research-and-deployment-log.md",
        "docs/09-bushi-zhengzong-notes.md",
        "docs/10-zengshan-case-index.md",
        "docs/11-external-project-benchmark.md",
        "docs/12-najia-engine-notes.md",
        "docs/13-accuracy-evaluation.md",
        "docs/14-github-versioning.md",
        "docs/15-multi-system-roadmap.md",
        "docs/16-ziwei-foundation.md",
        "docs/sources.md",
        "docs/website-plan.md",
    ]
    for rel in required_docs:
        if not (ROOT / rel).exists():
            errors.append(f"missing doc: {rel}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Validation ok: "
        f"{len(sources)} sources, {len(systems)} systems, {len(terms)} terms, "
        f"{len(ziwei_terms)} ziwei terms, "
        f"{len(rules)} rules, {len(classics)} classics, "
        f"{len(classic_notes)} classic notes, {len(case_index)} case slots, "
        f"{len(accuracy_cases)} accuracy cases, "
        f"{len(external_projects)} external projects"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
