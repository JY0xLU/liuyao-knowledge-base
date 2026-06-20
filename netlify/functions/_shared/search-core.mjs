export function jsonResponse(payload, init = {}) {
  const headers = new Headers(init.headers || {});
  headers.set("Content-Type", "application/json; charset=utf-8");
  headers.set("Cache-Control", "public, max-age=300");
  return new Response(JSON.stringify(payload), { ...init, headers });
}

export function errorResponse(message, status = 400) {
  return jsonResponse({ error: message }, { status });
}

function normalize(value) {
  return String(value || "").trim().toLowerCase();
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function contains(value, query) {
  if (!query) return true;
  return JSON.stringify(value).toLowerCase().includes(query.toLowerCase());
}

function scoreItem(item, terms) {
  const text = JSON.stringify(item).toLowerCase();
  return terms.reduce((sum, term) => {
    const matches = text.match(new RegExp(escapeRegExp(term), "g"));
    return sum + (matches ? matches.length : 0);
  }, 0);
}

export function searchPools(data) {
  return [
    ...(data.docs || []).map((item) => ({
      kind: "docs",
      kind_label: "文档",
      id: item.id,
      title: item.title,
      summary: item.summary,
      item,
    })),
    ...(data.rules || []).map((item) => ({
      kind: "rules",
      kind_label: "规则",
      id: item.id,
      title: item.title,
      summary: item.statement,
      item,
    })),
    ...(data.terms || []).map((item) => ({
      kind: "terms",
      kind_label: "术语",
      id: item.term,
      title: item.term,
      summary: item.definition,
      item,
    })),
    ...(data.sources || []).map((item) => ({
      kind: "sources",
      kind_label: "来源",
      id: item.id,
      title: item.title,
      summary: item.notes,
      item,
    })),
    ...(data.classics || []).map((item) => ({
      kind: "classics",
      kind_label: "古籍",
      id: item.id,
      title: item.title,
      summary: item.knowledge_tasks.join("；"),
      item,
    })),
    ...(data.classic_notes || []).map((item) => ({
      kind: "classic_notes",
      kind_label: "笔记",
      id: item.id,
      title: item.topic,
      summary: `${item.problem} ${item.rule_focus.join("；")}`,
      item,
    })),
    ...(data.case_index || []).map((item) => ({
      kind: "case_index",
      kind_label: "案例槽位",
      id: item.id,
      title: item.case_type,
      summary: `${item.question_pattern} ${item.must_record.join("；")}`,
      item,
    })),
    ...(data.accuracy_cases || []).map((item) => ({
      kind: "accuracy_cases",
      kind_label: "验证案例",
      id: item.id,
      title: item.title,
      summary: `${item.event_type} ${item.prediction.summary} ${item.actual_result.summary} score ${item.score.total}`,
      item,
    })),
    ...(data.external_projects || []).map((item) => ({
      kind: "external_projects",
      kind_label: "外部项目",
      id: item.id,
      title: `${item.owner}/${item.name}`,
      summary: `${item.scope} ${item.useful_patterns.join("；")} ${item.risks.join("；")}`,
      item,
    })),
  ];
}

export function searchKnowledgeBase(data, options = {}) {
  const query = normalize(options.query);
  const terms = query.split(/\s+/).filter(Boolean);
  const limit = Math.max(1, Math.min(Number(options.limit) || 30, 100));
  const kind = normalize(options.kind);
  const pools = searchPools(data).filter((entry) => !kind || entry.kind === kind);
  const results = pools
    .filter((entry) => contains(entry.item, query))
    .map((entry) => ({
      ...entry,
      score: terms.length ? scoreItem(entry.item, terms) : 1,
    }))
    .sort((a, b) => b.score - a.score || a.kind.localeCompare(b.kind) || a.title.localeCompare(b.title, "zh-Hans-CN"))
    .slice(0, limit);

  return {
    query,
    kind: kind || "all",
    limit,
    total: results.length,
    results,
  };
}
