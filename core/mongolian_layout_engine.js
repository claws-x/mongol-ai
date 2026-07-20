/**
 * Mongol AI Vertical Engine
 *
 * A capability-tested wrapper around the browser's native shaping engine.
 * It never splits Mongolian words into characters and never rotates the DOM.
 */
(function (global) {
    "use strict";

    const DEFAULT_SAMPLE = "ᠮᠣᠩᠭᠣᠯ";
    const MONGOLIAN_LETTER = /[\u1820-\u18AA]/u;
    const FVS = /[\u180B-\u180D\u180F]/u;

    class MongolVerticalEngine {
        constructor(options = {}) {
            this.options = {
                selector: options.selector || "[data-mongol-vertical]",
                fontFamily: options.fontFamily || "Mongol AI Noto",
                fontTimeout: options.fontTimeout || 5000,
            };
            this.mode = "pending";
            this.fontReady = false;
            this.measurements = null;
            this.observer = null;
        }

        async start() {
            document.documentElement.dataset.mongolEngineStatus = "pending";
            this.fontReady = await this.loadFont();
            const result = this.detectRenderingMode();
            this.mode = result.mode;
            this.measurements = result.measurements;

            document.documentElement.dataset.mongolEngineMode = this.mode;
            document.documentElement.dataset.mongolEngineStatus =
                this.mode === "unavailable" ? "degraded" : "ready";

            this.upgrade(document);
            this.observe();

            const report = this.getReport();
            document.dispatchEvent(new CustomEvent("mongolai:vertical-ready", { detail: report }));
            return report;
        }

        async loadFont() {
            if (!document.fonts || typeof document.fonts.load !== "function") return false;

            const load = document.fonts
                .load(`32px "${this.options.fontFamily}"`, DEFAULT_SAMPLE)
                .then((faces) => faces.length > 0)
                .catch(() => false);
            const timeout = new Promise((resolve) => {
                global.setTimeout(() => resolve(false), this.options.fontTimeout);
            });
            return Promise.race([load, timeout]);
        }

        detectRenderingMode() {
            if (!global.CSS || !CSS.supports("writing-mode", "vertical-lr")) {
                return { mode: "unavailable", measurements: null };
            }

            const mixed = this.probe("mixed");
            if (mixed.passes) return { mode: "native", measurements: mixed };

            if (CSS.supports("text-orientation", "sideways")) {
                const sideways = this.probe("sideways");
                if (sideways.passes) return { mode: "compat", measurements: sideways };
            }

            return { mode: "unavailable", measurements: mixed };
        }

        probe(orientation) {
            const host = document.createElement("div");
            host.setAttribute("aria-hidden", "true");
            Object.assign(host.style, {
                position: "fixed",
                inset: "auto auto 100vh 100vw",
                visibility: "hidden",
                pointerEvents: "none",
                contain: "strict",
            });

            const makeSample = (writingMode, textOrientation) => {
                const node = document.createElement("span");
                node.lang = "mn-Mong";
                node.textContent = DEFAULT_SAMPLE;
                Object.assign(node.style, {
                    display: "inline-block",
                    whiteSpace: "nowrap",
                    fontFamily: `"${this.options.fontFamily}", "Mongolian Baiti", sans-serif`,
                    fontSize: "32px",
                    lineHeight: "1.2",
                    letterSpacing: "normal",
                    writingMode,
                    textOrientation,
                });
                host.appendChild(node);
                return node;
            };

            const horizontal = makeSample("horizontal-tb", "mixed");
            const vertical = makeSample("vertical-lr", orientation);
            const upright = makeSample("vertical-lr", "upright");

            const flow = document.createElement("div");
            Object.assign(flow.style, {
                display: "inline-block",
                writingMode: "vertical-lr",
                textOrientation: orientation,
                fontFamily: `"${this.options.fontFamily}", "Mongolian Baiti", sans-serif`,
                fontSize: "24px",
                lineHeight: "1.2",
            });
            const first = document.createElement("span");
            const second = document.createElement("span");
            first.textContent = DEFAULT_SAMPLE;
            second.textContent = DEFAULT_SAMPLE;
            flow.append(first, document.createElement("br"), second);
            host.appendChild(flow);
            document.body.appendChild(host);

            const horizontalRect = horizontal.getBoundingClientRect();
            const verticalRect = vertical.getBoundingClientRect();
            const uprightRect = upright.getBoundingClientRect();
            const firstRect = first.getBoundingClientRect();
            const secondRect = second.getBoundingClientRect();

            const axisDelta = Math.abs(verticalRect.height - horizontalRect.width) /
                Math.max(horizontalRect.width, 1);
            const preservesRun = axisDelta < 0.45 && verticalRect.height < uprightRect.height * 0.9;
            const flowsLeftToRight = secondRect.left > firstRect.left;

            host.remove();
            return {
                orientation,
                passes: preservesRun && flowsLeftToRight,
                preservesRun,
                flowsLeftToRight,
                axisDelta: Number(axisDelta.toFixed(3)),
                horizontalWidth: Number(horizontalRect.width.toFixed(2)),
                verticalHeight: Number(verticalRect.height.toFixed(2)),
                uprightHeight: Number(uprightRect.height.toFixed(2)),
                columnAdvance: Number((secondRect.left - firstRect.left).toFixed(2)),
            };
        }

        upgrade(root = document) {
            const elements = [];
            if (root.nodeType === Node.ELEMENT_NODE && root.matches(this.options.selector)) {
                elements.push(root);
            }
            elements.push(...root.querySelectorAll(this.options.selector));

            for (const element of elements) {
                if (!element.lang || element.lang === "mn") element.lang = "mn-Mong";
                element.dataset.mongolEngineMode = this.mode;
                element.dataset.mongolEngineReady = "true";
            }
            return elements.length;
        }

        observe() {
            if (!global.MutationObserver || this.observer) return;
            this.observer = new MutationObserver((records) => {
                for (const record of records) {
                    for (const node of record.addedNodes) {
                        if (node.nodeType === Node.ELEMENT_NODE) this.upgrade(node);
                    }
                }
            });
            this.observer.observe(document.body, { childList: true, subtree: true });
        }

        validateText(text) {
            const codePoints = Array.from(text);
            const orphanVariationSelectors = [];
            for (let index = 0; index < codePoints.length; index += 1) {
                if (!FVS.test(codePoints[index])) continue;
                if (index === 0 || !MONGOLIAN_LETTER.test(codePoints[index - 1])) {
                    orphanVariationSelectors.push(index);
                }
            }
            return {
                valid: orphanVariationSelectors.length === 0 && !text.includes("�"),
                orphanVariationSelectors,
                containsMongolian: /[\u1800-\u18AF]/u.test(text),
                containsMvs: text.includes("\u180E"),
                containsNnbsp: text.includes("\u202F"),
                codePointLength: codePoints.length,
            };
        }

        render(element, text) {
            element.setAttribute("data-mongol-vertical", "");
            element.textContent = text;
            this.upgrade(element);
            return { element, validation: this.validateText(text), mode: this.mode };
        }

        getReport() {
            return {
                name: "Mongol AI Vertical Engine",
                version: "2.0.0",
                mode: this.mode,
                fontReady: this.fontReady,
                measurements: this.measurements,
            };
        }
    }

    const engine = new MongolVerticalEngine();
    global.MongolAI = global.MongolAI || {};
    global.MongolAI.VerticalEngine = MongolVerticalEngine;
    global.MongolAI.vertical = engine;

    const boot = () => engine.start().catch((error) => {
        document.documentElement.dataset.mongolEngineStatus = "degraded";
        global.console.error("Mongol AI Vertical Engine failed to start", error);
    });

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot, { once: true });
    } else {
        boot();
    }
})(window);
