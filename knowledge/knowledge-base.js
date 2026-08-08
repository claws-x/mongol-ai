"use strict";

const DATA_URL = "../data/knowledge/knowledge-base.json";

const TYPE_CONFIG = [
    { key: "all", label: "全部" },
    { key: "institutions", label: "机构" },
    { key: "people", label: "研究者" },
    { key: "publications", label: "论文" },
    { key: "resources", label: "资源" },
    { key: "standards", label: "标准" },
    { key: "sources", label: "来源" }
];

const state = { data: null, type: "all", query: "", script: "all" };

const byId = (id) => document.getElementById(id);

function element(tag, options = {}) {
    const node = document.createElement(tag);
    if (options.className) node.className = options.className;
    if (options.text !== undefined) node.textContent = options.text;
    if (options.href) {
        node.href = options.href;
        node.target = "_blank";
        node.rel = "noopener noreferrer";
    }
    return node;
}

function labelForStatus(status) {
    return {
        verified: "已核验",
        provisional: "待补证",
        rejected: "已拒绝"
    }[status] || status;
}

function flattenRecords(data) {
    const records = [];
    for (const config of TYPE_CONFIG.slice(1)) {
        for (const item of data[config.key]) {
            records.push({ ...item, entity_type: config.key });
        }
    }
    return records;
}

function recordTitle(record) {
    return record.title || record.name || record.id;
}

function recordKind(record) {
    if (record.entity_type === "institutions") return `${record.region} · ${record.kind}`;
    if (record.entity_type === "people") return record.roles.join(" · ");
    if (record.entity_type === "publications") return `${record.year} · ${record.venue} · ${record.publication_status}`;
    if (record.entity_type === "resources") return `${record.resource_type} · ${record.availability}`;
    if (record.entity_type === "standards") return `${record.owner} · ${record.normative_status}`;
    if (record.entity_type === "sources") return `${record.publisher} · Tier ${record.tier}`;
    return record.entity_type;
}

function recordTags(record) {
    return record.focus || record.topics || record.script_scope || [record.source_type].filter(Boolean);
}

function recordSummary(record, institutionMap) {
    if (record.evidence_summary) return record.evidence_summary;
    if (record.scope) return record.scope;
    if (record.notes) return record.notes;
    if (record.note) return record.note;
    if (record.entity_type === "people") {
        const affiliations = record.affiliation_ids.map((id) => institutionMap.get(id)?.name).filter(Boolean);
        return affiliations.length ? `公开机构关系：${affiliations.join("、")}` : "当前来源只证明其公开贡献，未推断机构关系。";
    }
    if (record.entity_type === "institutions") return `研究方向：${record.focus.join("、")}`;
    if (record.entity_type === "resources") return `维护者：${record.maintainer}；许可状态：${record.license_status}`;
    return "";
}

function matches(record) {
    if (state.type !== "all" && record.entity_type !== state.type) return false;
    if (state.script !== "all") {
        const scopes = record.script_scope || [];
        if (!scopes.includes(state.script)) return false;
    }
    if (!state.query) return true;
    const searchable = JSON.stringify(record).toLocaleLowerCase("zh-CN");
    return searchable.includes(state.query);
}

function renderMetrics() {
    const metricDefinitions = [
        ["sources", "可信来源"],
        ["institutions", "机构/团队"],
        ["people", "研究者"],
        ["publications", "研究成果"],
        ["resources", "数据/工具"],
        ["standards", "标准"]
    ];
    const container = byId("metrics");
    container.replaceChildren();
    for (const [key, label] of metricDefinitions) {
        const card = element("div", { className: "metric" });
        card.append(element("strong", { text: String(state.data[key].length) }));
        card.append(element("span", { text: label }));
        container.append(card);
    }
}

function renderTabs() {
    const container = byId("type-tabs");
    container.replaceChildren();
    for (const config of TYPE_CONFIG) {
        const count = config.key === "all"
            ? flattenRecords(state.data).length
            : state.data[config.key].length;
        const button = element("button", {
            className: "type-tab",
            text: `${config.label} ${count}`
        });
        button.type = "button";
        button.dataset.type = config.key;
        button.setAttribute("aria-pressed", String(state.type === config.key));
        button.addEventListener("click", () => {
            state.type = config.key;
            renderTabs();
            renderRecords();
        });
        container.append(button);
    }
}

function addSources(card, record, sourceMap) {
    const ids = record.entity_type === "sources" ? [record.id] : (record.source_ids || []);
    if (!ids.length) return;
    const section = element("div", { className: "sources" });
    section.append(element("span", { className: "sources-label", text: "原始证据" }));
    for (const sourceId of ids) {
        const source = sourceMap.get(sourceId);
        if (!source) continue;
        section.append(element("a", {
            className: "source-link",
            text: source.title,
            href: source.url
        }));
    }
    card.append(section);
}

function renderRecords() {
    const sourceMap = new Map(state.data.sources.map((source) => [source.id, source]));
    const institutionMap = new Map(state.data.institutions.map((institution) => [institution.id, institution]));
    const records = flattenRecords(state.data).filter(matches);
    const container = byId("cards");
    container.replaceChildren();

    byId("result-state").textContent = `显示 ${records.length} 条记录`;
    const activeLabel = TYPE_CONFIG.find((item) => item.key === state.type)?.label || "全部";
    byId("results-title").textContent = `${activeLabel}可信记录`;

    if (!records.length) {
        container.append(element("p", {
            className: "empty",
            text: "没有符合当前条件的记录。清除搜索词或切换文字系统后重试。"
        }));
        return;
    }

    for (const record of records) {
        const card = element("article", { className: "card" });
        const top = element("div", { className: "card-top" });
        const heading = element("div");
        heading.append(element("h3", { text: recordTitle(record) }));
        heading.append(element("p", { className: "kind", text: recordKind(record) }));
        top.append(heading);

        const status = record.verification || (record.tier === "A" ? "verified" : "provisional");
        top.append(element("span", {
            className: `status ${status}`,
            text: labelForStatus(status)
        }));
        card.append(top);

        const tags = element("div", { className: "tags" });
        const scopes = record.script_scope || [];
        for (const tag of [...recordTags(record), ...scopes].slice(0, 8)) {
            tags.append(element("span", { className: "tag", text: tag }));
        }
        card.append(tags);

        const summary = recordSummary(record, institutionMap);
        if (summary) card.append(element("p", { className: "summary", text: summary }));
        addSources(card, record, sourceMap);
        container.append(card);
    }
}

function renderGaps() {
    const list = byId("known-gaps");
    list.replaceChildren();
    for (const gap of state.data.coverage.known_gaps) {
        list.append(element("li", { text: gap }));
    }
    byId("next-review").textContent = `下次计划复核：${state.data.coverage.next_review_at}`;
}

function bindControls() {
    byId("search").addEventListener("input", (event) => {
        state.query = event.target.value.trim().toLocaleLowerCase("zh-CN");
        renderRecords();
    });
    byId("script-filter").addEventListener("change", (event) => {
        state.script = event.target.value;
        renderRecords();
    });
}

async function initialize() {
    try {
        const response = await fetch(DATA_URL, { cache: "no-store" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        state.data = await response.json();
        renderMetrics();
        renderTabs();
        renderRecords();
        renderGaps();
        bindControls();
        byId("updated-at").textContent = state.data.updated_at;
    } catch (error) {
        byId("result-state").textContent = "知识库加载失败";
        byId("cards").append(element("p", {
            className: "empty",
            text: `无法加载机器可读事实源：${error.message}`
        }));
    }
}

document.addEventListener("DOMContentLoaded", initialize);
