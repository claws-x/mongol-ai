import assert from "node:assert/strict";
import test from "node:test";

import { analyzeMongolianLexicalControls, lexicalControlSummary } from "../../core/mongolian_lexical_controls.mjs";

test("MVS before final A is a lexical candidate with explicit shaping intent", () => {
    const text = "\u182C\u1820\u1828\u180E\u1820";
    const [event] = analyzeMongolianLexicalControls(text);
    assert.equal(event.kind, "separated-final-vowel-candidate");
    assert.equal(event.control, "U+180E");
    assert.deepEqual(event.leftSequence, ["U+182C", "U+1820", "U+1828"]);
    assert.deepEqual(event.rightSequence, ["U+1820"]);
    assert.equal(event.semanticStatus, "requires-lexical-resolution");
    assert.equal(event.shapingIntent, "leftward-tail-a-or-e-and-preceding-form-effect");
});

test("Unicode 16+ MVS and legacy NNBSP suffix structures remain distinguishable", () => {
    const stem = "\u182E\u1823\u1829\u182D\u1823\u182F";
    const suffix = "\u1833\u1824\u1837";
    const modern = analyzeMongolianLexicalControls(`${stem}\u180E${suffix}`)[0];
    const legacy = analyzeMongolianLexicalControls(`${stem}\u202F${suffix}`)[0];
    assert.equal(modern.kind, "modern-separated-suffix-candidate");
    assert.equal(modern.shapingIntent, "unicode-16-plus-special-suffix-shaping");
    assert.equal(legacy.kind, "legacy-separated-suffix-candidate");
    assert.equal(legacy.shapingIntent, "unicode-pre-16-compatibility-separator");
    assert.deepEqual(modern.rightSequence, legacy.rightSequence);
});

test("orphan separators fail explicitly without deleting input", () => {
    for (const [control, kind] of [["\u180E", "orphan-mvs"], ["\u202F", "orphan-nnbsp"]]) {
        const summary = lexicalControlSummary(`\u1820${control}`);
        assert.equal(summary.eventCount, 1);
        assert.equal(summary.events[0].kind, kind);
        assert.equal(summary.events[0].semanticStatus, "invalid-or-incomplete-context");
        assert.deepEqual(summary.rawCodepoints, ["U+1820", control === "\u180E" ? "U+180E" : "U+202F"]);
    }
});
