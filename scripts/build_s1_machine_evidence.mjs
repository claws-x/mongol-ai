#!/usr/bin/env node
import fs from "node:fs";
import { evaluateCorrectnessTask } from "../core/correctness_evaluator.mjs";
import { LOCKED_FONT_SHA256, MongolianSuperEngine } from "../core/mongolian_super_engine.mjs";

if (process.argv.length !== 4) {
    throw new Error("usage: build_s1_machine_evidence.mjs REVIEW_QUEUE OUTPUT");
}

const [, , queuePath, outputPath] = process.argv;
const queue = JSON.parse(fs.readFileSync(queuePath, "utf8"));
const fontBytes = fs.readFileSync(new URL("../assets/fonts/NotoSansMongolian-Regular.ttf", import.meta.url));
const engine = new MongolianSuperEngine();
await engine.initFromFontBytes(fontBytes, { expectedHash: LOCKED_FONT_SHA256, overrides: [] });
const results = queue.tasks.map((task) => ({ task_id: task.id, category: task.category, ...evaluateCorrectnessTask(engine, task) }));
const byVerdict = results.reduce((counts, result) => {
    counts[result.verdict] = (counts[result.verdict] || 0) + 1;
    return counts;
}, {});
const report = engine.report();
const payload = {
    schema_version: "1.0.0",
    generated_at: queue.generated_at,
    evaluator: "Mongol AI correctness evaluator 1.0.0",
    scope: "Unicode mechanics and locked-font behavior; not linguistic truth",
    runtime: {
        harfbuzz: report.harfbuzz,
        font_sha256: report.fontSha256,
        font_locked: report.fontLocked,
        production_default_ignorables_preserved: false,
        control_artifacts_suppressed_from_svg: true,
    },
    summary: { task_count: results.length, by_verdict: byVerdict },
    results,
};
fs.writeFileSync(outputPath, `${JSON.stringify(payload, null, 2)}\n`);
