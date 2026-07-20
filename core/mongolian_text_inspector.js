/**
 * Explainable Unicode diagnostics for Traditional Mongolian text.
 * This module reports encoding facts; it does not claim linguistic correctness.
 */
(function (global) {
    "use strict";

    const MONGOLIAN_BLOCK = /[\u1800-\u18AF]/u;
    const MONGOLIAN_LETTER = /[\u1820-\u18AA]/u;
    const FVS = /[\u180B-\u180D\u180F]/u;
    const FORMAT_CONTROL = /[\u180B-\u180F\u200C\u200D\u202F]/u;

    class MongolianTextInspector {
        constructor() {
            this.corpus = [];
            this.corpusMeta = null;
        }

        async loadCorpus(url) {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Unicode corpus request failed: ${response.status}`);
            const payload = await response.json();
            this.corpus = payload.cases || [];
            this.corpusMeta = {
                unicodeVersion: payload.unicode_version,
                status: payload.status,
                caseCount: payload.case_count,
            };
            return this.corpusMeta;
        }

        analyze(text) {
            const codePoints = Array.from(text);
            const issues = [];
            const controls = [];
            let mongolianCount = 0;
            let letterCount = 0;

            codePoints.forEach((character, index) => {
                if (MONGOLIAN_BLOCK.test(character)) mongolianCount += 1;
                if (MONGOLIAN_LETTER.test(character)) letterCount += 1;
                if (FORMAT_CONTROL.test(character)) {
                    controls.push({ index, character, codePoint: this.formatCodePoint(character) });
                }
                if (FVS.test(character)) {
                    const previous = codePoints[index - 1];
                    if (!previous || !MONGOLIAN_LETTER.test(previous)) {
                        issues.push({
                            level: "error",
                            code: "orphan-fvs",
                            message: `${this.formatCodePoint(character)} 前缺少蒙古文字母，变体选择符不会可靠生效。`,
                        });
                    }
                }
            });

            if (text.includes("�")) {
                issues.push({ level: "error", code: "replacement-character", message: "发现 U+FFFD，文本可能在复制或转码时损坏。" });
            }
            if (text && mongolianCount === 0) {
                issues.push({ level: "warning", code: "no-mongolian", message: "当前文本未包含 Unicode 蒙古文区段字符。" });
            }

            if (text.normalize("NFC") !== text) {
                issues.push({
                    level: "warning",
                    code: "normalization-change",
                    message: "NFC 会改变这段文本；工作台不会自动规范化，请先核对来源。",
                });
            }

            const matchedCases = this.corpus
                .filter((item) => (
                    item.text &&
                    item.category !== "base_character" &&
                    text.includes(item.text)
                ))
                .map((item) => ({
                    id: item.id,
                    text: item.text,
                    category: item.category,
                    encodingStatus: item.review?.encoding || "unreviewed",
                    glyphStatus: item.review?.glyph_rendering || "unreviewed",
                }));

            const words = text.trim()
                ? text.trim().split(/[\u0009-\u000D\u0020]+/u).filter(Boolean).length
                : 0;

            return {
                stats: {
                    codePoints: codePoints.length,
                    words,
                    mongolian: mongolianCount,
                    letters: letterCount,
                    controls: controls.length,
                },
                controls,
                issues,
                matchedCases,
                corpusMeta: this.corpusMeta,
                validEncoding: !issues.some((issue) => issue.level === "error"),
            };
        }

        formatCodePoint(character) {
            return `U+${character.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")}`;
        }
    }

    global.MongolAI = global.MongolAI || {};
    global.MongolAI.TextInspector = MongolianTextInspector;
})(window);
