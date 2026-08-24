const FVS = new Set([0x180B, 0x180C, 0x180D, 0x180F]);
const MVS = 0x180E;
const ZWNJ = 0x200C;
const ZWJ = 0x200D;
const NNBSP = 0x202F;
const JOINING_STATES = new Set(["isolate", "initial", "medial", "final"]);

export function codePointLabel(character) {
    return `U+${character.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")}`;
}

export function sequenceKey(codepoints, joiningState) {
    return `${codepoints.join(" ")}|${joiningState}`;
}

function isMongolianBase(codePoint) {
    return (codePoint >= 0x1820 && codePoint <= 0x18AA) || (codePoint >= 0x11660 && codePoint <= 0x1167F);
}

export function tokenizeMongolianInput(text) {
    const characters = [...text];
    const tokens = [];
    for (let index = 0; index < characters.length; index += 1) {
        const character = characters[index];
        const codePoint = character.codePointAt(0);
        if (isMongolianBase(codePoint)) {
            const codepoints = [codePointLabel(character)];
            const controls = [];
            while (index + 1 < characters.length) {
                const next = characters[index + 1];
                const nextCodePoint = next.codePointAt(0);
                if (!FVS.has(nextCodePoint) && nextCodePoint !== MVS) break;
                index += 1;
                codepoints.push(codePointLabel(next));
                controls.push(codePointLabel(next));
            }
            tokens.push({ type: "mongolian-grapheme", text: characters.slice(index - controls.length, index + 1).join(""), codepoints, controls });
        } else if ([ZWNJ, ZWJ, NNBSP].includes(codePoint)) {
            tokens.push({ type: "format-control", text: character, codepoints: [codePointLabel(character)], controls: [codePointLabel(character)] });
        } else {
            tokens.push({ type: "literal", text: character, codepoints: [codePointLabel(character)], controls: [] });
        }
    }
    return tokens;
}

export function inferExplicitJoiningState(tokens, tokenIndex) {
    const before = tokens[tokenIndex - 1]?.codepoints.includes("U+200D") ?? false;
    const after = tokens[tokenIndex + 1]?.codepoints.includes("U+200D") ?? false;
    if (before && after) return "medial";
    if (after) return "initial";
    if (before) return "final";
    return "isolate";
}

export class SemanticGlyphRegistry {
    constructor(payload) {
        if (payload?.schemaVersion !== "1.0.0" || !Array.isArray(payload.targets)) throw new Error("invalid semantic glyph registry");
        this.payload = payload;
        this.bySequenceAndState = new Map();
        for (const target of payload.targets) {
            const key = sequenceKey(target.inputSequence, target.joiningState);
            if (this.bySequenceAndState.has(key)) throw new Error(`duplicate semantic registry key: ${key}`);
            this.bySequenceAndState.set(key, Object.freeze(target));
        }
    }

    resolve(codepoints, joiningState) {
        if (!JOINING_STATES.has(joiningState)) {
            return { status: "needs-joining-context", inputSequence: codepoints, joiningState: null, semanticRole: null };
        }
        const target = this.bySequenceAndState.get(sequenceKey(codepoints, joiningState))
            ?? this.bySequenceAndState.get(sequenceKey(codepoints, "any"));
        if (!target) return { status: "no-declared-semantic-role", inputSequence: codepoints, joiningState, semanticRole: null };
        return {
            status: "resolved",
            inputSequence: codepoints,
            joiningState,
            semanticRole: target.semanticRole,
            variationIntent: target.variationIntent,
            backend: target.backend,
            source: target.source,
        };
    }

    resolveText(text, joiningStates = new Map()) {
        const tokens = tokenizeMongolianInput(text);
        return tokens.map((token, index) => {
            if (token.type !== "mongolian-grapheme" || token.controls.length === 0) return { ...token, resolution: null };
            const explicit = inferExplicitJoiningState(tokens, index);
            const joiningState = joiningStates.get(index) ?? explicit;
            return { ...token, resolution: this.resolve(token.codepoints, joiningState) };
        });
    }
}
