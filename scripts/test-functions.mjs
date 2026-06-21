import data from "../netlify/functions/_shared/kb-data.mjs";
import { searchKnowledgeBase } from "../netlify/functions/_shared/search-core.mjs";
import searchHandler from "../netlify/functions/search.mts";
import caseSchemaHandler from "../netlify/functions/case-schema.mts";
import liurenCaseSchemaHandler from "../netlify/functions/liuren-case-schema.mts";

const failures = [];

function check(name, ok) {
  console.log(`- ${name}: ${ok ? "ok" : "FAIL"}`);
  if (!ok) failures.push(name);
}

const lost = searchKnowledgeBase(data, { query: "失物", kind: "case_index", limit: 10 });
const voidNotes = searchKnowledgeBase(data, { query: "旬空", kind: "classic_notes", limit: 10 });
const projects = searchKnowledgeBase(data, { query: "najia", kind: "external_projects", limit: 10 });
const systems = searchKnowledgeBase(data, { query: "紫微斗数", kind: "systems", limit: 10 });
const ziweiTerms = searchKnowledgeBase(data, { query: "紫微", kind: "ziwei_terms", limit: 10 });
const ziweiMajorStars = searchKnowledgeBase(data, { query: "十四主星", kind: "ziwei_terms", limit: 20 });
const ziweiRelations = searchKnowledgeBase(data, { query: "三方四正", kind: "ziwei_terms", limit: 10 });
const ziweiStructures = searchKnowledgeBase(data, { query: "命宫", kind: "ziwei_structures", limit: 10 });
const qimenTerms = searchKnowledgeBase(data, { query: "奇门遁甲", kind: "qimen_terms", limit: 10 });
const qimenGates = searchKnowledgeBase(data, { query: "八门", kind: "qimen_terms", limit: 10 });
const qimenStructures = searchKnowledgeBase(data, { query: "坎一宫", kind: "qimen_structures", limit: 10 });
const liurenTerms = searchKnowledgeBase(data, { query: "大六壬", kind: "liuren_terms", limit: 10 });
const liurenThreeTransmissions = searchKnowledgeBase(data, { query: "三传", kind: "liuren_terms", limit: 20 });
const liurenStructures = searchKnowledgeBase(data, { query: "初传", kind: "liuren_structures", limit: 10 });
const xiaoLiurenStructures = searchKnowledgeBase(data, { query: "大安", kind: "liuren_structures", limit: 10 });
const liurenCaseSchema = searchKnowledgeBase(data, { query: "four_lessons", kind: "liuren_case_schema", limit: 10 });
const accuracy = searchKnowledgeBase(data, { query: "评分", kind: "accuracy_cases", limit: 10 });
const retroAccuracy = searchKnowledgeBase(data, { query: "retrospective-calibration", kind: "accuracy_cases", limit: 10 });
const all = searchKnowledgeBase(data, { query: "回头克", limit: 20 });

check("function_data_has_docs", data.docs.length >= 13);
check("function_data_has_rules", data.rules.length >= 25);
check("function_data_has_notes", data.classic_notes.length >= 36);
check("function_data_has_case_slots", data.case_index.length >= 24);
check("function_data_has_systems", data.systems.length >= 4);
check("function_data_has_ziwei_terms", data.ziwei_terms.length >= 30);
check("function_data_has_ziwei_structures", data.ziwei_structures.palaces.length === 12 && data.ziwei_structures.major_stars.length === 14);
check("function_data_has_qimen_terms", data.qimen_terms.length >= 24);
check(
  "function_data_has_qimen_structures",
  data.qimen_structures.palaces.length === 9
    && data.qimen_structures.gates.length === 8
    && data.qimen_structures.stars.length === 9
    && data.qimen_structures.deities.length === 8,
);
check("function_data_has_liuren_terms", data.liuren_terms.length >= 36);
check(
  "function_data_has_liuren_structures",
  data.liuren_structures.subsystems.length === 2
    && data.liuren_structures.four_lessons.length === 4
    && data.liuren_structures.three_transmissions.length === 3
    && data.liuren_structures.heavenly_generals.length === 12
    && data.liuren_structures.xiao_liuren_palaces.length === 6,
);
check(
  "function_data_has_liuren_case_schema",
  data.liuren_case_schema.title === "LiurenCase"
    && data.liuren_case_schema.required.includes("subsystem")
    && data.liuren_case_schema.properties.chart.oneOf.length === 2,
);
check("function_data_has_accuracy_cases", data.accuracy_cases.length >= 4);
check("function_data_has_external_projects", data.external_projects.length >= 6);
check("search_case_index_lost_object", lost.results.some((item) => item.id === "zengshan-case-slot-010-lost-object-home"));
check("search_notes_void", voidNotes.results.some((item) => item.kind === "classic_notes" && item.title.includes("旬空")));
check("search_external_projects_najia", projects.results.some((item) => item.id === "github-bopo-najia"));
check("search_systems_ziwei", systems.results.some((item) => item.id === "ziwei"));
check("search_ziwei_terms_ziwei", ziweiTerms.results.some((item) => item.kind === "ziwei_terms" && item.title.includes("紫微")));
check(
  "search_ziwei_terms_major_stars",
  ziweiMajorStars.results.some((item) => item.id === "fourteen-major-stars" || item.item.group === "十四主星"),
);
check("search_ziwei_terms_sanfang", ziweiRelations.results.some((item) => item.id === "sanfang-sizheng"));
check("search_ziwei_structures_ming", ziweiStructures.results.some((item) => item.id === "palace-ming"));
check("search_qimen_terms_qimen", qimenTerms.results.some((item) => item.kind === "qimen_terms" && item.id === "qimen-dunjia"));
check("search_qimen_terms_gates", qimenGates.results.some((item) => item.id === "eight-gates"));
check("search_qimen_structures_kan", qimenStructures.results.some((item) => item.id === "palace-kan-1"));
check("search_liuren_terms_da", liurenTerms.results.some((item) => item.kind === "liuren_terms" && item.id === "da-liuren"));
check("search_liuren_terms_three_transmissions", liurenThreeTransmissions.results.some((item) => item.id === "three-transmissions"));
check("search_liuren_structures_initial", liurenStructures.results.some((item) => item.id === "transmission-initial"));
check("search_liuren_structures_daan", xiaoLiurenStructures.results.some((item) => item.id === "xiao-palace-daan"));
check("search_liuren_case_schema_four_lessons", liurenCaseSchema.results.some((item) => item.id === "liuren_case_schema"));
check("search_accuracy_cases_scoring", accuracy.results.some((item) => item.id === "accuracy-demo-2026-nba-finals-game-7"));
check("search_accuracy_cases_retro", retroAccuracy.results.some((item) => item.id === "accuracy-retro-2024-super-bowl-lviii"));
check("search_all_back_control", all.results.some((item) => item.title.includes("回头克") || JSON.stringify(item.item).includes("回头克")));
check("case_schema_available", data.case_schema.required.includes("judgment"));

const searchResponse = await searchHandler(new Request("https://example.test/api/search?q=najia&kind=external_projects"));
const searchPayload = await searchResponse.json();
check("handler_search_get_ok", searchResponse.status === 200 && searchPayload.results.some((item) => item.id === "github-bopo-najia"));

const ziweiResponse = await searchHandler(new Request("https://example.test/api/search?q=%E5%9B%9B%E5%8C%96&kind=ziwei_terms"));
const ziweiPayload = await ziweiResponse.json();
check("handler_search_ziwei_terms_ok", ziweiResponse.status === 200 && ziweiPayload.results.some((item) => item.id === "four-transformations"));

const qimenResponse = await searchHandler(new Request("https://example.test/api/search?q=%E5%85%AB%E9%97%A8&kind=qimen_terms"));
const qimenPayload = await qimenResponse.json();
check("handler_search_qimen_terms_ok", qimenResponse.status === 200 && qimenPayload.results.some((item) => item.id === "eight-gates"));

const liurenResponse = await searchHandler(new Request("https://example.test/api/search?q=%E5%9B%9B%E8%AF%BE&kind=liuren_terms"));
const liurenPayload = await liurenResponse.json();
check("handler_search_liuren_terms_ok", liurenResponse.status === 200 && liurenPayload.results.some((item) => item.id === "four-lessons"));

const schemaResponse = await caseSchemaHandler(new Request("https://example.test/api/case-schema"));
const schemaPayload = await schemaResponse.json();
check("handler_case_schema_get_ok", schemaResponse.status === 200 && schemaPayload.schema.title === "LiuyaoCase");

const liurenSchemaResponse = await liurenCaseSchemaHandler(new Request("https://example.test/api/liuren-case-schema"));
const liurenSchemaPayload = await liurenSchemaResponse.json();
check(
  "handler_liuren_case_schema_get_ok",
  liurenSchemaResponse.status === 200 && liurenSchemaPayload.schema.title === "LiurenCase",
);

const methodResponse = await searchHandler(new Request("https://example.test/api/search", { method: "POST" }));
check("handler_rejects_post", methodResponse.status === 405);

if (failures.length) {
  console.error("\nFunction tests failed:");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log("\nFunction tests ok.");
