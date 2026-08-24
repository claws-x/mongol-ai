import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

import { SemanticGlyphRegistry, tokenizeMongolianInput } from "../../core/semantic_glyph_engine.mjs";

const registryPayload = JSON.parse(fs.readFileSync(new URL("../../data/engine/s2-semantic-registry.json", import.meta.url), "utf8"));

test("S2 registry contains exactly 93 unique Unicode-declared semantic targets", () => {
    assert.equal(registryPayload.summary.targetCount, 93);
    assert.equal(registryPayload.summary.semanticRoleCount, 93);
    assert.equal(registryPayload.targets.length, 93);
    assert.equal(new Set(registryPayload.targets.map((target) => target.id)).size, 93);
    assert.equal(Object.values(registryPayload.summary.byBackendStatus).reduce((sum, count) => sum + count, 0), 93);
});

test("A plus FVS2 in explicit medial context resolves to the third-form semantic role", () => {
    const registry = new SemanticGlyphRegistry(registryPayload);
    const resolved = registry.resolveText("\u200D\u1820\u180C\u200D");
    const grapheme = resolved.find((token) => token.type === "mongolian-grapheme");
    assert.equal(grapheme.text, "\u1820\u180C");
    assert.equal(grapheme.resolution.status, "resolved");
    assert.equal(grapheme.resolution.joiningState, "medial");
    assert.equal(grapheme.resolution.semanticRole, "MONGOLIAN_A.medial.form3");
    assert.equal(grapheme.resolution.backend.status, "project-glyph-required");
});

test("format controls remain lossless tokens and are not mistaken for semantic glyphs", () => {
    const tokens = tokenizeMongolianInput("\u1820\u180C\u202F\u1821");
    assert.deepEqual(tokens.map((token) => token.text).join(""), "\u1820\u180C\u202F\u1821");
    assert.deepEqual(tokens[0].codepoints, ["U+1820", "U+180C"]);
    assert.equal(tokens[1].type, "format-control");
    assert.deepEqual(tokens[1].controls, ["U+202F"]);
});

test("undeclared sequence and joining-state combinations fail explicitly", () => {
    const registry = new SemanticGlyphRegistry(registryPayload);
    const result = registry.resolve(["U+1820", "U+180C"], "final");
    assert.equal(result.status, "no-declared-semantic-role");
    assert.equal(result.semanticRole, null);
});
