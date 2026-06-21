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


def iter_qimen_structure_items(structures):
    for key, value in structures.items():
        if isinstance(value, list):
            for item in value:
                yield key, item


def iter_liuren_structure_items(structures):
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


def check_qimen_terms(terms, source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    errors += require_unique(terms, "id", "qimen_terms")
    seen_terms: set[str] = set()
    for item in terms:
        term = item.get("term")
        if not term:
            errors.append(f"qimen_term missing term: {item}")
            continue
        if term in seen_terms:
            errors.append(f"qimen_term duplicate term: {term}")
        seen_terms.add(term)
        for key in ["category", "definition", "group", "boundary_notes"]:
            if not item.get(key):
                errors.append(f"qimen_term {term} missing {key}")
    required = {"奇门遁甲", "九宫", "八门", "九星", "八神", "值符", "值使", "阴遁阳遁"}
    missing = required - seen_terms
    if missing:
        errors.append(f"qimen_terms missing required terms: {', '.join(sorted(missing))}")
    errors += check_refs(terms, source_ids, "qimen_term")
    return errors


def check_liuren_terms(terms, source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    errors += require_unique(terms, "id", "liuren_terms")
    seen_terms: set[str] = set()
    for item in terms:
        term = item.get("term")
        if not term:
            errors.append(f"liuren_term missing term: {item}")
            continue
        if term in seen_terms:
            errors.append(f"liuren_term duplicate term: {term}")
        seen_terms.add(term)
        for key in ["category", "definition", "group", "boundary_notes"]:
            if not item.get(key):
                errors.append(f"liuren_term {term} missing {key}")
    required = {"六壬", "大六壬", "小六壬", "月将", "占时", "四课", "三传", "十二天将", "小六壬六宫"}
    missing = required - seen_terms
    if missing:
        errors.append(f"liuren_terms missing required terms: {', '.join(sorted(missing))}")
    errors += check_refs(terms, source_ids, "liuren_term")
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


def check_qimen_structures(structures, source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if structures.get("system") != "qimen":
        errors.append("qimen_structures system must be qimen")
    if not structures.get("boundary"):
        errors.append("qimen_structures missing boundary")

    required_counts = {
        "palaces": 9,
        "gates": 8,
        "stars": 9,
        "deities": 8,
        "chart_fields": 6,
    }
    for key, minimum in required_counts.items():
        value = structures.get(key)
        if not isinstance(value, list) or len(value) < minimum:
            errors.append(f"qimen_structures {key} must have at least {minimum} items")

    ids: set[str] = set()
    for group, item in iter_qimen_structure_items(structures):
        item_id = item.get("id")
        if not item_id:
            errors.append(f"qimen_structure {group} item missing id: {item}")
            continue
        if item_id in ids:
            errors.append(f"qimen_structure duplicate id: {item_id}")
        ids.add(item_id)
        if not item.get("name"):
            errors.append(f"qimen_structure {item_id} missing name")
        if not (item.get("focus") or item.get("core_focus") or item.get("description")):
            errors.append(f"qimen_structure {item_id} missing focus/core_focus/description")
        for ref in item.get("source_refs", []):
            if ref not in source_ids:
                errors.append(f"qimen_structure {item_id} references missing source {ref}")
    return errors


def check_liuren_structures(structures, source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if structures.get("system") != "liuren":
        errors.append("liuren_structures system must be liuren")
    if not structures.get("boundary"):
        errors.append("liuren_structures missing boundary")

    required_counts = {
        "subsystems": 2,
        "da_liuren_chart_fields": 8,
        "four_lessons": 4,
        "three_transmissions": 3,
        "heavenly_generals": 12,
        "xiao_liuren_palaces": 6,
        "case_fields": 6,
    }
    for key, minimum in required_counts.items():
        value = structures.get(key)
        if not isinstance(value, list) or len(value) < minimum:
            errors.append(f"liuren_structures {key} must have at least {minimum} items")

    ids: set[str] = set()
    for group, item in iter_liuren_structure_items(structures):
        item_id = item.get("id")
        if not item_id:
            errors.append(f"liuren_structure {group} item missing id: {item}")
            continue
        if item_id in ids:
            errors.append(f"liuren_structure duplicate id: {item_id}")
        ids.add(item_id)
        if not item.get("name"):
            errors.append(f"liuren_structure {item_id} missing name")
        if not (item.get("focus") or item.get("core_focus") or item.get("description")):
            errors.append(f"liuren_structure {item_id} missing focus/core_focus/description")
        for ref in item.get("source_refs", []):
            if ref not in source_ids:
                errors.append(f"liuren_structure {item_id} references missing source {ref}")
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


def check_liuren_case_schema(schema, source_ids: set[str], liuren_structures) -> list[str]:
    errors: list[str] = []
    if schema.get("title") != "LiurenCase":
        errors.append("liuren_case_schema title must be LiurenCase")
    required = set(schema.get("required", []))
    expected = {
        "id",
        "system",
        "subsystem",
        "topic",
        "question",
        "input_source",
        "chart",
        "judgment",
        "boundary_notes",
    }
    missing = expected - required
    if missing:
        errors.append(f"liuren_case_schema missing required fields: {', '.join(sorted(missing))}")
    props = schema.get("properties", {})
    subsystem = props.get("subsystem", {})
    if set(subsystem.get("enum", [])) != {"da_liuren", "xiao_liuren"}:
        errors.append("liuren_case_schema subsystem must separate da_liuren and xiao_liuren")
    chart = props.get("chart", {})
    if "oneOf" not in chart:
        errors.append("liuren_case_schema chart must use oneOf for Da/Xiao Liuren")
    defs = schema.get("$defs", {})
    for key in ["da_liuren_chart", "xiao_liuren_chart", "lesson", "transmission", "heavenly_general", "xiao_liuren_palace"]:
        if key not in defs:
            errors.append(f"liuren_case_schema missing $defs.{key}")
    da_required = set(defs.get("da_liuren_chart", {}).get("required", []))
    for key in ["month_general", "divination_hour", "day_ganzhi", "plates", "four_lessons", "three_transmissions"]:
        if key not in da_required:
            errors.append(f"liuren_case_schema da_liuren_chart missing required {key}")
    xiao_required = set(defs.get("xiao_liuren_chart", {}).get("required", []))
    for key in ["qike_start", "selected_palace", "sangong"]:
        if key not in xiao_required:
            errors.append(f"liuren_case_schema xiao_liuren_chart missing required {key}")
    source_refs = schema.get("x_source_refs", [])
    for ref in source_refs:
        if ref not in source_ids:
            errors.append(f"liuren_case_schema references missing source {ref}")
    structure_ids = {
        item.get("id")
        for item in liuren_structures.get("case_fields", [])
        if item.get("id")
    }
    for ref in schema.get("x_structure_refs", []):
        if ref not in structure_ids:
            errors.append(f"liuren_case_schema references missing liuren case field {ref}")
    return errors


def check_qimen_case_schema(schema, source_ids: set[str], qimen_structures) -> list[str]:
    errors: list[str] = []
    if schema.get("title") != "QimenCase":
        errors.append("qimen_case_schema title must be QimenCase")
    required = set(schema.get("required", []))
    expected = {
        "id",
        "system",
        "method",
        "time_system",
        "topic",
        "question",
        "input_source",
        "chart",
        "judgment",
        "boundary_notes",
    }
    missing = expected - required
    if missing:
        errors.append(f"qimen_case_schema missing required fields: {', '.join(sorted(missing))}")

    props = schema.get("properties", {})
    if props.get("system", {}).get("const") != "qimen":
        errors.append("qimen_case_schema system must be qimen")

    defs = schema.get("$defs", {})
    for key in [
        "qimen_method",
        "time_system",
        "palace_id",
        "palace_name",
        "gate_name",
        "star_name",
        "deity_name",
        "calendar_basis",
        "zhi_marker",
        "palace_cell",
        "topic_mapping",
        "shared_chart_fields",
        "hour_qimen_chart",
        "day_qimen_chart",
    ]:
        if key not in defs:
            errors.append(f"qimen_case_schema missing $defs.{key}")

    if set(defs.get("qimen_method", {}).get("enum", [])) != {"zhuanpan", "feipan", "other"}:
        errors.append("qimen_case_schema method must separate zhuanpan, feipan, and other")
    if set(defs.get("time_system", {}).get("enum", [])) != {"shi_jia", "ri_jia"}:
        errors.append("qimen_case_schema time_system must separate shi_jia and ri_jia")

    chart = props.get("chart", {})
    if len(chart.get("oneOf", [])) != 2:
        errors.append("qimen_case_schema chart must use oneOf for Shi/Ri Qimen")

    shared_required = set(defs.get("shared_chart_fields", {}).get("required", []))
    for key in ["method", "time_system", "calendar_basis", "dun_type", "ju_number", "zhi_fu", "zhi_shi", "palaces"]:
        if key not in shared_required:
            errors.append(f"qimen_case_schema shared_chart_fields missing required {key}")

    palaces = defs.get("shared_chart_fields", {}).get("properties", {}).get("palaces", {})
    if palaces.get("minItems") != 9 or palaces.get("maxItems") != 9:
        errors.append("qimen_case_schema palaces must require exactly 9 cells")

    hour_props = defs.get("hour_qimen_chart", {}).get("allOf", [{}, {}])[-1].get("properties", {})
    day_props = defs.get("day_qimen_chart", {}).get("allOf", [{}, {}])[-1].get("properties", {})
    if hour_props.get("time_system", {}).get("const") != "shi_jia":
        errors.append("qimen_case_schema hour_qimen_chart must const shi_jia")
    if day_props.get("time_system", {}).get("const") != "ri_jia":
        errors.append("qimen_case_schema day_qimen_chart must const ri_jia")

    source_refs = schema.get("x_source_refs", [])
    for ref in source_refs:
        if ref not in source_ids:
            errors.append(f"qimen_case_schema references missing source {ref}")

    structure_ids = {
        item.get("id")
        for item in qimen_structures.get("chart_fields", [])
        if item.get("id")
    }
    for ref in schema.get("x_structure_refs", []):
        if ref not in structure_ids:
            errors.append(f"qimen_case_schema references missing qimen chart field {ref}")
    return errors


def check_liuren_case_samples(samples, source_ids: set[str], schema) -> list[str]:
    errors: list[str] = []
    errors += require_unique(samples, "id", "liuren_case_samples")
    if len(samples) < 2:
        errors.append("liuren_case_samples must include at least one da_liuren and one xiao_liuren sample")

    required = set(schema.get("required", []))
    forbidden_liuyao_terms = {"hexagram", "lines", "six_kin", "world_response", "shi_line", "ying_line"}
    subsystems = {item.get("subsystem") for item in samples}
    if not {"da_liuren", "xiao_liuren"}.issubset(subsystems):
        errors.append("liuren_case_samples must cover da_liuren and xiao_liuren")

    for item in samples:
        sample_id = item.get("id", "unknown")
        missing = [key for key in required if key not in item]
        if missing:
            errors.append(f"liuren_case_sample {sample_id} missing required fields: {', '.join(sorted(missing))}")
        if item.get("system") != "liuren":
            errors.append(f"liuren_case_sample {sample_id} system must be liuren")
        subsystem = item.get("subsystem")
        if subsystem not in {"da_liuren", "xiao_liuren"}:
            errors.append(f"liuren_case_sample {sample_id} subsystem must be da_liuren or xiao_liuren")

        chart = item.get("chart", {})
        if chart.get("subsystem") != subsystem:
            errors.append(f"liuren_case_sample {sample_id} chart.subsystem must match subsystem")
        if not item.get("source_refs"):
            errors.append(f"liuren_case_sample {sample_id} missing source_refs")
        if not item.get("boundary_notes"):
            errors.append(f"liuren_case_sample {sample_id} missing boundary_notes")
        if item.get("sample_type") != "schema_fixture":
            errors.append(f"liuren_case_sample {sample_id} sample_type must be schema_fixture")

        text = json.dumps(item, ensure_ascii=False)
        for token in forbidden_liuyao_terms:
            if token in text:
                errors.append(f"liuren_case_sample {sample_id} contains Liuyao-only token {token}")
        if any(token in text for token in ["C:\\Users\\", "Desktop\\新建文件夹", "NETLIFY_AUTH_TOKEN", "x-access-token"]):
            errors.append(f"liuren_case_sample {sample_id} contains local path or private token marker")

        score = item.get("score", {})
        total = score.get("total")
        if not isinstance(total, (int, float)) or total < 0 or total > 100:
            errors.append(f"liuren_case_sample {sample_id} score.total must be 0-100")
        if item.get("outcome", {}).get("status") == "retrospective_calibration":
            if score.get("mode") != "retrospective_calibration_not_accuracy" or total != 0:
                errors.append(f"liuren_case_sample {sample_id} retrospective fixture must not count toward accuracy")
        if not score.get("dimensions"):
            errors.append(f"liuren_case_sample {sample_id} missing score.dimensions")

        for ref in item.get("source_refs", []):
            if ref not in source_ids:
                errors.append(f"liuren_case_sample {sample_id} references missing source {ref}")
        for ref in item.get("judgment", {}).get("rule_source_refs", []):
            if ref not in source_ids:
                errors.append(f"liuren_case_sample {sample_id} judgment references missing source {ref}")

        if subsystem == "da_liuren":
            for key in ["calendar_basis", "month_general", "divination_hour", "day_ganzhi", "plates"]:
                if not chart.get(key):
                    errors.append(f"liuren_case_sample {sample_id} da_liuren chart missing {key}")
            if len(chart.get("four_lessons", [])) != 4:
                errors.append(f"liuren_case_sample {sample_id} da_liuren chart must have four lessons")
            transmissions = chart.get("three_transmissions", {})
            if not {"initial", "middle", "final"}.issubset(transmissions):
                errors.append(f"liuren_case_sample {sample_id} da_liuren chart missing three transmissions")
            generals = chart.get("heavenly_generals", {})
            if len(generals) != 12:
                errors.append(f"liuren_case_sample {sample_id} da_liuren chart must map 12 heavenly generals")
        if subsystem == "xiao_liuren":
            if not chart.get("qike_start") or not chart.get("selected_palace"):
                errors.append(f"liuren_case_sample {sample_id} xiao_liuren chart missing qike_start/selected_palace")
            if not chart.get("sangong"):
                errors.append(f"liuren_case_sample {sample_id} xiao_liuren chart missing sangong")
            palace_order = chart.get("palace_order", [])
            if chart.get("selected_palace") not in palace_order:
                errors.append(f"liuren_case_sample {sample_id} selected_palace must exist in palace_order")
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
    qimen_terms = load_json("qimen_terms.json")
    qimen_structures = load_json("qimen_structures.json")
    qimen_case_schema = load_json("qimen_case_schema.json")
    liuren_terms = load_json("liuren_terms.json")
    liuren_structures = load_json("liuren_structures.json")
    rules = load_json("rules.json")
    classics = load_json("classics_index.json")
    classic_notes = load_json("classic_notes.json")
    case_index = load_json("case_index.json")
    accuracy_cases = load_json("accuracy_cases.json")
    external_projects = load_json("external_projects.json")
    case_schema = load_json("case_schema.json")
    liuren_case_schema = load_json("liuren_case_schema.json")
    liuren_case_samples = load_json("liuren_case_samples.json")

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
    errors += check_qimen_terms(qimen_terms, source_ids)
    errors += check_qimen_structures(qimen_structures, source_ids)
    errors += check_qimen_case_schema(qimen_case_schema, source_ids, qimen_structures)
    errors += check_liuren_terms(liuren_terms, source_ids)
    errors += check_liuren_structures(liuren_structures, source_ids)
    errors += check_refs(rules, source_ids, "rule")
    errors += check_refs(classics, source_ids, "classic")
    errors += check_rule_ids(case_schema, rule_ids)
    errors += check_liuren_case_schema(liuren_case_schema, source_ids, liuren_structures)
    errors += check_liuren_case_samples(liuren_case_samples, source_ids, liuren_case_schema)
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
        "docs/17-qimen-foundation.md",
        "docs/18-liuren-foundation.md",
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
        f"{len(qimen_terms)} qimen terms, "
        f"{len(liuren_terms)} liuren terms, "
        f"{len(rules)} rules, {len(classics)} classics, "
        f"{len(classic_notes)} classic notes, {len(case_index)} case slots, "
        f"{len(accuracy_cases)} accuracy cases, "
        f"{len(external_projects)} external projects, "
        f"qimen case schema, liuren case schema, {len(liuren_case_samples)} liuren case samples"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
