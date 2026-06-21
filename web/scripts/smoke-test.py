#!/usr/bin/env python3
"""Smoke-test static workbench data and core search semantics."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def contains(item, query: str) -> bool:
    return query.lower() in json.dumps(item, ensure_ascii=False).lower()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
    data_path = ROOT / "web" / "assets" / "kb-data.json"
    data_js_path = ROOT / "web" / "assets" / "kb-data.js"
    data = json.loads(data_path.read_text(encoding="utf-8"))

    checks = {
        "html_loads_data_js": "./assets/kb-data.js" in html,
        "app_uses_inline_data": "window.LIUYAO_KB_DATA" in app,
        "data_js_exists": data_js_path.exists() and data_js_path.stat().st_size > 1000,
        "has_docs": len(data["docs"]) >= 13,
        "has_research_log": any(doc["title"] == "研究与部署日志" for doc in data["docs"]),
        "has_bushi_notes_doc": any(doc["title"] == "卜筮正宗十八论与十八问答读书笔记" for doc in data["docs"]),
        "has_zengshan_case_doc": any(doc["title"] == "增删卜易案例抽取索引" for doc in data["docs"]),
        "has_external_project_doc": any(doc["title"] == "外部项目与源码参考" for doc in data["docs"]),
        "has_accuracy_doc": any(doc["title"] == "准确度验证与评分" for doc in data["docs"]),
        "has_github_versioning_doc": any(doc["title"] == "GitHub 项目化与版本迭代" for doc in data["docs"]),
        "has_multi_system_doc": any(doc["title"] == "多术数体系路线图" for doc in data["docs"]),
        "has_ziwei_foundation_doc": any(doc["title"] == "紫微斗数第一版资料层" for doc in data["docs"]),
        "has_qimen_foundation_doc": any(doc["title"] == "奇门遁甲第一版资料层" for doc in data["docs"]),
        "has_liuren_foundation_doc": any(doc["title"] == "大六壬 / 小六壬第一版资料层" for doc in data["docs"]),
        "has_systems": len(data.get("systems", [])) >= 4,
        "systems_contains_ziwei": any(contains(item, "紫微斗数") for item in data.get("systems", [])),
        "systems_contains_qimen": any(contains(item, "奇门遁甲") for item in data.get("systems", [])),
        "systems_contains_liuren": any(contains(item, "大六壬") for item in data.get("systems", [])),
        "app_has_systems_view": 'systems: ["体系总览"' in app,
        "app_has_ziwei_view": 'ziwei: ["紫微资料"' in app and 'data-view="ziwei"' in html,
        "app_has_qimen_view": 'qimen: ["奇门资料"' in app and 'data-view="qimen"' in html,
        "app_has_liuren_view": 'liuren: ["六壬资料"' in app and 'data-view="liuren"' in html,
        "has_ziwei_terms": len(data.get("ziwei_terms", [])) >= 30,
        "ziwei_contains_core_terms": all(
            any(item.get("term") == term for item in data.get("ziwei_terms", []))
            for term in ["紫微斗数", "命宫", "四化"]
        ),
        "has_ziwei_structures": len(data.get("ziwei_structures", {}).get("palaces", [])) == 12
        and len(data.get("ziwei_structures", {}).get("major_stars", [])) == 14,
        "has_qimen_terms": len(data.get("qimen_terms", [])) >= 24,
        "qimen_contains_core_terms": all(
            any(item.get("term") == term for item in data.get("qimen_terms", []))
            for term in ["奇门遁甲", "九宫", "八门", "值符", "值使"]
        ),
        "has_qimen_structures": len(data.get("qimen_structures", {}).get("palaces", [])) == 9
        and len(data.get("qimen_structures", {}).get("gates", [])) == 8
        and len(data.get("qimen_structures", {}).get("stars", [])) == 9
        and len(data.get("qimen_structures", {}).get("deities", [])) == 8,
        "has_liuren_terms": len(data.get("liuren_terms", [])) >= 36,
        "liuren_contains_core_terms": all(
            any(item.get("term") == term for item in data.get("liuren_terms", []))
            for term in ["六壬", "大六壬", "小六壬", "四课", "三传", "十二天将", "小六壬六宫"]
        ),
        "has_liuren_structures": len(data.get("liuren_structures", {}).get("subsystems", [])) == 2
        and len(data.get("liuren_structures", {}).get("four_lessons", [])) == 4
        and len(data.get("liuren_structures", {}).get("three_transmissions", [])) == 3
        and len(data.get("liuren_structures", {}).get("heavenly_generals", [])) == 12
        and len(data.get("liuren_structures", {}).get("xiao_liuren_palaces", [])) == 6,
        "liuren_case_schema_required": "subsystem" in data.get("liuren_case_schema", {}).get("required", [])
        and data.get("liuren_case_schema", {}).get("title") == "LiurenCase",
        "has_rules": len(data["rules"]) >= 20,
        "has_classic_notes": len(data.get("classic_notes", [])) >= 36,
        "has_case_index": len(data.get("case_index", [])) >= 24,
        "has_accuracy_cases": len(data.get("accuracy_cases", [])) >= 1,
        "has_external_projects": len(data.get("external_projects", [])) >= 6,
        "notes_contains_void": any(contains(note, "旬空") for note in data.get("classic_notes", [])),
        "cases_contains_lost_object": any(contains(item, "失物") for item in data.get("case_index", [])),
        "projects_contains_najia": any(contains(item, "najia") for item in data.get("external_projects", [])),
        "accuracy_contains_scoring": any(contains(item, "评分") for item in data.get("accuracy_cases", [])),
        "has_sources": len(data["sources"]) >= 10,
        "has_void_rule": any(rule["title"] == "旬空不是永远没有" for rule in data["rules"]),
        "search_void_finds_rule": any(contains(rule, "旬空") for rule in data["rules"]),
        "classics_contains_bushi": any(classic["title"] == "卜筮正宗" for classic in data["classics"]),
        "case_schema_required": "judgment" in data["case_schema"].get("required", []),
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        print("Smoke test failed:")
        for name in failed:
            print(f"- {name}")
        return 1
    print("Smoke test ok:")
    for name in checks:
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
