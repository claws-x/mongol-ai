import crypto from "node:crypto";

export const MONGOLIAN_LETTER_RE = /[\u1820-\u1842\u1843-\u1878\u1880-\u18AA\u{11660}-\u{1167F}]/u;
export const MONGOLIAN_RELEVANT_RE = /[\u1800-\u18AF\u202F\u200C\u200D\u{11660}-\u{1167F}]/u;
export const MONGOLIAN_CONTROL_RE = /[\u180B-\u180F\u202F\u200C\u200D]/u;

const NAMED_ENTITIES = Object.freeze({
    amp: "&",
    apos: "'",
    gt: ">",
    lt: "<",
    nbsp: "\u00A0",
    quot: '"',
});

export function codePointLabels(text) {
    return [...text].map((character) => `U+${character.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")}`);
}

export function decodeHtmlEntities(text) {
    return text.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/giu, (match, token) => {
        if (token[0] === "#") {
            const hexadecimal = token[1]?.toLowerCase() === "x";
            const value = Number.parseInt(token.slice(hexadecimal ? 2 : 1), hexadecimal ? 16 : 10);
            if (Number.isInteger(value) && value >= 0 && value <= 0x10FFFF) return String.fromCodePoint(value);
            return match;
        }
        return NAMED_ENTITIES[token.toLowerCase()] ?? match;
    });
}

export function htmlToText(html) {
    return decodeHtmlEntities(
        html
            .replace(/<!--[^]*?-->/gu, " ")
            .replace(/<(script|style|template|noscript)\b[^>]*>[^]*?<\/\1\s*>/giu, " ")
            .replace(/<(?:br|hr|p|div|li|article|section|h[1-6]|tr|td|th)\b[^>]*>/giu, "\n")
            .replace(/<[^>]+>/gu, " "),
    )
        .replace(/\r\n?/gu, "\n")
        .replace(/[\t\f\v ]+/gu, " ")
        .replace(/ *\n */gu, "\n")
        .replace(/\n{3,}/gu, "\n\n")
        .trim();
}

function isMongolianRelevant(character) {
    return MONGOLIAN_RELEVANT_RE.test(character);
}

function expandToTokenBoundary(characters, start, direction, limit) {
    let cursor = start;
    let remaining = limit;
    while (cursor >= 0 && cursor < characters.length && remaining > 0) {
        const character = characters[cursor];
        if (/\s/u.test(character)) break;
        cursor += direction;
        remaining -= 1;
    }
    return cursor;
}

export function extractMongolianSegments(text, options = {}) {
    const contextWidth = options.contextWidth ?? 24;
    const maxSegmentCodePoints = options.maxSegmentCodePoints ?? 256;
    const characters = [...text];
    const segments = [];
    let index = 0;

    while (index < characters.length) {
        if (!isMongolianRelevant(characters[index])) {
            index += 1;
            continue;
        }
        const runStart = index;
        let containsLetter = false;
        while (index < characters.length && (isMongolianRelevant(characters[index]) || /[ \t\u00A0]/u.test(characters[index]))) {
            if (MONGOLIAN_LETTER_RE.test(characters[index])) containsLetter = true;
            index += 1;
        }
        let runEnd = index;
        while (runEnd > runStart && /\s/u.test(characters[runEnd - 1])) runEnd -= 1;
        if (!containsLetter || runEnd <= runStart) continue;

        for (let chunkStart = runStart; chunkStart < runEnd; chunkStart += maxSegmentCodePoints) {
            const chunkEnd = Math.min(runEnd, chunkStart + maxSegmentCodePoints);
            const segmentText = characters.slice(chunkStart, chunkEnd).join("");
            const leftStart = Math.max(0, expandToTokenBoundary(characters, chunkStart - 1, -1, contextWidth) + 1);
            const rightEnd = Math.min(characters.length, expandToTokenBoundary(characters, chunkEnd, 1, contextWidth));
            segments.push({
                text: segmentText,
                codepoints: codePointLabels(segmentText),
                leftContext: characters.slice(leftStart, chunkStart).join(""),
                rightContext: characters.slice(chunkEnd, rightEnd).join(""),
                controls: [...segmentText]
                    .filter((character) => MONGOLIAN_CONTROL_RE.test(character))
                    .map((character) => `U+${character.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")}`),
            });
        }
    }
    return segments;
}

export function hashText(text) {
    return `sha256:${crypto.createHash("sha256").update(text, "utf8").digest("hex")}`;
}

export function buildCorpusDocument({ source, sourceUrl, fetchedAt, html, text = null }) {
    const extractedText = text ?? htmlToText(html);
    const segments = extractMongolianSegments(extractedText);
    return {
        schemaVersion: "1.0.0",
        sourceId: source.id,
        sourceUrl,
        fetchedAt,
        contentHash: hashText(html ?? extractedText),
        pageLanguage: source.language ?? "mn-Mong",
        license: source.license,
        redistributable: source.redistributable === true,
        segmentCount: segments.length,
        segments,
    };
}

export function buildCorpusStats(documents) {
    const codepoints = new Map();
    const controls = new Map();
    const domains = new Set();
    let segmentCount = 0;
    let mongolianCodePointCount = 0;

    for (const document of documents) {
        domains.add(new URL(document.sourceUrl).hostname);
        segmentCount += document.segmentCount;
        for (const segment of document.segments) {
            for (const [index, label] of segment.codepoints.entries()) {
                const character = [...segment.text][index];
                if (!MONGOLIAN_RELEVANT_RE.test(character)) continue;
                codepoints.set(label, (codepoints.get(label) ?? 0) + 1);
                mongolianCodePointCount += 1;
            }
            for (const label of segment.controls) controls.set(label, (controls.get(label) ?? 0) + 1);
        }
    }

    const sortedObject = (map) => Object.fromEntries([...map.entries()].sort(([a], [b]) => a.localeCompare(b)));
    return {
        schemaVersion: "1.0.0",
        scope: "raw-codepoint-and-context-observation-not-linguistic-truth",
        documentCount: documents.length,
        domainCount: domains.size,
        segmentCount,
        mongolianCodePointCount,
        codepoints: sortedObject(codepoints),
        controls: sortedObject(controls),
    };
}
