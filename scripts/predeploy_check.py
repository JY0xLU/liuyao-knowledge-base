#!/usr/bin/env python3
"""Pre-deploy checks for the static Liuyao workbench."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check(name: str, ok: bool, failures: list[str]) -> None:
    print(f"- {name}: {'ok' if ok else 'FAIL'}")
    if not ok:
        failures.append(name)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    failures: list[str] = []
    netlify_path = ROOT / "netlify.toml"
    package_path = ROOT / "package.json"
    index_path = ROOT / "web" / "index.html"
    app_path = ROOT / "web" / "app.js"
    engine_path = ROOT / "web" / "liuyao-engine.js"
    css_path = ROOT / "web" / "styles.css"
    data_path = ROOT / "web" / "assets" / "kb-data.json"
    data_js_path = ROOT / "web" / "assets" / "kb-data.js"
    function_data_path = ROOT / "netlify" / "functions" / "_shared" / "kb-data.mjs"
    function_search_core_path = ROOT / "netlify" / "functions" / "_shared" / "search-core.mjs"
    function_search_path = ROOT / "netlify" / "functions" / "search.mts"
    function_schema_path = ROOT / "netlify" / "functions" / "case-schema.mts"
    function_test_path = ROOT / "scripts" / "test-functions.mjs"
    engine_test_path = ROOT / "scripts" / "test-liuyao-engine.mjs"
    changelog_path = ROOT / "CHANGELOG.md"
    readme_path = ROOT / "README.md"
    docs_paths = sorted((ROOT / "docs").glob("*.md"))

    for path in [
        netlify_path,
        package_path,
        index_path,
        app_path,
        engine_path,
        css_path,
        data_path,
        data_js_path,
        function_data_path,
        function_search_core_path,
        function_search_path,
        function_schema_path,
        function_test_path,
        engine_test_path,
        changelog_path,
        readme_path,
    ]:
        check(f"exists:{path.relative_to(ROOT)}", path.exists(), failures)

    if failures:
        return 1

    netlify = read_text(netlify_path)
    package = json.loads(read_text(package_path))
    html = read_text(index_path)
    app = read_text(app_path)
    engine = read_text(engine_path)
    css = read_text(css_path)
    data = json.loads(read_text(data_path))
    data_js = read_text(data_js_path)
    function_data = read_text(function_data_path)
    function_search_core = read_text(function_search_core_path)
    function_search = read_text(function_search_path)
    function_schema = read_text(function_schema_path)
    changelog = read_text(changelog_path)
    readme = read_text(readme_path)
    public_text = "\n".join([readme, *(read_text(path) for path in docs_paths)])

    check("netlify_publish_web", re.search(r'publish\s*=\s*"web"', netlify) is not None, failures)
    check(
        "netlify_rebuilds_data",
        re.search(r'command\s*=\s*"npm run build:netlify"', netlify) is not None
        and data_path.exists()
        and data_js_path.exists()
        and function_data_path.exists(),
        failures,
    )
    check("netlify_functions_configured", 'directory = "netlify/functions"' in netlify, failures)
    check(
        "package_check_runs_all_python_checks",
        package["scripts"].get("check", "") == "python scripts/check.py",
        failures,
    )
    check(
        "html_loads_data_before_app",
        html.find("./assets/kb-data.js") != -1
        and html.find("./liuyao-engine.js") != -1
        and html.find("./app.js") != -1
        and html.find("./liuyao-engine.js") < html.find("./assets/kb-data.js") < html.find("./app.js"),
        failures,
    )
    check("app_has_file_protocol_fallback", "window.LIUYAO_KB_DATA" in app, failures)
    check("app_uses_api_search_with_fallback", "/api/search" in app and "localSearchResults" in app, failures)
    check("app_has_systems_view", 'systems: ["体系总览"' in app and 'data-view="systems"' in html, failures)
    check("app_has_ziwei_view", 'ziwei: ["紫微资料"' in app and 'data-view="ziwei"' in html, failures)
    check("app_has_qimen_view", 'qimen: ["奇门资料"' in app and 'data-view="qimen"' in html, failures)
    check("app_has_liuren_view", 'liuren: ["六壬资料"' in app and 'data-view="liuren"' in html, failures)
    check("app_has_caster_view", 'caster: ["装卦辅助", "手工起卦排盘"]' in app, failures)
    check("engine_exports_builder", "buildLiuyaoChart" in engine and "validateLiuyaoInput" in engine, failures)
    check("css_has_mobile_breakpoint", "@media (max-width: 820px)" in css, failures)
    check("css_has_search_status", ".search-status" in css, failures)
    check("css_has_caster_result", ".caster-result" in css and ".line-table" in css, failures)
    check("data_js_assigns_global", data_js.startswith("window.LIUYAO_KB_DATA = "), failures)
    check("function_data_exports_default", function_data.startswith("export default "), failures)
    check("function_search_uses_modern_export", "export default async" in function_search, failures)
    check("function_search_api_path", 'path: "/api/search"' in function_search, failures)
    check("function_case_schema_api_path", 'path: "/api/case-schema"' in function_schema, failures)
    check("function_search_core_has_case_index", "case_index" in function_search_core, failures)
    check("function_search_core_has_systems", "data.systems" in function_search_core, failures)
    check("function_search_core_has_accuracy_cases", "accuracy_cases" in function_search_core, failures)
    check("function_search_core_has_external_projects", "external_projects" in function_search_core, failures)
    check("function_search_core_has_ziwei_terms", "ziwei_terms" in function_search_core, failures)
    check("function_search_core_has_ziwei_structures", "ziwei_structures" in function_search_core, failures)
    check("function_search_core_has_qimen_terms", "qimen_terms" in function_search_core, failures)
    check("function_search_core_has_qimen_structures", "qimen_structures" in function_search_core, failures)
    check("function_search_core_has_liuren_terms", "liuren_terms" in function_search_core, failures)
    check("function_search_core_has_liuren_structures", "liuren_structures" in function_search_core, failures)
    check("docs_count", len(data.get("docs", [])) >= 13, failures)
    check(
        "research_log_in_site_data",
        any(doc.get("title") == "研究与部署日志" for doc in data.get("docs", [])),
        failures,
    )
    check(
        "bushi_notes_in_site_data",
        any(doc.get("title") == "卜筮正宗十八论与十八问答读书笔记" for doc in data.get("docs", [])),
        failures,
    )
    check(
        "zengshan_case_doc_in_site_data",
        any(doc.get("title") == "增删卜易案例抽取索引" for doc in data.get("docs", [])),
        failures,
    )
    check(
        "external_project_doc_in_site_data",
        any(doc.get("title") == "外部项目与源码参考" for doc in data.get("docs", [])),
        failures,
    )
    check(
        "multi_system_doc_in_site_data",
        any(doc.get("title") == "多术数体系路线图" for doc in data.get("docs", [])),
        failures,
    )
    check(
        "ziwei_foundation_doc_in_site_data",
        any(doc.get("title") == "紫微斗数第一版资料层" for doc in data.get("docs", [])),
        failures,
    )
    check(
        "qimen_foundation_doc_in_site_data",
        any(doc.get("title") == "奇门遁甲第一版资料层" for doc in data.get("docs", [])),
        failures,
    )
    check(
        "liuren_foundation_doc_in_site_data",
        any(doc.get("title") == "大六壬 / 小六壬第一版资料层" for doc in data.get("docs", [])),
        failures,
    )
    check("systems_count", len(data.get("systems", [])) >= 4, failures)
    check(
        "systems_cover_requested_scope",
        {"liuyao", "ziwei", "qimen", "liuren"}.issubset({item.get("id") for item in data.get("systems", [])}),
        failures,
    )
    check("rules_count", len(data.get("rules", [])) >= 20, failures)
    check("ziwei_terms_count", len(data.get("ziwei_terms", [])) >= 30, failures)
    check(
        "ziwei_terms_have_core_terms",
        {"紫微斗数", "命宫", "四化", "三方四正"}.issubset({item.get("term") for item in data.get("ziwei_terms", [])}),
        failures,
    )
    check(
        "ziwei_structures_have_core_counts",
        len(data.get("ziwei_structures", {}).get("palaces", [])) == 12
        and len(data.get("ziwei_structures", {}).get("major_stars", [])) == 14
        and len(data.get("ziwei_structures", {}).get("transformations", [])) == 4,
        failures,
    )
    check("qimen_terms_count", len(data.get("qimen_terms", [])) >= 24, failures)
    check(
        "qimen_terms_have_core_terms",
        {"奇门遁甲", "九宫", "八门", "九星", "八神", "值符", "值使"}.issubset(
            {item.get("term") for item in data.get("qimen_terms", [])}
        ),
        failures,
    )
    check(
        "qimen_structures_have_core_counts",
        len(data.get("qimen_structures", {}).get("palaces", [])) == 9
        and len(data.get("qimen_structures", {}).get("gates", [])) == 8
        and len(data.get("qimen_structures", {}).get("stars", [])) == 9
        and len(data.get("qimen_structures", {}).get("deities", [])) == 8,
        failures,
    )
    check("liuren_terms_count", len(data.get("liuren_terms", [])) >= 36, failures)
    check(
        "liuren_terms_have_core_terms",
        {"六壬", "大六壬", "小六壬", "四课", "三传", "十二天将", "小六壬六宫"}.issubset(
            {item.get("term") for item in data.get("liuren_terms", [])}
        ),
        failures,
    )
    check(
        "liuren_structures_have_core_counts",
        len(data.get("liuren_structures", {}).get("subsystems", [])) == 2
        and len(data.get("liuren_structures", {}).get("four_lessons", [])) == 4
        and len(data.get("liuren_structures", {}).get("three_transmissions", [])) == 3
        and len(data.get("liuren_structures", {}).get("heavenly_generals", [])) == 12
        and len(data.get("liuren_structures", {}).get("xiao_liuren_palaces", [])) == 6,
        failures,
    )
    check("classic_notes_count", len(data.get("classic_notes", [])) >= 36, failures)
    check(
        "classic_notes_have_linked_rules",
        all(note.get("linked_rule_ids") for note in data.get("classic_notes", [])),
        failures,
    )
    check("case_index_count", len(data.get("case_index", [])) >= 24, failures)
    check("accuracy_cases_count", len(data.get("accuracy_cases", [])) >= 4, failures)
    check(
        "accuracy_cases_mark_retrospective",
        any(item.get("status") == "retrospective-calibration" for item in data.get("accuracy_cases", [])),
        failures,
    )
    check("external_projects_count", len(data.get("external_projects", [])) >= 6, failures)
    check(
        "case_index_have_linked_rules",
        all(item.get("linked_rule_ids") for item in data.get("case_index", [])),
        failures,
    )
    check("sources_count", len(data.get("sources", [])) >= 10, failures)
    check("has_a_class_sources", any(source.get("class") == "A" for source in data.get("sources", [])), failures)
    check(
        "source_urls_are_http",
        all(str(source.get("url", "")).startswith(("https://", "http://")) for source in data.get("sources", [])),
        failures,
    )
    source_ids = [source.get("id") for source in data.get("sources", [])]
    rule_ids = [rule.get("id") for rule in data.get("rules", [])]
    term_names = [term.get("term") for term in data.get("terms", [])]
    check("unique_source_ids", len(source_ids) == len(set(source_ids)), failures)
    check("unique_rule_ids", len(rule_ids) == len(set(rule_ids)), failures)
    check("unique_terms", len(term_names) == len(set(term_names)), failures)
    check(
        "no_local_windows_paths_in_public_assets",
        "C:\\Users\\" not in data_js and "Desktop\\新建文件夹" not in data_js,
        failures,
    )
    check(
        "no_local_windows_paths_in_function_data",
        "C:\\Users\\" not in function_data and "Desktop\\新建文件夹" not in function_data,
        failures,
    )
    check(
        "no_local_windows_paths_in_public_docs",
        "C:\\Users\\" not in public_text
        and "Desktop\\新建文件夹" not in public_text
        and "codex-runtimes" not in public_text,
        failures,
    )
    check(
        "readme_has_deploy_commands",
        "npm run check" in readme and "npx netlify deploy --prod" in readme,
        failures,
    )
    check("changelog_has_current_version", "## v0.7.0 - 2026-06-21" in changelog, failures)

    if failures:
        print("\nPredeploy check failed:")
        for name in failures:
            print(f"- {name}")
        return 1

    print("\nPredeploy check ok.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
