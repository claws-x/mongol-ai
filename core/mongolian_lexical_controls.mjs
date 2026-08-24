import { codePointLabel, tokenizeMongolianInput } from "./semantic_glyph_engine.mjs";

const MVS = "U+180E";
const NNBSP = "U+202F";
const A_OR_E = new Set(["U+1820", "U+1821"]);

function graphemeRun(tokens, start, step) {
    const run = [];
    for (let index = start + step; index >= 0 && index < tokens.length; index += step) {
        const token = tokens[index];
        if (token.type !== "mongolian-grapheme") break;
        if (step < 0) run.unshift(...token.codepoints);
        else run.push(...token.codepoints);
    }
    return run;
}

function classify(control, leftSequence, rightSequence) {
    if (rightSequence.length === 0) {
        return {
            kind: control === MVS ? "orphan-mvs" : "orphan-nnbsp",
            semanticStatus: "invalid-or-incomplete-context",
            shapingIntent: "none-without-following-mongolian",
        };
    }
    if (control === NNBSP) {
        return {
            kind: "legacy-separated-suffix-candidate",
            semanticStatus: "requires-lexical-resolution",
            shapingIntent: "unicode-pre-16-compatibility-separator",
        };
    }
    if (rightSequence.length === 1 && A_OR_E.has(rightSequence[0])) {
        return {
            kind: "separated-final-vowel-candidate",
            semanticStatus: "requires-lexical-resolution",
            shapingIntent: "leftward-tail-a-or-e-and-preceding-form-effect",
        };
    }
    return {
        kind: "modern-separated-suffix-candidate",
        semanticStatus: "requires-lexical-resolution",
        shapingIntent: "unicode-16-plus-special-suffix-shaping",
    };
}

export function analyzeMongolianLexicalControls(text) {
    const tokens = tokenizeMongolianInput(text);
    const events = [];
    tokens.forEach((token, index) => {
        const control = token.codepoints[0];
        if (token.type !== "format-control" || (control !== MVS && control !== NNBSP)) return;
        const leftSequence = graphemeRun(tokens, index, -1);
        const rightSequence = graphemeRun(tokens, index, 1);
        events.push({
            index,
            control,
            controlName: control === MVS ? "MVS" : "NNBSP",
            leftSequence,
            rightSequence,
            ...classify(control, leftSequence, rightSequence),
            lineBreakIntent: "no-break",
            unicodeModel: "17.0.0",
            source: "Unicode Core Specification 17.0, section 13.5",
        });
    });
    return events;
}

export function lexicalControlSummary(text) {
    const events = analyzeMongolianLexicalControls(text);
    return {
        eventCount: events.length,
        requiresLexicalResolution: events.filter((event) => event.semanticStatus === "requires-lexical-resolution").length,
        events,
        rawCodepoints: [...text].map(codePointLabel),
    };
}
