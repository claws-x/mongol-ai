import { MongolianSuperEngine, PROFILES } from "../core/mongolian_super_engine.mjs";

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

function run() {
    const inputDocument = engine.createDocument(source.value, profile.value);
    const diagnostics = renderDiagnostics(inputDocument);
    profileNote.textContent = `${PROFILES[profile.value].note} 依据：${PROFILES[profile.value].evidence}`;
    output.replaceChildren();
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
document.querySelector("#copy-source").addEventListener("click", async () => {
    await navigator.clipboard.writeText(source.value);
});

try {
    const report = await engine.init();
    document.querySelector("#engine-version").textContent = report.version;
    document.querySelector("#hb-version").textContent = report.harfbuzz;
    document.querySelector("#font-hash").textContent = report.fontSha256;
    document.querySelector("#override-count").textContent = `${report.approvedOverrides} 条已批准`;
    run();
} catch (error) {
    setStatus("引擎初始化失败", "blocked");
    output.textContent = error.message;
}
