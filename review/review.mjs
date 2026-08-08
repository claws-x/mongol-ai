import {
    LosslessMongolianDocument,
    MongolianSuperEngine,
    PROFILES,
} from "../core/mongolian_super_engine.mjs";

const DB_NAME = "mongol-ai-s1";
const STORE = "records";
const PROFILE_MAP = {
    unicode_national: "unicode-national",
    onon_mn: "onon-mn",
    onon_mk: "onon-mk",
    onon_mw: "onon-mw",
    menksoft_raw: "menksoft-raw",
};
const EXPERT_ROLES = new Set(["native_speaker", "font_engineer", "publisher"]);
const STATUS_LABELS = {
    captured: "待审核",
    machine_verified: "机器已核验",
    linguist_verified: "人工已核验",
    approved: "已批准",
    rejected: "已拒绝",
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));
const now = () => new Date().toISOString();
const clone = (value) => structuredClone(value);

let tasks = [];
let records = new Map();
let currentTask = null;
let currentRecord = null;
let lockedEngine = null;
let lockedShape = null;
let referenceEngine = null;
let referenceFontName = null;
let selectedGlyphIndex = null;
let comparing = 0;
let composing = false;

function emptyRecord(task) {
    const timestamp = now();
    return {
        schema_version: "1.0.0",
        task_id: task.id,
        status: task.status || "captured",
        inputs: {
            unicode_national: task.text || "",
            onon_mn: "",
            onon_mk: "",
            onon_mw: "",
            menksoft_raw: "",
        },
        rendering: { native: {}, locked: {}, reference_font: {} },
        annotations: [],
        review: {
            reviewer: "",
            role: "collector",
            decision: "needs_resolution",
            notes: "",
        },
        reference: {
            image_data_url: null,
            image_name: null,
            font_name: null,
            font_sha256: null,
            ime_version: "",
            font_version: "",
            notes: "",
            onon_not_applicable: false,
        },
        audit: { created_at: timestamp, updated_at: timestamp, history: [] },
    };
}

function openDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, 1);
        request.onupgradeneeded = () => {
            if (!request.result.objectStoreNames.contains(STORE)) {
                request.result.createObjectStore(STORE, { keyPath: "task_id" });
            }
        };
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

async function dbRequest(mode, operation) {
    const db = await openDatabase();
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(STORE, mode);
        const request = operation(transaction.objectStore(STORE));
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
        transaction.oncomplete = () => db.close();
    });
}

const getAllRecords = () => dbRequest("readonly", (store) => store.getAll());
const putRecord = (record) => dbRequest("readwrite", (store) => store.put(record));

function setText(selector, value) {
    $(selector).textContent = value ?? "";
}

function statusFor(task) {
    return records.get(task.id)?.status || task.status || "captured";
}

function renderMetrics() {
    const counts = Object.fromEntries(Object.keys(STATUS_LABELS).map((key) => [key, 0]));
    tasks.forEach((task) => counts[statusFor(task)] += 1);
    const items = [
        [tasks.length, "总任务"],
        [counts.captured, "待审核"],
        [counts.machine_verified, "机器核验"],
        [counts.linguist_verified, "人工核验"],
        [counts.approved, "批准"],
        [counts.rejected, "拒绝"],
    ];
    const container = $("#metrics");
    container.replaceChildren(...items.map(([count, label]) => {
        const box = document.createElement("div");
        box.className = "metric";
        const strong = document.createElement("strong");
        strong.textContent = String(count);
        const span = document.createElement("span");
        span.textContent = label;
        box.append(strong, span);
        return box;
    }));
}

function renderTaskList() {
    const filter = $("#status-filter").value;
    const query = $("#task-search").value.trim().toLowerCase();
    const visible = tasks.filter((task) => {
        const haystack = [task.id, task.category, ...(task.code_points || [])].join(" ").toLowerCase();
        return (filter === "all" || statusFor(task) === filter) && (!query || haystack.includes(query));
    });
    const list = $("#task-list");
    list.replaceChildren(...visible.map((task) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = `task${task.id === currentTask?.id ? " active" : ""}`;
        const strong = document.createElement("strong");
        strong.textContent = `${task.id} · ${task.text || "自定义"}`;
        const small = document.createElement("small");
        small.textContent = `${task.category} · ${STATUS_LABELS[statusFor(task)]}`;
        button.append(strong, small);
        button.addEventListener("click", () => selectTask(task));
        return button;
    }));
}

function fillForm(record) {
    $$('[data-input-profile]').forEach((field) => {
        field.value = record.inputs[field.dataset.inputProfile] || "";
    });
    $("#onon-not-applicable").checked = record.reference.onon_not_applicable;
    $("#ime-version").value = record.reference.ime_version || "";
    $("#font-version").value = record.reference.font_version || "";
    $("#reference-notes").value = record.reference.notes || "";
    $("#reviewer").value = record.review.reviewer || "";
    $("#reviewer-role").value = record.review.role || "collector";
    $("#decision").value = record.review.decision || "needs_resolution";
    $("#target-status").value = record.status || "captured";
    $("#review-notes").value = record.review.notes || "";
}

function readForm() {
    $$('[data-input-profile]').forEach((field) => {
        currentRecord.inputs[field.dataset.inputProfile] = field.value;
    });
    Object.assign(currentRecord.reference, {
        onon_not_applicable: $("#onon-not-applicable").checked,
        ime_version: $("#ime-version").value.trim(),
        font_version: $("#font-version").value.trim(),
        notes: $("#reference-notes").value.trim(),
    });
    Object.assign(currentRecord.review, {
        reviewer: $("#reviewer").value.trim(),
        role: $("#reviewer-role").value,
        decision: $("#decision").value,
        notes: $("#review-notes").value.trim(),
    });
}

async function selectTask(task) {
    currentTask = task;
    currentRecord = clone(records.get(task.id) || emptyRecord(task));
    referenceEngine = null;
    referenceFontName = null;
    selectedGlyphIndex = null;
    setText("#task-priority", task.priority || "CUSTOM");
    setText("#task-title", `${task.id} · ${task.category}`);
    const source = $("#task-source");
    source.replaceChildren();
    if (task.source?.url) {
        const link = document.createElement("a");
        link.href = task.source.url;
        link.target = "_blank";
        link.rel = "noreferrer";
        link.textContent = `${task.code_points.join(" ")} · 官方来源`;
        source.append(link);
    } else {
        source.textContent = (task.code_points || []).join(" ");
    }
    fillForm(currentRecord);
    renderTaskList();
    renderAnnotations();
    setText("#save-status", "本地记录载入完成；未保存的更改不会改变队列状态。");
    await compare();
}

function renderDiagnostics() {
    const strip = $("#input-diagnostics");
    strip.replaceChildren(...$$('[data-input-profile]').map((field) => {
        const profile = PROFILE_MAP[field.dataset.inputProfile];
        const doc = new LosslessMongolianDocument(field.value, profile);
        const diagnostic = doc.diagnostics();
        const span = document.createElement("span");
        const flags = [];
        if (diagnostic.controls.length) flags.push(`${diagnostic.controls.length} 控制符`);
        if (diagnostic.pua.length) flags.push(`${diagnostic.pua.length} PUA`);
        if (!diagnostic.canShape) flags.push("禁止猜测塑形");
        span.textContent = `${PROFILES[profile].label}: ${diagnostic.codePointCount} 码位${flags.length ? ` · ${flags.join(" · ")}` : ""}`;
        return span;
    }));
}

function renderCodepoints(documentModel) {
    const body = $("#codepoint-table");
    body.replaceChildren(...documentModel.tokens.map((token) => {
        const row = document.createElement("tr");
        const values = [token.character || "∅", token.label, token.pua ? "PUA" : token.mongolian ? "Mongolian" : "其他", token.control || "—"];
        values.forEach((value) => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.append(cell);
        });
        return row;
    }));
}

function chooseGlyph(index) {
    selectedGlyphIndex = Number(index);
    $("#locked-output").querySelectorAll("[data-glyph-index]").forEach((path) => {
        path.classList.toggle("glyph-selected", Number(path.dataset.glyphIndex) === selectedGlyphIndex);
    });
    $("#glyph-table").querySelectorAll("tr[data-selectable]").forEach((row) => {
        row.classList.toggle("selected", Number(row.dataset.glyphIndex) === selectedGlyphIndex);
    });
    const glyph = lockedShape?.glyphs[selectedGlyphIndex];
    setText("#selected-glyph", glyph ? `glyph #${selectedGlyphIndex} · ID ${glyph.id} · cluster ${glyph.cluster}` : "尚未选择 glyph");
}

function renderGlyphs(shape) {
    const body = $("#glyph-table");
    body.replaceChildren(...shape.glyphs.map((glyph, index) => {
        const row = document.createElement("tr");
        row.dataset.selectable = "true";
        row.dataset.glyphIndex = String(index);
        [index, glyph.id, glyph.cluster, glyph.xAdvance].forEach((value) => {
            const cell = document.createElement("td");
            cell.textContent = String(value);
            row.append(cell);
        });
        row.addEventListener("click", () => chooseGlyph(index));
        return row;
    }));
}

async function compare() {
    if (!currentRecord || !lockedEngine) return;
    readForm();
    const ticket = ++comparing;
    const raw = currentRecord.inputs.unicode_national;
    const documentModel = lockedEngine.createDocument(raw, "unicode-national");
    $("#native-output").textContent = raw;
    renderDiagnostics();
    renderCodepoints(documentModel);
    selectedGlyphIndex = null;
    try {
        lockedShape = lockedEngine.shape(documentModel);
        if (lockedShape.status !== "shaped") throw new Error(lockedShape.reason);
        $("#locked-output").innerHTML = lockedEngine.renderSvg(lockedShape, { fontSize: 52 });
        renderGlyphs(lockedShape);
        const report = lockedEngine.report();
        setText("#locked-meta", `HarfBuzz ${report.harfbuzz} · SHA-256 ${report.fontSha256} · ${lockedShape.glyphs.length} glyph`);
        currentRecord.rendering.locked = {
            status: lockedShape.status,
            glyph_ids: lockedShape.glyphs.map((glyph) => glyph.id),
            clusters: lockedShape.glyphs.map((glyph) => glyph.cluster),
            font_sha256: report.fontSha256,
            font_locked: report.fontLocked,
            harfbuzz: report.harfbuzz,
        };
        currentRecord.rendering.native = { text: raw, css_writing_mode: "vertical-lr" };
        if (referenceEngine) {
            const referenceShape = referenceEngine.shape(referenceEngine.createDocument(raw, "unicode-national"));
            $("#reference-output").innerHTML = referenceEngine.renderSvg(referenceShape, { fontSize: 52 });
            const referenceReport = referenceEngine.report();
            currentRecord.rendering.reference_font = {
                glyph_ids: referenceShape.glyphs.map((glyph) => glyph.id),
                clusters: referenceShape.glyphs.map((glyph) => glyph.cluster),
                font_sha256: referenceReport.fontSha256,
                session_only: true,
            };
            currentRecord.reference.font_name = referenceFontName;
            currentRecord.reference.font_sha256 = referenceReport.fontSha256;
            setText("#reference-meta", `${referenceFontName} · SHA-256 ${referenceReport.fontSha256} · 会话内`);
        } else {
            renderReferenceImage();
        }
        if (ticket === comparing) setText("#compare-status", "三路证据已刷新");
    } catch (error) {
        lockedShape = null;
        $("#locked-output").replaceChildren();
        $("#glyph-table").replaceChildren();
        setText("#locked-meta", error.message);
        setText("#compare-status", "当前 Unicode 输入无法塑形");
    }
    renderGates();
}

function renderReferenceImage() {
    const output = $("#reference-output");
    output.replaceChildren();
    if (currentRecord.reference.image_data_url) {
        const image = document.createElement("img");
        image.className = "reference-image";
        image.alt = `参考字形截图：${currentRecord.reference.image_name || "未命名"}`;
        image.src = currentRecord.reference.image_data_url;
        output.append(image);
        setText("#reference-meta", `${currentRecord.reference.image_name} · 已写入本地证据记录`);
    } else {
        const span = document.createElement("span");
        span.textContent = "等待参考字体或截图";
        output.append(span);
        setText("#reference-meta", "");
    }
}

function gateResults(target = $("#target-status").value) {
    readForm();
    const machine = Boolean(
        currentRecord.inputs.unicode_national &&
        lockedShape?.status === "shaped" &&
        currentRecord.rendering.locked.font_locked
    );
    const expert = EXPERT_ROLES.has(currentRecord.review.role);
    const decided = ["correct", "incorrect"].includes(currentRecord.review.decision);
    const screenshot = Boolean(currentRecord.reference.image_data_url);
    const identity = Boolean(currentRecord.review.reviewer);
    const versions = Boolean(currentRecord.reference.ime_version && currentRecord.reference.font_version);
    const onon = Boolean(currentRecord.inputs.onon_mn || currentRecord.reference.onon_not_applicable);
    const notes = Boolean(currentRecord.review.notes);
    const allowedFrom = {
        captured: new Set(["captured"]),
        machine_verified: new Set(["captured", "machine_verified"]),
        linguist_verified: new Set(["machine_verified", "linguist_verified"]),
        approved: new Set(["linguist_verified", "approved"]),
        rejected: new Set(["captured", "machine_verified", "linguist_verified", "rejected"]),
    };
    const rules = target === "captured"
        ? [[Boolean(currentRecord.inputs.unicode_national), "已保存 Unicode 原始输入"]]
        : [[machine, "锁定字体的 HarfBuzz 输出已生成"]];
    rules.unshift([allowedFrom[target].has(currentRecord.status), `状态转换合法：${currentRecord.status} → ${target}`]);
    if (["linguist_verified", "approved"].includes(target)) {
        rules.push([identity, "已记录审核者"], [expert, "角色具备语言／字体／出版审核资格"], [decided, "已给出正确或错误结论"], [screenshot, "已附正确参考截图"], [versions, "已记录输入法与字体版本"]);
    }
    if (target === "approved") {
        rules.push([currentRecord.review.decision === "correct", "结论为正确"], [onon, "已有 Onon MN 样本或有不适用说明"], [notes, "已有审核说明"]);
    }
    if (target === "rejected") {
        rules.splice(0, rules.length, [identity, "已记录审核者"], [currentRecord.review.decision === "incorrect", "结论为错误"], [notes, "已有拒绝原因"]);
    }
    return rules;
}

function renderGates() {
    const rules = gateResults();
    const list = $("#gate-list");
    list.replaceChildren(...rules.map(([pass, label]) => {
        const item = document.createElement("li");
        item.className = pass ? "pass" : "fail";
        item.textContent = `${pass ? "✓" : "✕"} ${label}`;
        return item;
    }));
    const pass = rules.every(([value]) => value);
    setText("#gate-status", pass ? "允许进入目标状态" : "证据不足，禁止升级状态");
    return pass;
}

function renderAnnotations() {
    const list = $("#annotation-list");
    list.replaceChildren(...currentRecord.annotations.map((annotation) => {
        const item = document.createElement("li");
        const text = document.createElement("span");
        text.textContent = `glyph #${annotation.glyph_index} / ID ${annotation.glyph_id} · ${annotation.issue_type} · ${annotation.note}`;
        const remove = document.createElement("button");
        remove.type = "button";
        remove.className = "secondary";
        remove.textContent = "删除";
        remove.addEventListener("click", () => {
            currentRecord.annotations = currentRecord.annotations.filter((item) => item.id !== annotation.id);
            renderAnnotations();
        });
        item.append(text, remove);
        return item;
    }));
}

function addAnnotation() {
    if (selectedGlyphIndex === null || !lockedShape?.glyphs[selectedGlyphIndex]) {
        setText("#save-status", "请先点击 HarfBuzz SVG 字形或 glyph 表格行。");
        return;
    }
    const note = $("#issue-note").value.trim();
    if (!note) {
        setText("#save-status", "标注必须说明预期与实际差异。");
        return;
    }
    const glyph = lockedShape.glyphs[selectedGlyphIndex];
    currentRecord.annotations.push({
        id: crypto.randomUUID(),
        glyph_index: selectedGlyphIndex,
        glyph_id: glyph.id,
        cluster: glyph.cluster,
        issue_type: $("#issue-type").value,
        note,
        created_at: now(),
    });
    $("#issue-note").value = "";
    renderAnnotations();
}

async function save() {
    readForm();
    const target = $("#target-status").value;
    if (!renderGates()) {
        setText("#save-status", `未保存：${target} 的质量闸门未通过。`);
        return;
    }
    const previous = currentRecord.status;
    currentRecord.status = target;
    currentRecord.audit.updated_at = now();
    currentRecord.audit.history.push({ at: currentRecord.audit.updated_at, from: previous, to: target, reviewer: currentRecord.review.reviewer || null });
    await putRecord(clone(currentRecord));
    records.set(currentRecord.task_id, clone(currentRecord));
    renderMetrics();
    renderTaskList();
    setText("#save-status", `已保存到此浏览器 IndexedDB：${currentRecord.task_id} → ${target}`);
}

function exportRecord() {
    readForm();
    currentRecord.audit.updated_at = now();
    const blob = new Blob([`${JSON.stringify(currentRecord, null, 2)}\n`], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${currentRecord.task_id}-evidence.json`;
    link.click();
    URL.revokeObjectURL(url);
}

async function importRecord(file) {
    const payload = JSON.parse(await file.text());
    if (payload.schema_version !== "1.0.0" || typeof payload.task_id !== "string" || !payload.inputs || !payload.review || !payload.reference || !payload.audit) {
        throw new Error("不是有效的 S1 证据包");
    }
    let task = tasks.find((item) => item.id === payload.task_id);
    if (!task) {
        task = {
            id: payload.task_id,
            status: payload.status || "captured",
            priority: "CUSTOM",
            category: "imported_custom",
            text: payload.inputs.unicode_national || "",
            code_points: [],
            source: null,
        };
        tasks.push(task);
        saveCustomTasks();
    }
    await putRecord(payload);
    records.set(payload.task_id, payload);
    renderMetrics();
    await selectTask(task);
    setText("#save-status", `已导入并保存 ${payload.task_id}`);
}

function saveCustomTasks() {
    const custom = tasks.filter((task) => task.priority === "CUSTOM");
    localStorage.setItem("mongol-ai-s1-custom-tasks", JSON.stringify(custom));
}

async function createCustomTask() {
    const id = `s1-custom-${Date.now()}`;
    const task = { id, status: "captured", priority: "CUSTOM", category: "custom_word_or_phrase", text: "", code_points: [], source: null };
    tasks.push(task);
    saveCustomTasks();
    renderMetrics();
    await selectTask(task);
}

function wireEvents() {
    $("#status-filter").addEventListener("change", renderTaskList);
    $("#task-search").addEventListener("input", renderTaskList);
    $("#previous-task").addEventListener("click", () => {
        const index = tasks.findIndex((task) => task.id === currentTask.id);
        selectTask(tasks[(index - 1 + tasks.length) % tasks.length]);
    });
    $("#next-task").addEventListener("click", () => {
        const index = tasks.findIndex((task) => task.id === currentTask.id);
        selectTask(tasks[(index + 1) % tasks.length]);
    });
    $$('textarea, input:not([type="file"]), select').forEach((field) => {
        field.addEventListener("change", () => { if (!composing) compare(); });
    });
    $$('[data-input-profile]').forEach((field) => {
        field.addEventListener("compositionstart", () => { composing = true; });
        field.addEventListener("compositionend", () => { composing = false; compare(); });
        field.addEventListener("input", (event) => { if (!composing && !event.isComposing) compare(); });
    });
    $("#locked-output").addEventListener("click", (event) => {
        const path = event.target.closest?.("[data-glyph-index]");
        if (path) chooseGlyph(path.dataset.glyphIndex);
    });
    $("#add-annotation").addEventListener("click", addAnnotation);
    $("#target-status").addEventListener("change", renderGates);
    $("#save-record").addEventListener("click", save);
    $("#export-record").addEventListener("click", exportRecord);
    $("#import-record").addEventListener("click", () => $("#import-file").click());
    $("#import-file").addEventListener("change", async (event) => {
        try { await importRecord(event.target.files[0]); }
        catch (error) { setText("#save-status", `导入失败：${error.message}`); }
        event.target.value = "";
    });
    $("#new-task").addEventListener("click", createCustomTask);
    $("#reference-image").addEventListener("change", async (event) => {
        const file = event.target.files[0];
        if (!file) return;
        if (file.size > 5 * 1024 * 1024) {
            setText("#save-status", "参考截图超过 5 MB，未载入。");
            return;
        }
        currentRecord.reference.image_data_url = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = () => reject(reader.error);
            reader.readAsDataURL(file);
        });
        currentRecord.reference.image_name = file.name;
        renderReferenceImage();
        renderGates();
    });
    $("#reference-font").addEventListener("change", async (event) => {
        const file = event.target.files[0];
        if (!file) return;
        try {
            referenceEngine = new MongolianSuperEngine({ expectedFontHash: null });
            await referenceEngine.initFromFontBytes(await file.arrayBuffer(), { expectedHash: null, overrides: [] });
            referenceFontName = file.name;
            await compare();
        } catch (error) {
            referenceEngine = null;
            setText("#reference-meta", `参考字体载入失败：${error.message}`);
        }
    });
}

async function init() {
    try {
        const [response, saved] = await Promise.all([
            fetch("../data/quality/s1-review-queue.json"),
            getAllRecords(),
        ]);
        if (!response.ok) throw new Error(`任务队列载入失败：${response.status}`);
        const payload = await response.json();
        tasks = payload.tasks;
        try {
            const custom = JSON.parse(localStorage.getItem("mongol-ai-s1-custom-tasks") || "[]");
            tasks.push(...custom.filter((task) => !tasks.some((item) => item.id === task.id)));
        } catch { localStorage.removeItem("mongol-ai-s1-custom-tasks"); }
        records = new Map(saved.map((record) => [record.task_id, record]));
        lockedEngine = new MongolianSuperEngine();
        await lockedEngine.init();
        wireEvents();
        renderMetrics();
        renderTaskList();
        await selectTask(tasks[0]);
    } catch (error) {
        setText("#task-title", "S1 审核台初始化失败");
        setText("#save-status", error.message);
    }
}

init();
