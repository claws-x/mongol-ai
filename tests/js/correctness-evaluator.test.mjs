import assert from "node:assert/strict";
import fs from "node:fs";
import { test } from "node:test";
import { evaluateCorrectnessTask, glyphFingerprint } from "../../core/correctness_evaluator.mjs";
import { LOCKED_FONT_SHA256, MongolianSuperEngine } from "../../core/mongolian_super_engine.mjs";

async function lockedEngine() {
    const engine = new MongolianSuperEngine();
    const fontBytes = fs.readFileSync(new URL("../../assets/fonts/NotoSansMongolian-Regular.ttf", import.meta.url));
    await engine.initFromFontBytes(fontBytes, { expectedHash: LOCKED_FONT_SHA256, overrides: [] });
    return engine;
}

const queue = JSON.parse(fs.readFileSync(new URL("../../data/quality/s1-review-queue.json", import.meta.url), "utf8"));
const task = (id) => queue.tasks.find((item) => item.id === id);

test("standardized variants are scored only in Unicode-declared contexts", async () => {
    const engine = await lockedEngine();
    const result = evaluateCorrectnessTask(engine, task("s1-stdvar-001"));
    assert.equal(result.verdict, "machine_aligned");
    assert.equal(result.probes.find((probe) => probe.context === "initial").result, "outside_declared_context");
    assert.ok(result.probes.filter((probe) => probe.expectation_class === "normative_target").every((probe) => probe.result === "aligned"));
});

test("A third-form medial exposes the locked font conflict without drawing FVS", async () => {
    const engine = await lockedEngine();
    const result = evaluateCorrectnessTask(engine, task("s1-stdvar-002"));
    assert.equal(result.verdict, "machine_conflict");
    assert.equal(result.probes.find((probe) => probe.context === "medial").result, "missing_variant_response");
    const shape = engine.shape(engine.createDocument("\u200Dᠠ\u180C\u200D", "unicode-national"));
    assert.ok(shape.glyphs.some((glyph) => glyph.name === "fvs2" && glyph.controlArtifact));
    assert.doesNotMatch(engine.renderSvg(shape), /data-glyph-id="1469"/);
});

test("standalone selectors are invisible while MVS requests context", async () => {
    const engine = await lockedEngine();
    const selectorShape = engine.shape(engine.createDocument("\u180C", "unicode-national"));
    assert.doesNotMatch(engine.renderSvg(selectorShape), /<path /);
    assert.equal(evaluateCorrectnessTask(engine, task("s1-control-002")).verdict, "machine_aligned");
    assert.equal(evaluateCorrectnessTask(engine, task("s1-control-005")).verdict, "needs_context");
});

test("locked shaping fingerprints repeat exactly", async () => {
    const engine = await lockedEngine();
    const document = engine.createDocument("\u200Dᠠ\u180B\u200D", "unicode-national");
    assert.equal(glyphFingerprint(engine.shape(document)), glyphFingerprint(engine.shape(document)));
});

test("committed machine evidence is reproducible and honestly distributed", async () => {
    const evidence = JSON.parse(fs.readFileSync(new URL("../../data/quality/s1-machine-evidence.json", import.meta.url), "utf8"));
    const engine = await lockedEngine();
    const liveCounts = queue.tasks.map((item) => evaluateCorrectnessTask(engine, item)).reduce((counts, result) => {
        counts[result.verdict] = (counts[result.verdict] || 0) + 1;
        return counts;
    }, {});
    assert.deepEqual(liveCounts, evidence.summary.by_verdict);
    assert.deepEqual(evidence.summary.by_verdict, {
        machine_aligned: 48,
        machine_conflict: 16,
        machine_covered: 35,
        needs_context: 1,
    });
    assert.equal(evidence.runtime.production_default_ignorables_preserved, false);
    assert.equal(evidence.runtime.control_artifacts_suppressed_from_svg, true);
});
