"use strict";

const DRAFT_KEY = "mongol-ai.workspace.draft.v1";
const EMPTY_PREVIEW = "ᠮᠣᠩᠭᠣᠯ ᠪᠢᠴᠢᠭ";
const inspector = new MongolAI.TextInspector();

const input = document.getElementById("input");
const preview = document.getElementById("live-preview");
const conversation = document.getElementById("conversation");
const emptyState = document.getElementById("empty-state");
const diagnosticList = document.getElementById("diagnostic-list");
const corpusState = document.getElementById("corpus-state");
const draftState = document.getElementById("draft-state");
const responses = new Map([
    ["ᠰᠠᠶᠢᠨ", ["ᠰᠠᠶᠢᠨ ᠪᠠᠶᠢᠨ᠎ᠠ᠃", "ᠮᠡᠨᠳᠡ᠃"]],
    ["ᠪᠠᠶᠠᠷᠲᠠᠢ", ["ᠪᠠᠶᠠᠷᠲᠠᠢ᠃"]],
]);
const fallbackResponse = "ᠡᠨᠡ ᠪᠣᠯ ᠳᠦᠷᠢᠮ ᠳᠦ ᠰᠠᠭᠤᠷᠢᠯᠠᠭᠰᠠᠨ ᠲᠤᠷᠰᠢᠯᠲᠠ ᠪᠣᠯᠣᠨ᠎ᠠ᠃";
let saveTimer = null;

function insertAtCursor(value) {
    const start = input.selectionStart;
    const end = input.selectionEnd;
    input.setRangeText(value, start, end, "end");
    input.focus();
    updateWorkspace();
}

function previousGraphemeBoundary(value, cursor) {
    const prefix = value.slice(0, cursor);
    let boundary = 0;
    if (typeof Intl.Segmenter === "function") {
        const segments = new Intl.Segmenter("mn", { granularity: "grapheme" }).segment(prefix);
        for (const segment of segments) boundary = segment.index;
        return boundary;
    }

    const previous = Array.from(prefix).pop() || "";
    boundary = cursor - previous.length;
    if (/[\u180B-\u180D\u180F]/u.test(previous) && boundary > 0) {
        boundary -= (Array.from(value.slice(0, boundary)).pop() || "").length;
    }
    return boundary;
}

function deletePreviousCharacter() {
    const start = input.selectionStart;
    const end = input.selectionEnd;
    if (start !== end) {
        input.setRangeText("", start, end, "end");
    } else if (start > 0) {
        input.setRangeText("", previousGraphemeBoundary(input.value, start), start, "end");
    }
    input.focus();
    updateWorkspace();
}

function createMessage(speaker, text) {
    const message = document.createElement("article");
    message.className = "message";
    message.dataset.speaker = speaker;

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = speaker === "user" ? "你的输入" : "规则响应";

    const content = document.createElement("div");
    content.className = "mongolian-text";
    content.lang = "mn-Mong";
    content.setAttribute("data-mongol-vertical", "");
    content.textContent = text;

    message.append(label, content);
    return message;
}

function getResponse(text) {
    for (const [keyword, choices] of responses.entries()) {
        if (text.includes(keyword)) return choices[Math.floor(Math.random() * choices.length)];
    }
    return fallbackResponse;
}

function send() {
    const text = input.value.replace(/^[\u0009-\u000D\u0020]+|[\u0009-\u000D\u0020]+$/gu, "");
    if (!text) {
        input.focus();
        return;
    }

    emptyState?.remove();
    conversation.append(createMessage("user", text));
    conversation.append(createMessage("assistant", getResponse(text)));
    input.value = "";
    input.focus();
    conversation.scrollLeft = conversation.scrollWidth;
    updateWorkspace();
}

function setMetric(name, value) {
    document.querySelector(`[data-metric="${name}"]`).textContent = String(value);
}

function appendDiagnostic(level, message) {
    const item = document.createElement("li");
    item.dataset.level = level;
    item.textContent = message;
    diagnosticList.appendChild(item);
}

function renderDiagnostics(result) {
    diagnosticList.replaceChildren();
    setMetric("codePoints", result.stats.codePoints);
    setMetric("words", result.stats.words);
    setMetric("mongolian", result.stats.mongolian);
    setMetric("controls", result.stats.controls);

    for (const issue of result.issues) appendDiagnostic(issue.level, issue.message);
    if (result.controls.length) {
        const points = result.controls.map((item) => item.codePoint).join("、");
        appendDiagnostic("info", `检测到格式控制字符：${points}。复制、保存和预览均保留原始编码。`);
    }
    if (result.matchedCases.length) {
        const ids = result.matchedCases.slice(0, 5).map((item) => item.id).join("、");
        appendDiagnostic("info", `匹配 Unicode 编码基线：${ids}${result.matchedCases.length > 5 ? "…" : ""}。字形与语言用法仍需专家审核。`);
    }
    if (!result.issues.length && !result.controls.length && !result.matchedCases.length) {
        appendDiagnostic("success", input.value ? "未发现编码级阻断问题；这不代表拼写或语言用法已经审核。" : "输入蒙古文后显示编码诊断。 ");
    }
}

function queueDraftSave(text) {
    globalThis.clearTimeout(saveTimer);
    saveTimer = globalThis.setTimeout(() => {
        try {
            if (text) {
                localStorage.setItem(DRAFT_KEY, text);
                draftState.textContent = "草稿已保存在此浏览器";
            } else {
                localStorage.removeItem(DRAFT_KEY);
                draftState.textContent = "暂无本地草稿";
            }
        } catch {
            draftState.textContent = "浏览器禁止本地草稿保存";
        }
    }, 250);
}

function updateWorkspace() {
    const text = input.value;
    preview.textContent = text || EMPTY_PREVIEW;
    preview.dataset.empty = String(!text);
    renderDiagnostics(inspector.analyze(text));
    queueDraftSave(text);
}

async function copyDraft() {
    const text = input.value;
    if (!text) return;
    try {
        await navigator.clipboard.writeText(text);
    } catch {
        const helper = document.createElement("textarea");
        helper.value = text;
        helper.setAttribute("readonly", "");
        helper.style.position = "fixed";
        helper.style.opacity = "0";
        document.body.appendChild(helper);
        helper.select();
        document.execCommand("copy");
        helper.remove();
    }
    draftState.textContent = "已复制原始 Unicode 文本";
}

function downloadDraft() {
    if (!input.value) return;
    const blob = new Blob([input.value], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `mongol-ai-${new Date().toISOString().slice(0, 10)}.txt`;
    link.click();
    URL.revokeObjectURL(link.href);
    draftState.textContent = "已导出 UTF-8 文本";
}

function restoreDraft() {
    try {
        const saved = localStorage.getItem(DRAFT_KEY);
        if (saved) {
            input.value = saved;
            draftState.textContent = "已恢复此浏览器中的草稿";
        }
    } catch {
        draftState.textContent = "浏览器禁止本地草稿读取";
    }
}

document.querySelectorAll("[data-char]").forEach((button) => {
    button.addEventListener("click", () => insertAtCursor(button.dataset.char));
});

document.querySelectorAll("[data-group]").forEach((tab) => {
    tab.addEventListener("click", () => {
        document.querySelectorAll("[data-group]").forEach((item) => {
            item.setAttribute("aria-selected", String(item === tab));
        });
        document.querySelectorAll("[data-key-panel]").forEach((panel) => {
            panel.hidden = panel.dataset.keyPanel !== tab.dataset.group;
        });
    });
});

document.getElementById("clear-button").addEventListener("click", () => {
    input.value = "";
    input.focus();
    updateWorkspace();
});
document.getElementById("delete-button").addEventListener("click", deletePreviousCharacter);
document.getElementById("send-button").addEventListener("click", send);
document.getElementById("copy-button").addEventListener("click", copyDraft);
document.getElementById("download-button").addEventListener("click", downloadDraft);
input.addEventListener("input", updateWorkspace);
input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        send();
    }
});

document.addEventListener("mongolai:vertical-ready", (event) => {
    const state = document.getElementById("engine-state");
    const { mode, fontReady } = event.detail;
    const modeLabel = mode === "native" ? "原生竖排" : mode === "compat" ? "兼容竖排" : "降级显示";
    state.textContent = `Mongol AI Engine · ${modeLabel}${fontReady ? "" : " · 字体回退"}`;
});

restoreDraft();
updateWorkspace();
inspector.loadCorpus("../../data/quality/mongolian-unicode-cases.json")
    .then((meta) => {
        corpusState.textContent = `Unicode ${meta.unicodeVersion} · ${meta.caseCount} 条编码基线`;
        updateWorkspace();
    })
    .catch(() => {
        corpusState.textContent = "编码基线暂时无法加载";
    });
