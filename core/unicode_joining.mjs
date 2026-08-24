export const UNICODE_JOINING_VERSION = "17.0.0";
export const UNICODE_JOINING_SOURCE = "https://www.unicode.org/Public/17.0.0/ucd/extracted/DerivedJoiningType.txt";
export const UNICODE_JOINING_SOURCE_SHA256 = "f39ebe974825d6736aee15582250307aa532b2cfab3caf3f86bd23fddc9c5c4d";

// Compact, reviewable extraction of the Mongolian-relevant records in the
// version-locked UCD file. Code points not listed have Joining_Type=U.
const RANGES = Object.freeze([
    [0x1807, 0x1807, "D"],
    [0x180A, 0x180A, "C"],
    [0x180B, 0x180D, "T"],
    [0x180F, 0x180F, "T"],
    [0x1820, 0x1843, "D"],
    [0x1844, 0x1878, "D"],
    [0x1885, 0x1886, "T"],
    [0x1887, 0x18A8, "D"],
    [0x18A9, 0x18A9, "T"],
    [0x18AA, 0x18AA, "D"],
    [0x200D, 0x200D, "C"],
]);

export function joiningType(codePoint) {
    for (const [start, end, value] of RANGES) {
        if (codePoint >= start && codePoint <= end) return value;
    }
    return "U";
}

function joinsPreceding(value) {
    return value === "D" || value === "R" || value === "C";
}

function joinsFollowing(value) {
    return value === "D" || value === "L" || value === "C";
}

function significantNeighbour(tokens, start, step) {
    for (let index = start + step; index >= 0 && index < tokens.length; index += step) {
        const type = tokenJoiningType(tokens[index]);
        if (type !== "T") return { index, type };
    }
    return null;
}

export function tokenJoiningType(token) {
    const base = token?.codepoints?.[0];
    if (!base) return "U";
    return joiningType(Number.parseInt(base.slice(2), 16));
}

export function computeJoiningStates(tokens) {
    const states = new Map();
    tokens.forEach((token, index) => {
        if (token.type !== "mongolian-grapheme") return;
        const current = tokenJoiningType(token);
        const previous = significantNeighbour(tokens, index, -1);
        const next = significantNeighbour(tokens, index, 1);
        const connectsPreceding = Boolean(previous && joinsFollowing(previous.type) && joinsPreceding(current));
        const connectsFollowing = Boolean(next && joinsFollowing(current) && joinsPreceding(next.type));
        const state = connectsPreceding
            ? (connectsFollowing ? "medial" : "final")
            : (connectsFollowing ? "initial" : "isolate");
        states.set(index, state);
    });
    return states;
}
