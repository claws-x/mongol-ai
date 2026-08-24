import { MongolianSuperEngine, PROFILES } from "../core/mongolian_super_engine.mjs?v=0.7.0";
import { SemanticGlyphRegistry } from "../core/semantic_glyph_engine.mjs?v=0.7.0";
import { analyzeMongolianLexicalControls } from "../core/mongolian_lexical_controls.mjs?v=0.7.0";

const engine = new MongolianSuperEngine();
const form = document.querySelector("#engine-form");
const profile = document.querySelector("#profile");
const source = document.querySelector("#source-text");
const output = document.querySelector("#deterministic-output");
const status = document.querySelector("#render-status");
const profileNote = document.querySelector("#profile-note");
const codepointBody = document.querySelector("#codepoint-body");
const issueList = document.querySelector("#issue-list");
const roundtrip = document.querySelector("#roundtrip-status");
const imeStatus = document.querySelector("#ime-status");
const imeDetail = document.querySelector("#ime-detail");
const compositionCount = document.querySelector("#composition-count");
const lastCommit = document.querySelector("#last-commit");
const declaredProfile = document.querySelector("#declared-profile");
const semanticBody = document.querySelector("#semantic-body");
const lexicalControlBody = document.querySelector("#lexical-control-body");
let isComposing = false;
let imeEvents = [];
let semanticRegistry = null;

const requestedProfile = new URLSearchParams(window.location.search).get("profile");
if (requestedProfile && Object.hasOwn(PROFILES, requestedProfile)) {
    profile.value = requestedProfile;
}

function codePoints(text) {
    return Array.from(text, (character) => `U+${character.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")}`);
}

function recordImeEvent(type, event) {
    imeEvents.push({
        sequence: imeEvents.length + 1,
        type,
        data: typeof event.data === "string" ? event.data : null,
        inputType: event.inputType || null,
        isComposing: Boolean(event.isComposing),
        codePoints: typeof event.data === "string" ? codePoints(event.data) : [],
    });
    compositionCount.textContent = String(imeEvents.length);
}

function setStatus(text, kind = "") {
    status.textContent = text;
    status.className = `status ${kind}`.trim();
}

function renderDiagnostics(inputDocument) {
    const diagnostics = inputDocument.diagnostics();
    codepointBody.replaceChildren(...inputDocument.tokens.map((token) => {
        const row = document.createElement("tr");
        const values = [
            token.index + 1,
            token.control ? "不可见" : token.character === " " ? "空格" : token.character,
            token.label,
            token.pua ? "私用区" : token.mongolian ? "蒙古文区" : "其他",
            token.control || "—",
        ];
        values.forEach((value) => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });
        return row;
    }));
    issueList.replaceChildren(...diagnostics.issues.map((issue) => {
        const item = document.createElement("li");
        item.textContent = `${issue.level}: ${issue.code}`;
        return item;
    }));
    roundtrip.textContent = diagnostics.roundTripExact ? "原文往返一致" : "原文发生变化";
    roundtrip.className = `status ${diagnostics.roundTripExact ? "ok" : "blocked"}`;
    return diagnostics;
}

function semanticTrace(text) {
    return semanticRegistry ? semanticRegistry.resolveText(text) : [];
}

function renderSemanticTrace(trace) {
    const graphemes = trace.filter((token) => token.type === "mongolian-grapheme");
    semanticBody.replaceChildren(...graphemes.map((token) => {
        const row = document.createElement("tr");
        const values = [
            token.text,
            token.joiningType,
            token.joiningState,
            token.resolution?.semanticRole ?? (token.controls.length ? token.resolution?.status : "基础字母／无 FVS"),
            token.resolution?.backend?.status ?? "由字体后端塑形",
        ];
        values.forEach((value) => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });
        return row;
    }));
}

function lexicalControlEvents(text) {
    return analyzeMongolianLexicalControls(text);
}

function renderLexicalControls(events) {
    lexicalControlBody.replaceChildren(...events.map((event) => {
        const row = document.createElement("tr");
        const values = [
            `${event.controlName} (${event.control})`,
            event.kind,
            event.leftSequence.join(" ") || "—",
            event.rightSequence.join(" ") || "—",
            event.semanticStatus,
        ];
        values.forEach((value) => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });
        return row;
    }));
}

function run() {
    const inputDocument = engine.createDocument(source.value, profile.value);
    const diagnostics = renderDiagnostics(inputDocument);
    renderSemanticTrace(semanticTrace(inputDocument.raw));
    renderLexicalControls(lexicalControlEvents(inputDocument.raw));
    profileNote.textContent = `${PROFILES[profile.value].note} 依据：${PROFILES[profile.value].evidence}`;
    declaredProfile.textContent = PROFILES[profile.value].label;
    output.replaceChildren();
    if (!inputDocument.raw) {
        const message = document.createElement("p");
        message.textContent = "等待系统输入法提交文本。";
        output.appendChild(message);
        setStatus("等待输入");
        return;
    }
    if (!diagnostics.canShape) {
        const message = document.createElement("p");
        message.textContent = "已无损保存原文，但当前编码缺少权威映射，系统拒绝猜测塑形。";
        output.appendChild(message);
        setStatus("阻止猜测转换", "blocked");
        return;
    }
    try {
        engine.renderAccessible(output, inputDocument, { fontSize: 56, padding: 20 });
        setStatus("锁定塑形完成", "ok");
    } catch (error) {
        const message = document.createElement("p");
        message.textContent = `塑形失败：${error.message}`;
        output.appendChild(message);
        setStatus("塑形失败", "blocked");
    }
}

form.addEventListener("submit", (event) => { event.preventDefault(); run(); });
profile.addEventListener("change", run);
source.addEventListener("compositionstart", (event) => {
    isComposing = true;
    recordImeEvent("compositionstart", event);
    imeStatus.textContent = "候选组合中";
    imeStatus.className = "status blocked";
    imeDetail.textContent = "暂不塑形、不规范化、不改写输入框。";
});
source.addEventListener("compositionupdate", (event) => {
    recordImeEvent("compositionupdate", event);
    imeDetail.textContent = `候选内容 ${codePoints(event.data || "").join(" ") || "—"}`;
});
source.addEventListener("compositionend", (event) => {
    recordImeEvent("compositionend", event);
    isComposing = false;
    imeStatus.textContent = "候选已提交";
    imeStatus.className = "status ok";
    lastCommit.textContent = `${event.data || "空提交"} · ${codePoints(event.data || "").join(" ") || "无新增码位"}`;
    imeDetail.textContent = "已按输入框最终值重新塑形；原始文本保持不变。";
    run();
});
source.addEventListener("beforeinput", (event) => recordImeEvent("beforeinput", event));
source.addEventListener("input", (event) => {
    recordImeEvent("input", event);
    if (!isComposing && !event.isComposing) run();
});
document.querySelector("#copy-source").addEventListener("click", async () => {
    await navigator.clipboard.writeText(source.value);
});
document.querySelector("#export-evidence").addEventListener("click", () => {
    const inputDocument = engine.createDocument(source.value, profile.value);
    const evidence = {
        schemaVersion: "1.0.0",
        exportedAt: new Date().toISOString(),
        declaredProfile: profile.value,
        browserCannotIdentifySystemIme: true,
        raw: inputDocument.raw,
        codePoints: inputDocument.tokens.map((token) => token.label),
        diagnostics: inputDocument.diagnostics(),
        semanticTrace: semanticTrace(inputDocument.raw),
        lexicalControlEvents: lexicalControlEvents(inputDocument.raw),
        events: imeEvents,
        engine: engine.report(),
    };
    const blob = new Blob([JSON.stringify(evidence, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `mongol-ime-evidence-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(link.href);
});

try {
    const [report, registryResponse] = await Promise.all([
        engine.init(),
        fetch(new URL("../data/engine/s2-semantic-registry.json?v=0.7.0", import.meta.url)),
    ]);
    if (!registryResponse.ok) throw new Error(`semantic registry HTTP ${registryResponse.status}`);
    semanticRegistry = new SemanticGlyphRegistry(await registryResponse.json());
    document.querySelector("#engine-version").textContent = report.version;
    document.querySelector("#hb-version").textContent = report.harfbuzz;
    document.querySelector("#font-hash").textContent = report.fontSha256;
    document.querySelector("#override-count").textContent = `${report.approvedOverrides} 条已批准`;
    run();
    window.dispatchEvent(new CustomEvent("mongol-engine-ready"));
} catch (error) {
    setStatus("引擎初始化失败", "blocked");
    output.textContent = error.message;
    window.dispatchEvent(new CustomEvent("mongol-engine-failed", { detail: error.message }));
}
