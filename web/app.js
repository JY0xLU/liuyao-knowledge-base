const state = {
  data: null,
  view: "learn",
  query: "",
  selectedDoc: "00-learning-map",
  apiSearch: {
    query: "",
    status: "idle",
    results: null,
  },
};

let apiSearchTimer = null;
let apiSearchRequestId = 0;

const els = {
  search: document.querySelector("#globalSearch"),
  content: document.querySelector("#content"),
  navButtons: [...document.querySelectorAll(".nav-button")],
  docList: document.querySelector("#docList"),
  viewLabel: document.querySelector("#viewLabel"),
  viewTitle: document.querySelector("#viewTitle"),
  stats: document.querySelector("#statsGrid"),
  quickRules: document.querySelector("#quickRules"),
  primarySources: document.querySelector("#primarySources"),
  copyLink: document.querySelector("#copyLinkButton"),
  exportCase: document.querySelector("#exportCaseButton"),
  emptyTemplate: document.querySelector("#emptyTemplate"),
};

const viewTitles = {
  learn: ["学习路径", "术数学习工作台"],
  systems: ["体系总览", "奇门 · 六壬 · 紫微 · 六爻"],
  search: ["检索结果", "全库检索"],
  rules: ["规则卡", "可追踪断法规则"],
  terms: ["术语表", "六爻术语速查"],
  classics: ["古籍索引", "经典阅读路线"],
  notes: ["读书笔记", "十八论与问答笔记"],
  caseIndex: ["案例索引", "增删卜易案例槽位"],
  accuracy: ["验证评分", "事件验证与评分"],
  caster: ["装卦辅助", "手工起卦排盘"],
  projects: ["外部项目", "类似项目与源码参考"],
  sources: ["来源库", "资料来源与采信等级"],
  case: ["案例录入", "断卦复盘模板"],
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function slugLabel(path) {
  return path.replace(/^docs\//, "").replace(/\.md$/, "");
}

function setView(view) {
  state.view = view;
  els.navButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.view === view);
  });
  const [label, title] = viewTitles[view] || viewTitles.learn;
  els.viewLabel.textContent = label;
  els.viewTitle.textContent = title;
  render();
}

function matchText(item, query) {
  if (!query) return true;
  return JSON.stringify(item).toLowerCase().includes(query.toLowerCase());
}

function scoreItem(item, terms) {
  const text = JSON.stringify(item).toLowerCase();
  return terms.reduce((sum, term) => sum + (text.match(new RegExp(escapeRegExp(term), "g")) || []).length, 0);
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function markdownToHtml(markdown) {
  const lines = markdown.split(/\r?\n/);
  const html = [];
  let listOpen = false;
  let codeOpen = false;
  let tableBuffer = [];

  const closeList = () => {
    if (listOpen) {
      html.push("</ul>");
      listOpen = false;
    }
  };
  const flushTable = () => {
    if (!tableBuffer.length) return;
    const rows = tableBuffer
      .filter((line) => !/^\|\s*-+/.test(line))
      .map((line) => line.split("|").slice(1, -1).map((cell) => cell.trim()));
    if (rows.length) {
      const [head, ...body] = rows;
      html.push("<table><thead><tr>");
      head.forEach((cell) => html.push(`<th>${inlineMarkdown(cell)}</th>`));
      html.push("</tr></thead><tbody>");
      body.forEach((row) => {
        html.push("<tr>");
        row.forEach((cell) => html.push(`<td>${inlineMarkdown(cell)}</td>`));
        html.push("</tr>");
      });
      html.push("</tbody></table>");
    }
    tableBuffer = [];
  };

  lines.forEach((line) => {
    if (line.startsWith("```")) {
      flushTable();
      closeList();
      if (codeOpen) {
        html.push("</code></pre>");
      } else {
        html.push("<pre><code>");
      }
      codeOpen = !codeOpen;
      return;
    }
    if (codeOpen) {
      html.push(`${escapeHtml(line)}\n`);
      return;
    }
    if (line.includes("|") && line.trim().startsWith("|")) {
      closeList();
      tableBuffer.push(line);
      return;
    }
    flushTable();

    const trimmed = line.trim();
    if (!trimmed) {
      closeList();
      return;
    }
    const heading = trimmed.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      closeList();
      html.push(`<h${heading[1].length}>${inlineMarkdown(heading[2])}</h${heading[1].length}>`);
      return;
    }
    if (trimmed.startsWith("- ")) {
      if (!listOpen) {
        html.push("<ul>");
        listOpen = true;
      }
      html.push(`<li>${inlineMarkdown(trimmed.slice(2))}</li>`);
      return;
    }
    closeList();
    html.push(`<p>${inlineMarkdown(trimmed)}</p>`);
  });
  flushTable();
  closeList();
  if (codeOpen) html.push("</code></pre>");
  return html.join("");
}

function inlineMarkdown(value) {
  return escapeHtml(value)
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>')
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

function localSearchResults(query) {
  const terms = query.split(/\s+/).filter(Boolean);
  const pools = [
    ...(state.data.docs || []).map((item) => ({ type: "文档", title: item.title, body: item.summary, item })),
    ...(state.data.rules || []).map((item) => ({ type: "规则", title: item.title, body: item.statement, item })),
    ...(state.data.terms || []).map((item) => ({ type: "术语", title: item.term, body: item.definition, item })),
    ...(state.data.sources || []).map((item) => ({ type: "来源", title: item.title, body: item.notes, item })),
    ...(state.data.systems || []).map((item) => ({
      type: "体系",
      title: item.name,
      body: `${item.scope} ${item.core_objects.join("；")} ${item.product_modules.join("；")}`,
      item,
    })),
    ...(state.data.classics || []).map((item) => ({ type: "古籍", title: item.title, body: item.knowledge_tasks.join("；"), item })),
    ...(state.data.classic_notes || []).map((item) => ({
      type: "笔记",
      title: item.topic,
      body: `${item.problem} ${item.rule_focus.join("；")}`,
      item,
    })),
    ...(state.data.case_index || []).map((item) => ({
      type: "案例槽位",
      title: item.case_type,
      body: `${item.question_pattern} ${item.must_record.join("；")}`,
      item,
    })),
    ...(state.data.accuracy_cases || []).map((item) => ({
      type: "验证案例",
      title: item.title,
      body: `${item.event_type} ${item.prediction.summary} ${item.actual_result.summary} score ${item.score.total}`,
      item,
    })),
    ...(state.data.external_projects || []).map((item) => ({
      type: "外部项目",
      title: `${item.owner}/${item.name}`,
      body: `${item.scope} ${item.useful_patterns.join("；")} ${item.risks.join("；")}`,
      item,
    })),
  ];

  return pools
    .filter((entry) => (query ? matchText(entry.item, query) : true))
    .map((entry) => ({ ...entry, score: terms.length ? scoreItem(entry.item, terms) : 1 }))
    .sort((a, b) => b.score - a.score || a.type.localeCompare(b.type) || a.title.localeCompare(b.title, "zh-Hans-CN"))
    .slice(0, 30);
}

function apiSearchResults(payload) {
  return (payload.results || []).map((entry) => ({
    type: entry.kind_label || entry.kind || "结果",
    title: entry.title,
    body: entry.summary,
    score: entry.score,
    item: entry.item,
  }));
}

function canUseApiSearch() {
  return location.protocol === "http:" || location.protocol === "https:";
}

function scheduleApiSearch(query) {
  window.clearTimeout(apiSearchTimer);
  const trimmed = query.trim();
  if (!trimmed || !canUseApiSearch()) {
    state.apiSearch = { query: "", status: "idle", results: null };
    return;
  }

  state.apiSearch = { query: trimmed, status: "loading", results: null };
  apiSearchTimer = window.setTimeout(() => fetchApiSearch(trimmed), 220);
}

async function fetchApiSearch(query) {
  const requestId = ++apiSearchRequestId;
  try {
    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&limit=30`, {
      headers: { Accept: "application/json" },
    });
    if (!response.ok) throw new Error(`search api ${response.status}`);
    const payload = await response.json();
    if (requestId !== apiSearchRequestId || state.query.trim() !== query) return;
    state.apiSearch = { query, status: "ready", results: apiSearchResults(payload) };
    if (state.view === "search") render();
  } catch (_error) {
    if (requestId !== apiSearchRequestId || state.query.trim() !== query) return;
    state.apiSearch = { query, status: "fallback", results: null };
    if (state.view === "search") render();
  }
}

function renderStats() {
  const data = state.data;
  const stats = [
    ["文档", (data.docs || []).length],
    ["体系", (data.systems || []).length],
    ["术语", (data.terms || []).length],
    ["规则", (data.rules || []).length],
    ["来源", (data.sources || []).length],
    ["古籍", (data.classics || []).length],
    ["A 类源", (data.sources || []).filter((source) => source.class === "A").length],
  ];
  els.stats.innerHTML = stats
    .map(([label, value]) => `<div><dt>${label}</dt><dd>${value}</dd></div>`)
    .join("");
}

function renderInspector() {
  els.quickRules.innerHTML = state.data.rules
    .slice(0, 4)
    .map(
      (rule) => `
        <article class="mini-card">
          <strong>${escapeHtml(rule.title)}</strong>
          <span>${escapeHtml(rule.statement)}</span>
        </article>
      `,
    )
    .join("");

  els.primarySources.innerHTML = state.data.sources
    .filter((source) => source.class === "A")
    .slice(0, 4)
    .map(
      (source) => `
        <article class="mini-card">
          <strong>${escapeHtml(source.title)}</strong>
          <a href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(source.id)}</a>
        </article>
      `,
    )
    .join("");
}

function renderDocList() {
  els.docList.innerHTML = `
    <h2>文档</h2>
    ${state.data.docs
      .map(
        (doc) => `
          <button class="doc-button ${doc.id === state.selectedDoc ? "is-active" : ""}" data-doc="${doc.id}">
            ${escapeHtml(doc.title)}
          </button>
        `,
      )
      .join("")}
  `;
  els.docList.querySelectorAll(".doc-button").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedDoc = button.dataset.doc;
      setView("learn");
    });
  });
}

function renderLearn() {
  const doc = state.data.docs.find((item) => item.id === state.selectedDoc) || state.data.docs[0];
  els.content.innerHTML = `
    <div class="hero-grid">
      <article class="hero-card">
        <h3>把六爻学习从散乱资料变成可追踪系统</h3>
        <p>本工作台将教材、术语、规则卡、古籍来源和案例复盘放在同一个本地界面。先学结构，再查规则，最后用反馈案例校验。</p>
        <div class="tag-row">
          <span class="tag">本地优先</span>
          <span class="tag">来源可追踪</span>
          <span class="tag">规则可校验</span>
        </div>
      </article>
      <article class="card">
        <h3>当前文档</h3>
        <p>${escapeHtml(doc.summary)}</p>
        <div class="tag-row">
          <span class="tag">${escapeHtml(slugLabel(doc.path))}</span>
        </div>
      </article>
    </div>
    <article class="article markdown-body">${markdownToHtml(doc.markdown)}</article>
  `;
}

function renderSearch() {
  const query = state.query.trim();
  const hasApiResults = state.apiSearch.status === "ready" && state.apiSearch.query === query;
  const results = hasApiResults ? state.apiSearch.results : localSearchResults(query);
  const sourceLabel = hasApiResults ? "后端 API" : "本地数据包";
  const syncLabel = state.apiSearch.status === "loading" && state.apiSearch.query === query ? "后端同步中" : sourceLabel;

  if (!results.length) {
    els.content.innerHTML = els.emptyTemplate.innerHTML;
    return;
  }
  els.content.innerHTML = `
    <div class="search-status">
      <span class="tag">${escapeHtml(syncLabel)}</span>
      <span class="tag">${results.length} 条结果</span>
    </div>
    <div class="result-grid">${results
    .map(
      (entry) => `
        <article class="card">
          <div class="meta-row">
            <span class="tag">${entry.type}</span>
            <span class="tag">score ${entry.score}</span>
          </div>
          <h3>${escapeHtml(entry.title)}</h3>
          <p>${escapeHtml(entry.body || "")}</p>
        </article>
      `,
    )
    .join("")}</div>`;
}

function renderRules() {
  const query = state.query.trim();
  const rules = state.data.rules.filter((rule) => matchText(rule, query));
  els.content.innerHTML = `<div class="result-grid">${rules
    .map(
      (rule) => `
        <article class="card">
          <div class="meta-row">
            <span class="tag">${escapeHtml(rule.layer)}</span>
            <span class="tag">confidence ${escapeHtml(rule.confidence)}</span>
          </div>
          <h3>${escapeHtml(rule.title)}</h3>
          <p>${escapeHtml(rule.statement)}</p>
          <div class="tag-row">${rule.source_refs.map((ref) => `<span class="tag">${escapeHtml(ref)}</span>`).join("")}</div>
        </article>
      `,
    )
    .join("")}</div>`;
}

function renderTerms() {
  const query = state.query.trim();
  const terms = state.data.terms.filter((term) => matchText(term, query));
  els.content.innerHTML = `<div class="result-grid">${terms
    .map(
      (term) => `
        <article class="card">
          <div class="meta-row">
            <span class="tag">${escapeHtml(term.category)}</span>
            ${term.aliases.map((alias) => `<span class="tag">${escapeHtml(alias)}</span>`).join("")}
          </div>
          <h3>${escapeHtml(term.term)}</h3>
          <p>${escapeHtml(term.definition)}</p>
          <div class="tag-row">${term.source_refs.map((ref) => `<span class="tag">${escapeHtml(ref)}</span>`).join("")}</div>
        </article>
      `,
    )
    .join("")}</div>`;
}

function renderClassics() {
  const query = state.query.trim();
  const classics = state.data.classics.filter((classic) => matchText(classic, query));
  els.content.innerHTML = `<div class="result-grid">${classics
    .map(
      (classic) => `
        <article class="card">
          <div class="meta-row">
            <span class="tag">${escapeHtml(classic.role)}</span>
            <span class="tag">priority ${escapeHtml(classic.priority)}</span>
          </div>
          <h3>${escapeHtml(classic.title)}</h3>
          <p><strong>先读：</strong>${escapeHtml(classic.read_first.join("、"))}</p>
          <p><strong>任务：</strong>${escapeHtml(classic.knowledge_tasks.join("；"))}</p>
        </article>
      `,
    )
    .join("")}</div>`;
}

function renderNotes() {
  const query = state.query.trim();
  const notes = state.data.classic_notes.filter((note) => matchText(note, query));
  els.content.innerHTML = `<div class="result-grid">${notes
    .map(
      (note) => `
        <article class="card">
          <div class="meta-row">
            <span class="tag">${escapeHtml(note.section_group)}</span>
            <span class="tag">${escapeHtml(note.classic_title)}</span>
            <span class="tag">第 ${escapeHtml(note.order)} 条</span>
          </div>
          <h3>${escapeHtml(note.topic)}</h3>
          <p><strong>问题：</strong>${escapeHtml(note.problem)}</p>
          <p><strong>焦点：</strong>${escapeHtml(note.rule_focus.join("；"))}</p>
          <p><strong>字段：</strong>${escapeHtml(note.extraction_fields.join("、"))}</p>
          <div class="tag-row">${note.linked_rule_ids.map((ref) => `<span class="tag">${escapeHtml(ref)}</span>`).join("")}</div>
        </article>
      `,
    )
    .join("")}</div>`;
}

function renderCaseIndex() {
  const query = state.query.trim();
  const cases = state.data.case_index.filter((item) => matchText(item, query));
  els.content.innerHTML = `<div class="result-grid">${cases
    .map(
      (item) => `
        <article class="card">
          <div class="meta-row">
            <span class="tag">${escapeHtml(item.topic)}</span>
            <span class="tag">${escapeHtml(item.source_title)}</span>
            <span class="tag">${escapeHtml(item.status)}</span>
          </div>
          <h3>${escapeHtml(item.case_type)}</h3>
          <p><strong>问题型：</strong>${escapeHtml(item.question_pattern)}</p>
          <p><strong>主用神：</strong>${escapeHtml(item.main_god)}</p>
          <p><strong>必填：</strong>${escapeHtml(item.must_record.join("、"))}</p>
          <div class="tag-row">${item.linked_rule_ids.map((ref) => `<span class="tag">${escapeHtml(ref)}</span>`).join("")}</div>
        </article>
      `,
    )
    .join("")}</div>`;
}

function renderAccuracy() {
  const query = state.query.trim();
  const cases = (state.data.accuracy_cases || []).filter((item) => matchText(item, query));
  els.content.innerHTML = `<div class="result-grid">${cases
    .map(
      (item) => `
        <article class="card">
          <div class="meta-row">
            <span class="tag">${escapeHtml(item.event_type)}</span>
            <span class="tag">${escapeHtml(item.status)}</span>
            <span class="tag">${escapeHtml(item.event_date)}</span>
            <span class="tag">score ${escapeHtml(String(item.score.total))}</span>
            ${item.score.mode ? `<span class="tag">${escapeHtml(item.score.mode)}</span>` : ""}
          </div>
          <h3>${escapeHtml(item.title)}</h3>
          <p><strong>对象：</strong>${escapeHtml(item.subject)}</p>
          <p><strong>预测：</strong>${escapeHtml(item.prediction.summary)}</p>
          <p><strong>结果：</strong>${escapeHtml(item.actual_result.summary)}</p>
          <div class="score-grid">
            ${item.score.dimensions
              .map(
                (dimension) => `
                  <div>
                    <strong>${escapeHtml(dimension.name)}</strong>
                    <span>${escapeHtml(String(dimension.value))}/${escapeHtml(String(dimension.weight))}</span>
                  </div>
                `,
              )
              .join("")}
          </div>
          <div class="tag-row">
            ${[...(item.linked_rule_ids || []), ...(item.source_refs || [])].map((ref) => `<span class="tag">${escapeHtml(ref)}</span>`).join("")}
          </div>
        </article>
      `,
    )
    .join("")}</div>`;
}

function renderCaster() {
  els.content.innerHTML = `
    <div class="two-column">
      <article class="article">
        <h3>装卦辅助</h3>
        <form id="casterForm" class="form-grid">
          ${[1, 2, 3, 4, 5, 6]
            .map(
              (line) => `
                <label class="form-field">第 ${line} 爻
                  <select name="line_${line}">
                    <option value="7">少阳 7</option>
                    <option value="8">少阴 8</option>
                    <option value="9">老阳 9 动</option>
                    <option value="6">老阴 6 动</option>
                  </select>
                </label>
              `,
            )
            .join("")}
          <label class="form-field">日干
            <select name="day_stem">
              ${["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
                .map((stem) => `<option value="${stem}">${stem}</option>`)
                .join("")}
            </select>
          </label>
          <label class="form-field">日干支
            <input name="day_ganzhi" placeholder="例如：甲子" />
          </label>
          <label class="form-field">月建
            <select name="month_branch">
              <option value="">未填</option>
              ${["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
                .map((branch) => `<option value="${branch}">${branch}</option>`)
                .join("")}
            </select>
          </label>
          <label class="form-field">世爻修正
            <select name="shi_line">
              <option value="">自动</option>
              ${[1, 2, 3, 4, 5, 6].map((line) => `<option value="${line}">第 ${line} 爻</option>`).join("")}
            </select>
          </label>
          <label class="form-field">应爻修正
            <select name="ying_line">
              <option value="">自动</option>
              ${[1, 2, 3, 4, 5, 6].map((line) => `<option value="${line}">第 ${line} 爻</option>`).join("")}
            </select>
          </label>
        </form>
      </article>
      <article class="card">
        <h3>排盘结果</h3>
        <div id="casterResult" class="caster-result"></div>
      </article>
    </div>
  `;
  const form = document.querySelector("#casterForm");
  form.addEventListener("input", updateCasterResult);
  updateCasterResult();
}

function currentCasterChart() {
  const form = document.querySelector("#casterForm");
  if (!form || !window.LiuyaoEngine) return null;
  const data = Object.fromEntries(new FormData(form).entries());
  return window.LiuyaoEngine.buildLiuyaoChart({
    lines: [1, 2, 3, 4, 5, 6].map((line) => data[`line_${line}`] || "7"),
    dayStem: data.day_stem || "甲",
    dayGanzhi: data.day_ganzhi || "",
    monthBranch: data.month_branch || "",
    shiLine: data.shi_line || "",
    yingLine: data.ying_line || "",
  });
}

function updateCasterResult() {
  const target = document.querySelector("#casterResult");
  if (!target) return;
  try {
    const chart = currentCasterChart();
    if (!chart) throw new Error("Liuyao engine is not loaded.");
    target.innerHTML = `
      <div class="hexagram-summary">
        <strong>${escapeHtml(chart.primary.name)}</strong>
        <span>变卦：${escapeHtml(chart.changed.name)}</span>
        <span>卦宫：${escapeHtml(chart.palace.name)}宫${escapeHtml(chart.palace.element)}</span>
        <span>世应：${escapeHtml(String(chart.shiLine))}/${escapeHtml(String(chart.yingLine))}</span>
        <span>日辰：${escapeHtml(chart.time.dayGanzhi || "-")}</span>
        <span>月建：${escapeHtml(chart.time.monthBranch || "-")}</span>
        <span>旬空：${chart.time.voidBranches.length ? chart.time.voidBranches.map(escapeHtml).join("、") : "-"}</span>
        <span>${chart.soul ? escapeHtml(chart.soul) : "正卦"}</span>
        <span>卦码：${escapeHtml(chart.primary.mark)}</span>
        <span>动爻：${chart.movingLines.length ? chart.movingLines.join("、") : "无"}</span>
      </div>
      ${
        chart.hidden
          ? `<div class="hidden-gods">
              <strong>伏神</strong>
              <span>${escapeHtml(chart.hidden.palaceHexagram)}</span>
              ${chart.hidden.missingRelatives
                .map(
                  (item) =>
                    `<span>${escapeHtml(item.relative)}：${escapeHtml(item.ganzhi)}${escapeHtml(item.element)}（${escapeHtml(
                      String(item.line),
                    )}爻）</span>`,
                )
                .join("")}
            </div>`
          : `<div class="hidden-gods"><strong>伏神</strong><span>五类六亲齐备</span></div>`
      }
      <table class="line-table">
        <thead><tr><th>爻位</th><th>爻象</th><th>纳甲</th><th>五行</th><th>六神</th><th>六亲</th><th>月日</th><th>旬空</th><th>世应</th></tr></thead>
        <tbody>
          ${chart.lines
            .slice()
            .reverse()
            .map(
              (line) => `
                <tr>
                  <td>${line.index}</td>
                  <td>${escapeHtml(line.label)}${line.moving ? ` → ${escapeHtml(line.changedTo)}` : ""}</td>
                  <td>${escapeHtml(line.ganzhi || "-")}</td>
                  <td>${escapeHtml(line.element || "-")}</td>
                  <td>${escapeHtml(line.sixSpirit || "-")}</td>
                  <td>${escapeHtml(line.sixRelative || "-")}</td>
                  <td>${escapeHtml([line.monthStatus, line.dayStatus].filter(Boolean).join(" / ") || "-")}</td>
                  <td>${escapeHtml(line.voidLabel || "-")}</td>
                  <td>${escapeHtml(line.role || "-")}</td>
                </tr>
              `,
            )
            .join("")}
        </tbody>
      </table>
    `;
  } catch (error) {
    target.innerHTML = `<p class="error-text">${escapeHtml(error.message)}</p>`;
  }
}

function renderProjects() {
  const query = state.query.trim();
  const projects = state.data.external_projects.filter((item) => matchText(item, query));
  els.content.innerHTML = `<div class="result-grid">${projects
    .map(
      (item) => `
        <article class="card">
          <div class="meta-row">
            <span class="tag">${escapeHtml(item.language || "unknown")}</span>
            <span class="tag">${escapeHtml(item.project_type)}</span>
            <span class="tag">${escapeHtml(String(item.stars))} stars</span>
          </div>
          <h3>${escapeHtml(item.owner)}/${escapeHtml(item.name)}</h3>
          <p>${escapeHtml(item.scope)}</p>
          <p><strong>借鉴：</strong>${escapeHtml(item.useful_patterns.join("；"))}</p>
          <p><strong>风险：</strong>${escapeHtml(item.risks.join("；"))}</p>
          <a href="${escapeHtml(item.url)}" target="_blank" rel="noreferrer">${escapeHtml(item.url)}</a>
        </article>
      `,
    )
    .join("")}</div>`;
}

function renderSystems() {
  const query = state.query.trim();
  const systems = (state.data.systems || []).filter((item) => matchText(item, query));
  els.content.innerHTML = `<div class="result-grid">${systems
    .map(
      (item) => `
        <article class="card">
          <div class="meta-row">
            <span class="tag">${escapeHtml(item.id)}</span>
            <span class="tag">${escapeHtml(item.status)}</span>
          </div>
          <h3>${escapeHtml(item.name)}</h3>
          <p>${escapeHtml(item.scope)}</p>
          <p><strong>资料路线：</strong>${escapeHtml(item.source_strategy)}</p>
          <p><strong>风险边界：</strong>${escapeHtml(item.risk_notes)}</p>
          <div class="tag-row">${item.core_objects.map((term) => `<span class="tag">${escapeHtml(term)}</span>`).join("")}</div>
          <div class="score-grid">
            <div>
              <strong>产品模块</strong>
              <span>${escapeHtml(String(item.product_modules.length))}</span>
            </div>
            <div>
              <strong>下一步</strong>
              <span>${escapeHtml(String(item.next_steps.length))}</span>
            </div>
          </div>
        </article>
      `,
    )
    .join("")}</div>`;
}

function renderSources() {
  const query = state.query.trim();
  const sources = state.data.sources.filter((source) => matchText(source, query));
  els.content.innerHTML = `<div class="result-grid">${sources
    .map(
      (source) => `
        <article class="card">
          <div class="meta-row">
            <span class="source-class class-${escapeHtml(source.class)}">${escapeHtml(source.class)} 类</span>
            <span class="tag">${escapeHtml(source.type)}</span>
          </div>
          <h3>${escapeHtml(source.title)}</h3>
          <p>${escapeHtml(source.notes)}</p>
          <a href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(source.url)}</a>
        </article>
      `,
    )
    .join("")}</div>`;
}

function renderCaseForm() {
  els.content.innerHTML = `
    <div class="two-column">
      <article class="article">
        <h3>案例录入</h3>
        <p>案例只保存在浏览器表单里。点击导出案例会生成 JSON 文件，适合后续进入案例库。</p>
        <form id="caseForm" class="form-grid">
          <label class="form-field is-wide">问题
            <textarea name="question" required placeholder="例如：本周五面试能否进入下一轮？"></textarea>
          </label>
          <label class="form-field">专题
            <select name="topic">
              <option value="career">事业</option>
              <option value="wealth">财运</option>
              <option value="relationship">感情</option>
              <option value="exam">考试</option>
              <option value="health">健康</option>
              <option value="lost_object">失物</option>
              <option value="travel">出行</option>
              <option value="lawsuit">官司</option>
              <option value="other">其他</option>
            </select>
          </label>
          <label class="form-field">起卦时间
            <input name="cast_time" type="datetime-local" />
          </label>
          <label class="form-field">本卦
            <input name="primary" placeholder="例如：风火家人" />
          </label>
          <label class="form-field">变卦
            <input name="changed" placeholder="例如：山火贲" />
          </label>
          <label class="form-field">主用神
            <input name="main_god" placeholder="例如：官鬼" />
          </label>
          <label class="form-field">动爻
            <input name="moving_lines" placeholder="例如：2,5" />
          </label>
          <label class="form-field is-wide">证据链
            <textarea name="evidence" placeholder="月建、日辰、世应、动变、空破墓绝..."></textarea>
          </label>
          <label class="form-field is-wide">结论
            <textarea name="summary" placeholder="先趋势，再条件，再应期。"></textarea>
          </label>
          <label class="form-field is-wide">反馈
            <textarea name="feedback" placeholder="实际结果和复盘。"></textarea>
          </label>
        </form>
      </article>
      <article class="card">
        <h3>录入标准</h3>
        <p>案例必须保留问题原文、时间范围、用神理由、动变证据和实际反馈。没有反馈的卦例只能作练习，不能升级为强规则。</p>
        <button class="ghost-button" id="useCasterButton" type="button">打开装卦辅助</button>
        <div class="tag-row">
          <span class="tag">case_schema.json</span>
          <span class="tag">反馈优先</span>
          <span class="tag">证据链</span>
        </div>
      </article>
    </div>
  `;
  document.querySelector("#useCasterButton")?.addEventListener("click", () => setView("caster"));
}

function currentCasePayload() {
  const form = document.querySelector("#caseForm");
  if (!form) return null;
  const data = Object.fromEntries(new FormData(form).entries());
  const moving = data.moving_lines
    ? data.moving_lines
        .split(",")
        .map((item) => Number(item.trim()))
        .filter(Boolean)
    : [];
  return {
    id: `case-${new Date().toISOString().slice(0, 10)}-draft`,
    question: data.question || "",
    topic: data.topic || "other",
    cast_time: data.cast_time || new Date().toISOString(),
    hexagram: {
      primary: data.primary || "",
      changed: data.changed || "",
      moving_lines: moving,
    },
    use_gods: {
      main: data.main_god || "",
    },
    judgment: {
      summary: data.summary || "",
      evidence: data.evidence ? data.evidence.split(/\n+/).filter(Boolean) : [],
    },
    feedback: {
      actual_result: data.feedback || "",
    },
    derived_chart: currentCasterChart(),
  };
}

function exportCase() {
  const payload = currentCasePayload();
  if (!payload) {
    setView("case");
    return;
  }
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `${payload.id}.json`;
  anchor.click();
  URL.revokeObjectURL(url);
}

function copyCurrentView() {
  const text = `${location.origin}${location.pathname}#${state.view}`;
  navigator.clipboard?.writeText(text);
  els.copyLink.textContent = "已复制";
  setTimeout(() => {
    els.copyLink.textContent = "复制当前视图";
  }, 1200);
}

function render() {
  if (!state.data) return;
  if (state.query && state.view === "learn") {
    setView("search");
    return;
  }
  if (state.view === "learn") renderLearn();
  if (state.view === "systems") renderSystems();
  if (state.view === "search") renderSearch();
  if (state.view === "rules") renderRules();
  if (state.view === "terms") renderTerms();
  if (state.view === "classics") renderClassics();
  if (state.view === "notes") renderNotes();
  if (state.view === "caseIndex") renderCaseIndex();
  if (state.view === "accuracy") renderAccuracy();
  if (state.view === "caster") renderCaster();
  if (state.view === "projects") renderProjects();
  if (state.view === "sources") renderSources();
  if (state.view === "case") renderCaseForm();
}

function bindEvents() {
  els.navButtons.forEach((button) => {
    button.addEventListener("click", () => setView(button.dataset.view));
  });
  els.search.addEventListener("input", (event) => {
    state.query = event.target.value;
    if (state.query) state.view = "search";
    scheduleApiSearch(state.query);
    setView(state.view);
  });
  els.copyLink.addEventListener("click", copyCurrentView);
  els.exportCase.addEventListener("click", exportCase);
}

async function init() {
  if (window.LIUYAO_KB_DATA) {
    state.data = window.LIUYAO_KB_DATA;
  } else {
    const response = await fetch("./assets/kb-data.json");
    state.data = await response.json();
  }
  renderStats();
  renderInspector();
  renderDocList();
  bindEvents();
  const initialHash = location.hash.replace("#", "");
  if (initialHash && viewTitles[initialHash]) state.view = initialHash;
  setView(state.view);
}

init().catch((error) => {
  els.content.innerHTML = `
    <div class="empty-state">
      <h3>数据加载失败</h3>
      <p>${escapeHtml(error.message)}。请先运行 web/scripts/build-data.py，或通过本地服务器打开页面。</p>
    </div>
  `;
});
