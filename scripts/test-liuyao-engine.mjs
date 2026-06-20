import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const engine = require("../web/liuyao-engine.js");

const failures = [];

function check(name, ok, detail = "") {
  console.log(`- ${name}: ${ok ? "ok" : "FAIL"}${detail ? ` (${detail})` : ""}`);
  if (!ok) failures.push(name);
}

function eq(name, actual, expected) {
  check(name, actual === expected, `expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
}

function eqList(name, actual, expected) {
  eq(name, actual.join(","), expected.join(","));
}

const qian = engine.buildLiuyaoChart({
  lines: ["young_yang", "young_yang", "young_yang", "young_yang", "young_yang", "young_yang"],
  dayStem: "甲",
  palaceElement: "金",
  lineElements: ["水", "木", "土", "火", "金", "土"],
  shiLine: 3,
  yingLine: 6,
});

eq("all_yang_primary_hexagram", qian.primary.name, "乾为天");
eq("all_yang_changed_hexagram", qian.changed.name, "乾为天");
check("all_yang_has_no_moving_lines", qian.movingLines.length === 0);
eq("jia_day_first_six_spirit", qian.lines[0].sixSpirit, "青龙");
eq("jia_day_sixth_six_spirit", qian.lines[5].sixSpirit, "玄武");
eq("palace_generates_line_is_descendant", qian.lines[0].sixRelative, "子孙");
eq("palace_controls_line_is_wealth", qian.lines[1].sixRelative, "妻财");
eq("line_generates_palace_is_parent", qian.lines[2].sixRelative, "父母");
eq("line_controls_palace_is_official", qian.lines[3].sixRelative, "官鬼");
eq("same_element_is_sibling", qian.lines[4].sixRelative, "兄弟");
eq("manual_shi_line_marked", qian.lines[2].role, "世");
eq("manual_ying_line_marked", qian.lines[5].role, "应");

const tai = engine.buildLiuyaoChart({
  lines: [9, 7, 7, 8, 8, 8],
  dayStem: "癸",
});

eq("old_yang_primary_before_change", tai.primary.name, "地天泰");
eq("old_yang_changed_after_change", tai.changed.name, "地风升");
eq("moving_line_number_is_one_based", tai.movingLines.join(","), "1");
eq("gui_day_first_six_spirit", tai.lines[0].sixSpirit, "玄武");

const li = engine.buildLiuyaoChart({
  lines: [7, 8, 7, 7, 8, 7],
  dayStem: "甲",
});

eq("li_primary_hexagram", li.primary.name, "离为火");
eq("li_primary_mark_bottom_to_top", li.primary.mark, "101101");
eq("li_palace_name", li.palace.name, "离");
eq("li_palace_element", li.palace.element, "火");
eqList(
  "li_najia_matches_reference_project",
  li.lines.map((line) => line.ganzhi),
  ["己卯", "己丑", "己亥", "己酉", "己未", "己巳"],
);
eqList(
  "li_line_elements_derive_from_branches",
  li.lines.map((line) => line.element),
  ["木", "土", "水", "金", "土", "火"],
);
eqList(
  "li_six_relatives_use_palace_element",
  li.lines.map((line) => line.sixRelative),
  ["父母", "子孙", "官鬼", "妻财", "子孙", "兄弟"],
);
eq("li_pure_world_line", li.shiLine, 6);
eq("li_pure_response_line", li.yingLine, 3);
eq("li_auto_world_role", li.lines[5].role, "世");
eq("li_auto_response_role", li.lines[2].role, "应");

const taiStatic = engine.buildLiuyaoChart({
  lines: [7, 7, 7, 8, 8, 8],
  dayStem: "癸",
});

eq("tai_static_mark", taiStatic.primary.mark, "111000");
eq("tai_static_world_line", taiStatic.shiLine, 3);
eq("tai_static_response_line", taiStatic.yingLine, 6);
eq("tai_static_palace_name", taiStatic.palace.name, "坤");
eq("tai_static_palace_element", taiStatic.palace.element, "土");

const wandering = engine.buildLiuyaoChart({
  lines: [8, 8, 8, 7, 8, 7],
});

eq("huodijin_is_wandering_soul", wandering.primary.name, "火地晋");
eq("huodijin_soul_type", wandering.soul, "游魂");
eq("huodijin_world_line", wandering.shiLine, 4);
eq("huodijin_response_line", wandering.yingLine, 1);
eq("huodijin_palace_name", wandering.palace.name, "乾");

const returning = engine.buildLiuyaoChart({
  lines: [7, 7, 7, 7, 8, 7],
});

eq("huotiandayu_is_returning_soul", returning.primary.name, "火天大有");
eq("huotiandayu_soul_type", returning.soul, "归魂");
eq("huotiandayu_world_line", returning.shiLine, 3);
eq("huotiandayu_response_line", returning.yingLine, 6);
eq("huotiandayu_palace_name", returning.palace.name, "乾");

check("tai_has_hidden_god_when_parent_absent", Boolean(taiStatic.hidden));
eq("tai_hidden_palace_hexagram", taiStatic.hidden?.palaceHexagram, "坤为地");
eq("tai_hidden_missing_relative", taiStatic.hidden?.missingRelatives?.[0]?.relative, "父母");
eq("tai_hidden_missing_line", taiStatic.hidden?.missingRelatives?.[0]?.line, 2);
eq("tai_hidden_missing_ganzhi", taiStatic.hidden?.missingRelatives?.[0]?.ganzhi, "乙巳");
eq("tai_hidden_missing_element", taiStatic.hidden?.missingRelatives?.[0]?.element, "火");

eqList("jiazi_void_branches", engine.calculateVoidBranches("甲子"), ["戌", "亥"]);
eqList("guiyou_void_branches", engine.calculateVoidBranches("癸酉"), ["戌", "亥"]);
eqList("jiaxu_void_branches", engine.calculateVoidBranches("甲戌"), ["申", "酉"]);

const liTimed = engine.buildLiuyaoChart({
  lines: [7, 8, 7, 7, 8, 7],
  dayGanzhi: "甲子",
  monthBranch: "申",
});

eq("day_ganzhi_infers_six_spirit", liTimed.lines[0].sixSpirit, "青龙");
eqList("chart_time_void_branches", liTimed.time.voidBranches, ["戌", "亥"]);
eq("chart_time_day_branch", liTimed.time.dayBranch, "子");
eq("chart_time_month_branch", liTimed.time.monthBranch, "申");
eq("hai_line_is_void_under_jiazi", liTimed.lines[2].void, true);
eq("hai_line_void_label", liTimed.lines[2].voidLabel, "旬空");
eq("zi_day_generates_mao_line", liTimed.lines[0].dayStatus, "日生");
eq("zi_day_controls_si_line", liTimed.lines[5].dayStatus, "日克");
eq("shen_month_controls_mao_line", liTimed.lines[0].monthStatus, "月克");
eq("shen_month_generates_hai_line", liTimed.lines[2].monthStatus, "月生");

const invalid = engine.validateLiuyaoInput({ lines: [7, 7, 7], dayStem: "甲" });
check("validation_rejects_missing_lines", invalid.errors.some((item) => item.includes("6")));

if (failures.length) {
  console.error("\nLiuyao engine tests failed:");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log("\nLiuyao engine tests ok.");
