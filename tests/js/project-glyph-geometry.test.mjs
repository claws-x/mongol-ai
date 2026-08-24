import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";

import { ProjectGlyphGeometryRegistry, validateProjectGlyphAsset } from "../../core/project_glyph_geometry.mjs";

const payload = JSON.parse(fs.readFileSync(new URL("../../data/engine/project-glyph-geometry.json", import.meta.url), "utf8"));

test("all 18 unsupported semantic roles have deterministic geometry contracts", () => {
    const registry = new ProjectGlyphGeometryRegistry(payload);
    assert.equal(payload.summary.requirementCount, 18);
    assert.equal(payload.summary.assetCount, 0);
    assert.equal(payload.requirements.length, 18);
    assert.equal(new Set(payload.requirements.map((item) => item.semanticRole)).size, 18);
    for (const requirement of payload.requirements) {
        const result = registry.resolve(requirement.semanticRole);
        assert.equal(result.status, "asset-missing");
        assert.deepEqual(result.violations, ["asset-missing"]);
    }
});

test("medial project glyph contract accepts aligned entry and exit anchors", () => {
    const requirement = payload.requirements.find((item) => item.semanticRole === "MONGOLIAN_A.medial.form3");
    const asset = {
        semanticRole: requirement.semanticRole,
        unitsPerEm: 1000,
        advance: 500,
        path: "M0 0L500 0L500 80L0 80Z",
        bbox: { xMin: 0, yMin: 0, xMax: 500, yMax: 80 },
        anchors: { entry: { x: 0, y: 40 }, exit: { x: 500, y: 40 } },
        source: { kind: "mongol-ai-original", license: "OFL-1.1" },
    };
    assert.deepEqual(validateProjectGlyphAsset(requirement, asset), []);
});

test("geometry validator rejects discontinuity, unsafe path, and unlicensed outlines", () => {
    const requirement = payload.requirements.find((item) => item.semanticRole === "MONGOLIAN_A.medial.form3");
    const violations = validateProjectGlyphAsset(requirement, {
        semanticRole: requirement.semanticRole,
        unitsPerEm: 1000,
        advance: 500,
        path: "M0 0L500 0<script>",
        bbox: { xMin: 0, yMin: 0, xMax: 500, yMax: 200 },
        anchors: { entry: { x: 100, y: 0 }, exit: { x: 400, y: 200 } },
        source: { kind: "unknown", license: "" },
    });
    assert.ok(violations.includes("unsafe-svg-path"));
    assert.ok(violations.includes("entry-not-on-leading-edge"));
    assert.ok(violations.includes("exit-not-on-trailing-edge"));
    assert.ok(violations.includes("stem-axis-discontinuity"));
    assert.ok(violations.includes("unacceptable-outline-source"));
    assert.ok(violations.includes("missing-outline-license"));
});

test("initial final and isolate requirements expose the correct connector topology", () => {
    const byState = Object.fromEntries(payload.requirements.map((item) => [item.joiningState, item.requiredAnchors]));
    assert.deepEqual(byState.initial, { entry: false, exit: true });
    assert.deepEqual(byState.medial, { entry: true, exit: true });
    assert.deepEqual(byState.final, { entry: true, exit: false });
    assert.deepEqual(byState.isolate, { entry: false, exit: false });
});
