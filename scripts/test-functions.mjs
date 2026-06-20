import data from "../netlify/functions/_shared/kb-data.mjs";
import { searchKnowledgeBase } from "../netlify/functions/_shared/search-core.mjs";
import searchHandler from "../netlify/functions/search.mts";
import caseSchemaHandler from "../netlify/functions/case-schema.mts";

const failures = [];

function check(name, ok) {
  console.log(`- ${name}: ${ok ? "ok" : "FAIL"}`);
  if (!ok) failures.push(name);
}

const lost = searchKnowledgeBase(data, { query: "失物", kind: "case_index", limit: 10 });
const voidNotes = searchKnowledgeBase(data, { query: "旬空", kind: "classic_notes", limit: 10 });
const projects = searchKnowledgeBase(data, { query: "najia", kind: "external_projects", limit: 10 });
const accuracy = searchKnowledgeBase(data, { query: "评分", kind: "accuracy_cases", limit: 10 });
const retroAccuracy = searchKnowledgeBase(data, { query: "retrospective-calibration", kind: "accuracy_cases", limit: 10 });
const all = searchKnowledgeBase(data, { query: "回头克", limit: 20 });

check("function_data_has_docs", data.docs.length >= 13);
check("function_data_has_rules", data.rules.length >= 25);
check("function_data_has_notes", data.classic_notes.length >= 36);
check("function_data_has_case_slots", data.case_index.length >= 24);
check("function_data_has_accuracy_cases", data.accuracy_cases.length >= 4);
check("function_data_has_external_projects", data.external_projects.length >= 6);
check("search_case_index_lost_object", lost.results.some((item) => item.id === "zengshan-case-slot-010-lost-object-home"));
check("search_notes_void", voidNotes.results.some((item) => item.kind === "classic_notes" && item.title.includes("旬空")));
check("search_external_projects_najia", projects.results.some((item) => item.id === "github-bopo-najia"));
check("search_accuracy_cases_scoring", accuracy.results.some((item) => item.id === "accuracy-demo-2026-nba-finals-game-7"));
check("search_accuracy_cases_retro", retroAccuracy.results.some((item) => item.id === "accuracy-retro-2024-super-bowl-lviii"));
check("search_all_back_control", all.results.some((item) => item.title.includes("回头克") || JSON.stringify(item.item).includes("回头克")));
check("case_schema_available", data.case_schema.required.includes("judgment"));

const searchResponse = await searchHandler(new Request("https://example.test/api/search?q=najia&kind=external_projects"));
const searchPayload = await searchResponse.json();
check("handler_search_get_ok", searchResponse.status === 200 && searchPayload.results.some((item) => item.id === "github-bopo-najia"));

const schemaResponse = await caseSchemaHandler(new Request("https://example.test/api/case-schema"));
const schemaPayload = await schemaResponse.json();
check("handler_case_schema_get_ok", schemaResponse.status === 200 && schemaPayload.schema.title === "LiuyaoCase");

const methodResponse = await searchHandler(new Request("https://example.test/api/search", { method: "POST" }));
check("handler_rejects_post", methodResponse.status === 405);

if (failures.length) {
  console.error("\nFunction tests failed:");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log("\nFunction tests ok.");
