// Browser runtime is vendored because GitHub Pages artifacts intentionally do
// not publish node_modules. Keep this path inside the public repository tree.
import * as hb from "../assets/vendor/harfbuzzjs/index.mjs";

const ENGINE_VERSION = "0.8.0";
const FONT_URL = new URL("../assets/fonts/NotoSansMongolian-Regular.ttf", import.meta.url);
const OVERRIDES_URL = new URL("../data/engine/glyph-overrides.json", import.meta.url);
const LOCKED_FONT_SHA256 = "a28ba3cde3de22de7ddc934bd5d5babe54e6ce28c073a288cd978ffcf26b295b";
const CONTROL_NAMES = new Map([
    [0x180b, "FVS1"], [0x180c, "FVS2"], [0x180d, "FVS3"], [0x180e, "MVS"],
    [0x180f, "FVS4"], [0x200c, "ZWNJ"], [0x200d, "ZWJ"], [0x202f, "NNBSP"],
]);

const PROFILES = Object.freeze({
    "unicode-national": {
        label: "国家标准／Unicode 已提交文本",
        encoding: "unicode",
        evidence: "https://ime.onon.cn/help-index.html",
        note: "逐码位保留输入；不自动 NFC、删控制符或替换空格。",
    },
    "onon-mn": {
        label: "Onon MN（国家标准）已提交文本",
        encoding: "unicode",
        evidence: "https://ime.onon.cn/help-index.html",
        note: "接收 Onon 候选提交后的文本；不模拟其闭源词库和按键候选算法。",
    },
    "onon-mk": {
        label: "Onon MK／蒙科立编码原文",
        encoding: "menksoft-pua",
        evidence: "https://ime.onon.cn/help-index.html",
        note: "无官方公开、可再分发的完整映射表时只做无损保存，不猜测转码。",
    },
    "onon-mw": {
        label: "Onon MW（民委共享工程）原文",
        encoding: "mw-private",
        evidence: "https://ime.onon.cn/help-index.html",
        note: "缺少权威完整映射时只做无损保存，不猜测转码。",
    },
    "menksoft-raw": {
        label: "蒙科立原始编码",
        encoding: "menksoft-pua",
        evidence: "https://ime.onon.cn/zh-CN/about",
        note: "保留 PUA 和原始码位；只有经授权并经测试的映射表才能进入转换层。",
    },
});

function codePointLabel(codePoint) {
    return `U+${codePoint.toString(16).toUpperCase().padStart(4, "0")}`;
}

function isMongolian(codePoint) {
    return codePoint >= 0x1800 && codePoint <= 0x18af;
}

function isPua(codePoint) {
    return (codePoint >= 0xe000 && codePoint <= 0xf8ff) ||
        (codePoint >= 0xf0000 && codePoint <= 0xffffd) ||
        (codePoint >= 0x100000 && codePoint <= 0x10fffd);
}

function isControlArtifactName(name) {
    return /^(?:fvs[1-4]|mvs)(?:\.|$)/i.test(name || "");
}

async function sha256(bytes) {
    const digest = await crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

export class LosslessMongolianDocument {
    constructor(raw, profile = "unicode-national") {
        if (!(profile in PROFILES)) throw new Error(`Unknown input profile: ${profile}`);
        this.raw = String(raw ?? "");
        this.profile = profile;
        this.profileInfo = PROFILES[profile];
        this.tokens = Array.from(this.raw, (character, index) => {
            const codePoint = character.codePointAt(0);
            return Object.freeze({
                index,
                character,
                codePoint,
                label: codePointLabel(codePoint),
                control: CONTROL_NAMES.get(codePoint) || null,
                mongolian: isMongolian(codePoint),
                pua: isPua(codePoint),
            });
        });
        Object.freeze(this.tokens);
    }

    serialize() {
        return this.raw;
    }

    diagnostics() {
        const pua = this.tokens.filter((token) => token.pua);
        const controls = this.tokens.filter((token) => token.control);
        const issues = [];
        if (this.raw.includes("�")) issues.push({ level: "error", code: "replacement-character" });
        if (this.raw.normalize("NFC") !== this.raw) {
            issues.push({ level: "warning", code: "normalization-would-change-input" });
        }
        if (this.profileInfo.encoding !== "unicode") {
            issues.push({ level: "blocked", code: "authoritative-mapping-required" });
        }
        if (pua.length && this.profileInfo.encoding === "unicode") {
            issues.push({ level: "warning", code: "unexpected-private-use-codepoint" });
        }
        return {
            profile: this.profile,
            encoding: this.profileInfo.encoding,
            roundTripExact: this.serialize() === this.raw,
            codePointCount: this.tokens.length,
            controls,
            pua,
            issues,
            canShape: this.profileInfo.encoding === "unicode" && !issues.some((item) => item.level === "error"),
        };
    }
}

export class MongolianSuperEngine {
    constructor(options = {}) {
        this.fontUrl = options.fontUrl ? new URL(options.fontUrl, location.href) : FONT_URL;
        this.overridesUrl = options.overridesUrl ? new URL(options.overridesUrl, location.href) : OVERRIDES_URL;
        this.expectedFontHash = options.expectedFontHash === undefined ? LOCKED_FONT_SHA256 : options.expectedFontHash;
        this.fontHash = null;
        this.font = null;
        this.face = null;
        this.overrides = [];
        this.ready = false;
    }

    async init() {
        const [fontResponse, overrideResponse] = await Promise.all([
            fetch(this.fontUrl), fetch(this.overridesUrl),
        ]);
        if (!fontResponse.ok) throw new Error(`Font request failed: ${fontResponse.status}`);
        if (!overrideResponse.ok) throw new Error(`Override request failed: ${overrideResponse.status}`);
        const fontBytes = await fontResponse.arrayBuffer();
        const overridePayload = await overrideResponse.json();
        return this.initFromFontBytes(fontBytes, {
            expectedHash: this.expectedFontHash,
            overrides: overridePayload.overrides || [],
        });
    }

    async initFromFontBytes(fontBytes, options = {}) {
        const bytes = fontBytes instanceof ArrayBuffer ? fontBytes : fontBytes.buffer.slice(
            fontBytes.byteOffset, fontBytes.byteOffset + fontBytes.byteLength
        );
        this.fontHash = await sha256(bytes);
        const expectedHash = options.expectedHash === undefined ? null : options.expectedHash;
        if (expectedHash && this.fontHash !== expectedHash) {
            throw new Error(`Font integrity mismatch: ${this.fontHash}`);
        }
        this.overrides = (options.overrides || []).filter((item) => item.status === "approved");
        const blob = new hb.Blob(bytes);
        this.face = new hb.Face(blob);
        this.font = new hb.Font(this.face);
        this.ready = true;
        return this.report();
    }

    report() {
        return {
            name: "Mongol AI Deterministic Shaping Engine",
            version: ENGINE_VERSION,
            ready: this.ready,
            harfbuzz: hb.versionString(),
            fontSha256: this.fontHash,
            expectedFontSha256: this.expectedFontHash,
            fontLocked: Boolean(this.expectedFontHash && this.fontHash === this.expectedFontHash),
            approvedOverrides: this.overrides.length,
        };
    }

    createDocument(raw, profile) {
        return new LosslessMongolianDocument(raw, profile);
    }

    shape(document) {
        if (!this.ready) throw new Error("Engine is not initialized");
        const diagnostics = document.diagnostics();
        if (!diagnostics.canShape) {
            return { status: "blocked", diagnostics, glyphs: [], reason: "authoritative-mapping-required" };
        }
        const buffer = new hb.Buffer();
        buffer.addText(document.raw);
        // Mongolian fonts conventionally shape on a horizontal baseline; the completed
        // run is rotated into top-to-bottom flow. Shaping directly as TTB selects a
        // different metric path and breaks joining in common OpenType fonts.
        buffer.setDirection(hb.Direction.LTR);
        buffer.setScript("Mong");
        buffer.setLanguage("mn");
        // Default-ignorables still participate in joining and GSUB. Preserving them
        // asks HarfBuzz to emit their font glyphs, which can visibly draw ZWJ/FVS
        // control glyphs into the production SVG.
        buffer.setFlags(hb.BufferFlag.DEFAULT);
        hb.shape(this.font, buffer);
        let glyphs = buffer.getGlyphInfosAndPositions().map((glyph) => {
            const name = this.font.glyphName(glyph.codepoint) || null;
            return {
            id: glyph.codepoint,
            name,
            cluster: glyph.cluster,
            xAdvance: glyph.xAdvance || 0,
            yAdvance: glyph.yAdvance || 0,
            xOffset: glyph.xOffset || 0,
            yOffset: glyph.yOffset || 0,
            path: this.font.glyphToPath(glyph.codepoint),
            controlArtifact: isControlArtifactName(name),
        }});
        const override = this.findOverride(document);
        if (override) glyphs = this.applyOverride(glyphs, override);
        return {
            status: "shaped",
            diagnostics,
            glyphs,
            overrideId: override?.id || null,
            fontHash: this.fontHash,
            harfbuzz: hb.versionString(),
            upem: this.face.upem,
        };
    }

    findOverride(document) {
        const codePoints = document.tokens.map((token) => token.label).join(" ");
        return this.overrides.find((item) =>
            item.profile === document.profile && item.code_points === codePoints &&
            item.font_sha256 === this.fontHash
        );
    }

    applyOverride(glyphs, override) {
        if (!Array.isArray(override.glyph_ids) || override.glyph_ids.length !== glyphs.length) {
            throw new Error(`Invalid approved override: ${override.id}`);
        }
        return glyphs.map((glyph, index) => ({
            ...glyph,
            id: override.glyph_ids[index],
            path: this.font.glyphToPath(override.glyph_ids[index]),
        }));
    }

    renderSvg(shapeResult, options = {}) {
        if (shapeResult.status !== "shaped") throw new Error("Blocked input cannot be rendered");
        const fontSize = Number(options.fontSize || 42);
        const padding = Number(options.padding || 16);
        const scale = fontSize / shapeResult.upem;
        const extents = this.font.hExtents();
        const ascender = extents.ascender || shapeResult.upem;
        const descender = extents.descender || -Math.round(shapeResult.upem * 0.2);
        const renderedGlyphs = options.showControlArtifacts
            ? shapeResult.glyphs
            : shapeResult.glyphs.filter((glyph) => !glyph.controlArtifact);
        const advance = renderedGlyphs.reduce((sum, glyph) => sum + glyph.xAdvance, 0);
        const width = Math.ceil((ascender - descender) * scale + padding * 2);
        const height = Math.ceil(Math.max(advance * scale, fontSize) + padding * 2);
        let penX = 0;
        const paths = renderedGlyphs.map((glyph) => {
            const index = shapeResult.glyphs.indexOf(glyph);
            const transform = `translate(${penX + glyph.xOffset} ${glyph.yOffset})`;
            penX += glyph.xAdvance;
            return `<path d="${glyph.path}" transform="${transform}" data-glyph-index="${index}" data-glyph-id="${glyph.id}" data-cluster="${glyph.cluster}"/>`;
        }).join("");
        const groupTransform = `translate(${padding - descender * scale} ${padding}) rotate(90) scale(${scale} ${-scale})`;
        return `<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" data-engine="mongol-ai-${ENGINE_VERSION}" data-font-sha256="${this.fontHash}"><g transform="${groupTransform}" fill="currentColor">${paths}</g></svg>`;
    }

    renderAccessible(container, inputDocument, options = {}) {
        const result = this.shape(inputDocument);
        container.replaceChildren();
        if (result.status === "blocked") {
            throw new Error(result.reason);
        }
        const visual = globalThis.document.createElement("div");
        visual.className = "mongol-deterministic-visual";
        visual.setAttribute("aria-hidden", "true");
        visual.innerHTML = this.renderSvg(result, options);
        const accessible = globalThis.document.createElement("span");
        accessible.className = "sr-only mongol-source-text";
        accessible.lang = "mn-Mong";
        accessible.textContent = inputDocument.raw;
        container.append(visual, accessible);
        return result;
    }
}

export { ENGINE_VERSION, LOCKED_FONT_SHA256, PROFILES, codePointLabel };
